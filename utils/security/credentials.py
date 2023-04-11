import os
import csv

from utils import string_to_array
from scripts import init

app_name = 'password-manager'
super_path = app_name.join(os.path.normpath(os.path.realpath(__file__).lower()).split(app_name)[:-1])+app_name

data_path = init.get_config()['path']['data']

def is_name(name):
    with open(os.path.normpath(f'{data_path}/credentials.csv')) as csv_file:
        credentials_list = csv.DictReader(csv_file)

        for credentials in credentials_list:
            if name == credentials['name']:
                return True

def update_credentials(new_credentials):
    path = os.path.normpath(f'{data_path}/credentials.csv')

    with open(path,'r+') as csv_file:
        rows = [row for row in csv.DictReader(csv_file)]
        csv_file.truncate(0)

    with open(path,'w') as csv_file:
        credentials_writer = csv.DictWriter(csv_file,fieldnames=init.get_credential_fields())

        credentials_writer.writeheader()

        for credentials in rows:
            credentials_writer.writerow(new_credentials if new_credentials['name'] == credentials['name'] else credentials)

def append_credentials(new_credentials):
    with open(os.path.normpath(f'{data_path}/credentials.csv'),'a+') as csv_file:
        credentials_reader = csv.DictReader(csv_file)

        credentials_writer = csv.DictWriter(csv_file,fieldnames=init.get_credential_fields())
        credentials_writer.writerow(new_credentials)

def save_credentials(new_credentials):
    if is_name(new_credentials['name']):
        update_credentials(new_credentials)
    else:
        append_credentials(new_credentials)

def get_credentials(name=None,username=None,unlock=None):
    with open(os.path.normpath(f'{data_path}/credentials.csv')) as csv_file:
        credentials_reader = csv.DictReader(csv_file)

        for row in credentials_reader:
            if (name is not None and row['name'] == name) or (username is not None and username in string_to_array.convert(row['usernames'])) or (unlock is not None and unlock in string_to_array.convert(row['unlocks'])):
                yield row

def in_array_substring(value,array):
    for item in array:
        if value in item:
            return True

def search_credentials(search):
    with open(os.path.normpath(f'{data_path}/credentials.csv')) as csv_file:
        credentials_reader = csv.DictReader(csv_file)

        for row in credentials_reader:
            if (search in row['name']) or in_array_substring(search,string_to_array.convert(row['usernames'])) or in_array_substring(search,string_to_array.convert(row['unlocks'])):
                yield row
