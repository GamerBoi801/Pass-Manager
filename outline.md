# Password Manager CLI Project Outline

## Project Overview
- **Purpose**: Develop a secure CLI password manager that generates, stores, and retrieves passwords, with autofill capabilities for popular web browsers.
- **Technologies Used**: 
  - Python
  - SQLite (or another database)
  - Cryptography libraries (e.g., `cryptography`)
  - Browser automation libraries (e.g., `selenium`, `pyautogui`)

## Features to Implement

### 1. Password Generation
-  Implement a robust password generator.
  -  Allow user-defined parameters (length, character types).
  -  Ensure complexity (at least one character from each selected category).

### 2. User Authentication
-  Create a master password system.
  -  Hash the master password for secure storage using PBKDF2 or bcrypt.
  -  Implement user registration and login functionality.

### 3. Secure Storage
-  Choose a database for storing passwords (e.g., SQLite).
-  Design database schema:
  -  User table (for master password and settings).
  -  Password entries table (for storing individual passwords).
-  Implement encryption for stored passwords.

### 4. Command-Line Interface (CLI)
-  Use a library like **Click** or **Argparse** to create an intuitive CLI.
  -  Implement commands for adding, retrieving, updating, and deleting passwords.
  -  Provide help commands and usage instructions.

### 5. Autofill Functionality
-  Implement autofill capabilities for browsers:
  -  Use **Selenium** to automate browser actions for filling in login forms.
  -  Optionally use **pyperclip** to copy passwords to the clipboard for manual pasting.

### 6. Password Management Features
-  Add functionality to:
  -  Create, read, update, and delete passwords.
  -  Search for passwords by website or username.
  -  Organize passwords into categories or tags.

### 7. Password Health Check
-  Implement a feature to assess password strength and provide recommendations.

### 8. Breach Monitoring
-  Integrate breach detection services to notify users of compromised passwords.

### 9. Backup and Recovery
-  Allow users to back up their password vault securely.
-  Implement recovery options in case of lost access.

## Development Steps

### Phase 1: Planning and Setup
-  Define project requirements and scope.
-  Set up version control (e.g., Git).
-  Create a virtual environment for dependencies.

### Phase 2: Core Functionality Development
-  Implement password generation feature.
-  Develop user authentication system.
-  Set up secure storage with encryption.

### Phase 3: CLI Development
-  Design and build the CLI using Click or Argparse.
-  Integrate core functionalities into the CLI commands.

### Phase 4: Autofill Implementation
-  Develop browser automation scripts using Selenium or pyautogui.
-  Test autofill functionality across different browsers.

### Phase 5: Testing and Debugging
-  Conduct unit tests for individual components.
-  Perform integration testing for overall functionality.
-  Fix bugs and optimize performance.

### Phase 6: Documentation and Deployment
-  Write user documentation and guides on how to use the CLI tool.
-  Prepare code documentation (docstrings, comments).
-  Deploy the application as a package or executable.



# My plan
### first time use
 - initaializes db
 - 