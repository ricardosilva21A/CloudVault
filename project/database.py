import sqlite3

def connect_db():
    """
    @brief Connects to the SQLite database.

    @return Connection object if successful, None otherwise.
    """
    try:
        conn = sqlite3.connect('passwords.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_db():
    """
    @brief Creates the passwords table in the SQLite database if it doesn't exist.

    @details This function creates a table named 'passwords' with columns for id, site, username, and password.
    """
    conn = connect_db()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS passwords
                         (id INTEGER PRIMARY KEY, site TEXT, username TEXT, password BLOB)''')
            conn.commit()
            print("Database and table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

def add_password(site, username, encrypted_password):
    """
    @brief Adds a new password to the database.

    @param site The site for which the password is stored.
    @param username The username for the site.
    @param encrypted_password The encrypted password to be stored.
    """
    conn = connect_db()
    if conn:
        try:
            # Check if there's already an entry with the same site and username
            existing_passwords = search_passwords_by_site_user(site=site, user=username)
            if existing_passwords:
                # Ask user if they want to overwrite the existing password
                print(f"A password entry already exists for site '{site}' and username '{username}':")
                print(existing_passwords)
                overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
                if overwrite != 'y':
                    print("Operation canceled.")
                    return
            
            # If not overwriting or no existing entry, proceed to add the password
            c = conn.cursor()
            c.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)", (site, username, encrypted_password))
            conn.commit()
            print("Password added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding password: {e}")
        finally:
            conn.close()

def update_password(site, username, encrypted_password):
    """
    @brief Updates an existing password in the database.

    @param site The site for which the password is stored.
    @param username The username for the site.
    @param encrypted_password The new encrypted password to be stored.
    """
    conn = connect_db()
    if conn:
        try:
            c = conn.cursor()
            c.execute("UPDATE passwords SET password = ? WHERE site = ? AND username = ?", (encrypted_password, site, username))
            conn.commit()
            print("Password updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating password: {e}")
        finally:
            conn.close()

def get_passwords():
    """
    @brief Retrieves all passwords from the database.

    @return A list of tuples containing the passwords.
    """
    conn = connect_db()
    if conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM passwords")
            passwords = c.fetchall()
            return passwords
        except sqlite3.Error as e:
            print(f"Error fetching passwords: {e}")
            return []
        finally:
            conn.close()
    return []

def search_passwords_by_site_user(site=None, user=None):
    """
    @brief Searches for passwords by site and/or username.

    @param site The site to search for.
    @param user The username to search for.
    @return A list of tuples containing the matching passwords.
    """
    conn = connect_db()
    c = conn.cursor()

    if site and user:
        c.execute("SELECT * FROM passwords WHERE site LIKE ? AND username LIKE ?", ('%' + site + '%', '%' + user + '%'))
    elif site:
        c.execute("SELECT * FROM passwords WHERE site LIKE ?", ('%' + site + '%',))
    elif user:
        c.execute("SELECT * FROM passwords WHERE username LIKE ?", ('%' + user + '%',))
    else:
        c.execute("SELECT * FROM passwords")

    passwords = c.fetchall()
    conn.close()
    return passwords

def delete_password(site, username):
    """
    @brief Deletes a password from the database.

    @param site The site for which the password is stored.
    @param username The username for the site.
    """
    conn = connect_db()
    if conn:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM passwords WHERE site = ? AND username = ?", (site, username))
            conn.commit()
            print(f"Password deleted successfully for {site} and user {username}.")
        except sqlite3.Error as e:
            print(f"Error deleting password: {e}")
        finally:
            conn.close()

# Testando a função add_password() com um exemplo
if __name__ == "__main__":
    create_db()  # Certifica-se de que o banco de dados e a tabela existam

    # Exemplo de uso da função add_password()
    site = "google.com"
    username = "tdbem"
    encrypted_password = "oi"

    add_password(site, username, encrypted_password)
