from cryptography.fernet import Fernet

# Gerar uma chave e salvá-la em um arquivo
def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_file:
        chave_file.write(chave)

# Exemplo de modificação da função carregar_chave para aceitar um argumento de caminho
def carregar_chave(caminho_chave="chave.key"):
    with open(caminho_chave, "rb") as chave_arquivo:
        chave = chave_arquivo.read()
    return chave

# Criptografar uma senha
def criptografar_senha(senha):
    chave = carregar_chave()
    f = Fernet(chave)
    senha_encriptada = f.encrypt(senha.encode())
    return senha_encriptada

# Descriptografar uma senha
def descriptografar_senha(senha_encriptada):
    chave = carregar_chave()
    f = Fernet(chave)
    senha_decriptada = f.decrypt(senha_encriptada).decode()
    return senha_decriptada

# Gerar a chave uma vez (execute apenas uma vez)
if __name__ == "__main__":
    gerar_chave()
