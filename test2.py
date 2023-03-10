import socket
import sys

HOST, PORT = "localhost", 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 서버에 연결하고 데이터를 전송

    sock.connect((HOST, PORT))

    while True:
        data = input()
        data = data.encode('utf-8')
        sock.sendall(data)

        # 데이터를 수신하고 소켓 연결을 닫음
        received = sock.recv(1024)
        print(f"Sent: {data}")
        print(f"Receiverd: {received}")
finally:
    sock.close()
