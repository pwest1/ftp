# -------------------- Server code--------------------
from socket import *
import sys  # sys module for accessing cl arguments
import threading
import os


def recvAll(sock, numBytes):
    # The buffer
    recvBuff = ""
    # The temporary buffer
    tmpBuff = ""
    # Keep receiving till all is received
    while len(recvBuff) < numBytes:
        # Attempt to receive bytes
        tmpBuff = sock.recv(numBytes)
        # The other side has closed the socket
        if not tmpBuff:
            break
        # Add the received bytes to the buffer
        recvBuff += tmpBuff
    return recvBuff


def establish_data_connection(connection_socket):
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.bind(('', 0))
    data_socket.listen(1)
    connection_socket.send(str(data_socket.getsockname()[1]).encode())
    print("Data Channel Opened")
    return data_socket


# function to handle client connection

def handle_client_connection(connectionSocket):
    print("Connecting to client")
    while True:
        command = connectionSocket.recv(1024).decode()
        if not command:
            break
        if command == 'get':
            filename = connectionSocket.recv(1024).decode()
            dataSocket = establish_data_connection(connectionSocket)

        elif command == 'put':
            filename = connectionSocket.recv(1024).decode()
            dataSocket = establish_data_connection(connectionSocket)
            fileData = ""
            # The temporary buffer to store the received
            # data.
            recvBuff = ""
            # The size of the incoming file
            fileSize = 0
            # The buffer containing the file size
            fileSizeBuff = ""
            # Receive the first 10 bytes indicating the
            # size of the file
            fileSizeBuff = recvAll(dataSocket, 10)
            # Get the file size
            fileSize = int(fileSizeBuff)
            print("The file size is ", fileSize)
            # Get the file data
            fileData = recvAll(dataSocket, fileSize)
            print("The file data is: ")
            print(fileData)
            # Close our side
            dataSocket.close()

        elif command == 'ls':
            dataSocket = establish_data_connection(connectionSocket)
            files = "\n".join(os.listdir())
            dataSocket.send(files.encode())

        elif command == 'quit':
            print("Closing client connection")
            break
        else:
            print("Invalid Command")
            break
    connectionSocket.close()


# -------------main server code ------------------------------
if len(sys.argv) != 2:
    print("Error Invalid argument length")
    sys.exit(1)
if not sys.argv[1].isdigit():
    print("Port number must be an integer")
    sys.exit()

# The port on which to listen
# extract port number from comand-line arguments
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
