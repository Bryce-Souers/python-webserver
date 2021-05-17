import socket
import sys
import os
import errno
import time

# Bryce Souers
# web_client.py - Attempts to connect to a local web server and request a file
# Overview:
# 	Parse arguments from command line into variables
# 	Create an IPv4 TCP socket
# 	Attempt to connect to a local web server
# 	Send an HTTP request with a file we want in the header
# 	Keep reading in data from the socket until we receive the full file data

# Check arguments for validity
if(len(sys.argv) < 4):
	print("CLIENT >> [ERROR]: Usage: python3 " + sys.argv[0] + " serverAddr serverPort filename")
	sys.exit(1)
server_ip = sys.argv[1]
server_port = int(sys.argv[2])
file_name = sys.argv[3]

# Create and setup IPv4/TCP socket connection
try:
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
	print("CLIENT >> [ERROR]: Socket creation failed.\n" + str(e))
	sys.exit(1)

# Connect to the server
try:
	client_socket.connect((server_ip, server_port))
except socket.error as e:
	print("CLIENT >> [ERROR]: Socket failed to connect to server.\n" + str(e))
	sys.exit(1)

print('------The client is ready to send--------')
print(str(client_socket.getsockname()) + '-->' + str(client_socket.getpeername()))

# Send an HTTP GET request which tells which file the client wants
try:
	getRequest = "GET /" + file_name + " HTTP/1.1\r\nHost: " + server_ip + "\r\n"
	getRequest = getRequest + "Accept: text/html\r\nConnection: keep-alive\r\n"
	getRequest = getRequest + "User-agent: RoadRunner/1.0\r\n\r\n"
	# Send request over socket
	client_socket.send(getRequest.encode())
except error as e:
	print("CLIENT >> [ERROR]: Could not send GET request: " + str(e))
	clientSocket.close()
	sys.exit(1)

# Loop to keep pulling data from socket receive buffer and appending to message
message = ""
while True:
	# Artificial throttling of client
	time.sleep(0.1)
	try:
		# Receive 16 bytes from the socket connection
		newPart = client_socket.recv(16)
		# Append data to the previous data
		message = message + newPart.decode()
		# If there's no more data, print out the aggregated message received
		if not newPart:
			print (message, flush=True)
			break
		if message[len(message)-1] != "\n":
			continue
		else:
			print(message, flush=True)
			message = ""
	except error as e:
		print('Error reading socket: ' + str(e))
		sys.exit(1)

client_socket.close()  
sys.exit(0) 
