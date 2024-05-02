# ----------------------- Client code----------------------
from socket import *
import sys

sys.path.append("..")
import cmd
from helper import rec_file_data, recvAll, send_file_data, status_check, send_status, rec_status
import os




def establish_data_connection(clientSocket):
    """
       Establishes a data connection with the server.

       This function receives the data port number from the clientSocket,
       creates a new socket (data_socket), and connects it to the server using the received port number.

       Parameters:
           clientSocket (socket): A socket connected to the server used for communication.

       Returns:
           data_socket (socket): A new socket connected to the server's data port for data transmission.
    """
    data_port = int(clientSocket.recv(1024).decode())
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.connect((serverName, data_port))
    print("Client Data Channel Opened")
    return data_socket


class FTP(cmd.Cmd):
    """
    Class: FTP

    Description:
        A command-line interface for interacting with an FTP server. Supports commands to upload ("put"),
        download ("get"), list directory contents ("ls"), and quit the connection ("quit").

    Methods:
        do_put(self, args):
            Uploads a file to the server. Requires a file argument.

        do_get(self, args):
            Downloads a file from the server. Requires a file argument.

        do_ls(self, args):
            Lists directory contents on the server. Does not take any arguments.

        do_quit(self, args):
            Closes the connection with the server and exits the FTP client.

    """
    def do_put(self, args):
        """
        Uploads a file to the server. Requires a file argument.
        """
        if len(args) > 0:
            command = "put"
            filename = args
            clientSocket.send(command.encode())
            clientSocket.send(filename.encode())
            data_socket = establish_data_connection(clientSocket)
            send_file_data(data_socket, filename)
            rec_status(clientSocket)

        else:
            print("Put command requires file argument")

    # function to retrieve a file from the server
    def do_get(self, args):
        """
        Downloads a file from the server. Requires a file argument.
        """
        if len(args) > 0:
            command = "get"
            filename = args
            clientSocket.send(command.encode())
            clientSocket.send(filename.encode())
            data_socket = establish_data_connection(clientSocket)
            status = rec_file_data(data_socket, filename)
            send_status(clientSocket, status)


        else:
            print("Get Command requires file argument")

    def do_ls(self, args):
        """
        Lists directory contents on the server. Does not take any arguments.
        """
        if not len(args) == 0:
            print('ls command does not take any arguments')
        else:
            command = "ls"
            clientSocket.send(command.encode())
            data_socket = establish_data_connection(clientSocket)
            rec_file_data(data_socket, "ls", False)

    def do_quit(self, args):
        """
        Closes the connection with the server and exits the FTP client.
        """
        data = "quit"
        clientSocket.send(data.encode())
        clientSocket.close()
        print("Connection Closed.")
        return True


#----------Main Client Code -------------------
if len(sys.argv) != 3:
    print("Please provide the correct format: client.py <Address> <Port_Number>")
    sys.exit(1)

# extract port number from comand-line arguments
try:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
except ValueError:
    print("Port number must be an integer")
    sys.exit(1)

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
