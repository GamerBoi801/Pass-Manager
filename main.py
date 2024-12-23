from db import initialize_db, add_password, get_password, delete_password, update_password
from user import first_use, parse_args, list_passwords, validate_master_password
from utils import encrypt_password, decrypt_password, generate_random_password
from config import DB_PATH, ENCRYPTION_KEY_SIZE, IV_SIZE, DEFAULT_PASSWORD_LENGTH
import os

if __name__ == '__main__':
    if not(os.path.exists(DB_PATH)):
        first_use()
