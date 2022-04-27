import rsa


class RSA:

    @staticmethod
    def generate_keys():
        (pub_key, priv_key) = rsa.newkeys(1024)
        with open('pubkey.pem', 'wb') as f:
            f.write(pub_key.save_pkcs1('PEM'))

        with open('privkey.pem', 'wb') as f:
            f.write(priv_key.save_pkcs1('PEM'))

    @staticmethod
    def load_keys():
        with open('pubkey.pem', 'rb') as f:
            pubKey = rsa.PublicKey.load_pkcs1(f.read())

        with open('privkey.pem', 'rb') as f:
            privKey = rsa.PrivateKey.load_pkcs1(f.read())

        return pubKey, privKey

    @staticmethod
    def encrypt(msg, key):
        return rsa.encrypt(msg.encode('ascii'), key)

    @staticmethod
    def decrypt(ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('ascii')
        except:
            return False


RSA.generate_keys()
pubKey, privKey = RSA.load_keys()

print("pubKey for client 1: \n", pubKey)
print("privKey for client 1: \n", privKey)
print("pubKey for client 2: \n", pubKey)
print("privKey for client 2: \n", privKey)

