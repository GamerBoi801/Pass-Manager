import sqlite3
from utils import decrypt_password
#database configuration
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
