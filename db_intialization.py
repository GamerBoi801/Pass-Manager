import sqlite3
import logging, hashlib, getpass

# setting up logging configuration
logging.basicConfig(level=logging.ERRORa,
                     format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

def initialize_db():
    connection = sqlite3.connect('password_manager.db') # creates a new db if it does not exist
    cursor = connection.cursor() # object used to execute SQL commands 

    try:

        #creates the users table
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS users(
                           user_id INTEGER PRIMARY KEY,
                           master_password_hash TEXT NOT NULL
                           );
                       ''')

        #creates the passwords table
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS passwords(
                           id INTEGER PRIMARY KEY,
                           user_id INTEGER NOT NULL,
                           website TEXT NOT NULL,
                           username TEXT NOT NULL,
                           password TEXT NOT NULL,
                           FOREIGN KEY(user_id) REFERENCES users(id)
                           ); 
                       ''') 
        
        #prompting 4 master password
        master_password = getpass.getpass('Enter a master password: ')

        #hashing the master password
        master_password_hash = hashlib.sha256(master_password.encode()).hexdigest()

        #inserting it into db
        cursor.execute('''
                       INSERT INTO users(master_password_hash)
                       VALUES(?);
                       ''', (master_password_hash,))
        
        connection.commit() # commits the changes to the db

    except sqlite3.Error as error:
        logging.error(f'Error: {error}')
    
    finally:
        cursor.close()  
        connection.close() # closes the connection to the db

def user_login():
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    try:
        master_password = getpass.getpass('Enter your master password: ')
        cursor = connection.cursor()

    except sqlite3.Error as error:
        logging.error(f'Error: {error}')


if __name__ == '__main__':
    initialize_db()
    print('Database initialized successfully')