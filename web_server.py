import socket
import sys
import errno
import os

# Bryce Souers
# web_server.py - Runs a web server that sends back files using HTTP
# Overview:
# 	Get server port argument from command line
# 	Create a IPv4 TCP socket
# 	Accept connection requests
#		Parse HTTP header from request
#		Send requested file back to client with HTTP

# Check for server port argument
server_port = -1
if(len(sys.argv) < 2):
	print("SERVER >> [ERROR]: Missing server port argument: " + str(sys.argv[0]) + " port.")
	sys.exit(1)
else:
	try:
		server_port = int(sys.argv[1])
	except ValueError:
		print("SERVER >> [ERROR]: Invalid server port argument given. Number expected.")
		sys.exit(1)

# Create and setup IPv4 TCP socket
try:
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(('', server_port))
	server_socket.listen()
	print("SERVER >> [SUCCESS]: Socket created and setup successfully.")
except socket.error as e:
	print("SERVER >> [ERROR]: Socket creation failed: %s" %(e))
	sys.exit(1)

# Main loop to continually accept connection requests
while True:
	print('\r\nReady to serve...')
	try:
		# Accept a connection (this line of code blocks execution until a connection is received)
		connection_socket, connection_address = server_socket.accept()
		print("SERVER >> [" + str(connection_address) + "]: Connected successfully.")
		# Receive the HTTP header from the client (tells us what the client is requesting)
		get_message = connection_socket.recv(1024).decode()
		# Split HTTP request into lines
		get_lines = get_message.split("\r\n")
		get_data = {}
		# Loop through each line in HTTP request
		for i in range(len(get_lines)):
			line = get_lines[i]
			if(len(line) == 0): continue
			# Check that the first line is a valid HTTP request
			if(i == 0):
				line_data = line.split(" ", 3)
				# Check that the request is a GET request and that there are 3 arguments
				if(line_data[0] != "GET" or len(line_data) != 3):
					print("SERVER >> [ERROR]: Received an invalid GET request.")
					connection_socket.close()
					server_socket.close()
					sys.exit(1)
				# Store the request information into an associative array
				get_data["protocol"] = line_data[0]
				get_data["requested_file"] = line_data[1]
				get_data["http_version"] = line_data[2]
			else:
				# Parse the other lines after that into the same associative array
				line = line.replace(" ", "")
				line_data = line.split(":", 1)
				if(":" not in line or len(line_data) != 2):
					print("SERVER >> [ERROR]: Invalid header received.")
					print(get_message)
					connection_socket.close()
					server_socket.close()
					sys.exit(1)
				get_data[line_data[0]] = line_data[1]
		# Check that the requested file is the "stop" command
		if(str(get_data["requested_file"][1:]).lower() == "stop"):
			print("SERVER >> [STOP] Stop command received, shutting down...")
			connection_socket.close()
			server_socket.close()
			exit(0)
		# Try to open the requsted file (if it fails the IOError will catch it)
		file = open(get_data["requested_file"][1:], "r")
		outputdata = file.read()
		# Send HTTP response header with 200 OK message (request was successful)
		output_header = "HTTP/1.1 200 OK\r\nContent-Length: " + str(len(outputdata)) + "\r\nContent-Type: text/html\r\n\r\n"
		connection_socket.send(output_header.encode())
		# Send parts of requested file as fast as possible
		for i in range(0, len(outputdata)):
			connection_socket.send(outputdata[i].encode())
		connection_socket.send("\r\n".encode())
		# Close the connection after the file is sent
		connection_socket.close()
		print("SERVER >> [200 OK] Sent '" + str(get_data["requested_file"][1:]) + "'.")
	except IOError as e:
		# File was not found on the server, send a 404 response
		file = open("404.html", "r")
		outputdata = file.read()
		output_header = "HTTP/1.1 404 Not Found\r\nContent-Length: " + str(len(outputdata)) + "\r\nContent-Type: text/html\r\n\r\n"
		# Send 404 Not Found HTTP header
		connection_socket.send(output_header.encode())
		# Send 404 file
		for i in range(0, len(outputdata)):
			connection_socket.send(outputdata[i].encode())
		connection_socket.send("\r\n".encode())
		print("SERVER >> [404 Not Found] '" + str(get_data["requested_file"][1:]) + "' does not exist.")
		connection_socket.close()
	except KeyboardInterrupt:
		# Received keyboard interrupt, shut down server
		print("\r\nSERVER >> [INTERRUPT] Shutting down...")
		# Cleanup
		server_socket.close()
		sys.exit(0)
# Final cleanup
server_socket.close()
sys.exit()
