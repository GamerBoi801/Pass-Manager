import sqlite3, bcrypt

def initialize_db():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor() #connecting the db to execute commands
    try:
        #creating table in the db
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
                  username TEXT NOT NULL,
                  master_password TEXT NOT NULL );
                  ''')
        
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close() # closes the connection to the db

def add_password(service, username, password):
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
    
    # adding password to the db
    c.execute('''
INSERT INTO Passwords(service_name, username, password) 
              VALUES(?, ?, ?)
              ''', (service, username, hashed_password)
              )
    
    
    conn.commit()
    conn.close()

def get_password(service):
    user_master_password = input('Please enter your Master Password: ') #prompts the user for the master password

    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()

    #retreiving the master password from the db
    c.execute(''' 
            SELECT master_password FROM id = 1  
            ''') # in the meantime provided there is only one user
    
    result = c.fetchone() #fetches the result from the db
    
    if result:
        stored_hash_password = result[0]
        if bcrypt.checkpw(user_master_password, stored_hash_password):
            # retrives the password from the db
            c.execute('''
            SELECT * FROM Passwords WHERE service_name = ?
            ,(service);
            ''' )
            password_entry = c.fetchone()

            if password_entry:
                return password_entry[0]
            else:
                print('Password not found')
        else:
            print('Master Password is incorrect, ACCESS DENIED')
        

            
        