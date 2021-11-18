import os.path, subprocess, os
from subprocess import STDOUT, PIPE
import socket
import threading
import datetime
import re
import tempfile


originalClsName = ""

def compile_java(java_file):
    os.system(f"javac {java_file} 2> logJava")
    f = open('logJava', 'r')
    l = f.read()
    if len(l) > 0:
        return l
    else:
        return 0


def execute_java(java_file, stdin):
    java_class, ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    tempf2 = tempfile.TemporaryFile()
    with tempfile.TemporaryFile() as tempf1:
        proc = subprocess.Popen(cmd, stdin = PIPE, stdout=tempf1, stderr=tempf2)
        stdout, stderr = proc.communicate(input=stdin)
        tempf1.seek(0)
        tempf2.seek(0)
        if stderr is None:
            return tempf1.read().decode()
        else:
            return stderr.decode()

def pipe(clientConnection):
    # timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    # java_file = f'{timeStamp}.java'
    timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    clsName = 'Java'+timeStamp
    text = clientConnection.recv(2048).decode()
    print(text)
    q=re.search('public class', text).span()
    s= q[1]+1
    r=re.search(' ', text[s:]).span()
    r1= re.search('{', text[s:]).span()

    

    if r[0] < r1[0]:
        originalClsName = text[s:s+r[0]]
        # print(text[s:s+r[0]])
        text = text[:s] + clsName + text[s+r[0]:]
    else:
        originalClsName = text[s:s+r1[0]] 
        # print(text[s:s+r1[0]])
        text = text[:s] + clsName + text[s+r1[0]:]

    f = open(clsName + '.java', 'w')

    
    f.write(text)
    f.close()

    input = clientConnection.recv(2048).decode()
    print(input)

    flag = 0

    try:
       flag = compile_java(clsName + '.java')
    except:
        print("Compilation error in java code")

    if not flag:
        try:
            clientConnection.send(execute_java(clsName + '.java', input.encode()).encode())
        except:
            print("RunTime error in java code")
    else:
        flag = re.sub(clsName, originalClsName, flag)
        clientConnection.send(flag.encode())
    
    clientConnection.close()

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creation successful!")
except socket.error as err:
    print("Socket creation failed with error", str(err))

ipAddr = "127.0.0.1"
portNo = 9999

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
