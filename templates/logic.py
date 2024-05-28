import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class RechPayChecksum:
    def __init__(self):
        self.iv = b"@@@@&&&&####$$$$"  # Initialization Vector (IV)
    
    def encrypt(self, input_data, key):
        cipher = AES.new(key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(input_data.encode(), AES.block_size))
        return ciphertext

    def decrypt(self, encrypted_data, key):
        cipher = AES.new(key, AES.MODE_CBC, self.iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted_data.decode()

    def generate_signature(self, params, key):
        if isinstance(params, dict):
            params_str = "|".join([f"{k}:{v}" for k, v in params.items()])
        elif isinstance(params, str):
            params_str = params
        else:
            raise ValueError("Input 'params' should be a dictionary or a string")

        # Calculate the SHA-256 hash of the concatenated parameters
        sha256_hash = hashlib.sha256(params_str.encode()).hexdigest()

        # Encrypt the SHA-256 hash using AES-128-CBC with the provided key
        key_bytes = key.encode()  # Convert the key to bytes
        encrypted_hash = self.encrypt(sha256_hash, key_bytes)

        return encrypted_hash

    def verify_signature(self, params, key, checksum):
        # Decrypt the checksum using AES-128-CBC with the provided key
        key_bytes = key.encode()  # Convert the key to bytes
        decrypted_checksum = self.decrypt(checksum, key_bytes)

        if isinstance(params, dict):
            params_str = "|".join([f"{k}:{v}" for k, v in params.items()])
        elif isinstance(params, str):
            params_str = params
        else:
            raise ValueError("Input 'params' should be a dictionary or a string")

        # Calculate the SHA-256 hash of the concatenated parameters
        sha256_hash = hashlib.sha256(params_str.encode()).hexdigest()

        # Check if the decrypted checksum matches the calculated SHA-256 hash
        return decrypted_checksum == sha256_hash

import requests
import time
# Example usage:
params = {
    "gateway_type":"Advanced",
    "upiuid": "paytmqr28100505010110sggy9gsszk@paytm",
    "token":'82e16b-54fd81-687682-f76ade-14d412',
    "orderId":f'SPINFOTECH{int(time.time())}',
    "txnAmount":10,
    "txnNote":"hello",
    "cust_Mobile":'9193660086',
    "cust_Email":'admGGin@demo.com',
    "callback_url":"https://apiqr.upibuz.in/trial/txnResult.php",
}
original_key = '4xGhRSabz1'
original_key_bytes = original_key.encode('utf-8')
# key = original_key.ljust(16, '\0')[:16].encode('utf-8')
key = (original_key_bytes + b'\0' * (16 - len(original_key_bytes)))[:16].decode()
 # Your key as a string
rechpay_checksum = RechPayChecksum()
signature = rechpay_checksum.generate_signature(params, key)
print("Generated Signature:", signature.hex())

params["checksum"] = signature.hex()

url = "https://apiqr.upibuz.in/order/payment"
response = requests.post(url, data=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print(response.text)
else:
    print(f"Request failed with status code {response.status_code}")

