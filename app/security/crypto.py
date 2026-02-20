from cryptography.fernet import Fernet
import os

KEY_PATH = "secrets/report_key.key"

def get_key():
    os.makedirs("secrets", exist_ok=True)
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)
    else:
        with open(KEY_PATH, "rb") as f:
            key = f.read()
    return key


def encrypt_file(path: str):
    key = get_key()
    fernet = Fernet(key)
    with open(path, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(path + ".enc", "wb") as f:
        f.write(encrypted)
    os.remove(path)


def decrypt_file(enc_path: str, out_path: str):
    key = get_key()
    fernet = Fernet(key)
    with open(enc_path, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    with open(out_path, "wb") as f:
        f.write(decrypted)
