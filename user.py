#handles all the user realted operations
import hashlib, getpass, os
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


