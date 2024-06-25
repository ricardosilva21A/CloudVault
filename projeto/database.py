import sqlite3

# Create database and table
def create_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (id INTEGER PRIMARY KEY, site TEXT, username TEXT, password BLOB)''')
    conn.commit()
    conn.close()

# Add a password to the database
def add_password(site, username, encrypted_password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)", (site, username, encrypted_password))
    conn.commit()
    conn.close()

# Get passwords from the database

def get_passwords():
    try:
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute("SELECT * FROM passwords")
        passwords = c.fetchall()
        conn.close()
        return passwords
    except sqlite3.OperationalError as e:
        print(f"Error accessing database: {e}")
        return []

# Function to search passwords by site or username
def search_passwords_by_site_user(filter):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    # SQL query to search passwords by site or username
    c.execute("SELECT * FROM passwords WHERE site LIKE ? OR username LIKE ?", ('%'+filter+'%', '%'+filter+'%'))
    passwords = c.fetchall()

    conn.close()
    return passwords
