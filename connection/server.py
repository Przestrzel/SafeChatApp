import socket
import sys
import threading


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.server_port = 10000
        self.clients = []
        self.connections = []

        self.sock.bind(('0.0.0.0', self.server_port))
        self.sock.listen()

        print("Server is starting...")

    def handle_client(self, conn, addr):
        print(f"[Connection from: {addr}")
        while True:
            data = conn.recv(1024).decode('utf-8')
            for connection in self.connections:
                connection.send(data.encode())
            if not data:
                print(str(addr[0]) + ':' + str(addr[1]), " disconected")
                self.connections.remove(conn)
                conn.close()
                break

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
            thread.start()
            self.connections.append(conn)
            print(f"[Active connections: {threading.activeCount() - 1}")

server = Server()
server.run()