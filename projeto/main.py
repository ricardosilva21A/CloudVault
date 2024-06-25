import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import string
import random
import hashlib
import pyperclip
import customtkinter as ctk
from encryption import encrypt_password, decrypt_password, generate_key, load_key
from database import create_db, add_password, get_passwords, search_passwords_by_site_user

# Inicialização do banco de dados
create_db()


# Define the master password (simple example)
stored_master_password = hashlib.sha256("123".encode()).hexdigest()

# Function to generate a secure password with options
def generate_custom_password():
    top = tk.Toplevel()
    top.title("Generate Custom Password")
    top.geometry("400x300")

    label_title = tk.Label(top, text="Custom Password Generator", font=("Arial", 16))
    label_title.pack(pady=10)

    # Labels and Entry for password length
    frame_length = ttk.Frame(top)
    frame_length.pack(pady=10)

    label_length = ttk.Label(frame_length, text="Password Length:")
    label_length.grid(row=0, column=0, padx=10, sticky="w")
    entry_length = ttk.Entry(frame_length, width=10)
    entry_length.grid(row=0, column=1, padx=10)

    # Checkbuttons for password options
    frame_options = ttk.Frame(top)
    frame_options.pack(pady=10)

    var_uppercase = tk.IntVar()
    var_numbers = tk.IntVar()
    var_symbols = tk.IntVar()

    check_uppercase = ttk.Checkbutton(frame_options, text="Include Uppercase", variable=var_uppercase)
    check_uppercase.grid(row=0, column=0, padx=10, sticky="w")
    check_numbers = ttk.Checkbutton(frame_options, text="Include Numbers", variable=var_numbers)
    check_numbers.grid(row=0, column=1, padx=10, sticky="w")
    check_symbols = ttk.Checkbutton(frame_options, text="Include Symbols", variable=var_symbols)
    check_symbols.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")

    # Button to generate password
    btn_generate = ttk.Button(top, text="Generate Password", command=lambda: generate_and_show_custom_password(top, entry_length.get(), var_uppercase.get(), var_numbers.get(), var_symbols.get()))
    btn_generate.pack(pady=10)

    # Function to generate and display the custom password
    def generate_and_show_custom_password(top, length, include_uppercase, include_numbers, include_symbols):
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
            tk.messagebox.showinfo("Generated Password", f"Your generated password is:\n{generated_password}")

            top.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the password length.")

# Function to authenticate the user when starting the program
def authenticate_on_start():
    global stored_master_password
    while True:
        master_password_entered = tk.simpledialog.askstring("Authentication", "Enter your master password to access the password manager:", show='*')
        if master_password_entered is None:
            exit()  # If user cancels, exit the program
        master_password_hash = hashlib.sha256(master_password_entered.encode()).hexdigest()

        if master_password_hash == stored_master_password:
            tk.messagebox.showinfo("Authentication", "Authentication successful. Welcome to the Password Manager.")
            break
        else:
            tk.messagebox.showerror("Authentication Error", "Incorrect master password. Please try again.")

# Function to add password
def add_password_ui():
    site = simpledialog.askstring("Site", "Site name:")
    user = simpledialog.askstring("User", "Username:")
    password = simpledialog.askstring("Password", "Password:", show='*')

    if not site or not user or not password:
        tk.messagebox.showerror("Error", "All fields must be filled!")
        return

    encrypted_password = encrypt_password(password)
    add_password(site, user, encrypted_password)
    tk.messagebox.showinfo("Success", "Password added successfully!")

# Function to display all passwords in the accounts list
def show_passwords_in_list():
    passwords = get_passwords()

    # Clear the current list
    listbox_passwords.delete(0, tk.END)

    for password in passwords:
        site, _, _ = password[1], password[2], password[3]
        listbox_passwords.insert(tk.END, site)

# Function to show passwords filtered by site or user
def show_filtered_passwords(event=None):
    filter_text = entry_search.get()

    if filter_text:
        passwords = search_passwords_by_site_user(filter_text)
        listbox_passwords.delete(0, tk.END)  # Clear the current list

        for password in passwords:
            site, _, _ = password[1], password[2], password[3]
            listbox_passwords.insert(tk.END, site)
    else:
        show_passwords_in_list()

# Function to display user and password when clicking on the accounts list
def show_user_and_password(event):
    widget = event.widget
    if widget.curselection():
        index = int(widget.curselection()[0])
        site = widget.get(index)

        master_password_entered = tk.simpledialog.askstring("Master Password", "Enter your master password to view the password:", show='*')
        master_password_hash = hashlib.sha256(master_password_entered.encode()).hexdigest()

        if master_password_hash == stored_master_password:
            passwords = search_passwords_by_site_user(site)

            if passwords:
                decrypted_password = decrypt_password(passwords[0][3])
                pyperclip.copy(decrypted_password)

                # Create window to display user and password
                top = tk.Toplevel()
                top.title(f"Password Details for {site}")
                top.geometry("300x150")

                label_user = tk.Label(top, text=f"User: {passwords[0][2]}", font=("Arial", 12))
                label_user.pack(pady=10)

                label_password = tk.Label(top, text=f"Password: {decrypted_password}", font=("Arial", 12))
                label_password.pack(pady=10)

                # Button to copy to clipboard
                btn_copy = tk.Button(top, text="Copy to Clipboard", command=lambda: pyperclip.copy(decrypted_password))
                btn_copy.pack(pady=10)

                # Focus on the window
                top.focus_force()
            else:
                tk.messagebox.showerror("Error", f"Could not find the password for {site}.")
        else:
            tk.messagebox.showerror("Authentication Error", "Incorrect master password.")
    else:
        tk.messagebox.showerror("Selection Error", "Please select an item from the list.")

# Create the main application
app = ctk.CTk()
app.geometry("400x400")
app.title("Password Manager")

# Widgets of the main interface
label = ctk.CTkLabel(app, text="Password Manager")
label.pack(pady=10)

# Frame for the list of passwords
frame_list = ttk.Frame(app)
frame_list.pack(padx=20, pady=10, side=tk.LEFT, fill=tk.Y)

scrollbar = ttk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_passwords = tk.Listbox(frame_list, yscrollcommand=scrollbar.set, width=30)
listbox_passwords.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar.configure(command=listbox_passwords.yview)

# Event to display user and password when clicking on the list
listbox_passwords.bind("<Double-Button-1>", show_user_and_password)

# Frame for buttons
frame_buttons = ctk.CTkFrame(app)
frame_buttons.pack(pady=10, padx=20, side=tk.TOP, fill=tk.X)

btn_add_password = ctk.CTkButton(frame_buttons, text="Add Password", command=add_password_ui)
btn_add_password.pack(pady=10, padx=10, fill=tk.X)

btn_generate_password = ctk.CTkButton(frame_buttons, text="Generate Password", command=generate_custom_password)
btn_generate_password.pack(pady=10, padx=10, fill=tk.X)

btn_exit = ctk.CTkButton(frame_buttons, text="Exit", command=app.quit)
btn_exit.pack(pady=10, padx=10, fill=tk.X)

# Frame for search bar
frame_search = ctk.CTkFrame(app)
frame_search.pack(padx=20, pady=10, side=tk.TOP, fill=tk.X)

entry_search = ctk.CTkEntry(frame_search, width=30)
entry_search.pack(pady=10, padx=10, side=tk.LEFT, fill=tk.X, expand=True)

btn_search = ctk.CTkButton(frame_search, text="Search", command=show_filtered_passwords)
btn_search.pack(pady=10, padx=10, side=tk.RIGHT)

entry_search.bind("<Return>", show_filtered_passwords)

# Display all passwords in the list at startup
show_passwords_in_list()

# Authenticate the user when starting the program
authenticate_on_start()

# Main loop
app.mainloop()
