# Client code
from socket import *
import sys

if len(sys.argv) != 2:
    print("Error Invalid argument length")
    sys.exit(1)
# The port on which to listen
#extract port number from comand-line arguments
try:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
except ValueError:
    print("Port number must be an integer")
    sys.exit(1)
# Name and port number of the server to which want to connect.


# Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
clientSocket.connect((serverName, serverPort))

# A string we want to send to the server
data = "Hello world! This is a very long string."

bytesSent = 0

# Keep sending bytes until all bytes are sent
while bytesSent != len(data):
    # Send that string!
    bytesSent += clientSocket.send(data.encode())

# Close the socket
clientSocket.close()
