# config.py

#database configuration
DB_PATH = 'password_manager.db'  

#encryption configuration
ENCRYPTION_KEY_SIZE = 16  # 16BYTES- 128bits
ENCRYPTION_MODE = 'CBC'    # AES mode (CBC)
IV_SIZE = 16                #size of the initialization vector in bytes

DEFAULT_PASSWORD_LENGTH = 16
