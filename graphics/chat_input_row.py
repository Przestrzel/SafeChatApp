from kivy.uix.gridlayout import GridLayout
from graphics.chat_message_input import ChatMessageInput
from graphics.chat_button import ChatButton
from messages.message import Message


class ChatInputRow(GridLayout):

    def __init__(self, add_message, send_message, **kwargs):
        super(ChatInputRow, self).__init__(**kwargs)
        self.cols = 2
        self.add_message = add_message
        self.send_message = send_message
        self.message = ChatMessageInput()
        self.add_widget(self.message)
        self.send_button = ChatButton(self.send_message_ui, "Send")
        self.add_widget(self.send_button)

    def clear_input(self):
        self.message.text = ''

    def send_message_ui(self, _):
        if len(self.message.text) > 0:
            self.add_message(Message(text=self.message.text, is_my_message=True))
            self.send_message(self.message.text)

        self.clear_input()
