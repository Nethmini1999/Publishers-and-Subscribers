import socket
import sys

HEADER =64
PORT=5000

SERVER="127.0.0.1" 
ADDR=(SERVER,PORT)
FORMAT='utf-8'

class MyClientApp:
    def __init__(self, server_ip, port, client_type):
        self.server_ip = server_ip
        self.port = int(port)
        self.client_type = client_type
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.server_ip, self.port)
        self.client_socket.connect(server_address)
        print(f"Connected to server: {server_address}")
        self.client_socket.sendall(self.client_type.encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

    def receive_message(self):
        message = self.client_socket.recv(1024).decode()
        print(f"Received from server: {message}")

    def disconnect(self):
        self.client_socket.sendall("terminate".encode())
        self.client_socket.close()
        print("Client connection closed")

    def run_publisher(self):
        self.connect()

        while True:
            message = input("Type a message to publish: ")
            self.send_message(message)

            if message.lower() == "terminate":
                break

        self.disconnect()

    def run_subscriber(self):
        self.connect()

        while True:
            self.receive_message()

        self.disconnect()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python my_client.py <server_ip> <port> <client_type>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = sys.argv[2]
    client_type = sys.argv[3]
    client_app = MyClientApp(server_ip, port, client_type)

    if client_type == "PUBLISHER":
        client_app.run_publisher()
    elif client_type == "SUBSCRIBER":
        client_app.run_subscriber()
