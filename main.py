from graphics.app import ChatApp
from encryption.RSA_key_generator import RSAKeygen
import sys

if __name__ == '__main__':
    client_name = sys.argv[1]
    app = ChatApp(client_name)
    app.run()

