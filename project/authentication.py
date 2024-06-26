# authentication.py

import pyotp
import qrcode

# Função para gerar uma chave secreta
def generate_secret_key():
    return pyotp.random_base32()

# Função para gerar a URI do TOTP
def generate_totp_uri(username, secret_key):
    return pyotp.totp.TOTP(secret_key, issuer_name=username).provisioning_uri(username, issuer_name=username)

# Função para gerar o QR Code
def generate_qr_code(uri, filename):
    img = qrcode.make(uri)
    img.save(filename)

# Função para verificar o código TOTP
def verify_totp_token(secret_key, token):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(token)
