import os.path, subprocess
from subprocess import STDOUT, PIPE
import socket
import threading
import datetime
import re

def compile_java(java_file):
    subprocess.check_call(['javac', java_file])


def execute_java(java_file, stdin):
    java_class, ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin = PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = proc.communicate(input=stdin.encode())
    if stderr is None:
        return stdout.decode()
    else:
        return stderr.decode()

def pipe(clientConnection):
    timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    java_file = f'{timeStamp}.java'
    f = open(java_file, 'wb')
    file = clientConnection.recv(2048)
    f.write(file)
    f.close

    input = clientConnection.recv(2048).decode()
    try:
        compile_java(java_file)
        clientConnection.send(execute_java(java_file, input))
    except:
        print("ERROR in java code")
try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creation successful!")
except socket.error as err:
    print("Socket creation failed with error", str(err))

ipAddr = "127.0.0.1"
portNo = 9999

try: 
    serverSocket.bind((ipAddr, portNo))
    print("Soxket has been bound on port no", portNo)
except socket.error as err:
    print("Failed to bind the socket with error", str(err))

try:
    serverSocket.listen(10)
    print("Server is listening")
except socket.error as err:
    print("Failed to listen with error", str(err))

while(True):
    try:
        clientConnection, clientAddr = serverSocket.accept()
        print("Connection established successfully")
    except socket.error as err:
        print("Connection failed with error", str(err))
    

    tid = threading.Thread(target=pipe, args=(clientConnection,))
    tid.start()
