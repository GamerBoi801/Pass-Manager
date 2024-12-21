# CLI Password Manager Project Structure

## 1. Core Files

### 1.1 `db.py`
- **Purpose**: Manage database initialization and operations.
- **Functions to Include**:
  - `initialize_db()`: Create the database and tables if they don't exist.
  - `add_password(service, username, password)`: Insert a new password entry.
  - `get_passwords()`: Retrieve all stored passwords.
  - `delete_password(service)`: Remove a password entry by service name.
  - `update_password(service, new_password)`: Update an existing password.


### 1.2 `user.py`
- **Purpose**: Handle user interactions and CLI functionalities using argparse.
- **Functions to Include**:
  - `first_use()`: Set up the master password and username for the first time.
  - `parse_args()`: Use argparse to define and parse command-line arguments.
  - `list_passwords()`: Display all stored passwords in a user-friendly format.
  - `add_new_password()`: Collect input from the user to add a new password.
  - `vlaidate_master_password()`: validates master password for the user_attempt parameter

### 1.3 `main.py`
- **Purpose**: Serve as the entry point for the program, importing necessary modules.
- **Functions to Include**:
  - `main()`: Coordinate the flow of the application, calling functions from `user.py` and `db.py`.

### 1.4 `rehpic.py`
- **Purpose**: contains the encrypting and decryting algorithms
**Functions**: 
- `encrypt_password()`
- `decrypt_password()`
## 2. Additional Files

### 2.1 `utils.py`
- **Purpose**: Contain utility functions that can be reused across different modules.
- **Functions to Include**:
  - `encrypt_password(password)`: Encrypt a given password before storing it.
  - `decrypt_password(encrypted_password)`: Decrypt a stored password when retrieving it.
  - `generate_random_password(length)`: Generate a strong random password.

### 2.2 `config.py`
- **Purpose**: Store configuration settings for the application.
- **Contents**:
  - Default values for encryption methods, database paths, etc.
  - Load settings from a configuration file if available.

### 2.3 `cli.py`
- **Purpose**: Handle command-line interface interactions more extensively.
- **Functions to Include**:
  - Implement subcommands (e.g., list, add, delete) using argparse for better organization.


## 3. Suggested Routines

### 3.1 User Authentication
- Implement routines to securely handle user authentication, including checking the master password.

### 3.2 Password Management
- Add routines for listing, adding, updating, and deleting passwords with proper error handling.

### 3.3 Backup Functionality
- Implement a routine to back up the database to a specified location or export passwords to a file.

### 3.4 Logging
- Create a logging module to track actions performed by the user (e.g., adding or deleting passwords).

### 3.5 Clipboard Integration
- Add functionality to copy passwords to the clipboard for easy pasting into login forms.
### **[Schema](schema.sql)**