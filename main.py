import os, sqlite3, pyfiglet, argparse, bcrypt
import secrets, string, random, getpass
from prettytable import PrettyTable

#constants
# Database path for storing passwords
DB_PATH = 'password_manager.db'

# Default password length for generated passwords
DEFAULT_PASSWORD_LENGTH = 16

def validate_master_password():
    user_attempt = getpass.getpass('Please enter the Master Password: ')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute('''
            SELECT master_password FROM user WHERE id = 1;
            ''')
        stored_master_password = c.fetchone()

        if stored_master_password:
            hashed_password = stored_master_password
            if bcrypt.checkpw(user_attempt.encode('utf-8'), hashed_password):                   
                c.close()
                return True
            else:
                print('ACCESS DENIED: WRONG MASTER PASSWORD. ')
                return False
        else:
            print('No master password found in the db. ')
            return False
        
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        c.close()
        conn.close()

def first_use():
    
    # this intialises everything for first time use
    txt = 'Welcome to the Password Manager!! '
    print(pyfiglet.figlet_format(txt))
    
    #initialize_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor() #connecting the db to execute commands
    try:
        #creating password table in the db
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
                  master_password TEXT NOT NULL
                        );
                  ''')
        conn.commit()
        
        # creating and saving the master password and username
        username = input('Please Enter a username: ')
        while True:
            password1 = getpass.getpass('Please Enter a Master Password: ')
            password2 = getpass.getpass('Re-enter the Master Password: ')
            if password1 == password2:
                break
            print('Passwords do not match! Try Again')
        
        # additions to the database
        #encrypting 
        password2 = password2.encode('utf-8')
        key = bcrypt.gensalt()
        hashed_password= bcrypt.hashpw(password2, key)   
        c.execute('''
            INSERT INTO user (username, master_password) 
            VALUES (?, ?)
        ''', (username, hashed_password))

        conn.commit()  
        print('Username and master password are set!!')
                
    except sqlite3.Error or TypeError as e:
        print(f"An error occurred while inserting data: {e}")
    finally:
        c.close()
        conn.close()



def parse_args():
    #creates the parser
    parser = argparse.ArgumentParser(description='CLI Password Manager')

    #subparsers for different commands
    subparsers = parser.add_subparsers(dest='command')

    #subparser for add_password(service, username, password)
    add_parser = subparsers.add_parser('add', help='Add a new password')
    add_parser.add_argument('service', help='Name of the service')
    add_parser.add_argument('username', help='Username for that service')
    add_parser.add_argument('password', help='Password for that service')

    #subparser for first_use()
    first_parser = subparsers.add_parser('first-use', help='Initializes the program for first use/ Also to be used in case of an error')

    #subparser for update_password(service, new_password)
    update_parser = subparsers.add_parser('update', help='Command to update a password for a service')
    update_parser.add_argument('service', help='Service for which the password is updated')
    update_parser.add_argument('new_password', help='The new updated password')

    #subparser delete_password(service)
    del_parser = subparsers.add_parser('delete', help='Delete the password for that service')
    del_parser.add_argument('service', help='Service for which the password would be deleted')

    #subparser generate_random_password(length)
    create_parser = subparsers.add_parser('create', help='Creates a new random password')
    create_parser.add_argument('length', type=int, help='The length of the password to generate :: Should be more than 16 characters')

    return parser.parse_args()  

def add_password(service, username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
    
    # adding password to the db
    c.execute('''
        INSERT INTO Passwords(service_name, username, password) 
              VALUES(?, ?, ?)
              ''', (service, username, hashed_password) #stores the password
              )


    conn.commit()
    conn.close()
    
    print(f'Password Added for {service}!!')


def delete_password(service):
    if validate_master_password():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c. execute('''
                DELETE FROM Passwords WHERE service_name = ?; ''', 
                (service,))

        conn.commit()
        conn.close()
        print(f'Deleted password for {service}')


def update_password(service, new_password):
    if validate_master_password():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        new_password = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(new_password, salt)
        
        #updates the password field with the new one
        c. execute('''
                UPDATE Passwords SET password = ?
                    WHERE service_name = ?;
                ''', (hashed, service))
                
        
        conn.commit()
        conn.close()
        print(f'Updated password for {service}')

import string
import secrets

DEFAULT_PASSWORD_LENGTH = 16

def generate_random_password(length=DEFAULT_PASSWORD_LENGTH):
    if length < DEFAULT_PASSWORD_LENGTH:
        print('Password length must be at least 16 characters')
        return None

    #character set
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = string.punctuation

    #combining all characters
    characters = uppercase + lowercase + digits + special

    #lsit to hold the password chars
    password = []

    # at least onece from every char-set
    password.append(secrets.choice(uppercase))
    password.append(secrets.choice(lowercase))
    password.append(secrets.choice(digits))
    password.append(secrets.choice(special))

    for i in range(length - 4):
        password.append(secrets.choice(characters))

    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


def main():
    if not(os.path.exists(DB_PATH)):
        first_use()  
       
    args = parse_args()
    try:
        #execute commands based on parsed arguments
        if args.command == 'add':
            add_password(args.service, args.username, args.password)
        elif args.command == 'first-use':
            first_use()
        elif args.command == 'update':
            update_password(args.service, args.new_password)
        elif args.command == 'delete':
            delete_password(args.service)
        elif args.command == 'create':
            result = generate_random_password(args.length)
            print(f'Generated Password: {result}')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()