#handles all the user realted operations
import bcrypt, sqlite3, pyfiglet
from db_1 import initialize_db
from utils import encrypt_password, decrypt_password, generate_random_password
from config import DB_PATH, ENCRYPTION_KEY_SIZE, IV_SIZE, DEFAULT_PASSWORD_LENGTH
from prettytable import PrettyTable
import argparse
    

