#handles all the user realted operations
import hashlib, getpass, os, sqlite3, bcrypt
from db import initialize_db, execute_query, fetch_query

def user_login():
    master_password = getpass.getpass("Enter master password: ")
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest()

    stored_hash = fetch_query("SELECT  master_password_hash FROM users LIMIT 1")

    if stored_hash and stored_hash[0][0] == hashed_password:
        print("Login successful")
        return True
    else:
        print('Invalid Master Password')
        return False

def first_time_user():
    db_exisits = os.path.exists('password_manager.db') #checking if db exists
    
    if not db_exisits:
        initialize_db() # creats db if not exists

    return user_login() #calls user_login function after intialization


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
    except sqlite3.Error as e:
        print(e)
    finally:
        c.close()
        conn.close()

    