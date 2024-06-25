import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import string
import random
import hashlib
import pyperclip
import customtkinter as ctk
from encryption import criptografar_senha, descriptografar_senha, gerar_chave, carregar_chave
from database import criar_db, adicionar_senha, obter_senhas, buscar_senha_por_site_usuario

# Definir a senha mestra (exemplo simples)
senha_mestra_armazenada = hashlib.sha256("123".encode()).hexdigest()

# Função para gerar senha segura com opções
def gerar_senha_personalizada():
    top = tk.Toplevel()
    top.title("Gerar Senha Personalizada")

    # Labels e Entry para tamanho da senha
    label_tamanho = tk.Label(top, text="Tamanho da Senha:")
    label_tamanho.pack(pady=10)
    entry_tamanho = tk.Entry(top)
    entry_tamanho.pack()

    # Checkbuttons para opções de senha
    var_maiusculas = tk.IntVar()
    var_numeros = tk.IntVar()
    var_simbolos = tk.IntVar()

    check_maiusculas = tk.Checkbutton(top, text="Incluir Maiúsculas", variable=var_maiusculas)
    check_maiusculas.pack()
    check_numeros = tk.Checkbutton(top, text="Incluir Números", variable=var_numeros)
    check_numeros.pack()
    check_simbolos = tk.Checkbutton(top, text="Incluir Símbolos", variable=var_simbolos)
    check_simbolos.pack()

    # Botão para gerar senha
    btn_gerar = ttk.Button(top, text="Gerar Senha", command=lambda: gerar_e_exibir_senha_personalizada(top, entry_tamanho.get(), var_maiusculas.get(), var_numeros.get(), var_simbolos.get()))
    btn_gerar.pack(pady=10)

    # Função para gerar e exibir a senha personalizada
    def gerar_e_exibir_senha_personalizada(top, tamanho, incluir_maiusculas, incluir_numeros, incluir_simbolos):
        try:
            tamanho = int(tamanho)
            if tamanho <= 0:
                messagebox.showerror("Erro", "O tamanho da senha deve ser maior que zero.")
                return

            caracteres = string.ascii_lowercase
            if incluir_maiusculas:
                caracteres += string.ascii_uppercase
            if incluir_numeros:
                caracteres += string.digits
            if incluir_simbolos:
                caracteres += string.punctuation

            senha_gerada = ''.join(random.choice(caracteres) for _ in range(tamanho))
            tk.messagebox.showinfo("Senha Gerada", f"Sua senha gerada é:\n{senha_gerada}")

            top.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido para o tamanho da senha.")

# Função para autenticar o usuário ao visualizar uma senha
def autenticar_visualizacao():
    senha_mestra_digitada = tk.simpledialog.askstring("Senha Mestra", "Digite sua senha mestra para visualizar a senha:", show='*')
    senha_mestra_hash = hashlib.sha256(senha_mestra_digitada.encode()).hexdigest()

    return senha_mestra_hash == senha_mestra_armazenada

# Função para exibir usuário e senha ao clicar em um item da lista
def exibir_usuario_e_senha(event):
    widget = event.widget
    index = int(widget.curselection()[0])
    site = widget.get(index)

    if autenticar_visualizacao():
        senhas = buscar_senha_por_site_usuario(site)

        if senhas:
            usuario, senha_encriptada = senhas[0][2], senhas[0][3]
            senha_decriptada = descriptografar_senha(senha_encriptada)

            top = tk.Toplevel()
            top.title("Detalhes da Senha")

            label_usuario = tk.Label(top, text=f"Usuário: {usuario}")
            label_usuario.pack(pady=10)

            label_senha = tk.Label(top, text=f"Senha: {senha_decriptada}")
            label_senha.pack(pady=10)

            btn_copy_user = ctk.CTkButton(top, text="Copiar Usuário", command=lambda: pyperclip.copy(usuario))
            btn_copy_user.pack(pady=5)

            btn_copy_password = ctk.CTkButton(top, text="Copiar Senha", command=lambda: pyperclip.copy(senha_decriptada))
            btn_copy_password.pack(pady=5)

            btn_close = ctk.CTkButton(top, text="Fechar", command=top.destroy)
            btn_close.pack(pady=10)
        else:
            messagebox.showerror("Erro", f"Não foi possível encontrar a senha para {site}.")

# Configurar o Customtkinter
ctk.set_appearance_mode("dark")  # Tema escuro
ctk.set_default_color_theme("blue")  # Tema de cor azul

# Criar a aplicação principal
app = ctk.CTk()
app.geometry("400x400")
app.title("Gerenciador de Senhas")

# Frame para a lista de contas com barra de rolagem
frame_lista = ctk.CTkFrame(app)
frame_lista.pack(padx=20, pady=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_senhas = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set)
listbox_senhas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar.config(command=listbox_senhas.yview)

# Frame para botões do lado esquerdo
frame_botoes = ctk.CTkFrame(app)
frame_botoes.pack(padx=20, pady=10, side=tk.LEFT)

btn_gerar_senha = ctk.CTkButton(frame_botoes, text="Gerar Senha", command=gerar_senha_personalizada)
btn_gerar_senha.pack(pady=10, padx=10, fill=tk.X)

# Mostrar as senhas na lista ao iniciar o programa
senhas = obter_senhas()
for senha in senhas:
    site, _, _ = senha[1], senha[2], senha[3]
    listbox_senhas.insert(tk.END, site)

# Bind para exibir usuário e senha ao clicar na lista de contas
listbox_senhas.bind("<Double-Button-1>", exibir_usuario_e_senha)

# Iniciar a aplicação
app.mainloop()
