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

    def __init__(self, add_message, client_name, update_progress):
        self.addr = socket.gethostbyname(socket.gethostname())
        self.sock.connect((self.addr, 10000))
        self.add_message = add_message
        self.client_name = client_name
        self.update_progress = update_progress
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
            file_size = os.path.getsize(text)
            frame = Frame(file_size, FrameType.FILE, file_name)
            data_bytes = pickle.dumps(frame)

            size_in_4_bytes = struct.pack('I', len(data_bytes))
            frame_size = Frame(size_in_4_bytes, FrameType.SIZE)
            data_size = pickle.dumps(frame_size)
            self.sock.sendall(data_size)
            self.sock.sendall(data_bytes)

            file = open(text, "rb")
            progress = 0
            while True:
                data = file.read(1024)
                if not data:
                    break

                self.sock.sendall(data)
                progress += 1024
                self.update_progress(progress/file_size * 100)

            file.close()

    def get_message(self):
        size = len(pickle.dumps(Frame(struct.pack('I', 420), FrameType.SIZE)))
        while True:
            data = self.sock.recv(size)
            if not data:
                continue
            frame = pickle.loads(data)
            if frame.frame_type == FrameType.SIZE:
                size = struct.unpack('I', frame.data)
                size = size[0]
            elif frame.frame_type == FrameType.TEXT and size is not None:
                self.add_message(Message(str(frame.data), is_my_message=False))
            elif frame.frame_type == FrameType.FILE and size is not None:
                Path(f'data/{self.client_name}').mkdir(parents=True, exist_ok=True)

                with open(f'data/{self.client_name}/' + frame.file_name, "wb") as file:
                    file_size = frame.data
                    while file_size > 0:
                        file_data = self.sock.recv(1024)
                        file_size = file_size - len(file_data)
                        file.write(file_data)
                self.add_message(Message(str('Plik :' + frame.file_name), is_my_message=False))
