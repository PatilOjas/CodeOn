import math
import socket
import time
import threading


timeKeepersDict = dict()

class Time:
	def __init__(self, t) -> None:
		self.timeout_in = t 

def countdown(t, clientConnection):
	while t.timeout_in >=0:
		mins, secs = divmod(t.timeout_in, 60) 
		print(f"Time remaining: ", end=" ")
		print(f"{'{:02d}'.format(mins)}:{'{:02d}'.format(secs)}", end='\r')
		time.sleep(1)
		t.timeout_in -= 1
	clientConnection.send("Time Up!!!!".encode())
	
def clientHandeler(clientConnection):
	start = time.time()
	incoming = clientConnection.recv(1024).decode()
	print(incoming)
	incomingData = eval(incoming)
	if incomingData['secret'] not in timeKeepersDict.keys():
		timeOut = Time(incomingData['time'])
		tid = threading.Thread(target=countdown, args=(timeOut, clientConnection,))
		tid.start()
		timeKeepersDict[incomingData['secret']] = {'timeOut': timeOut, 'start': time.time()}

	elif incomingData['secret'] in timeKeepersDict.keys():
		clientTime = time.time()
		timeKeepersDict[incomingData['secret']]['timeOut'].timeout_in += math.ceil( clientTime - timeKeepersDict[incomingData['secret']]['start']) * 2
		print(f"Compensating {math.ceil(clientTime - start) * 2} seconds")

try:
	# Creates a socket and if it fails, it will raise an error
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket creation successfull!!!")
except socket.error as err:
	print("Socket creation failed with error", str(err))

# Default port for server 
portNo = 4441


# Bind the socket
try:
	serverSocket.bind(("127.0.0.1", portNo))
	print(f"Socket has been bound at the port {portNo}")
except socket.error as err:
	print("Failed to Bind the socket with error", str(err))

# Put the socket in the passive mode
try:
	serverSocket.listen(10)
	print("Server is listening")
except socket.error as err:
	print("Failed to listen with error", str(err))


while True:
	try:
		clientConnection, clientAddr = serverSocket.accept()
		print(f"Connection established successfully with {clientAddr}")
	except socket.error:
		print("Connection failed with error", socket.error)

	tid = threading.Thread(target=clientHandeler, args=(clientConnection,))
	tid.start()