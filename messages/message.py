class Message:
    def __init__(self, text, is_my_message):
        self.text = text
        self.is_my_message = is_my_message

    def __len__(self):
        return len(self.text);