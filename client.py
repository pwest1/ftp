# ----------------------- Client code----------------------
from socket import *
import sys
import cmd
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
def establish_data_connection(clientSocket):
    data_port = int(clientSocket.recv(1024).decode())
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.connect(serverName, data_port)
    print("Client Data Channel Opened")
    return data_socket


def send_file_data(data_socket, filename="NA"):
    file_obj = open(filename, "r")
    # The number of bytes sent
    num_sent = 0
    # The file data
    file_data = None
    # Keep sending until all is sent
    while True:
        # Read 65536 bytes of data
        file_data = file_obj.read(65536)
        # Make sure we did not hit EOF
        if file_data:
            # Get the size of the data read
            # and convert it to string
            data_size_str = str(len(file_data))
            # Prepend 0's to the size string
            # until the size is 10 bytes
            while len(data_size_str) < 10:
                data_size_str = "0" + data_size_str
            # Prepend the size of the data to the
            # file data.
            file_data = data_size_str + file_data
            # The number of bytes sent
            num_sent = 0
            # Send the data!
            while len(file_data) > num_sent:
                num_sent += data_socket.send(file_data[num_sent:])
        # The file has been read. We are done
        else:
            break
    print("Sent ", num_sent, " bytes.")
    # Close the socket and the file
    data_socket.close()
    file_obj.close()


def rec_file_data(data_socket, filename="NA"):
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
    fileSizeBuff = recvAll(data_socket, 10)
    # Get the file size
    fileSize = int(fileSizeBuff)
    print("The file size is ", fileSize)
    # Get the file data
    fileData = recvAll(data_socket, fileSize)
    if not filename == "NA":
        with open(filename, "wb") as file:
            file.write(fileData)
    else:
        print("The file data is: ")
        print(fileData)
    # Close our side
    data_socket.close()


class FTP(cmd.Cmd):
    # function to put file in server
    def do_put(self, args):
        if len(args) > 0:
            command = "put"
            filename = args
            clientSocket.send(command.encode())
            clientSocket.send(filename.encode())
            data_socket = establish_data_connection(clientSocket)
            send_file_data(data_socket, filename)


        else:
            print("Invalid command length")

    # functn to retrieve a file from the server
    def do_get(self, args):
        if len(args) > 0:
            command = "get"
            filename = args
            clientSocket.send(command.encode())
            clientSocket.send(filename.encode())
            data_socket = establish_data_connection(clientSocket)
            rec_file_data(data_socket, filename)

        else:
            print("Invalid command length")

    def do_ls(self, args):
        if not len(args) == 0:
            print('ls command does not take any arguments')
        else:
            command = "ls"
            clientSocket.send(command.encode())
            data_socket = establish_data_connection(clientSocket)
            rec_file_data(data_socket)

    def do_quit(self, args):
        data = "quit"
        clientSocket.send(data.encode())
        clientSocket.close()
        print("Connection Closed.")
        return True


if len(sys.argv) != 3:
    print("Error Invalid argument length")
    sys.exit(1)
# The port on which to listen

# extract port number from comand-line arguments
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
# connection established message
print("Connection Established with server")

# create instance of FTP command interpreter
ftp_cli = FTP()
ftp_cli.prompt = 'ftp> '

ftp_cli.cmdloop('FTP Connection established')

# Close the socket
clientSocket.close()
