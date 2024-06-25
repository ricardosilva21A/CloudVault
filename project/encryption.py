"""
@file encryption.py
@brief Functions for encrypting and decrypting passwords using cryptography.fernet.

Authors:
- Ricardo Silva
- Guillermo
- Saúl

@date 2024
@version 1.0
@note SAP: PYTHON 2024

This module provides functions to generate encryption keys, encrypt passwords, and decrypt passwords
using the cryptography.fernet library.
"""

from cryptography.fernet import Fernet

def generate_key():
    """
    @brief Generates an encryption key and saves it to a file named 'key.key'.
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key(key_path="key.key"):
    """
    @brief Loads the encryption key from a specified file.

    @param key_path The path to the file containing the encryption key (default is 'key.key').
    @return The encryption key loaded from the file.
    """
    with open(key_path, "rb") as key_file:
        key = key_file.read()
    return key

def encrypt_password(password):
    """
    @brief Encrypts a password using the loaded encryption key.

    @param password The password to encrypt.
    @return The encrypted password as bytes.
    """
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    """
    @brief Decrypts an encrypted password using the loaded encryption key.

    @param encrypted_password The encrypted password to decrypt (as bytes).
    @return The decrypted password as a string.
    """
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Generate the encryption key once (execute only once)
if __name__ == "__main__":
    generate_key()