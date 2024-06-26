from socket import *
import sys
import cmd
import os


def status_check(status):
    """
    Checks the status of a file transfer and prints a corresponding message.

    Parameters:
        status (bool): The status of the file transfer. True if successful, False otherwise.
    """
    if status:
        print("File Transfer Success")
    else:
        print("File Transfer Failed")
    return None


def send_status(control_socket, status):
    """
    Sends the status of a file transfer over a control socket and prints the status message.

    Parameters:
        control_socket (socket): The control socket used for communication.
        status (bool): The status of the file transfer. True if successful, False otherwise.
    """
    control_socket.send(str(status).encode())
    status_check(status)


def rec_status(control_socket):
    """
    Receives the status of a file transfer from a control socket and prints the status message.

    Parameters:
        control_socket (socket): The control socket used for communication.
    """
    str_status = control_socket.recv(1024).decode()
    if str_status == "True":
       status_check(True)
    else:
        status_check(False)


def recvAll(sock, numBytes):
    """
    Receives a specified number of bytes from a socket.

    Parameters:
        sock (socket): The socket from which to receive data.
        numBytes (int): The number of bytes to receive.

    Returns:
        recvBuff (bytes): The received bytes.
    """
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
    """
    Sends file data over a data socket.

    Parameters:
        data_socket (socket): The socket used for data transmission.
        filename (str): The name of the file to send.
    """
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
    """
       Receives file data over a data socket.

       Parameters:
           data_socket (socket): The socket used for data transmission.
           filename (str): The name of the file to save the received data.
           save (bool): Whether to save the received data to a file.

       Returns:
           all_rec (bool): True if all data was received successfully, False otherwise.
       """
    all_rec = "False"
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
    if len(fileData) == fileSize:
        all_rec = "True"
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
    return all_rec
