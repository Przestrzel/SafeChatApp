from kivy.uix.progressbar import ProgressBar


class ChatProgressBar(ProgressBar):

    def __init__(self, value, **kwargs):
        super(ChatProgressBar, self).__init__(**kwargs)
        self.value = value
        self.max = 100

    def set_value(self, progress_value):
        self.value = progress_value
        if self.value > 100:
            self.value = 0

