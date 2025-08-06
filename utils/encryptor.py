from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return encrypted

def decrypt_data(token, key):
    f = Fernet(key)
    decrypted = f.decrypt(token).decode()
    return decrypted