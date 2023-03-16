import os
import sys

if __name__ == '__main__':
    sys.path.insert(1,os.getcwd())

    from utils.security import encryption
    from utils.security import credentials
    from utils import format
    from scripts import init

import getpass
import random

def get_generated_password():
    length = int(input('Input the length of your new password\n>> '))
    allowed_chars = init.get_config()['format']['generated_password']['allowed_chars']

    for i in range(length):
        yield random.choice(allowed_chars)

def get_password_unlocks(usernames=[],unlocks=[]):
    if len(unlocks) != 0:
        print('This password already unlocks:')

        for unlock in unlocks:
            print(unlock)

    while True:
        new_unlock = input('Add an unlock to this password (leave this empty to finish)\n>> ')

        if new_unlock == '':
            return (usernames,unlocks)
        else:
            usernames.append(input('Input the username for this specific unlock\n>> '))
            unlocks.append(new_unlock)

if __name__ == '__main__':
    while True:
        name = format.from_name(input('Input a name for your password\n>> '),'password_name')

        if credentials.is_name(name):
            replace_old = input('This name already exists, do you want to replace all data that is attached to this name? (Y/n)\n>> ')
            if replace_old:
                break
        else:
            break

    get_password_from_input = input('Do you want to input a password or generate one? (Y=input/n=generate)\n>> ')

    if get_password_from_input == 'Y':
        encrypted_password = encryption.encrypt_password_by_name(getpass.getpass('Input your password\n>> '),name)
    else:
        password = ''.join([char for char in get_generated_password()])
        print(f'This is your generated password: "{password}"')
        encrypted_password = encryption.encrypt_password_by_name(password,name)

    path_to_key = encryption.get_path_to_key(name)

    usernames,unlocks = get_password_unlocks()

    new_credentials = {
        "name":name,
        "password":encrypted_password.decode('utf-8'),
        "path_to_key":path_to_key,
        "usernames":usernames,
        "unlocks":unlocks
    }

    credentials.save_credentials(new_credentials)
