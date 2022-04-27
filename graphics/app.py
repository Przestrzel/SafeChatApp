from kivy.app import App
from kivy.core.window import Window
from graphics.chat_page import ChatPage


class ChatApp(App):

    def __init__(self, **kwargs):
        super(ChatApp, self).__init__(**kwargs)
        Window.clearcolor = (0.1, 0.1, 0.1, 0.9)
        Window.size = (1024, 768)
        self.title = 'SafeChatApp'
        self.chat_page = ChatPage()
        self.history = self.chat_page.history

    def build(self):
        return self.chat_page
