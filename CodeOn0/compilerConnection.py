import socket
import time
import xmlrpc.client

class CompilerConn:
    def compilerConnJava(self, code):
        portNo = 9999

        proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9999/")

        recieved = proxy.JavaCompiler(code, "1\n6\n")
        
        return recieved

    def compilerConnPython(self, code):
        portNo = 7777

        proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:7777/")

        recieved = proxy.PyInterpreter(code, "Hooman\nBeing\n")
        
        return recieved

    def compilerConnCPP(self, code):
        portNo = 6666

        proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:6666/")
        
        recieved = proxy.CppCompiler(code, "1\n4\n")
        
        return recieved

