#Get Password - PM

import os
import sys

app_name = 'password-manager'
super_path = app_name.join(os.path.normpath(os.path.realpath(__file__).lower()).split(app_name)[:-1])+app_name

if __name__ == '__main__':
    sys.path.insert(1,super_path)

    from utils.security import encryption
    from utils.security import credentials
    from utils import string_to_array

search = input('Search >> ')

credentials_list = [cred for cred in credentials.search_credentials(search)]

for credential in credentials_list:
    name = credential['name']
    encrypted_password = credential['password'].encode()
    print(f'"{name}": "{encryption.decrypt_password_by_name(encrypted_password,name)}"')

    usernames = string_to_array.convert(credential['usernames'])
    unlocks = string_to_array.convert(credential['unlocks'])

    for unlock in unlocks:
        username = usernames[unlocks.index(unlock)]
        print(f'\t"{unlock}" is unlocked with the username "{username}"')
