"""
@file database.py
@brief Functions for database operations in the Password Manager.

Authors:
- Ricardo Silva
- Guillermo
- Saúl

@date 2024
@version 1.0
@note SAP: PYTHON 2024

This module provides functions to connect to the database, create tables, add, search, and update passwords.
"""

import sqlite3

def connect_db():
    """
    @brief Connects to the SQLite database.

    @return A connection object or None if connection fails.
    """
    try:
        conn = sqlite3.connect('passwords.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_db():
    """
    @brief Creates the passwords table if it does not exist.
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
    else:
        print("Failed to connect to database.")

def add_password(site, username, encrypted_password):
    """
    @brief Adds a new password to the database.

    @param site The site associated with the password.
    @param username The username associated with the password.
    @param encrypted_password The encrypted password.
    """
    conn = connect_db()
    if conn:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)", (site, username, encrypted_password))
            conn.commit()
            print("Password added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding password: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to database.")

def update_password(site, username, encrypted_password):
    """
    @brief Updates an existing password in the database.

    @param site The site associated with the password.
    @param username The username associated with the password.
    @param encrypted_password The new encrypted password.
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
    else:
        print("Failed to connect to database.")

def get_passwords():
    """
    @brief Retrieves all passwords from the database.

    @return A list of tuples containing all passwords.
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
    else:
        print("Failed to connect to database.")
        return []

def search_passwords_by_site_user(filter_text):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    # Consulta para buscar por site ou usuário
    c.execute("SELECT * FROM passwords WHERE site LIKE ? OR username LIKE ?", ('%' + filter_text + '%', '%' + filter_text + '%'))
    passwords = c.fetchall()

    conn.close()
    return passwords
    

def delete_password(site, username):
    """
    @brief Deletes an existing password from the database.

    @param site The site associated with the password.
    @param username The username associated with the password.
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
    else:
        print("Failed to connect to database.")
