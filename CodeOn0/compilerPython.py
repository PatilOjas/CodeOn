import os.path, subprocess
from subprocess import STDOUT, PIPE
import datetime
import re
from xmlrpc.server import SimpleXMLRPCServer

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

def pipe(code, input):
    timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    fileName = 'Python' + timeStamp + '.py'
  
    
    f = open(fileName, 'w')
    f.write(code)
    f.close()

    print(input)
  
    op = interpret_python(fileName, input.encode()) 
    return op.encode()
    
    

ipAddr = "127.0.0.1"
portNo = 7777

server = SimpleXMLRPCServer((ipAddr, portNo))
server.register_function(pipe, 'PyInterpreter')

print(f"Server started at {ipAddr}:{portNo}")
server.serve_forever()
