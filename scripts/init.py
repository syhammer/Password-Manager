#Initialize - PM

import os
import sys

app_name = 'password-manager'
super_path = app_name.join(os.path.normpath(os.path.realpath(__file__).lower()).split(app_name)[:-1])+app_name

sys.path.insert(1,super_path)

import json

def get_config():
    with open(os.path.normpath(f'{super_path}/config.json')) as config_file:
        return json.load(config_file)

data_path = get_config()['path']['data']

def get_credential_fields():
    return get_config()['credentials']['csv']['fields']

def get_credential_fields_neat():
    return ','.join(get_credential_fields())

def create_shortcut(executable_name,path_to_executable,operating_system,file_extension):
    desktop = os.path.normpath(os.path.expanduser("~/Desktop"))

    if operating_system == 'linux':
        shortcut = (
            f'( exec "{path_to_executable}" )'
        )
    elif operating_system == 'windows':
        shortcut = (
            f'call "{path_to_executable}"'
        )

    with open(os.path.normpath(f'{desktop}/{executable_name}.{file_extension}'),'w') as shortcut_file:
        shortcut_file.write(shortcut)

def create_executable(script,operating_system,file_extension):
    name,path = script

    if operating_system == 'linux':
        executable = (
            f'python {path}'
        )
    elif operating_system == 'windows':
        executable = (
            f'python {path}\n'+
            f'pause'
        )

    executable_path = os.path.normpath(f'{super_path}/executables/{operating_system}/{name}.{file_extension}')

    with open(executable_path,'w') as executable_file:
        executable_file.write(executable)

    create_shortcut(name,executable_path,operating_system,file_extension)

def generate_executables(types):
    path_to_scripts = os.path.normpath(f'{super_path}/scripts')

    scripts = []

    for dirpath,dirnames,filenames in os.walk(path_to_scripts):
        if dirpath != path_to_scripts:
            continue

        for filename in filenames:
            if filename == '__init__.py':
                continue
            path = os.path.join(dirpath,filename)
            with open(path) as script:
                name = script.readline().strip('\n')[1:]
            scripts.append((name,path))

    if 'linux' in types:
        os.mkdir(f'{super_path}/executables/linux')
    elif 'windows' in types:
        os.mkdir(f'{super_path}/executables/windows')

    for script in scripts:
        if 'linux' in types:
            create_executable(script,'linux','sh')
        if 'windows' in types:
            create_executable(script,'windows','bat')


if __name__ == '__main__':
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
        os.mkdir(data_path+"/keys")
        os.mkdir(data_path+"/salt")

    path_to_credentials = os.path.normpath(data_path+'/credentials.csv')

    if not os.path.isfile(path_to_credentials) or input(f'Do you want to clear your credentials, which are located in "{path_to_credentials}"? (Y/n)\n>> ') == 'Y':
        with open(path_to_credentials,'w') as credentials_file:
            credentials_file.write(get_credential_fields_neat()+'\n')

    types = []

    for type in get_config()['os']['supported']:
        if input(f'Do you want to generate executables for "{type}"? (Y/n)\n>> ') == 'Y':
            types.append(type)

    if not os.path.isdir(f'{super_path}/executables') or len(types) > 0:
        os.mkdir(f'{super_path}/executables')

        generate_executables(types)

    print('Initialized')
