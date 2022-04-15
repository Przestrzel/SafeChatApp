from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

MESSAGE_BORDER = 12


class ChatHistory(GridLayout):

    def __init__(self, **kwargs):
        super(ChatHistory, self).__init__(**kwargs)
        self.height = Window.size[1]*0.9
        self.cols = 1
        self.rows = 22
        self.size_hint_y = None
        self.row_default_height = 60

    def add_message(self, text):
        self.add_widget(ChatHistoryMessage(text=text, is_my_message=True))


class ChatHistoryMessage(AnchorLayout):

    def __init__(self, text, is_my_message, **kwargs):
        super(ChatHistoryMessage, self).__init__(**kwargs)
        self.anchor_x = 'left' if is_my_message else 'right'
        self.anchor_y = 'center'
        self.padding = [20, 10, 0, 10] if is_my_message else [0, 10, 20, 10]
        self.message = ChatHistoryMessageLabel(text=text, is_my_message=is_my_message)
        self.add_widget(self.message)


class ChatHistoryMessageLabel(Label):

    def __init__(self, text, is_my_message, **kwargs):
        super(ChatHistoryMessageLabel, self).__init__(**kwargs)
        self.text = text
        self.border = 50
        self.is_my_message = is_my_message
        self.color = (0.9, 0.9, 0.9, 1)
        self.size_hint_x = None

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0.8, 0, 0.7) if self.is_my_message else Color(0, 0, 0.8, 0.7)
            RoundedRectangle(pos=self.pos,
                             size=self.size,
                             radius=[0, MESSAGE_BORDER, MESSAGE_BORDER, MESSAGE_BORDER] if self.is_my_message
                             else [MESSAGE_BORDER, 0, MESSAGE_BORDER, MESSAGE_BORDER])
