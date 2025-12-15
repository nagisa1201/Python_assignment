'''
Author: Nagisa 2964793117@qq.com
Date: 2025-11-18 22:02:03
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2025-11-20 20:32:40
FilePath: \python_assignment\assignment2\UpHostTCP.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import socket
def tcp_image_server(bind_ip, bind_port, save_image_path):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5)
    print(f"TCP上位机已启动，监听 {bind_ip}:{bind_port}...")
    try:
        client_conn, client_addr = server_socket.accept()
        print(f"已建立连接：{client_addr}")
        image_data = client_conn.recv(4096)
        print(f"收到图像数据，长度：{len(image_data)}字节")

        with open(save_image_path, 'wb') as f:
            f.write(image_data)
        print(f"图像已保存到：{save_image_path}")
        
        client_conn.send("Success".encode('utf-8'))
        print(f"已发送回复给{client_addr}：Success")
    except FileNotFoundError:
        print(f"错误：保存路径不存在 → {save_image_path}")
    except Exception as e:
        print(f"服务端异常：{e}")
    finally:
        client_conn.close()
        server_socket.close()
        print("连接已关闭")
if __name__ == "__main__":
    BIND_IP = "0.0.0.0"  
    BIND_PORT = 9999   
    SAVE_IMAGE = "D:\\project\\vscode_pro\\python_assignment\\assignment2\\received_image.png"
    tcp_image_server(BIND_IP, BIND_PORT, SAVE_IMAGE)