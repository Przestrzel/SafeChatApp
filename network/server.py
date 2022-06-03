import socket
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
            data = conn.recv(4096)
            for connection in self.connections:
                if connection == conn:
                    continue
                connection.sendall(data)

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
            thread.start()
            self.connections.append(conn)
            print(f"[Active connections: {threading.activeCount() - 1}")


server = Server()
server.run()
