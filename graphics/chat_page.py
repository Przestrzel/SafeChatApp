from kivy.uix.gridlayout import GridLayout
from graphics.chat_history import ChatHistory
from graphics.chat_input_row import ChatInputRow
from connection.client import Client
from messages.message_stack import MessageStack


class ChatPage(GridLayout):

    def __init__(self, **kwargs):
        super(ChatPage, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.message_stack = MessageStack()
        self.history = ChatHistory(get_message=self.message_stack.pop)
        self.client = Client(add_message=self.message_stack.push)
        self.input_row = ChatInputRow(self.history.add_message, self.client.send_message)
        self.add_widget(self.history)
        self.add_widget(self.input_row)

