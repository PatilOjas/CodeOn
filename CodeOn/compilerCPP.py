import os.path, subprocess
import os
from subprocess import STDOUT, PIPE
import socket
import threading
import datetime
import re

def execute_cpp(filename, stdin):
    cmd = [f'./{filename}']
    proc = subprocess.Popen(cmd,  stdin = PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = proc.communicate(input=stdin)
    if stderr is None:
        print(stdout.decode())
        return stdout.decode()
    elif proc.returncode != 0:
        print(stderr.decode())
        return stderr.decode()

def compile_cpp(filename):
    # subprocess.check_call([f'g++ -o {filename}', filename+'.cpp'])
    os.system(f"g++ -o {filename} {filename}.cpp 2> logCPP")
    f = open('logCPP', 'r')
    l = f.read()
    if len(l) > 0:
        return l
    else:
        return 0


def pipe(clientConnection):
    timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    fileName = 'CPP' + timeStamp
  
    code = clientConnection.recv(2048).decode()
  
    f = open(fileName+ '.cpp', 'w')
    f.write(code)
    f.close()

    input = clientConnection.recv(2048).decode()
    print(input)
  
    flag = 1
    try:
        flag = compile_cpp(fileName)
    except:
        print("Compilation error")

    if not flag:
        try:
            op = execute_cpp(fileName, input.encode()) 
            clientConnection.send(op.encode())
        except:
            print("RunTime error")
    else:
        clientConnection.send(flag.encode())
    
    clientConnection.close()

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creation successful!")
except socket.error as err:
    print("Socket creation failed with error", str(err))

ipAddr = "127.0.0.1"
portNo = 6666

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