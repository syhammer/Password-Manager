import os

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import secrets
import base64

from scripts import init

app_name = 'password-manager'
super_path = app_name.join(os.path.normpath(os.path.realpath(__file__).lower()).split(app_name)[:-1])+app_name

data_path = init.get_data_path()

def generate_key(key_id,save=True):
    key = Fernet.generate_key()

    if save:
        with open(os.path.normpath(f'{data_path}/keys/{key_id}.key'),'wb') as key_file:
            key_file.write(key)

    return key

def get_path_to_key(name):
    return os.path.normpath(f'{data_path}/keys/{name}_key.key')

def set_key(key_id,key):
    with open(os.path.normpath(f'{data_path}/keys/{key_id}.key'),'wb') as key_file:
        key_file.write(key)

def get_key(key_id):
    path = os.path.normpath(f'{data_path}/keys/{key_id}.key')

    if os.path.isfile(path):
        with open(path,'rb') as key_file:
            return key_file.read()
    else:
        key = generate_key(key_id)
        return key

def encrypt_string(string,key_id):
    fernet = Fernet(get_key(key_id))
    return fernet.encrypt(string.encode())

def decrypt_bytes(bytes,key_id):
    fernet = Fernet(get_key(key_id))
    return fernet.decrypt(bytes).decode("utf-8")

def generate_salt(salt_id,size=16,save=True):
    salt = secrets.token_bytes(size)

    if save:
        with open(os.path.normpath(f'{data_path}/salt/{salt_id}.salt'),'wb') as salt_file:
            salt_file.write(salt)

    return salt

def get_salt(salt_id):
    path = os.path.normpath(f'{data_path}/salt/{salt_id}.salt')

    if os.path.isfile(path):
        with open(path, 'rb') as salt_file:
            return salt_file.read()
    else:
        salt = generate_salt(salt_id)
        return salt

def derive_key(salt, password):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def generate_password_key(password, salt_id,derived_key_id=None):
    salt = get_salt(salt_id)
    derived_key = derive_key(salt, password)
    key = base64.urlsafe_b64encode(derived_key)

    if derived_key_id != None:
        set_key(derived_key_id,key)

    return key

def encrypt_password(password,key_id):
    fernet = Fernet(get_key(key_id))
    return fernet.encrypt(password.encode())

def encrypt_password_by_name(password,name):
    key_id = name+'_key'
    salt_id = name+'_salt'

    generate_password_key(password,salt_id,key_id)

    return encrypt_password(password,key_id)

def decrypt_password(encrypted_password,key_id):
    fernet = Fernet(get_key(key_id))

    try:
        return fernet.decrypt(encrypted_password).decode("utf-8")
    except cryptography.fernet.InvalidToken:
        print("Invalid token, most likely the password is incorrect")
        return None

def decrypt_password_by_name(password,name):
    key_id = name+'_key'

    return decrypt_password(password,key_id)
