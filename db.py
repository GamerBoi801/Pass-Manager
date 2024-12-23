import sqlite3, bcrypt
from user import validate_master_password
from utils import encrypt_password, decrypt_password

def initialize_db():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor() #connecting the db to execute commands
    try:
        #creating table in the db
        c.execute('''
              CREATE TABLE IF NOT EXISTS Passwords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
                  );    
            ''')
        
        #creates the user table for storing the master password
        c.execute('''  
        CREATE TABLE IF NOT EXISTS user(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  master_password TEXT NOT NULL );
                  ''')
        
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close() # closes the connection to the db

def add_password(service, username, password):
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()

    hashed_password = encrypt_password(password) 
    
    # adding password to the db
    c.execute('''
INSERT INTO Passwords(service_name, username, password) 
              VALUES(?, ?, ?)
              ''', (service, username, hashed_password)
              )
    
    
    conn.commit()
    conn.close()

def get_password(service):
    if validate_master_password():
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()

        c.execute('''
                  SELECT master_password FROM user WHERE id = 1;
                  ''')
        result = c.fetchone()
        conn.commit()
        conn.close()

        return decrypt_password(result)

def delete_password(service):
    if validate_master_password():
        conn = sqlite3.connect('password_manager.db')
        c =conn.cursor()

        c. execute('''
                DELETE FROM Passwords WHERE service_name = ?''', service)
        conn.commit()
        conn.close()

def update_password(service, new_password):
    if validate_master_password():
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
    
        hashed = encrypt_password(new_password)
        #updates the password field with the new one
        c. execute('''
                UPDATE Passswords SET password = ?
                    WHERE service_name = ?;
                ''', (hashed, service))
        
        conn.commit()
        conn.close()