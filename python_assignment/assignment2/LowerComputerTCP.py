import socket
import os
def tcp_image_client(image_path, server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        print(f"已连接上位机：{server_ip}:{server_port}")
        if not os.path.exists(image_path):
            print(f"错误：图像文件不存在 → {image_path}")
            return
        image_size = os.path.getsize(image_path)
        if image_size >= 4096:
            print(f"错误：文件过大（{image_size}字节），需小于4096字节")
            return
        print(f"图像文件大小：{image_size}字节（符合要求）")
        with open(image_path, 'rb') as f:
            image_data = f.read()  
        client_socket.send(image_data)
        print(f"已发送图像数据，长度：{len(image_data)}字节")
        response = client_socket.recv(1024)
        print(f"收到上位机回复：{response.decode('utf-8')}")
    except ConnectionRefusedError:
        print(f"错误：无法连接上位机，请先启动服务端")
    except Exception as e:
        print(f"客户端异常：{e}")
    finally:
        client_socket.close()
        print("客户端连接已关闭")
if __name__ == "__main__":
    IMAGE_FILE = "D:\\project\\vscode_pro\\python_assignment\\assignment2\\Bochii.jpg"
    SERVER_IP = "127.0.0.1"  
    SERVER_PORT = 9999    
    tcp_image_client(IMAGE_FILE, SERVER_IP, SERVER_PORT)