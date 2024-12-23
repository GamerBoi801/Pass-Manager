from db import initialize_db, add_password, get_password, delete_password, update_password
from user import first_use, parse_args, list_passwords, validate_master_password
from utils import encrypt_password, decrypt_password, generate_random_password
import os

if __name__ == '__main__':
    if not(os.path.exists('password_manager.db')):
        first_use()
    
    else:
