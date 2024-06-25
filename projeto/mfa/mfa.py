import pyotp
import qrcode
from io import BytesIO
import base64
import webbrowser

## Params ####
# mfamain("jambo@parranda.es")
##############################
# Generate a TOTP secret for the user
def generate_totp_secret():
    return pyotp.random_base32()

# Generate a QR code for the TOTP secret
def generate_qr_code(secret, user_email):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user_email, issuer_name='SecureApp')

    # Generate QR code image
    qr = qrcode.make(uri)
    buffered = BytesIO()
    qr.save(buffered, format='PNG')
    qr_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return qr_image_base64

# Verify the TOTP code entered by the user
def verify_totp_code(secret, user_code):
    totp = pyotp.TOTP(secret)
    return totp.verify(user_code)

# Main function to demonstrate MFA setup and verification
def mfamain(user_email):
    # Simulated user email (you can replace this with actual user input)
    if not user_email:
        user_email = "user@example.com"

    # Generate a TOTP secret for the user
    secret = generate_totp_secret()
    print(f"TOTP secret for {user_email}: {secret}")

    # Generate QR code image
    qr_image_base64 = generate_qr_code(secret, user_email)

    # Display the QR code to the user (using default image viewer)
    qr_image_path = 'totp_qr.png'
    with open(qr_image_path, 'wb') as f:
        f.write(base64.b64decode(qr_image_base64))

    print("A QR code has been generated. It will now be displayed in your default image viewer.")
    webbrowser.open(qr_image_path)

    # In a real application, the user would scan this QR code with their authenticator app.

    # Ask the user to enter the TOTP code from their authenticator app
    user_code = input("Enter the TOTP code from your authenticator app: ")

    # Verify the TOTP code entered by the user
    if verify_totp_code(secret, user_code):
        print("TOTP code is valid! MFA setup is successful.")
        return True
    else:
        print("TOTP code is invalid! MFA setup failed.")
        return False
