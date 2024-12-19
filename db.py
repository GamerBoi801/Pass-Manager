import sqlite3
import logging, hashlib, getpass

# setting up logging configuration
logging.basicConfig(level=logging.ERRORa,
                     format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

def initialize_database():
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()
    
    try:
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_password_hash TEXT NOT NULL
            );
        ''')

        # Create passwords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            ); 
        ''')
        
        connection.commit()  # Save changes

    except sqlite3.Error as e:
        logging.error(f"An error occurred while initializing the database: {e.args}")
        print("An error occurred while initializing the database.")

    finally:
        cursor.close()  # Close cursor
        connection.close()  # Close connection

def execute_query(query, params):
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        connection.commit()
    
    except sqlite3.Error as error:
        logging.error(f'An error occurred during query execution: {error.args}')
    
    finally:
        cursor.close()
        connection.close()


def fetch_query(query, params):
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    
    except sqlite3.Error as error:
        logging.error(f'An error occurred during fetch execution: {error.args}')
    
    finally:
        cursor.close()
        connection.close()
