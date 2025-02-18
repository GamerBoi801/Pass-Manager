# CLI Password Manager

A secure command-line password manager that allows users to store and manage passwords using encryption. Works seamlessly across Linux and Windows.

## Table of Contents
- [Features](#features)
- [Usage Commands](#usage-commands)
- [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Required Libraries](#required-libraries)
    - [Steps to Install](#steps-to-install)
- [Security Consideration](#security-considerations)
- [Contributing](#contributing)
- [Configuration](#configuration)
- [Contact](#contact-information)


## Features

- **Add Passwords**: Store service credentials securely.
- **Update Password**: Modify existing passwords for existing services.
- **Delete Passwords**: Removes stored passwords.
- **Generate Random Passwords**: Creates strong, random passwords.
- **Security**: Uses AES-128 encryption with a unique initialization vector for each password, ensuring secure storage of sensitive info.

## Installation

### Prerequisites
Before you begin, ensure you have the following installed:

- **Python 3**: Make sure you have Python 3 installed on your machine.
- ***Required Libraries**: Install the required libraries using `pip`.

### Required Libraries

- `prettytable`: for displaying data in a formatted table.
- `sqlite3`: for database management (this is included with Python's standard library).
- `argparse`: for parsing command-line arguments.
- `random`: for generating random passwords.
- `os`: for interacting with the operating system.
- `bcrypt`: for encrypting passwords.
- `getpass`: Allow confidential input of passwords on the CLI.
- `secrets`: More secure randomness.

## Security Considerations

- Always use strong, unique passwords for each service.
- Regularly update your passwords, and avoid reusing them across services.
- Ensure that your local environment is secure by keeping your OS updated.

## Steps to Install 

1. **Clone the repository**: 
    ```bash
    git clone https://github.com/GamerBoi801/Pass-Manager.git
    
    cd Pass-Manager
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    python pass_manager.py
    ```

## Contributing

Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## Contact Information
For questions or support, please reach out to me at MSK_working@proton.me

## Changes from Version 1.00 - 2.00:
- removing config.py with bcrypt
 - removing get_password , show_password
 - remvoing the encrypt and decrypt algorithms
- adding reset password
- changing encryption to bcrypt
- changing the schema to remove key column

## Getting Started 

### Initial Setup 

Follow these steps to set up the CLI password manager for the first time:

1. **Initialize the database**:
    ```bash
    python pass_manager.py first-use
    ```
2. **Start using the password manager**:
    ```bash
    python pass_manager.py --help
    ```