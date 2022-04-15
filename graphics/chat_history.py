from kivy.uix.label import Label
from kivy.core.window import Window


class ChatHistory(Label):

    def __init__(self, **kwargs):
        super(ChatHistory, self).__init__(**kwargs)
        self.height = Window.size[1]*0.9
        self.size_hint_y = None
        