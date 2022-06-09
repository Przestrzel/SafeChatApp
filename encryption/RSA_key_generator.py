from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


class RSAKeygen:

    @staticmethod
    def generate_keys(client_name, encrypt, chosen_mode):
        keys = RSA.generate(1024)
        pub_key = keys.publickey().export_key(format='PEM', passphrase=None, pkcs=1)
        priv_key = keys.export_key(format='PEM', passphrase=None, pkcs=1)
        priv_key_encrypted = encrypt(priv_key, chosen_mode)

        Path(f'keys/{client_name}').mkdir(parents=True, exist_ok=True)

        with open(f'keys/{client_name}/pubkey.pem', 'wb') as f:
            f.write(pub_key)

        with open(f'keys/{client_name}/privkey.pem', 'wb') as f:
            f.write(priv_key_encrypted)

    @staticmethod
    def load_keys(client_name, decrypt, chosen_mode):
        with open(f'keys/{client_name}/pubkey.pem', 'rb') as f:
            pub_key = f.read()

        with open(f'keys/{client_name}/privkey.pem', 'rb') as f:
            priv_key_encrypted = f.read()
            priv_key = decrypt(priv_key_encrypted, chosen_mode)
        return pub_key, priv_key

    @staticmethod
    def encrypt(msg, key):
        import_key = RSA.import_key(key)
        cipher = PKCS1_OAEP.new(key=import_key)
        return cipher.encrypt(msg)

    @staticmethod
    def decrypt(ciphertext, key):
        import_key = RSA.import_key(key)
        cipher = PKCS1_OAEP.new(key=import_key)
        return cipher.decrypt(ciphertext)
