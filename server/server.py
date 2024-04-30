# -------------------- Server code--------------------
from socket import *
import sys  # sys module for accessing cl arguments
sys.path.append("..")
import threading
import os
from helper import rec_file_data, recvAll, send_file_data


def establish_data_connection(connection_socket):
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.bind(('', 0))
    data_socket.listen(1)
    data_port = data_socket.getsockname()[1]
    connection_socket.send(str(data_port).encode())
    data_conn, _ = data_socket.accept()
    print("Data Channel Opened")

    return data_conn


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
            send_file_data(dataSocket, filename)

        elif command == 'put':
            filename = connectionSocket.recv(1024).decode()
            dataSocket = establish_data_connection(connectionSocket)
            rec_file_data(dataSocket, filename)


        elif command == 'ls':
            dataSocket = establish_data_connection(connectionSocket)
            files = os.listdir()
            with open("file_list.txt", "w") as file:
                file.write("\n".join(files))
            #file_data = "\n".join(files).encode()
            send_file_data(dataSocket, "file_list.txt")
            os.remove("file_list.txt")

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
