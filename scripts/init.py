import os
import sys

sys.path.insert(1,os.getcwd())

import json

def get_config():
    with open(os.path.normpath(f'{os.getcwd()}/config.json')) as config_file:
        return json.load(config_file)

def get_credential_fields():
    return get_config()['credentials']['csv']['fields']

def get_credential_fields_neat():
    return ','.join(get_credential_fields())

if __name__ == '__main__':
    if not os.path.isdir(f'{os.getcwd()}/data'):
        os.mkdir(f'{os.getcwd()}/data')
        os.mkdir(f'{os.getcwd()}/data/keys')
        os.mkdir(f'{os.getcwd()}/data/salt')

    path_to_credentials = os.path.normpath(f'{os.getcwd()}/data/credentials.csv')

    with open(path_to_credentials,'w') as credentials_file:
        credentials_file.write(get_credential_fields_neat()+'\n')
