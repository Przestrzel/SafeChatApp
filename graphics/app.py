from kivy.app import App
from kivy.core.window import Window

from encryption.RSA_key_generator import RSAKeygen
from encryption.AESCipher import AESCipher
from graphics.chat_page import ChatPage


class ChatApp(App):

    def __init__(self, client_name, **kwargs):
        super(ChatApp, self).__init__(**kwargs)
        Window.clearcolor = (0.1, 0.1, 0.1, 0.9)
        Window.size = (1024, 768)
        self.title = 'SafeChatApp'
        self.chat_page = ChatPage(client_name)
        self.aes = AESCipher(client_name)
        RSAKeygen().generate_keys(client_name, self.aes.encrypt)
        # pub_key, priv_key = RSAKeygen().load_keys(client_name, self.aes.decrypt)
        self.history = self.chat_page.upper.history
        self.input_row = self.chat_page.input_row

    def build(self):
        return self.chat_page
