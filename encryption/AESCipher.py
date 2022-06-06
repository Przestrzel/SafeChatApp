import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCipher(object):

    def __init__(self, key, hash_key=True):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest() if hash_key else key

    def encrypt(self, raw, mode):
        padded_raw = pad(raw, self.bs)
        if mode == AES.MODE_ECB:
            cipher = AES.new(self.key, mode)
            return cipher.encrypt(padded_raw)
        else:
            iv = Random.new().read(self.bs)
            cipher = AES.new(self.key, mode, iv)
            return iv + cipher.encrypt(padded_raw)

    def decrypt(self, enc, mode):
        if mode == AES.MODE_ECB:
            cipher = AES.new(self.key, AES.MODE_ECB)
            raw = cipher.decrypt(enc)
            return unpad(raw, self.bs)
        else:
            cipher = AES.new(self.key, mode, enc[:AES.block_size])
            raw = cipher.decrypt(enc[AES.block_size:])
            return unpad(raw, self.bs)
