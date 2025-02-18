#lib
import os
import sqlite3
import pyfiglet
import bcrypt
import typer
import secrets
import string
import getpass
from prettytable import PrettyTable

#constants
#db path for storing passwords
DB_PATH = 'password_manager.db'

#default password length for generated passwords
DEFAULT_PASSWORD_LENGTH = 16

app = typer.Typer(help="CLI Password Manager")

def db_connection():
    return sqlite3.connect(DB_PATH) 

def validate_master_password():
    user_attempt = getpass.getpass('Please enter the Master Password: ')
    if not os.path.exists(DB_PATH):
        typer.echo("Database not found. Please run the 'first-use' command to set up the application.")
        return False
    conn = db_connection()
    c = conn.cursor()

    try:
        c.execute('''
            SELECT master_password FROM user WHERE id = 1;
            ''')
        stored_master_password = c.fetchone()

        if stored_master_password:

            hashed_password = stored_master_password[0]

            if bcrypt.checkpw(user_attempt.encode('utf-8'), hashed_password):                   
                return True
            
            else:
                typer.echo('ACCESS DENIED: WRONG MASTER PASSWORD. ')
                return False
        else:
            typer.echo('No master password found in the db. ')
            return False
        
    except sqlite3.Error as e:
        typer.echo(f'DataBase Error: {e}')
        return False
    finally:
        c.close()
        conn.close()

@app.command()
def first_use():
    """Sets-up  the application for first use"""
    
    txt = 'Welcome to the Password Manager!! '
    typer.echo(pyfiglet.figlet_format(txt))
    
    #initialize_db()
    conn = db_connection()
    c = conn.cursor() #connecting the db to execute commands
    
    try:
        #creating password table in the db
        c.execute('''
              CREATE TABLE IF NOT EXISTS Passwords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
                  );    
            ''')
        
        #creates the user table for storing the master password
        c.execute('''  
        CREATE TABLE IF NOT EXISTS user(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  master_password TEXT NOT NULL
                        );
                  ''')
        conn.commit()
        
        while True:
            password1 = getpass.getpass('Please Enter a Master Password: ')
            password2 = getpass.getpass('Re-enter the Master Password: ')
            if password1 == password2:
                break
            typer.echo('Passwords do not match! Try Again')
        
        # adding the master_passsord to the db
        password2 = password2.encode('utf-8')
        key = bcrypt.gensalt()
        hashed_password= bcrypt.hashpw(password2, key)   
        
        c.execute('''
            INSERT INTO user (master_password) 
            VALUES (?)
        ''', (hashed_password,))

        conn.commit()  
        typer.echo('Username and master password are set!!')
                
    except sqlite3.Error or TypeError as e:
        typer.echo(f"An error occurred while inserting data: {e}")
    finally:
        c.close()
        conn.close()

    typer.echo('Setup complete. You can now use the password manager. ')

@app.command()
def add(service, username, password):
    """Adding a new password for a service"""
    conn = db_connection()
    c = conn.cursor()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
    
    # adding password to the db
    c.execute('''
        INSERT INTO Passwords(service_name, username, password) 
              VALUES(?, ?, ?)
              ''', (service, username, hashed_password)   #stores the password
              )

    conn.commit()
    conn.close()
    
    typer.echo(f'Password Added for {service}!!')


@app.command()
def delete(service):
    """Delete a password for a service."""
    if validate_master_password():
        conn = db_connection()
        c = conn.cursor()


        c. execute('''
                DELETE FROM Passwords WHERE service_name = ?; ''', 
                (service,))

        conn.commit()
        conn.close()
        typer.echo(f'Deleted password for {service}')

def update(service, new_password):
    """Update an exsisting passwod for a specific """
    if validate_master_password():

        conn = db_connection()
        c = conn.cursor()

        new_password = new_password.encode('utf-8')

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(new_password, salt)
        
        #updates the password field with the new one
        c. execute('''
                UPDATE Passwords SET password = ?
                    WHERE service_name = ?;
                ''', (hashed, service))
                    
        conn.commit()
        conn.close()
        
        typer.echo(f'Updated password for {service}')

@app.command()
def generate(length=DEFAULT_PASSWORD_LENGTH):
    length = int(length)

    """Generate a random password for a given length"""
    if length < DEFAULT_PASSWORD_LENGTH:
        print('Password length must be at least 16 characters')
        return typer.echo('Password length must be at least 16 characters')

    #combining all characters
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    typer.echo(f'Generated Password: {password}')
  
#main() function
if __name__ == '__main__':    
    app()
 