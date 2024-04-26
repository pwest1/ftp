# Server code
from socket import *
import sys #sys module for accessing cl arguments

if len(sys.argv) != 2:
    print("Error Invalid argument length")
    sys.exit(1)
# The port on which to listen
#extract port number from comand-line arguments
try:
    serverPort = int(sys.argv[1])
except ValueError:
    print("Port number must be an integer")
    sys.exit(1)

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

    # The temporary buffer
    tmpBuff = ""
    data = ""
    while len(data) != 40:
        # Receive whatever the newly connected client has to send
        tmpBuff = connectionSocket.recv(40)

        # The other side unexpectedly closed its socket
        if not tmpBuff:
            break

        # Save the data
        data += tmpBuff.decode()

    print(data)

    # Close the socket
    connectionSocket.close()
