import socket
import struct
import threading
from time import sleep

from encryption.AESCipher import AESCipher
from encryption.RSA_key_generator import RSAKeygen
from encryption.session_key import SessionKey
from messages.message import Message
import os
import pickle
from pathlib import Path
from network.frame import Frame, FrameType
from Crypto.Cipher import AES


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, add_message, client_name, update_progress):
        self.aes = AESCipher(client_name)
        RSAKeygen().generate_keys(client_name, self.aes.encrypt)
        self.pub_key, self.priv_key = RSAKeygen().load_keys(client_name, self.aes.decrypt)
        self.stranger_key = None
        self.addr = socket.gethostbyname(socket.gethostname())
        self.sock.connect((self.addr, 10000))
        self.add_message = add_message
        self.client_name = client_name
        self.session_key = None

        self.update_progress = update_progress
        self.receive = threading.Thread(target=self.get_message, daemon=True)
        self.receive.start()

    def send_message(self, text, is_text=True):
        session_key = SessionKey.generate_key(32)
        if self.stranger_key is None:
            return
        session_encrypted = RSAKeygen.encrypt(session_key, self.stranger_key)
        frame = Frame(session_encrypted, FrameType.SESSION_KEY)
        data_bytes = pickle.dumps(frame)

        size_in_4_bytes = struct.pack('I', len(data_bytes))
        frame_size = Frame(size_in_4_bytes, FrameType.SIZE)
        data_size = pickle.dumps(frame_size)
        self.sock.sendall(data_size)

        self.sock.sendall(data_bytes)

        aes_cipher = AESCipher(session_key, False)
        sleep(0.1)
        if is_text:
            encrypted_text = aes_cipher.encrypt(bytes(text, 'utf-8'), AES.MODE_ECB)
            frame = Frame(encrypted_text, FrameType.TEXT)
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
                self.update_progress(progress / file_size * 100)

            file.close()

    def get_message(self):
        size = 8192
        while True:
            data = self.sock.recv(size)
            if not data:
                continue
            frame = pickle.loads(data)
            if frame.frame_type == FrameType.CONNECTED:
                frame = Frame(self.pub_key, FrameType.RSA_KEY)
                data_bytes = pickle.dumps(frame)
                self.sock.sendall(data_bytes)
            elif frame.frame_type == FrameType.SESSION_KEY:
                self.session_key = RSAKeygen.decrypt(frame.data, self.priv_key)
            elif frame.frame_type == FrameType.RSA_KEY:
                self.stranger_key = frame.data
            elif frame.frame_type == FrameType.SIZE:
                size = struct.unpack('I', frame.data)
                size = size[0]
            elif frame.frame_type == FrameType.TEXT and size is not None:
                aes_cipher = AESCipher(self.session_key, False)
                decrypted_message = aes_cipher.decrypt(frame.data, AES.MODE_ECB)
                self.add_message(Message(decrypted_message.decode('utf-8'), is_my_message=False))
            elif frame.frame_type == FrameType.FILE and size is not None:
                Path(f'data/{self.client_name}').mkdir(parents=True, exist_ok=True)

                with open(f'data/{self.client_name}/' + frame.file_name, "wb") as file:
                    file_size = frame.data
                    while file_size > 0:
                        file_data = self.sock.recv(1024)
                        file_size = file_size - len(file_data)
                        file.write(file_data)
                self.add_message(Message(str('Plik :' + frame.file_name), is_my_message=False))
