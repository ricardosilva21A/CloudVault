import tkinter as tk
from tkinter import messagebox, simpledialog
import string
import random
import hashlib
import pyperclip
import customtkinter as ctk
from encryption import encrypt_password, decrypt_password
from database import create_db, add_password, get_passwords, search_passwords_by_site_user

# Criar banco de dados se não existir
create_db()

# Define a master password (exemplo simples)
stored_master_password = hashlib.sha256("123".encode()).hexdigest()

# Função para gerar uma senha segura com opções
def generate_custom_password():
    top = tk.Toplevel()
    top.title("Generate Custom Password")
    top.geometry("400x300")

    label_title = ctk.CTkLabel(top, text="Custom Password Generator", font=("Arial", 16))
    label_title.pack(pady=10)

    # Labels e Entry para comprimento da senha
    frame_length = ctk.CTkFrame(top)
    frame_length.pack(pady=10)

    label_length = ctk.CTkLabel(frame_length, text="Password Length:")
    label_length.grid(row=0, column=0, padx=10, sticky="w")
    entry_length = ctk.CTkEntry(frame_length, width=10)
    entry_length.grid(row=0, column=1, padx=10)

    # Checkbuttons para opções de senha
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

    # Botão para gerar senha
    btn_generate = ctk.CTkButton(top, text="Generate Password", command=lambda: generate_and_show_custom_password(top, entry_length.get(), var_uppercase.get(), var_numbers.get(), var_symbols.get()))
    btn_generate.pack(pady=10)

    # Função para gerar e exibir a senha personalizada
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

# Função para autenticar o usuário ao iniciar o programa
def authenticate_on_start():
    global stored_master_password
    while True:
        master_password_entered = tk.simpledialog.askstring("Authentication", "Enter your master password to access the password manager:", show='*')
        if master_password_entered is None:
            exit()  # Se o usuário cancelar, sair do programa
        master_password_hash = hashlib.sha256(master_password_entered.encode()).hexdigest()

        if master_password_hash == stored_master_password:
            tk.messagebox.showinfo("Authentication", "Authentication successful. Welcome to the Password Manager.")
            break
        else:
            tk.messagebox.showerror("Authentication Error", "Incorrect master password. Please try again.")

# Função para adicionar senha
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

# Função para exibir todas as senhas na lista de contas
def show_passwords_in_list():
    passwords = get_passwords()

    # Limpar a lista atual
    listbox_passwords.delete(0, tk.END)

    for password in passwords:
        site, _, _ = password[1], password[2], password[3]
        listbox_passwords.insert(tk.END, site)

# Função para mostrar senhas filtradas por site ou usuário
def show_filtered_passwords(event=None):
    filter_text = entry_search.get()

    if filter_text:
        passwords = search_passwords_by_site_user(filter_text)
        listbox_passwords.delete(0, tk.END)  # Limpar a lista atual

        for password in passwords:
            site, _, _ = password[1], password[2], password[3]
            listbox_passwords.insert(tk.END, site)
    else:
        show_passwords_in_list()

# Função para exibir usuário e senha ao clicar na lista de contas
# Função para exibir usuário e senha ao clicar na lista de contas
def show_user_and_password(event):
    widget = event.widget
    if widget.curselection():
        index = int(widget.curselection()[0])
        site = widget.get(index)

        master_password_entered = tk.simpledialog.askstring("Senha Mestra", "Digite sua senha mestra para visualizar a senha:", show='*')
        master_password_hash = hashlib.sha256(master_password_entered.encode()).hexdigest()

        if master_password_hash == stored_master_password:
            passwords = search_passwords_by_site_user(site)

            if passwords:
                user = passwords[0][2]
                decrypted_password = decrypt_password(passwords[0][3])
                pyperclip.copy(decrypted_password)

                # Criar janela para exibir usuário e senha
                top = tk.Toplevel()
                top.title(f"Detalhes da Senha para {site}")
                top.geometry("300x150")

                label_user = tk.Label(top, text=f"Usuário: {user}", font=("Arial", 12))
                label_user.pack(pady=10)

                label_password = tk.Label(top, text=f"Senha: {decrypted_password}", font=("Arial", 12))
                label_password.pack(pady=10)

                # Botão para copiar para a área de transferência
                btn_copy = tk.Button(top, text="Copiar para Clipboard", command=lambda: pyperclip.copy(decrypted_password))
                btn_copy.pack(pady=10)

                # Focus para a janela
                top.focus_force()
            else:
                tk.messagebox.showerror("Erro", f"Não foi possível encontrar a senha para {site}.")
        else:
            tk.messagebox.showerror("Erro de Autenticação", "Senha mestra incorreta.")
    else:
        tk.messagebox.showerror("Erro de Seleção", "Por favor, selecione um item da lista.")


# Criar o aplicativo principal
app = ctk.CTk()
app.geometry("400x400")
app.title("Password Manager")

# Widgets da interface principal
label = ctk.CTkLabel(app, text="Password Manager")
label.pack(pady=10)

# Frame para a lista de senhas
frame_list = ctk.CTkFrame(app)
frame_list.pack(padx=20, pady=10, side=tk.LEFT, fill=tk.Y)

scrollbar = ctk.CTkScrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_passwords = tk.Listbox(frame_list, yscrollcommand=scrollbar.set, width=30)
listbox_passwords.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar.configure(command=listbox_passwords.yview)

# Evento para exibir usuário e senha ao clicar na lista
listbox_passwords.bind("<Double-Button-1>", show_user_and_password)

# Frame para botões
frame_buttons = ctk.CTkFrame(app)
frame_buttons.pack(pady=10, padx=20, side=tk.TOP, fill=tk.X)

btn_add_password = ctk.CTkButton(frame_buttons, text="Add Password", command=add_password_ui)
btn_add_password.pack(pady=5, padx=10, fill=tk.X)

btn_generate_password = ctk.CTkButton(frame_buttons, text="Generate Password", command=generate_custom_password)
btn_generate_password.pack(pady=5, padx=10, fill=tk.X)

# Campo de pesquisa
entry_search = ctk.CTkEntry(frame_buttons, placeholder_text="Search by site or user")
entry_search.pack(pady=5, padx=10, fill=tk.X)
entry_search.bind("<KeyRelease>", show_filtered_passwords)

# Inicializar a lista de senhas
show_passwords_in_list()

# Autenticar ao iniciar o programa
authenticate_on_start()

# Iniciar o aplicativo
app.mainloop()
