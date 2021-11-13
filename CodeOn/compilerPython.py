import os.path, subprocess
from subprocess import STDOUT, PIPE
import socket
import threading
import datetime
import re

def interpret_python(filename, stdin):
    cmd = ['python3', filename]
    proc = subprocess.Popen(cmd,  stdin = PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = proc.communicate(input=stdin)
    if stderr is None:
        print(stdout.decode())
        return stdout.decode()
    elif proc.returncode != 0:
        print(stderr.decode())
        return stderr.decode()

def pipe(clientConnection):
    timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    fileName = 'Python' + timeStamp + '.py'
  
    code = clientConnection.recv(2048).decode()
  
    f = open(fileName, 'w')
    f.write(code)
    f.close()

    input = clientConnection.recv(2048).decode()
    print(input)
  
    # try:
    op = interpret_python(fileName, input.encode()) 
    clientConnection.send(op.encode())
    # except:
    #     print("ERROR in python code")
    
    clientConnection.close()

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creation successful!")
except socket.error as err:
    print("Socket creation failed with error", str(err))

ipAddr = "127.0.0.1"
portNo = 7777

try: 
    serverSocket.bind((ipAddr, portNo))
    print("Socket has been bound on port no", portNo)
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


# interpret_python('Hi.py', 'Ojas\nPatil')