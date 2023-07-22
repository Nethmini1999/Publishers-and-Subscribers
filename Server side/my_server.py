

import socket
import threading
import sys

PORT = int(sys.argv[1])

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.client_type = None

    def run(self):
        try:
            self.client_type = self.client_socket.recv(1024).decode()
            print(f"New client connected: {self.client_address}. Type: {self.client_type}")
            self.send_message("Welcome to the server!")

            while True:
                message = self.client_socket.recv(1024).decode()
                if message:
                    if self.client_type == "PUBLISHER":
                        server.broadcast_message(self, message)
                    elif self.client_type == "SUBSCRIBER":
                        print(message)
                else:
                    break
        except ConnectionResetError:
            pass
        finally:
            self.client_socket.close()
            server.remove_client(self)

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

class Server:
    def __init__(self, port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.server_socket.bind(('', self.port))
        self.server_socket.listen()

        print(f"Server started on port {self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_handler = ClientHandler(client_socket, client_address)
            self.clients.append(client_handler)
            client_handler.start()

    def broadcast_message(self, sender, message):
        for client in self.clients:
            if client != sender and client.client_type == "SUBSCRIBER":
                client.send_message(message)

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
            print(f"Client disconnected: {client.client_address}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python my_server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = Server(port)
    server.start()
