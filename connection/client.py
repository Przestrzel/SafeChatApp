import socket
import threading
from messages.message import Message

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, add_message):
        self.addr = socket.gethostbyname(socket.gethostname())
        self.sock.connect((self.addr, 10000))
        self.add_message = add_message
        self.receive = threading.Thread(target=self.get_message, daemon=True)
        self.receive.start()

    def send_message(self, text):
        self.sock.send(bytes(str(text), 'utf-8'))

    def get_message(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            self.add_message(
                Message(str(data, 'utf-8'), is_my_message=False)
            )

