
class MessageStack:
    def __init__(self):
        self.messages = []

    def push(self, message):
        self.messages.append(message)

    def pop(self):
        if len(self.messages) > 0:
            return self.messages.pop()
        return ""
