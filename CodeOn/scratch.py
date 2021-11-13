import os.path, subprocess
from subprocess import STDOUT, PIPE


def compile_java(java_file):
    proc = subprocess.Popen(['javac', java_file])
    # if proc.returncode != 0:
    #     print("Error:")
    #     print(proc.stdout)
    #     return -1


def execute_java(java_file, stdin):
    java_class, ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd,  stdin = PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = proc.communicate(input=stdin.encode())
    print(stderr)
    if stderr is None:
        print("STDOUT")
        print(stdout.decode())
    elif proc.returncode != 0:
        print("STDERROR")
        print(stderr.decode())

# if not compile_java('Hi.java'):
compile_java('Java20211113093651166484.java')
execute_java('Java20211113093651166484.java', '1\n0\n')

# import os

# x = os.system("javac Hi.java")
