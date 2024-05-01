# Project Name: TCP Client-Server File Transfer

## Description
TCP Client-Server File Transfer is a project implementing a client-server architecture for transferring files over sockets. It comprises two main components: a client and a server, communicating via a control channel and a data channel.

## Students
- Junhao Guo
- Nhi Danis
- Alvaro Samayoa
- Peter West
- Steven Delgado

## Programming Language
Python

## Execution Instructions

### Server
1. Open a terminal.
2. Navigate to the directory containing the `server.py` file.
3. Run the following command to start the server:
    ```bash
    python server.py <port>
    ```
   Replace `<port>` with the desired port number (e.g., 12345).

### Client
1. Open another terminal.
2. Navigate to the directory containing the `client.py` file.
3. Run the following command to start the client:
    ```bash
    python client.py <server_address> <port>
    ```
   Replace `<server_address>` with the IP address or hostname of the server, and `<port>` with the port number on which the server is listening.

## Available Commands (Client)
- `put <filename>`: Upload a file to the server.
- `get <filename>`: Download a file from the server.
- `ls`: List files on the server.
- `quit`: Disconnect from the server and exit the client.

## Special Notes
- The project utilizes TCP/IP sockets for communication.
- The control channel handles command/response messages.
- The data channel is responsible for transferring file data.
- Ensure that both client and server are running on compatible systems with network connectivity.

## Diagram
![FTP Diagram](FTP.drawio.png)
