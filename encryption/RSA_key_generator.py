import rsa


class RSAKeygen:

    @staticmethod
    def generate_keys(client_name):
        (pub_key, priv_key) = rsa.newkeys(1024)
        with open(f'pubkey_{client_name}.pem', 'wb') as f:
            f.write(pub_key.save_pkcs1('PEM'))

        with open(f'privkey_{client_name}.pem', 'wb') as f:
            f.write(priv_key.save_pkcs1('PEM'))

    @staticmethod
    def load_keys(client_name):
        with open(f'pubkey_{client_name}.pem', 'rb') as f:
            pubKey = rsa.PublicKey.load_pkcs1(f.read())

        with open(f'privkey_{client_name}.pem', 'rb') as f:
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
