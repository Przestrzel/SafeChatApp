from kivy.uix.gridlayout import GridLayout
from graphics.chat_history import ChatHistory
from graphics.chat_input_row import ChatInputRow


class ChatPage(GridLayout):

    def __init__(self, **kwargs):
        super(ChatPage, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.history = ChatHistory()
        self.input_row = ChatInputRow(self.history.add_message)
        self.add_widget(self.history)
        self.add_widget(self.input_row)
