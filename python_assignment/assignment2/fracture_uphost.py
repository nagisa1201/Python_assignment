'''
Author: Nagisa 2964793117@qq.com
Date: 2025-11-19 14:40:33
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2025-11-20 20:52:14
FilePath: \python_assignment\assignment2\fracture_uphost.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import socket
import os
import time  

def tcp_image_server(bind_ip, bind_port, save_dir, block_size=1024, timeout=30):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5)
    print(f"TCP服务端启动，监听 {bind_ip}:{bind_port}（块大小：{block_size}字节，超时：{timeout}秒）...")
    client_conn = None
    save_path = ""
    try:
        client_conn, client_addr = server_socket.accept()
        print(f"客户端连接：{client_addr}")
        client_conn.settimeout(timeout)
        # 接收元信息
        meta_data = client_conn.recv(1024).decode('utf-8').strip()
        filename, file_size_str = meta_data.split('|', 1)
        file_size = int(file_size_str)
        print(f"下位机发送的原文件：{filename}（大小：{file_size}字节）")               
        file_name_only, file_ext = os.path.splitext(filename)
        # 生成时间戳年月日_时分秒
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        # 新文件名：原名称_时间戳.后缀
        new_filename = f"{file_name_only}_{timestamp}{file_ext}"
        # 拼接最终存储路径
        save_path = os.path.join(save_dir, new_filename)
        print(f"新存储路径：{save_path}")
        # 协商分块数
        chunk_num = (file_size + block_size - 1) // block_size
        client_conn.send(f"200|{chunk_num}".encode('utf-8'))
        print(f"协商成功，需分{chunk_num}块传输")
        received_size = 0
        try:
            with open(save_path, 'wb') as f:
                for i in range(chunk_num):
                    try:
                        chunk_data = client_conn.recv(block_size)
                        if not chunk_data:
                            print(f"第{i+1}块接收失败（客户端断开）")
                            client_conn.send(b"Fail: Chunk Lost")
                            if os.path.exists(save_path):
                                os.remove(save_path)  # 删除不完整文件
                            return
                        f.write(chunk_data)
                        received_size += len(chunk_data)
                        client_conn.send(b"ACK")
                    except socket.timeout:
                        print(f"第{i+1}块接收超时")
                        client_conn.send(b"Fail: Timeout")
                        if os.path.exists(save_path):
                            os.remove(save_path)
                        return
                    except Exception as e:
                        print(f"第{i+1}块处理异常：{str(e)}")
                        client_conn.send(b"Fail: Chunk Error")
                        if os.path.exists(save_path):
                            os.remove(save_path)
                        return
        except OSError as e:
            if e.winerror == 32:
                print(f"错误：写入文件时被占用！请关闭所有访问该文件的程序。")
                if os.path.exists(save_path):
                    os.remove(save_path)
                client_conn.send(b"Fail: File Occupied When Writing")
                return
        # 校验完整性
        if received_size == file_size:
            client_conn.send(b"Success")
            print(f"文件接收完成！存储路径：{save_path}")
        else:
            print(f"传输不完整：接收{received_size}字节≠原文件{file_size}字节")
            client_conn.send(b"Fail: Size Mismatch")
            if os.path.exists(save_path):
                os.remove(save_path)
    except socket.timeout:
        print(f"连接超时（{timeout}秒无数据）")
        if os.path.exists(save_path) and os.path.getsize(save_path) != file_size:
            os.remove(save_path)
    except Exception as e:
        print(f"服务端全局异常：{str(e)}")
        if os.path.exists(save_path) and os.path.getsize(save_path) != file_size:
            os.remove(save_path)
    finally:
        if client_conn:
            client_conn.close()
            print(f"关闭客户端连接：{client_addr}")
        server_socket.close()
        print("服务端套接字关闭")
if __name__ == "__main__":
    BIND_IP = "0.0.0.0"
    BIND_PORT = 9999
    SAVE_DIR = "D:\\project\\vscode_pro\\python_assignment\\assignment2"
    tcp_image_server(BIND_IP, BIND_PORT, SAVE_DIR, block_size=1024, timeout=30)