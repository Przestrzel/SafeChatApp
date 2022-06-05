from secrets import token_bytes


class SessionKey:

    @staticmethod
    def generate_key(length=32):
        return token_bytes(length)
