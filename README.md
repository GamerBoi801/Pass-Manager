# CLI Password Manager

A secure command-line password manager that allows users to store and manage passwords using encryption.

## Table of Contents



## Features

- **Add Passwords**: Store service credentials securely.
- **Retrieve Passwords**: Fetch and decrypt passwords for specific services.
- **Update Passwords**: Modify existing passwords.
- **Delete Passwords**: Remove stored passwords.
- **List All Passwords**: Display all stored passwords in a formatted table.
- **Generate Random Passwords**: Create strong, random passwords.
- **Security**: Uses AES-128 encryption with a unique initialization vector for each password, ensuring secure storage of sensitive info.

## Installation

### Prerequisites
Before you begin, ensure you have the following installed:

- **Python 3**: Make sure you have Python 3 installed on your machine.
- ***Required Libraries**: Install the required libraries using `pip`.

### Required Libraries

- `pycryptodome`: for encryption and decryption of passwords.
- `prettytable`: for displaying data in a formatted table.
- `sqlite3`: for database management (this is included with Python's standard library).
- `argparse`: for parsing command-line arguments.
- `base64`: for encoding and decoding data.
- `random`: for generating random passwords.
- `os`: for interacting with the operating system.

