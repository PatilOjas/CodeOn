import socket
import time

class CompilerConn:
    def compilerConnJava(self, code):
        try:
            # Creates a socket and if it fails, it will raise an error
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket creation successfull!!!")
        except socket.error:
            print("Socket creation failed with error", str(socket.error))

        # Default port for server 
        portNo = 9999

        # Bind the socket
        try:
            clientSocket.bind(("127.0.0.1", 8888))
            print("Socket has been bound at the port 8888")
        except socket.error as err:
            print("Failed to Bind the socket with error", str(err))

        # Connects to server
        try:
            clientSocket.connect(("127.0.0.1", portNo))
            print("Connection successfull!!!")
        except socket.error:
            print("Failed to connect with error", socket.error)
        
        print('test\n',code)
        clientSocket.send(code.encode())
        time.sleep(2)
        clientSocket.send("1\n1\n".encode())
        recieved = clientSocket.recv(2048).decode()
        clientSocket.close()
        # print(recieved)

        return recieved

