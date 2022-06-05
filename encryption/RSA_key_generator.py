from pathlib import Path

import rsa


class RSAKeygen:

    @staticmethod
    def generate_keys(client_name):
        (pub_key, priv_key) = rsa.newkeys(1024)
        Path('keys/{client_name}').mkdir(parents=True, exist_ok=True)

        with open(f'keys/{client_name}/pubkey.pem', 'wb') as f:
            f.write(pub_key.save_pkcs1('PEM'))

        with open(f'keys/{client_name}/privkey.pem', 'wb') as f:
            f.write(priv_key.save_pkcs1('PEM'))

    @staticmethod
    def load_keys(client_name):
        Path('keys/{client_name}').mkdir(parents=True, exist_ok=True)

        with open(f'keys/{client_name}/pubkey.pem', 'rb') as f:
            pubKey = rsa.PublicKey.load_pkcs1(f.read())

        with open(f'keys/{client_name}/privkey.pem', 'rb') as f:
            privKey = rsa   .PrivateKey.load_pkcs1(f.read())

        return pubKey, privKey

    @staticmethod
    def encrypt(msg, key):
        return rsa.encrypt(msg.encode('ascii'), key)

    @staticmethod
    def decrypt(ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('ascii')
        except KeyError:
            return False
