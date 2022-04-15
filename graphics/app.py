from kivy.app import App
from kivy.core.window import Window
from graphics.chat_page import ChatPage


class ChatApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 0.9)
        Window.size = (1024, 768)
        self.title = 'SafeChatApp'
        return ChatPage()

