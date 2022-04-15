from kivy.uix.button import Button


class ChatButton(Button):

    def __init__(self, callback, text, **kwargs):
        super(ChatButton, self).__init__(**kwargs)
        self.text = text
        self.padding = (12, 10)
        self.font_family = "Roboto"
        self.bind(on_press=callback)

