import socket
import sys
import subprocess
import os


# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
port = int(sys.argv[1])  # Get port number from command line arguments

# Define buffer size
BUFFER_SIZE = 1024

# Bind to the port
s.bind(('', port))

# Put the socket into listening mode
s.listen(5)
print('Server is listening on port:', port)

def data_server(c):
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSocket.bind(('', 0))
    c.send(str(dataSocket.getsockname()[1]).encode('utf-8'))
    dataSocket.listen(5)
    accptedSocket, dataAddr = dataSocket.accept()

    return accptedSocket

def send_data(socket, data): 
    #get the size of the data as a header
    size_header = str(len(data))

    #prepend 0's to the size string
    #until the size is 10 bytes
    while len(size_header) < 10: 
        size_header = "0" + size_header
    #prepend the size of the data to the file data
    data = size_header + data

    #the number of bytes sent
    numSent = 0

    #send the data
    while len(data) >  numSent: 
        numSent += socket.send(fileData[numSent:])

def receive_data(socket, numBytes):
    recvBuff = ""
    tmpBuff = ""

    #keep receiving till all is received
    while len(recvBuff) < numBytes:
        #attempt to receive bytes
        tmpBuff = sock.recv(numBytes)
        #the other side has closed the socket
        if not tmpBuff:
            break
        #add the received bytes to the buffer
        recvBuff += tmpBuff
    
    return recvBuff

# A forever loop until we interrupt it or an error occurs
while True:
    # Establish connection with client
    c, addr = s.accept()
    print('Got connection from', addr)

    while True:
        # Receive command from the client
        command = c.recv(BUFFER_SIZE).decode('utf-8')
        if not command:
            break  # Client has disconnected
        elif command == 'ls':
            # List files on the server
            files = os.listdir()
            c.send('\n'.join(files).encode('utf-8'))
        elif command.startswith('get '):
            # Send file to the client
            filename = command[4:]
            fileData = ""
            try:
                with open(filename, 'rb') as f:
                    fileData = f.read()
                    c.send(b'File ok!')
            except FileNotFoundError:
                c.send(b'File not found')
                continue
            dataSender = data_server(c)
            dataSender.send(fileData)
        elif command.startswith('put '):
            # Receive file from the client
            buffer = c.recv(BUFFER_SIZE)
            print(buffer)
            if buffer == b'File not found':
                continue
            dataReciever = data_server(c)
            filename = command[4:]
            with open(filename, 'wb') as f:
                print('Recieving file!')
                f.write(dataReciever.recv(BUFFER_SIZE))
            dataReciever.close
        elif command == 'quit':
            break  # Client has requested to disconnect

    # Close the connection with the client
    c.close()
