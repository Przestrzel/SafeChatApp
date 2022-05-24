from utils.enums import MessageType

class Message:
    def __init__(self, text, is_my_message, message_type=MessageType.TEXT):
        self.text = text
        self.is_my_message = is_my_message
        self.message_type = message_type

    def __len__(self):
        return len(self.text)
