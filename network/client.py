import socket
import threading
from messages.message import Message
import os
import pickle

from network.frame import Frame, FrameType


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, add_message):
        self.addr = socket.gethostbyname(socket.gethostname())
        self.sock.connect((self.addr, 10000))
        self.add_message = add_message
        self.receive = threading.Thread(target=self.get_message, daemon=True)
        self.receive.start()

    def send_message(self, text, is_text=True):
        if is_text:
            frame = Frame(text, FrameType.TEXT)
            data_bytes = pickle.dumps(frame)
            # self.sock.send(bytes(str(text), 'utf-8'))
            self.sock.send(data_bytes)
        else:
            # text is path to file
            _, file_name = os.path.split(text)
            print(file_name)
            self.sock.send(bytes(str(file_name), 'utf-8'))

            file = open(text, "r")
            data = file.read()

            frame = Frame(data, FrameType.FILE, file_name)
            data_bytes = pickle.dumps(frame)
            self.sock.send(data_bytes)
            file.close()

            # pass


    def get_message(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            frame = pickle.loads(data)
            if frame.frame_type == FrameType.TEXT:
                self.add_message(Message(str(frame.data, 'utf-8'), is_my_message=False))
            elif frame.frame_type == FrameType.FILE:
                with open('downloaded_files/' + frame.file_name, "a+b") as file:
                    file.write(frame.data)
                self.add_message(Message(str('💌 :' + frame.file_name, 'utf-8'), is_my_message=False))

