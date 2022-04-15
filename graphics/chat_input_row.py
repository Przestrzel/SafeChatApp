from kivy.uix.gridlayout import GridLayout
from graphics.chat_message_input import ChatMessageInput
from graphics.chat_button import ChatButton


class ChatInputRow(GridLayout):

    def __init__(self, **kwargs):
        super(ChatInputRow, self).__init__(**kwargs)
        self.cols = 2
        self.message = ChatMessageInput()
        self.add_widget(self.message)
        self.send_button = ChatButton(ChatInputRow.send_message, "Send")
        self.add_widget(self.send_button)

    @staticmethod
    def send_message(self):
        print("Sending")
