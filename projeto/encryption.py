from cryptography.fernet import Fernet

# Generate a key and save it to a file
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Example of modifying the load_key function to accept a file path argument
def load_key(key_path="key.key"):
    with open(key_path, "rb") as key_file:
        key = key_file.read()
    return key

# Encrypt a password
def encrypt_password(passwords):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(passwords.encode())
    return encrypted_password

# Decrypt a password
def decrypt_password(encrypted_passwords):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_passwords).decode()
    return decrypted_password

# Generate the key once (execute only once)
if __name__ == "__main__":
    generate_key()
