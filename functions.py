import os
from config import KEY_FILE
from cryptography.fernet import Fernet

def load_key():
    """Loads a key from the `secret.key` file or creates a new one if the file does not exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    return key

# Loading the encryption key
key = load_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()