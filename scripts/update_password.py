import os
import sys

if __name__ == '__main__':
    sys.path.insert(1,os.getcwd())

    from utils.security import encryption
    from utils.security import credentials
    from utils import input_gen
    from utils import string_to_array

    from scripts import save_password

def update_credential(credential):
    new_usernames,new_unlocks = save_password.get_password_unlocks(string_to_array.convert(credential['usernames']),string_to_array.convert(credential['unlocks']))
    credential['usernames'] = new_usernames
    credential['unlocks'] = new_unlocks
    return credential

search = input('Search >> ')

credentials_list = [cred for cred in credentials.search_credentials(search)]

new_credentials = []

for credential in credentials_list:
    name = credential['name']

    if input(f'Do you want to update "{name}"? (Y/n)\n>> ') == 'Y':
        new_credentials.append(update_credential(credential))

for new_credential in new_credentials:
    name = new_credential['name']
    print(f'Updated "{name}"')

    credentials.save_credentials(new_credential)
