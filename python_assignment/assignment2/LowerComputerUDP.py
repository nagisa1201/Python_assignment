import socket
def udp_client(file_path, server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()  
        client_socket.sendto(file_content.encode('utf-8'), (server_ip, server_port))
        response, server_addr = client_socket.recvfrom(1024)
        print(f"收到上位机回复：{response.decode('utf-8')}（来自{server_addr}）")
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}")
    except Exception as e:
        print(f"通信异常：{e}")
    finally:
        # 5. 关闭套接字
        client_socket.close()
if __name__ == "__main__":
    CLIENT_FILE = "D:\\project\\vscode_pro\\python_assignment\\assignment2\\923110800532tlf.txt" 
    SERVER_IP = "127.0.0.1"          
    SERVER_PORT = 8888             
    udp_client(CLIENT_FILE, SERVER_IP, SERVER_PORT)