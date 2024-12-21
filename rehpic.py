from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def encrypt_password(password):
    key = get_random_bytes(16)  # Generate a random 128-bit key
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Initialization vector
    ciphertext = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
    
    # Return the IV and ciphertext encoded in base64 for storage
    return base64.b64encode(iv + ciphertext).decode('utf-8'), key


def decrypt_password(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]  # Extract the IV from the beginning
    ciphertext = encrypted_data[16:]  # The rest is the ciphertext
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return decrypted.decode('utf-8')
