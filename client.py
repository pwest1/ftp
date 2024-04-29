#----------------------- Client code----------------------
from socket import *
import sys
import cmd
import os

class FTP(cmd.Cmd):
    #function to put file in server
    def do_put(self, args):
        print(len(args))
        if len(args) == 1:
            command = "put"
            clientSocket.send(command.encode())


        else:
            print("Invalid command length")

    #functn to retrieve a file from the server
    def do_get(self, args):
        if len(args) == 1:
            command = "get"
            clientSocket.send(command.encode())

        else:
            print("Invalid command length")

    def do_ls(self, args):
        if not len(args) == 0:
            print('ls command does not take any arguments')
        else:
            command = "ls"
            clientSocket.send(command.encode())
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
# connection established message
print("Connection Established with server")

#create instance of FTP command interpreter
ftp_cli = FTP()
ftp_cli.prompt = 'ftp> '

ftp_cli.cmdloop('FTP Connection established')

# Close the socket
clientSocket.close()
