# Corona Reverse Shell

Python Reverse shell

## Getting Started
Simple multiclient python reverse shell with extra functionalities

Firstly run the server program using any available python IDE and ensure the interpreter is running python 3. 
Wait for a few seconds allowing the listener to actively listen for new connection before running the client program


# Accessing active connection list 

Simply run the 'list' command to display all active connection to the server in a tabular fashion. 


# Starting a session 

To start a session with a connected node simply use the "select" statement followed by the client ID of the connected node


# Features 
   Corona Shell Commands
               'list':['lists all active connections'] \
               'select (target Client_ID)':['selects a target and creates a session between the server and the client machine '] \
               'guide': Display Corona's user commands \
      Client Commands \
              'quit':['takes you back to the Corona shell interface'] \
              'wifi_passwords':['gets all known wifi password that the client node has ever connected to'], \
              'screenshot':['takes a screen shot of the client machine'], \
              'camshot':['captures an image from the client's webcam'], \
              'encrypt (password) (directory)':[encrypts all files in the directory specified'] [if directory is not specified all files in the current directory will be encrypted], \
              'decrypt (password) (directory)':['decrypts all files in the directory specified'] [if directory is not specified all files in the current directory will be decrypted], \
              'get (filename or path)':['gets file from the victim's machine and sends it over to the server'], \
              'send (filename or path)':['send file from server and stores it on the victim's machine'] \


## Author

* **Xand**
