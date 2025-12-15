import socket
import os
def tcp_image_client(server_ip, server_port, image_path, block_size=1024, timeout=30):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout)  
    try:
        # 连接服务端
        client_socket.connect((server_ip, server_port))
        print(f"已连接服务器：{server_ip}:{server_port}")
        # 校验本地文件
        if not os.path.exists(image_path):
            print(f"图像文件不存在：{image_path}")
            client_socket.send(b"Fail: File Not Found")
            return
        filename = os.path.basename(image_path)
        file_size = os.path.getsize(image_path)
        print(f"待发送文件：{filename}（大小：{file_size}字节）")
        # 发送元信息
        client_socket.send(f"{filename}|{file_size}".encode('utf-8'))
        # 接收协商结果
        response = client_socket.recv(1024).decode('utf-8').strip()
        if not response.startswith("200"):
            print(f"协商失败，服务端回复：{response}")
            return
        chunk_num = int(response.split('|')[1])
        print(f"协商成功，需分{chunk_num}块传输（块大小：{block_size}字节）")
        # 分块发送 等待ACK+异常重试
        sent_size = 0
        with open(image_path, 'rb') as f:
            for i in range(chunk_num):
                try:
                    # 读取当前块
                    chunk_data = f.read(block_size)
                    if not chunk_data:
                        print(f"第{i+1}块读取失败")
                        client_socket.send(b"Fail: Read Chunk")
                        return
                    # 发送块数据
                    client_socket.send(chunk_data)
                    sent_size += len(chunk_data)
                    # 等待服务端ACK
                    ack = client_socket.recv(1024)
                    if ack != b"ACK":
                        print(f"第{i+1}块未收到ACK，服务端回复：{ack.decode('utf-8', errors='ignore')}")
                        return
                except socket.timeout:
                    print(f"第{i+1}块发送超时（{timeout}秒未收到ACK）")
                    return
                except Exception as e:
                    print(f"第{i+1}块发送异常：{str(e)}")
                    return
        final_response = client_socket.recv(1024).decode('utf-8', errors='ignore')
        if final_response == "Success":
            print(f"传输成功！服务端回复：{final_response}")
        else:
            print(f"传输失败！服务端回复：{final_response}")
    except ConnectionRefusedError:
        print("无法连接服务端，请先启动服务端")
    except socket.timeout:
        print(f"连接超时（{timeout}秒未建立连接/无响应）")
    except Exception as e:
        print(f"客户端全局异常：{str(e)}")
    finally:
        client_socket.close()
        print("客户端套接字关闭")
if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 9999
    IMAGE_PATH = "D:\\project\\vscode_pro\\python_assignment\\assignment2\\mygo.jpg"
    tcp_image_client(SERVER_IP, SERVER_PORT, IMAGE_PATH, block_size=1024, timeout=30)