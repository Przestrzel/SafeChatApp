import socket
import struct
import threading
from messages.message import Message
import os
import pickle
from pathlib import Path

from network.frame import Frame, FrameType


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, add_message, client_name):
        self.addr = socket.gethostbyname(socket.gethostname())
        self.sock.connect((self.addr, 10000))
        self.add_message = add_message
        self.client_name = client_name
        self.receive = threading.Thread(target=self.get_message, daemon=True)
        self.receive.start()

    def send_message(self, text, is_text=True):
        if is_text:
            frame = Frame(text, FrameType.TEXT)
            data_bytes = pickle.dumps(frame)
            size_in_4_bytes = struct.pack('I', len(data_bytes))
            frame_size = Frame(size_in_4_bytes, FrameType.SIZE)
            data_size = pickle.dumps(frame_size)
            self.sock.sendall(data_size)

            self.sock.sendall(data_bytes)
        else:
            _, file_name = os.path.split(text)
            file = open(text, "r")
            data = file.read()
            frame = Frame(data, FrameType.FILE, file_name)
            data_bytes = pickle.dumps(frame)

            size_in_4_bytes = struct.pack('I', len(data_bytes))
            frame_size = Frame(size_in_4_bytes, FrameType.SIZE)
            data_size = pickle.dumps(frame_size)
            self.sock.sendall(data_size)

            self.sock.sendall(data_bytes)
            file.close()

    def get_message(self):
        size = len(pickle.dumps(Frame(struct.pack('I', 420), FrameType.SIZE)))
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            frame = pickle.loads(data)
            if frame.frame_type == FrameType.SIZE:
                size = struct.unpack('I', frame.data)
                size = size[0]
            if frame.frame_type == FrameType.TEXT and size is not None:
                self.add_message(Message(str(frame.data), is_my_message=False))
            elif frame.frame_type == FrameType.FILE and size is not None:
                Path(f'data/{self.client_name}').mkdir(parents=True, exist_ok=True)
                with open(f'data/{self.client_name}/' + frame.file_name, "w+") as file:
                    file.write(frame.data)
                self.add_message(Message(str('Plik :' + frame.file_name), is_my_message=False))
