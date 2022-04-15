from kivy.uix.button import Button


class ChatButton(Button):

    def __init__(self, callback, text, **kwargs):
        super(ChatButton, self).__init__(**kwargs)
        self.text = text
        self.bind(on_press=callback)

