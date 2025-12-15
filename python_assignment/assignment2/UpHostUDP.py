import socket
def udp_server(bind_ip, bind_port, save_file_path):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((bind_ip, bind_port))
    print(f"上位机已启动，监听 {bind_ip}:{bind_port}...")
    try:
        data, client_addr = server_socket.recvfrom(1024)
        with open(save_file_path, 'w', encoding='utf-8') as f:
            f.write(data.decode('utf-8')) 
        print(f"数据已保存到文件：{save_file_path}")
        response = "Success".encode('utf-8')
        server_socket.sendto(response, client_addr)
        print(f"已发送回复给{client_addr}：Success")
    except Exception as e:
        print(f"服务端异常：{e}")
    finally:
        server_socket.close()
if __name__ == "__main__":
    BIND_IP = "0.0.0.0"        # 监听所有网络接口
    BIND_PORT = 8888           
    SAVE_FILE = "D:\\project\\vscode_pro\\python_assignment\\assignment2\\923110800532tlf_received.txt"  # 上位机保存文件的路径
    udp_server(BIND_IP, BIND_PORT, SAVE_FILE)