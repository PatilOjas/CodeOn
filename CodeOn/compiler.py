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
    stdout, stderr = proc.communicate(input=stdin)
    if stderr is None:
        return stdout.decode()
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
        print(text[s:s+r[0]])
        text = text[:s] + clsName + text[s+r[0]:]
    else:
        print(text[s:s+r1[0]])
        text = text[:s] + clsName + text[s+r1[0]:]

    f = open(clsName + '.java', 'w')

    
    f.write(text)
    f.close()

    input = clientConnection.recv(2048).decode()
    print(input)
    try:
        compile_java(clsName + '.java')
        clientConnection.send(execute_java(clsName + '.java', input.encode()).encode())
    except:
        print("ERROR in java code")
    
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
