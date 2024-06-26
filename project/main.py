"""
@file password_manager.py
@brief Password Manager application for securely storing and managing passwords.

Authors:
- Ricardo Silva
- Guillermo López de Arechavaleta
- Saúl Sauca

@date 2024
@version 1.0
@note SAP: PYTHON 2024

This program allows users to securely store passwords for different websites,
generate custom passwords, and manage them securely using encryption techniques.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import string
import random
import hashlib
import pyperclip
from PIL import Image, ImageTk
import customtkinter as ctk  # Assuming this is your custom Tkinter library
from encryption import encrypt_password, decrypt_password
from database import create_db, add_password, get_passwords, search_passwords_by_site_user
import os

# Initialize or create the database
create_db()

# Path to store the hash of the master password
MASTER_PASSWORD_FILE = "master_password.txt"

def hash_password(password):
    """
    @brief Hashes the given password using SHA-256.

    @param password The password to hash.
    @return The hashed password as a hexadecimal string.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def save_master_password(password_hash):
    """
    @brief Saves the hashed master password to a file.

    @param password_hash The hashed master password to save.
    """
    with open(MASTER_PASSWORD_FILE, "w") as file:
        file.write(password_hash)

def load_master_password():
    """
    @brief Loads the hashed master password from a file.

    @return The hashed master password as a string, or None if the file doesn't exist.
    """
    if os.path.exists(MASTER_PASSWORD_FILE):
        with open(MASTER_PASSWORD_FILE, "r") as file:
            return file.read().strip()
    return None

# Load the stored master password hash
stored_master_password = load_master_password()

def setup_master_password():
    """
    @brief Guides the user through setting up the master password.

    @return The hashed master password once successfully set up.
    """
    while True:
        new_master_password = simpledialog.askstring("Setup Master Password", "Set your master password:", show='*')
        confirm_master_password = simpledialog.askstring("Confirm Master Password", "Confirm your master password:", show='*')

        if new_master_password and new_master_password == confirm_master_password:
            password_hash = hash_password(new_master_password)
            save_master_password(password_hash)
            messagebox.showinfo("Setup Complete", "Master password has been set up successfully.")
            return password_hash
        else:
            messagebox.showerror("Error", "Passwords do not match or were not provided. Please try again.")

def authenticate_on_start():
    """
    @brief Authenticates the user at the start of the program.

    Prompts the user to enter the master password and verifies it against the stored hash.
    """
    global stored_master_password

    if stored_master_password is None:
        stored_master_password = setup_master_password()

    while True:
        master_password_entered = simpledialog.askstring("Authentication", "Enter your master password to access the password manager:", show='*')
        if master_password_entered is None:
            exit()  # Exit the program if the user cancels
        master_password_hash = hash_password(master_password_entered)

        if master_password_hash == stored_master_password:
            messagebox.showinfo("Authentication", "Authentication successful. Welcome to the Password Manager.")
            break
        else:
            messagebox.showerror("Authentication Error", "Incorrect master password. Please try again.")
def generate_custom_password():
    """
    @brief Generates a custom password based on user preferences.

    Allows users to specify password length and select character types (uppercase, numbers, symbols).
    """
    top = tk.Toplevel()
    top.title("Generate Custom Password")
    top.geometry("500x400")  # Increased size of the popup window

    label_title = ctk.CTkLabel(top, text="Custom Password Generator", font=("Arial", 16))
    label_title.pack(pady=10)

    # Labels and entry for password length
    frame_length = ctk.CTkFrame(top)
    frame_length.pack(pady=10)

    label_length = ctk.CTkLabel(frame_length, text="Password Length:", width=30)
    label_length.grid(row=0, column=0, padx=10, sticky="w")
    entry_length = ctk.CTkEntry(frame_length, width=50)
    entry_length.grid(row=0, column=1, padx=10)

    # Checkbuttons for password options
    frame_options = ctk.CTkFrame(top)
    frame_options.pack(pady=10)

    var_uppercase = tk.IntVar()
    var_numbers = tk.IntVar()
    var_symbols = tk.IntVar()

    check_uppercase = ctk.CTkCheckBox(frame_options, text="Include Uppercase", variable=var_uppercase)
    check_uppercase.grid(row=0, column=0, padx=10, sticky="w")
    check_numbers = ctk.CTkCheckBox(frame_options, text="Include Numbers", variable=var_numbers)
    check_numbers.grid(row=0, column=1, padx=10, sticky="w")
    check_symbols = ctk.CTkCheckBox(frame_options, text="Include Symbols", variable=var_symbols)
    check_symbols.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")

    # Textbox to display generated password
    frame_password = ctk.CTkFrame(top)
    frame_password.pack(pady=10)

    label_generated_password = ctk.CTkLabel(frame_password, text="Generated Password:")
    label_generated_password.grid(row=0, column=0, padx=10, sticky="w")

    entry_generated_password = ctk.CTkEntry(frame_password, width=300, state="readonly")  # Readonly textbox
    entry_generated_password.grid(row=1, column=0, padx=10)

    # Button to generate password
    btn_generate = ctk.CTkButton(top, text="Generate Password", command=lambda: generate_and_show_custom_password(top, entry_length.get(), var_uppercase.get(), var_numbers.get(), var_symbols.get()))
    btn_generate.pack(pady=10)

    def generate_and_show_custom_password(top, length, include_uppercase, include_numbers, include_symbols):
        """
        @brief Generates and displays a custom password based on user input.

        @param top The top-level Tkinter window.
        @param length The length of the password to generate.
        @param include_uppercase Whether to include uppercase letters in the password.
        @param include_numbers Whether to include numbers in the password.
        @param include_symbols Whether to include symbols in the password.
        """
        try:
            length = int(length)
            if length <= 0:
                messagebox.showerror("Error", "Password length must be greater than zero.")
                return

            characters = string.ascii_lowercase
            if include_uppercase:
                characters += string.ascii_uppercase
            if include_numbers:
                characters += string.digits
            if include_symbols:
                characters += string.punctuation

            generated_password = ''.join(random.choice(characters) for _ in range(length))
            entry_generated_password.configure(state="normal")  # Allow modification
            entry_generated_password.delete(0, tk.END)  # Clear previous content
            entry_generated_password.insert(0, generated_password)  # Display generated password
            entry_generated_password.configure(state="readonly")  # Disable modification

            messagebox.showinfo("Generated Password", f"Your generated password is:\n{generated_password}")

            top.focus_force()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the password length.")

    # Button to copy password to clipboard
    btn_copy_password = ctk.CTkButton(top, text="Copy to Clipboard", command=lambda: copy_to_clipboard(entry_generated_password.get()))
    btn_copy_password.pack(pady=10)

    def copy_to_clipboard(password):
        """
        @brief Copies the generated password to the clipboard.

        @param password The generated password to copy.
        """
        top.clipboard_clear()
        top.clipboard_append(password)
        top.update()  # Ensure clipboard content is updated

    top.mainloop()


def add_password_ui():
    """
    @brief Prompts the user to add a new password to the database.

    Encrypts the password and adds it to the database.
    """
    site = simpledialog.askstring("Site", "Site name:")
    user = simpledialog.askstring("User", "Username:")
    password = simpledialog.askstring("Password", "Password:", show='*')

    if not site or not user or not password:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    encrypted_password = encrypt_password(password)
    add_password(site, user, encrypted_password)
    messagebox.showinfo("Success", "Password added successfully!")

    show_passwords_in_list()  # Update the passwords list

def show_passwords_in_list():
    """
    @brief Retrieves and displays all passwords in the listbox.
    """
    passwords = get_passwords()

    listbox_passwords.delete(0, tk.END)  # Clear the current list

    for password in passwords:
        site, user, _ = password[1], password[2], password[3]
        listbox_passwords.insert(tk.END, f"{site} | {user}")

def show_filtered_passwords(event=None):
    """
    @brief Filters and displays passwords based on search criteria.

    @param event The event (typically a key release in the search entry).
    """
    filter_text = entry_search.get()

    if filter_text:
        passwords = search_passwords_by_site_user(filter_text)
        listbox_passwords.delete(0, tk.END)  # Clear the current list

        for password in passwords:
            site, user, _ = password[1], password[2], password[3]
            listbox_passwords.insert(tk.END, f"{site} | {user}")
    else:
        show_passwords_in_list()

def show_user_and_password(event):
    """
    @brief Displays the username and decrypted password when an item in the listbox is double-clicked.

    @param event The event triggered by double-clicking on an item in the listbox.
    """
    widget = event.widget
    if widget.curselection():
        index = int(widget.curselection()[0])
        site_and_user = widget.get(index)

        # Extract site and user from the selected item in the list
        site, user = site_and_user.split(" | ")

        master_password_entered = simpledialog.askstring("Master Password", "Enter your master password to view the password:", show='*')
        master_password_hash = hash_password(master_password_entered)

        if master_password_hash == stored_master_password:
            passwords = search_passwords_by_site_user(site, user)

            if passwords:
                decrypted_password = decrypt_password(passwords[0][3])
                pyperclip.copy(decrypted_password)

                top = tk.Toplevel()
                top.title(f"Password Details for {site}")
                top.geometry("300x150")

                label_user = tk.Label(top, text=f"User: {user}", font=("Arial", 12))
                label_user.pack(pady=10)

                label_password = tk.Label(top, text=f"Password: {decrypted_password}", font=("Arial", 12))
                label_password.pack(pady=10)

                btn_copy = tk.Button(top, text="Copy to Clipboard", command=lambda: pyperclip.copy(decrypted_password))
                btn_copy.pack(pady=10)

                top.focus_force()
            else:
                messagebox.showerror("Error", f"Password not found for {site} and user {user}.")
        else:
            messagebox.showerror("Authentication Error", "Incorrect master password.")
    else:
        messagebox.showerror("Selection Error", "Please select an item from the list.")

def add_example_passwords():
    """
    @brief Adds example passwords to the database for testing purposes.
    """
    add_password('example.com', 'user1@example.com', encrypt_password('password123'))
    add_password('example.com', 'user2@example.com', encrypt_password('qwerty456'))
    add_password('example.net', 'admin@example.net', encrypt_password('securepassword'))
    show_passwords_in_list()  # Update the passwords list


def clear_all_data():
    """
    @brief Clears all data from the database.
    """
    clear_all_data()
    messagebox.showinfo("Data Cleared", "All data has been cleared from the database.")
    show_passwords_in_list()

# Create the main application window
app = ctk.CTk()
app.geometry("600x400")
app.title("Password Manager")

# Widgets for the main interface
label = ctk.CTkLabel(app, text="Password Manager")
label.pack(pady=10)

# Frame for buttons
frame_buttons = ctk.CTkFrame(app)
frame_buttons.pack(pady=10, padx=20, side=tk.LEFT, fill=tk.Y)

btn_add_password = ctk.CTkButton(frame_buttons, text="Add Password", command=add_password_ui)
btn_add_password.pack(pady=5, padx=10, fill=tk.X)

btn_generate_password = ctk.CTkButton(frame_buttons, text="Generate Password", command=generate_custom_password)
btn_generate_password.pack(pady=5, padx=10, fill=tk.X)

btn_add_example_passwords = ctk.CTkButton(frame_buttons, text="Add Example Passwords", command=add_example_passwords)
btn_add_example_passwords.pack(pady=5, padx=10, fill=tk.X)

btn_clear_all_data = ctk.CTkButton(frame_buttons, text="Clear All Data", command=clear_all_data)
btn_clear_all_data.pack(pady=5, padx=10, fill=tk.X)

# Search field
entry_search = ctk.CTkEntry(frame_buttons, placeholder_text="Search by site or user")
entry_search.pack(pady=5, padx=10, fill=tk.X)
entry_search.bind("<KeyRelease>", show_filtered_passwords)

# Frame for password list
frame_list = ctk.CTkFrame(app)
frame_list.pack(padx=20, pady=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)

scrollbar = ctk.CTkScrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_passwords = tk.Listbox(frame_list, yscrollcommand=scrollbar.set, width=30, font=('Arial', 14))
listbox_passwords.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar.configure(command=listbox_passwords.yview)

# Event to show user and password details on double-click
listbox_passwords.bind("<Double-Button-1>", show_user_and_password)

# Initialize the password list
show_passwords_in_list()

# Authenticate at the start of the program
authenticate_on_start()

# Run the application
app.mainloop()
