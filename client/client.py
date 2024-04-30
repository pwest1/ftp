# ----------------------- Client code----------------------
from socket import *
import sys
sys.path.append("..")
import cmd
from helper import rec_file_data, recvAll, send_file_data
import os


def establish_data_connection(clientSocket):
    data_port = int(clientSocket.recv(1024).decode())
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.connect((serverName, data_port))
    print("Client Data Channel Opened")
    return data_socket


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
            rec_file_data(data_socket, "ls", False)

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
