# Password Manager

## Initialization:

To initialize this script upon install, you _must_ enter the following:
```Batchfile
npm start
```
This will install the **npm** and **python** dependencies as well as run an initialization script that creates the necessary folder structure.

## How to Use

There are 3 preprogrammed operations that this script can do:

* Save a password
    In order to run this operation, you must enter the following:
    ```Batchfile
    npm run save-password
    ```
    This will allow you to input any password or have it generated. You can then tell the script what it's used for and what usernames go with it. Once those steps are completed, the password will be encrypted and archived.

* Get a password
    In order to run this operation, you must enter the following:
    ```Batchfile
    npm run get-password
    ```
    This is how you access your passwords, as they are otherwise encrypted. You are given the option to search through your entire password archive. The search results are found based on password names, usernames, and unlocks.

* Update a password
    In order to run this operation, you must enter the following:
    ```Batchfile
    npm run update-password
    ```
    You can update a password's username and unlocks. For instance, you could use this password for a new account, update your password archive, and let it know about your new login.

Alternatively, you can use the executables that are created during the initialization process. Currently, only Windows and Linux executables are supported.
