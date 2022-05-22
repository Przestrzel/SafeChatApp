from graphics.app import ChatApp
from encryption.RSA_key_generator import RSAKeygen
import sys

if __name__ == '__main__':
    try:
        client_name = sys.argv[1]
        app = ChatApp()
        app.run()
    except TypeError:
        print("Invalid argument occurred")

