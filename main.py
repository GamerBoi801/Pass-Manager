import random 
import string

def main():
    print('Welcome to the Password Creator')
    # user input loop 
    while True:
        try:
            # no. of passwords to generate
            number = int(input('How many Passwords would you like to have generated: '))
            if number <= 0:
                raise ValueError('Number should be a positive integer.')
            
            # length of password
            length = int(input('How many Characters should your password consist of: '))
            if length < 8:
                raise ValueError('Password should be at least 8 characters long.') 

            # Uppercase || lowercase
            uppercase = input('Should your password have UPPERCASE Characters? [y/n]: ').lower()
            lowercase = input('Should your password have lowercase Characters? [y/n]: ').lower()

            options = ['y', 'yes']
            include_uppercase = uppercase in options
            include_lowercase = lowercase in options
            
            #sSpecial characters
            special = input('Should your password have special characters? [y/n]: ').lower()
            include_special = special in options

            # digits
            digits = input('Should your passwords include numeric digits? [y/n]: ').lower()
            include_digits = digits in options

            # returns a dict from the password generator
            codes = password_generator(
                number=number,
                length=length,
                include_uppercase=include_uppercase,
                include_lowercase=include_lowercase,
                include_special=include_special,
                include_digits=include_digits)

            # printing the passwords 
            print('Here are your passwords! ')
            print()
            for key, value in codes.items():
                print(f'{key}. {value}')
                
            
            #encrypt Y|N
            encrypt_bool = input('Should we encrypt your passwords too? [y/n]: ').lower()
            include_encrypt = encrypt_bool in options
            if include_encrypt:
                print('Here are your encrypted passwords: ')
                print()
                for key, value in codes.items():
                    cipher = encrypt_mine(str(value))
                    print(f'{key}. {cipher}')  
            

            break  
        
        except ValueError as e:
            print(f'Error: {e}')

def password_generator(number=1, length=16, include_uppercase=True, include_lowercase=True, include_special=True, include_digits=True):
    passwords = {}
    for i in range(number):
        password = ''
  
        character_pool = ''
            
        if include_uppercase:
            character_pool += string.ascii_uppercase
        if include_lowercase:
            character_pool += string.ascii_lowercase
        if include_digits:
            character_pool += string.digits
        if include_special:
            character_pool += string.punctuationd

        if not character_pool:
            raise ValueError('At least one character type must be selected')
        
        # generate a password until it reaches the desired length
        while len(password) < length:
            password += random.choice(character_pool)
    
        # appending the generated password to the dictionary
        passwords[i + 1] = password

    return passwords      


def encrypt_mine(string):
    encrypted_chars = []
    key = 3  # key for the caesar cipher

    for char in string:
        if char.isalpha(): 
            
            if char.isupper():
                # calc new position
                new_position = (ord(char) - ord('A') + key) % 26 + ord('A')
            elif char.islower():
                new_position = (ord(char) - ord('a') + key) % 26 + ord('a')
            
            # appending the encrypted character
            encrypted_chars.append(chr(new_position))
        else:
            # non alphabetic characters remain unchanged
            encrypted_chars.append(char)

    # joins the list of characters into a single returnable string
    return ''.join(encrypted_chars)
  

if __name__ == "__main__":
    main()
