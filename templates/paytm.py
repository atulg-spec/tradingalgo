import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class RechPayChecksum:
    iv = b"@@@@&&&&####$$$$"

    # Use a valid AES-256 key
    aes_key = "4xGhRSabz1"  # Replace this with your 32-byte (256-bit) key

    @staticmethod
    def encrypt(input, key):
        key = key.encode('utf-8')
        if 'openssl_encrypt' in dir():
            data = AES.new(key, AES.MODE_CBC, RechPayChecksum.iv).encrypt(input.encode())
        else:
            size = AES.block_size
            input = RechPayChecksum.pkcs5_pad(input.encode(), size)
            cipher = AES.new(key, AES.MODE_CBC, RechPayChecksum.iv)
            data = cipher.encrypt(input)
            data = base64.b64encode(data).decode()
        return data

    @staticmethod
    def decrypt(encrypted, key):
        key = key.encode('utf-8')
        if 'openssl_decrypt' in dir():
            data = AES.new(key, AES.MODE_CBC, RechPayChecksum.iv).decrypt(encrypted)
            data = data.decode('utf-8').rstrip('\0')
        else:
            encrypted = base64.b64decode(encrypted)
            cipher = AES.new(key, AES.MODE_CBC, RechPayChecksum.iv)
            data = cipher.decrypt(encrypted)
            data = RechPayChecksum.pkcs5_unpad(data).decode()
        return data

    @staticmethod
    def generate_signature(params, key):
        if not isinstance(params, (str, dict)):
            raise Exception("string or dictionary expected, {} given".format(type(params)))

        if isinstance(params, dict):
            params = RechPayChecksum.get_string_by_params(params)
        return RechPayChecksum.generate_signature_by_string(params, key)

    @staticmethod
    def verify_signature(params, key, checksum):
        if not isinstance(params, (str, dict)):
            raise Exception("string or dictionary expected, {} given".format(type(params)))

        if 'CHECKSUMHASH' in params:
            del params['CHECKSUMHASH']

        if isinstance(params, dict):
            params = RechPayChecksum.get_string_by_params(params)

        return RechPayChecksum.verify_signature_by_string(params, key, checksum)

    @staticmethod
    def generate_signature_by_string(params, key):
        salt = RechPayChecksum.generate_random_string(4)
        return RechPayChecksum.calculate_checksum(params, key, salt)

    @staticmethod
    def verify_signature_by_string(params, key, checksum):
        rechpay_hash = RechPayChecksum.decrypt(checksum, key)
        salt = rechpay_hash[-4:]
        return rechpay_hash == RechPayChecksum.calculate_hash(params, salt)

    @staticmethod
    def generate_random_string(length):
        import random
        import string
        data = "9876543210ZYXWVUTSRQPONMLKJIHGFEDCBAabcdefghijklmnopqrstuvwxyz!@#$&_"
        random_string = ''.join(random.choice(data) for _ in range(length))
        return random_string

    @staticmethod
    def get_string_by_params(params):
        sorted_params = sorted(params.items())
        params = '|'.join([str(value) if value is not None and str(value).lower() != "null" else "" for _, value in sorted_params])
        return params

    @staticmethod
    def calculate_hash(params, salt):
        final_string = params + "|" + salt
        hash_value = hashlib.sha256(final_string.encode()).hexdigest()
        return hash_value + salt

    @staticmethod
    def calculate_checksum(params, key, salt):
        hash_string = RechPayChecksum.calculate_hash(params, salt)
        return RechPayChecksum.encrypt(hash_string, key)

    @staticmethod
    def pkcs5_pad(text, blocksize):
        pad = blocksize - (len(text) % blocksize)
        return text + bytes([pad] * pad)

    @staticmethod
    def pkcs5_unpad(text):
        pad = text[-1]
        return text[:-pad]

def hash_decrypt(msg_encrypted_bundle, password):
    password = hashlib.sha1(password.encode()).hexdigest()

    components = msg_encrypted_bundle.split(':')
    iv = components[0].encode()
    salt = hashlib.sha256((password + components[1]).encode()).digest()
    encrypted_msg = base64.b64decode(components[2])

    cipher = AES.new(salt, AES.MODE_CBC, iv)
    decrypted_msg = cipher.decrypt(encrypted_msg).decode()
    msg = decrypted_msg[41:]
    return msg

if __name__ == "__main__":
    params = {
        "gateway_type": "Robotics",
        "upiuid": "paytmqr28100505010110sggy9gsszk@paytm",
        "token": '82e16b-54fd81-687682-f76ade-14d412',
        "orderId": "7d161217pf",
        "txnAmount": '10.0',
        "txnNote": "hello",
        "cust_Mobile": '9193660086',
        "cust_Email": 'admGGin@demo.com',
        "callback_url": "http://127.0.0.1:8000",
    }

    print(RechPayChecksum.generate_signature(
        params, RechPayChecksum.aes_key))
