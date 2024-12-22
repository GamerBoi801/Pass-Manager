#handles all the user realted operations
import bcrypt, sqlite3, pyfiglet
from db import initialize_db
from rehpic import encrypt_password, decrypt_password
from prettytable import PrettyTable


def first_use():
    initialize_db()
    
    # welcome message
    txt = 'Welcome to the Password Manager!! '
    print(pyfiglet.figlet_format(txt))

    # creting and saving the master password and username
    username = input('Please Enter a username: ')
    
    while True:
        password1 = input('Please Enter a Master Password: ')
        password2 = input('Re-enter the Master Password: ')
        if password1 == password2:
            break
        print('Passwords do not match! Try Again')

    # additions to the database
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    
    hashed_password = encrypt_password(password2)  
    
    try:
        c.execute('''
            INSERT INTO users (username, master_password_hash) 
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()  

        print('Username and master password are set!!')
        
    except sqlite3.Error as e:
        print(f"An error occurred while inserting data: {e}")
    
    finally:
        c.close()
        conn.close() 



def validate_master_password():
    user_attempt = input('Please enter the Master Password: ')

    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()

    try:
        c.execute('''
            SELECT master_password FROM user WHERE id = 1;
            ''')
        stored_master_password = c.fetchone()

        if stored_master_password:
            stored_master_password = stored_master_password[0]
            if bcrypt.checkpw(user_attempt.encode(), stored_master_password.encode()):
                c.close()
                return True
            else:
                print('No master password found in the db. ')
                return False
        else:
            print('ACCESS DENIED: WRONG MASTER PASSWORD. ')
            return False
        
    except sqlite3.Error as e:
        print(e)
    finally:
        c.close()
        conn.close()

def list_passwords():
    table = PrettyTable()
    table.field_names = ["Service Name", "username", "Password"]
    
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()

    c.execute('''SELECT service_name, username, password 
              FROM Passwords;
              ''')
    results = c.fetchall()