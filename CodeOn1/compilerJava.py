import os.path, subprocess, os
from subprocess import STDOUT, PIPE
import datetime
import re
import tempfile
from xmlrpc.server import SimpleXMLRPCServer

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

def pipe(text, input):
    # timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    # java_file = f'{timeStamp}.java'
    timeStamp = re.sub(r'[\s:.-]', '', str(datetime.datetime.now()))
    clsName = 'Java'+timeStamp
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

    print(input)

    flag = 0

    try:
       flag = compile_java(clsName + '.java')
    except:
        print("Compilation error in java code")

    if not flag:
        try:
            return execute_java(clsName + '.java', input.encode()).encode()
        except:
            print("RunTime error in java code")
    else:
        flag = re.sub(clsName, originalClsName, flag)
        return flag.encode()
    
    
ipAddr = "127.0.0.1"
portNo = 9999


server = SimpleXMLRPCServer((ipAddr, portNo))
server.register_function(pipe, 'JavaCompiler')

print(f"Server started at {ipAddr}:{portNo}")
server.serve_forever()
