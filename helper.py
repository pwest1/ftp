from socket import *
import sys
import cmd
import os

def recvAll(sock, numBytes):
    # The buffer
    recvBuff = b""
    # The temporary buffer
    tmpBuff = ""
    # Keep receiving till all is received
    while len(recvBuff) < numBytes:
        # Attempt to receive bytes
        tmpBuff = sock.recv(numBytes - len(recvBuff))
        # The other side has closed the socket
        if not tmpBuff:
            break
        # Add the received bytes to the buffer
        recvBuff += tmpBuff
    return recvBuff

def send_file_data(data_socket, filename="NA"):
    file_obj = open(filename, "rb")
    # The number of bytes sent
    num_sent = 0
    # The file data
    file_data = None
    # Keep sending until all is sent
    while True:
        # Read 65536 bytes of data
        file_data = file_obj.read()
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
            file_data = (data_size_str.encode() + file_data)
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


def rec_file_data(data_socket, filename="NA", save=True):
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
    if save:
        # Save the file to the current directory with the specified filename
        with open(filename, "wb") as file:
            file.write(fileData)
    else:
        # Print the file data
        print("Directory: ")
        print(fileData.decode())

    # Close our side
    data_socket.close()