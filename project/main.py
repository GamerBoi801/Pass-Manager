from db import initialize_db, add_password, get_password, delete_password, update_password
from user import first_use, parse_args, list_passwords, validate_master_password
from utils import encrypt_password, decrypt_password, generate_random_password
from config import DB_PATH, ENCRYPTION_KEY_SIZE, IV_SIZE, DEFAULT_PASSWORD_LENGTH
import os

if __name__ == '__main__':
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
