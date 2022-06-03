from kivy.uix.gridlayout import GridLayout
from graphics.chat_toolbox import Toolbox
from graphics.chat_history import ChatHistory
from graphics.chat_input_row import ChatInputRow
from network.client import Client
from messages.message_stack import MessageStack


class ChatPage(GridLayout):

    def __init__(self, client_name, **kwargs):
        super(ChatPage, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.rows_minimum = {0: 650, 1: 100}
        self.message_stack = MessageStack()
        self.client = Client(self.message_stack.push, client_name)
        self.upper = ChatPageUpper(get_message=self.message_stack.pop, send_message=self.client.send_message,
                                   add_message=self.message_stack.push)
        self.input_row = ChatInputRow(self.upper.history.add_message, self.client.send_message)
        self.add_widget(self.upper)
        self.add_widget(self.input_row)


class ChatPageUpper(GridLayout):

    def __init__(self, get_message, send_message, add_message, **kwargs):
        super(ChatPageUpper, self).__init__(**kwargs)
        self.cols = 2
        self.cols_minimum = {0: 800, 1: 200}
        self.history = ChatHistory(get_message)
        self.toolbox = Toolbox(send_message, add_message)
        self.add_widget(self.history)
        self.add_widget(self.toolbox)

    def update_progress_bar(self, value):
        self.history.load_progress(value)
