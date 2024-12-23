#handles all the user realted operations
import bcrypt, sqlite3, pyfiglet
from db import initialize_db
from utils import encrypt_password, decrypt_password
from prettytable import PrettyTable
import argparse


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
        return False
    finally:
        c.close()
        conn.close()

def list_passwords():
    table = PrettyTable() #creates the PrettyTable obj
    #displays passwords in a pretty table 

    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()

    c.execute('''SELECT service_name, username, password 
              FROM Passwords;
              ''')
    results = c.fetchall()
    
    #creates a list of the columns names
    column_names = [description[0] for description in c.description()]

    #sets the field names for the PrettyTable
    table.field_names = column_names

    #adding the rows to the prettytable
    for row in results:
        table.add_row(row)

    print(table) #outputs the table

def parse_args():
    #creates the parser
    parser = argparse.ArgumentParser(description='Password Manager Tool')

    #subparsers for different commands
    subparsers = parser.add_subparsers(dest='command')

    #subparser for add_password(service, username, password)
    add_parser = subparsers.add_parser('add', help='Add a new password')
    add_parser.add_argument('service', help='Name of the service')
    add_parser.add_argument('username', help='Username for that service')
    add_parser.add_argument('password', help='Password for that service')

    #subparser for get_password(service)
    get_parser = subparsers.add_parser('get', help='Fetches the password for a service')
    get_parser.add_argument('service', help='Name of the service')

    #subparser for first_use()
    first_parser = subparsers.add_parser('first-use', help='Initializes the program for first use')

    #subparser for list_passwords()
    list_parser = subparsers.add_parser('list-all', help='Lists all the passwords stored in the db')

    #subparser for update_password(service, new_password)
    update_parser = subparsers.add_parser('update', help='Command to update a password for a service')
    update_parser.add_argument('service', help='Service for which the password is updated')
    update_parser.add_argument('new_password', help='The new updated password')

    #subparser delete_password(service)
    del_parser = subparsers.add_parser('delete', help='Delete the password for that service')
    del_parser.add_argument('service', help='Service for which the password would be deleted')

    #subparser generate_random_password(length)
    create_parser = subparsers.add_parser('create', help='Creates a new random password')
    create_parser.add_argument('length', type=int, help='The length of the password to generate')

    return parser.parse_args()  #