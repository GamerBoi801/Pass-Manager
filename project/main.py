from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from prettytable import PrettyTable
import base64, random
import os, sqlite3, pyfiglet, argparse

#CONST
DB_PATH = 'password_manager.db'  

#encryption configuration
ENCRYPTION_KEY_SIZE = 16  # 16BYTES- 128bits
ENCRYPTION_MODE = 'CBC'    # AES mode (CBC)
IV_SIZE = 16                #size of the initialization vector in bytes

DEFAULT_PASSWORD_LENGTH = 16

def validate_master_password():
    user_attempt = input('Please enter the Master Password: ')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute('''
            SELECT master_password FROM user WHERE id = 1;
            ''')
        stored_master_password = c.fetchone()

        if stored_master_password:
            stored_master_password = stored_master_password[0]
            if decrypt_password(stored_master_password) == user_attempt:
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

def first_use():
    
    # this intialises everything for first time use
    txt = 'Welcome to the Password Manager!! '
    print(pyfiglet.figlet_format(txt))
    
    #initialize_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor() #connecting the db to execute commands
    try:
        #creating passwordd table in the db
        c.execute('''
              CREATE TABLE IF NOT EXISTS Passwords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        key TEXT NOT NULL
                  );    
            ''')
        
        #creates the user table for storing the master password
        c.execute('''  
        CREATE TABLE IF NOT EXISTS user(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  master_password TEXT NOT NULL );
                  ''')
        conn.commit()
        
        # creting and saving the master password and username
        username = input('Please Enter a username: ')
        while True:
            password1 = input('Please Enter a Master Password: ')
            password2 = input('Re-enter the Master Password: ')
            if password1 == password2:
                break
            print('Passwords do not match! Try Again')
        
        # additions to the database
        hashed_password = encrypt_password(password2)   
        c.execute('''
            INSERT INTO user (username, master_password) 
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()  
        print('Username and master password are set!!')
                
    except sqlite3.Error as e:
        print(f"An error occurred while inserting data: {e}")
    finally:
        c.close()
        conn.close()


def list_passwords():
    table = PrettyTable() #creates the PrettyTable obj
    #displays passwords in a pretty table 

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''SELECT service_name, username, password 
              FROM Passwords;
              ''')
    results = c.fetchall()
    
    #creates a list of the columns names
    column_names = [description[0] for description in c.description]

    #sets the field names for the PrettyTable
    table.field_names = column_names

    #adding the rows to the prettytable
    for row in results:
        table.add_row(row)

    print(table) #outputs the table
    
    conn.close()

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

    return parser.parse_args()  

def add_password(service, username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    hashed_password, key = encrypt_password(password) 
    
    # adding password to the db
    c.execute('''
        INSERT INTO Passwords(service_name, username, password, key) 
              VALUES(?, ?, ?, ?)
              ''', (service, username, hashed_password, key.hex()) #stores the key as a hex string
              )


    conn.commit()
    conn.close()
    print(f'Password Added for {service}!!')

def get_password(service):
    if validate_master_password():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute('''
                  SELECT username, password, key FROM Passwords WHERE service_name = ?;
                  ''', (service))
        result = c.fetchone()
        if result:
            username, encrypted, key_hex = result
            key = bytes.fromhex(key)

            decrypted = decrypt_password(encrypted, key)

            print(f'Service: {service}, Username: {username}, Password: {decrypted}')
        else:
            print('No password found for this service.')
        conn.close()

def delete_password(service):
    if validate_master_password():
        conn = sqlite3.connect(DB_PATH)
        c =conn.cursor()

        c. execute('''
                DELETE FROM Passwords WHERE service_name = ?''', service)
        conn.commit()
        conn.close()

def update_password(service, new_password):
    if validate_master_password():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    
        hashed, key = encrypt_password(new_password)
        #updates the password field with the new one
        c. execute('''
                UPDATE Passswords SET password = ?, key = ?
                    WHERE service_name = ?;
                ''', (hashed, key, service))
        
        conn.commit()
        conn.close()

def encrypt_password(password):
    key = get_random_bytes(16)  # Generate a random 128-bit key
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Initialization vector
    ciphertext = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
    
    # Return only the IV and ciphertext encoded in base64 for storage
    encrypted_data = base64.b64encode(iv + ciphertext).decode('utf-8')
    
    # Return the encrypted password as a string
    return encrypted_data, key 

def decrypt_password(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]  # Extract the IV from the beginning
    ciphertext = encrypted_data[16:]  # The rest is the ciphertext
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return decrypted.decode('utf-8')

def generate_random_password(length = DEFAULT_PASSWORD_LENGTH):
    #character sets
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    special = "!@#$%^&*()"
    
    #combines all characters
    characters = uppercase + lowercase + digits + special
    
    #list to hold password characters
    password = []
    
    #ensures at least one character from each category (optional)
    password.append(random.choice(uppercase))
    password.append(random.choice(lowercase))
    password.append(random.choice(digits))
    password.append(random.choice(special))
    
    for i in range(length - 4):
        password.append(random.choice(characters))
    
    random.shuffle(password)
    return ''.join(password)

def main():
    if not(os.path.exists(DB_PATH)):
        first_use()  
       
    args = parse_args()
    try:
        #execute commands based on parsed arguments
        if args.command == 'add':
            add_password(args.service, args.username, args.password)
        elif args.command == 'get':
            get_password(args.service)
        elif args.command == 'first-use':
            first_use()
        elif args.command == 'list-all':
            list_passwords()
        elif args.command == 'update':
            update_password(args.service, args.new_password)
        elif args.command == 'delete':
            delete_password(args.service)
        elif args.command == 'create':
            generate_random_password(args.length)
    except Exception as e:
        print(f'An error ocurred: {e}')

if __name__ == '__main__':
    main()