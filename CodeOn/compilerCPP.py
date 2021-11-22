import os.path, subprocess
import os
from subprocess import STDOUT, PIPE
import datetime
import re
from xmlrpc.server import SimpleXMLRPCServer

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


def pipe(code, input):
    timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    fileName = 'CPP' + timeStamp
  
  
    f = open(fileName+ '.cpp', 'w')
    f.write(code)
    f.close()

    print(input)
  
    flag = 1
    try:
        flag = compile_cpp(fileName)
    except:
        print("Compilation error")

    if not flag:
        try:
            op = execute_cpp(fileName, input.encode()) 
            return op.encode()
        except:
            print("RunTime error")
    else:
        return flag.encode()
    


ipAddr = "127.0.0.1"
portNo = 6666

server = SimpleXMLRPCServer((ipAddr, portNo))
server.register_function(pipe, 'CppCompiler')

print(f"Server started at {ipAddr}:{portNo}")
server.serve_forever()