import socket
import threading
import pickle

from network.frame import Frame, FrameType


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.server_port = 10000
        self.clients = []
        self.connections = []
        self.connection_established = False
        self.sock.bind(('0.0.0.0', self.server_port))
        self.sock.listen()

        print("Server is starting...")

    def handle_client(self, conn, addr):
        print(f"[Connection from: {addr}")
        while True:
            data = conn.recv(1024)
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
            if threading.activeCount() - 1 == 2 and not self.connection_established:
                self.connection_established = True
                frame = Frame(None, FrameType.CONNECTED)
                data_bytes = pickle.dumps(frame)
                for connection in self.connections:
                    connection.sendall(data_bytes)
            print(f"[Active connections: {threading.activeCount() - 1}")


server = Server()
server.run()
