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
        self.upper = ChatPageUpper(get_message=self.message_stack.pop, add_message=self.message_stack.push,
                                   client_name=client_name)
        self.input_row = ChatInputRow(self.upper.history.add_message, self.upper.client.send_message)

        self.add_widget(self.upper)
        self.add_widget(self.input_row)


class ChatPageUpper(GridLayout):

    def __init__(self, get_message, add_message, client_name, **kwargs):
        super(ChatPageUpper, self).__init__(**kwargs)
        self.cols = 2
        self.cols_minimum = {0: 800, 1: 200}
        self.client = Client(add_message, client_name, self.update_progress_bar)
        self.history = ChatHistory(get_message)
        self.toolbox = Toolbox(self.client.send_message, add_message)
        self.add_widget(self.history)
        self.add_widget(self.toolbox)

    def update_progress_bar(self, value):
        self.history.load_progress(value)
