import sqlite3

# Criar banco de dados e tabela
def criar_db():
    conn = sqlite3.connect('senhas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS senhas
                 (id INTEGER PRIMARY KEY, site TEXT, usuario TEXT, senha BLOB)''')
    conn.commit()
    conn.close()

# Adicionar uma senha ao banco de dados
def adicionar_senha(site, usuario, senha_encriptada):
    conn = sqlite3.connect('senhas.db')
    c = conn.cursor()
    c.execute("INSERT INTO senhas (site, usuario, senha) VALUES (?, ?, ?)", (site, usuario, senha_encriptada))
    conn.commit()
    conn.close()

# Obter senhas do banco de dados
def obter_senhas():
    conn = sqlite3.connect('senhas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM senhas")
    senhas = c.fetchall()
    conn.close()
    return senhas


# Função para buscar senhas por site ou usuário
def buscar_senha_por_site_usuario(filtro):
    conn = sqlite3.connect('senhas.db')
    c = conn.cursor()

    # Consulta SQL para buscar senhas por site ou usuário
    c.execute("SELECT * FROM senhas WHERE site LIKE ? OR usuario LIKE ?", ('%'+filtro+'%', '%'+filtro+'%'))
    senhas = c.fetchall()

    conn.close()
    return senhas
