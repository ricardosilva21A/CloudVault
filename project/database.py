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

    @return The database connection object.
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

def search_passwords_by_site_user(site, user):
    """
    @brief Searches for passwords by site and username.

    @param site The site to search for.
    @param user The username to search for.
    @return A list of tuples containing the matching passwords.
    """
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM passwords WHERE site=? AND username=?", (site, user))
            passwords = cursor.fetchall()
            return passwords
        except sqlite3.Error as e:
            print(f"Error searching passwords: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Failed to connect to database.")
        return []
