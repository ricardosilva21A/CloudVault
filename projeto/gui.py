import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import string
import random
import hashlib
import pyperclip
from encryption import criptografar_senha, descriptografar_senha, gerar_chave, carregar_chave
from database import criar_db, adicionar_senha, obter_senhas, buscar_senha_por_site_usuario

# Definir a senha mestra (exemplo simples)
senha_mestra_armazenada = hashlib.sha256("123".encode()).hexdigest()

class PasswordManagerGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Gerenciador de Senhas")
        self.geometry("800x400")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        self.frames = {}

        for F in (LoginPage, SignupPage, ManagePasswordsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=1, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Login", font=("Arial", 18))
        label.pack(pady=10,padx=10)

        label_username = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")

        entry_username = ttk.Entry(self)
        entry_password = ttk.Entry(self, show="*")

        label_username.pack()
        entry_username.pack()
        label_password.pack()
        entry_password.pack()

        login_button = ttk.Button(self, text="Login", command=lambda: self.login(entry_username.get(), entry_password.get(), controller))
        login_button.pack()

        signup_button = ttk.Button(self, text="Sign Up", command=lambda: controller.show_frame(SignupPage))
        signup_button.pack()

    def login(self, username, password, controller):
        if username == "admin" and password == "admin":
            messagebox.showinfo("Login Successful", "Welcome, admin!")
            controller.show_frame(ManagePasswordsPage)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Sign Up", font=("Arial", 18))
        label.pack(pady=10,padx=10)

        label_username = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")

        entry_username = ttk.Entry(self)
        entry_password = ttk.Entry(self, show="*")

        label_username.pack()
        entry_username.pack()
        label_password.pack()
        entry_password.pack()

        signup_button = ttk.Button(self, text="Sign Up", command=lambda: self.signup(entry_username.get(), entry_password.get()))
        signup_button.pack()

        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(LoginPage))
        back_button.pack()

    def signup(self, username, password):
        messagebox.showinfo("Sign Up Successful", f"Account created for {username}")

class ManagePasswordsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Gerenciar Senhas", font=("Arial", 18))
        label.pack(pady=10, padx=10)

        # Botão para adicionar senha
        btn_adicionar_senha = ttk.Button(self, text="Adicionar Senha", command=self.adicionar_senha)
        btn_adicionar_senha.pack(pady=10, padx=10, fill=tk.X)

        # Listbox para mostrar as senhas
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_senhas = tk.Listbox(self, yscrollcommand=scrollbar.set, font=("Arial", 12))
        self.listbox_senhas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.listbox_senhas.yview)

        # Carregar as senhas na lista ao iniciar
        self.carregar_senhas()

        # Botão para sair
        btn_sair = ttk.Button(self, text="Sair", command=self.sair)
        btn_sair.pack(pady=10, padx=10, side=tk.BOTTOM)

        # Bind para mostrar detalhes ao clicar na senha
        self.listbox_senhas.bind("<Double-Button-1>", self.mostrar_detalhes_senha)

    def carregar_senhas(self):
        senhas = obter_senhas()
        self.listbox_senhas.delete(0, tk.END)

        for senha in senhas:
            site, _, _ = senha[1], senha[2], senha[3]
            self.listbox_senhas.insert(tk.END, site)

    def adicionar_senha(self):
        site = simpledialog.askstring("Site", "Nome do site:")
        usuario = simpledialog.askstring("Usuário", "Nome de usuário:")
        senha = simpledialog.askstring("Senha", "Senha:", show='*')

        if not site or not usuario or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        senha_encriptada = criptografar_senha(senha)
        adicionar_senha(site, usuario, senha_encriptada)
        messagebox.showinfo("Sucesso", "Senha adicionada com sucesso!")
        self.carregar_senhas()

    def sair(self):
        self.controller.show_frame(LoginPage)

    def mostrar_detalhes_senha(self, event):
        # Obter o índice da senha selecionada
        index = self.listbox_senhas.curselection()
        if index:
            index = int(index[0])

            # Pedir senha mestra para mostrar os detalhes da senha
            senha_mestra_digitada = simpledialog.askstring("Autenticação", "Digite sua senha mestra para mostrar os detalhes da senha:", show='*')
            senha_mestra_hash = hashlib.sha256(senha_mestra_digitada.encode()).hexdigest()

            if senha_mestra_hash != senha_mestra_armazenada:
                messagebox.showerror("Erro de Autenticação", "Senha mestra incorreta. Tente novamente.")
                return

            # Obter senha encriptada do banco de dados
            senhas = obter_senhas()
            senha_encriptada = senhas[index][3]

            # Descriptografar a senha
            senha_decriptada = descriptografar_senha(senha_encriptada)

            # Exibir detalhes da senha
            messagebox.showinfo("Detalhes da Senha", f"Site: {senhas[index][1]}\nUsuário: {senhas[index][2]}\nSenha: {senha_decriptada}")

if __name__ == "__main__":
    app = PasswordManagerGUI()
    app.mainloop()
