from kivy.uix.textinput import TextInput
from kivy.core.window import Window


class ChatMessageInput(TextInput):

    def __init__(self, **kwargs):
        super(ChatMessageInput, self).__init__(**kwargs)
        self.width = Window.size[0] * 0.85
        self.size_hint_x = None
        self.multiline = True
        self.background_color = (0.9, 0.9, 0.9, 1)
        self.padding = (12, 10)
