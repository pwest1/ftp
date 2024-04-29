#-------------------- Server code--------------------
from socket import *
import sys #sys module for accessing cl arguments
import threading
import os

#function to handle client connection
def handle_client_connection(connectionSocket):
    print("Connecting to client")
    while True:
        command = connectionSocket.recv(1024).decode()
        if not command:
            break
        if command == 'get':
            print('get')
        elif command == 'put':
            print('put')
        elif command == 'ls':
            print('ls')
        elif command == 'quit':
            print("Closing client connection")
            break
        else:
            print("Invalid Command")
            break
    connectionSocket.close()
#function to handle get command
def get(connectionSocket):
    return True
#function to handle put command
def put(connectionSocket):
    return True
#function to handle ls command
def ls(connectionSocket):
    return True
#-------------main server code ------------------------------
if len(sys.argv) != 2:
    print("Error Invalid argument length")
    sys.exit(1)
if not sys.argv[1].isdigit():
    print("Port number must be an integer")
    sys.exit()

# The port on which to listen
#extract port number from comand-line arguments
else:
    serverPort = int(sys.argv[1])

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the port
serverSocket.bind(('', serverPort))

# Start listening for incoming connections
serverSocket.listen(1)

print("The server is ready to receive")

# Forever accept incoming connections
while True:
    # Accept a connection; get client's socket
    connectionSocket, addr = serverSocket.accept()
    client_thread = threading.Thread(target=handle_client_connection, args=(connectionSocket,))
    client_thread.start()

