import socket
import time
import random


try:
	# Creates a socket and if it fails, it will raise an error
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket creation successfull!!!")
except socket.error:
	print("Socket creation failed with error", str(socket.error))

# Default port for server 
portNo = 5555

# Connects to server
try:
	clientSocket.connect(("127.0.0.1", portNo))
	print("Connection successfull!!!")
except socket.error:
	print("Failed to connect with error", socket.error)


incomingData = eval(clientSocket.recv(1024).decode().strip())
print(incomingData['Question'])
# time.sleep(5)
clientSocket.send(str(time.time()).encode())
while incomingData['time'] >= 0:
	mins, secs = divmod(incomingData['time'], 60) 
	print(f"Time remaining: {'{:02d}'.format(mins)}:{'{:02d}'.format(secs)}", end='\r')
	time.sleep(1)
	incomingData['time'] -= 1	
print("\nTime Up!!!!")
