# CloudVault
# Password Manager Application

This is a simple password manager application built with Python and Tkinter, designed to securely store and manage passwords using encryption.

## Features

- **Add Password:** Allows users to add passwords for various sites securely.
- **Generate Password:** Provides a tool to generate strong passwords based on specified criteria.
- **View Passwords:** Displays a list of saved passwords and allows filtering by site or user.
- **Copy to Clipboard:** Enables copying decrypted passwords to the clipboard for easy use.
- **Encryption:** Uses Fernet encryption from the cryptography library to encrypt passwords stored in the database.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
   ```

2. **Install dependencies:**

Ensure you have Python installed. Install the required Python packages:

   ```bash
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
   ``` 

3. **Generate encryption key:**

Run the encryption script to generate the encryption key file (key.key):

```bash
python encryption.py
```

## Usage
1. Run the application:

```bash
python main.py
``` 

2. **Authentication:**
- On first launch, you will be prompted to enter a master password (default is '123' for demonstration purposes).
- Enter this master password to access the password manager.

3. **Functionality:**
- **Add Password:** Click "Add Password" to enter details for a new password.
- **Generate Password:** Click "Generate Password" to create a strong password based on your preferences.
- **View Passwords:** The main interface displays a list of saved passwords. Double-click an item to view details (authentication required).
- **Search:** Use the search bar to filter passwords by site or username.

## Technologies Used

- **Python:** Core programming language.
- **Tkinter:** Python's standard GUI library.
- **SQLite:** Lightweight SQL database for storing passwords.
- **cryptography:** Python library for encryption (used for password security).

## Contributing

Contributions are welcome! If you have suggestions, bug reports, or want to contribute code, please submit an issue or pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
