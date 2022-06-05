import os

from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from graphics.chat_progressbar import ChatProgressBar

from utils.enums import MessageType

MESSAGE_BORDER = 12
MAX_MESSAGE_LENGTH = 280
MIN_MESSAGE_LENGTH = 40


class ChatHistory(GridLayout):

    def __init__(self, get_message, **kwargs):
        super(ChatHistory, self).__init__(**kwargs)
        self.height = Window.size[1] * 0.9
        self.cols = 1
        self.rows = 22
        self.size_hint_y = None
        self.row_default_height = 60
        self.get_message = get_message
        self.progress_bar = ChatProgressBar(value=0)
        Clock.schedule_interval(self.listen_stack, 0.1)

    def add_message(self, message):
        if message.message_type == MessageType.FILE:
            self.load_progress(0)
        else:
            self.add_widget(ChatHistoryMessage(message))

    def load_progress(self, value):
        if value > 0:
            is_progress_bar_on = False
            for c in list(self.children):
                if isinstance(c, ChatProgressBar):
                    is_progress_bar_on = True

            if not is_progress_bar_on:
                self.add_widget(self.progress_bar)

        if self.progress_bar.value + value >= 100:
            for c in list(self.children):
                if isinstance(c, ChatProgressBar):
                    self.remove_widget(c)

        self.progress_bar.set_value(self.progress_bar.value + value)

    def listen_stack(self, dt):
        message = self.get_message()
        if len(message) > 0:
            self.add_message(message)


class ChatHistoryMessage(AnchorLayout):

    def __init__(self, message, **kwargs):
        super(ChatHistoryMessage, self).__init__(**kwargs)
        self.anchor_x = 'right' if message.is_my_message else 'left'
        self.anchor_y = 'center'
        self.padding = [20, 10, 0, 10] if not message.is_my_message else [0, 10, 20, 10]
        self.message = ChatHistoryMessageLabel(message)
        self.add_widget(self.message)


class ChatHistoryMessageLabel(Label):

    def __init__(self, message, **kwargs):
        super(ChatHistoryMessageLabel, self).__init__(**kwargs)
        text = message.text if message.message_type == MessageType.TEXT else {os.path.split(message.text)[1]}
        file_prefix = "Przesłano" if message.is_my_message else "Otrzymano"
        self.text = text if message.message_type == MessageType.TEXT else f"{file_prefix} plik: {text}"
        self.is_my_message = message.is_my_message
        self.message_type = message.message_type
        message_length = len(self.text) * 13

        if message_length > MAX_MESSAGE_LENGTH:
            message_length = MAX_MESSAGE_LENGTH
        elif message_length < MIN_MESSAGE_LENGTH:
            message_length = MIN_MESSAGE_LENGTH

        self.width = message_length
        self.text_size = self.size
        self.padding = [10, 0]
        self.halign = 'right' if self.is_my_message else 'left'
        self.valign = 'center'
        self.color = (0.9, 0.9, 0.9, 1)
        self.size_hint_x = None

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0.8, 0, 0.7) if not self.is_my_message else Color(0, 0, 0.8, 0.7)
            RoundedRectangle(pos=self.pos,
                             size=self.size,
                             radius=[0, MESSAGE_BORDER, MESSAGE_BORDER, MESSAGE_BORDER] if not self.is_my_message
                             else [MESSAGE_BORDER, 0, MESSAGE_BORDER, MESSAGE_BORDER])
