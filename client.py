import socket
import sys
import os

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
port = int(sys.argv[2])  # Get port number from command line arguments
server_machine = sys.argv[1]  # Get server machine from command line arguments

# Define buffer size
BUFFER_SIZE = 1024

# Connect to the server on local computer
s.connect((server_machine, port))

def data_client(s):
    dataPort = s.recv(BUFFER_SIZE).decode('utf-8')
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSocket.connect((server_machine, int(dataPort)))

    return dataSocket

def send_data(socket, data): 
    #get the size of the data as a header
    size_header = str(len(data))

    #prepend 0's to the size string
    #until the size is 10 bytes
    while len(size_header) < 10: 
        size_header = "0" + size_header
    
    #prepend the size of the data to the file data
    data = size_header + data.decode('utf-8')
    data = data.encode('utf-8')
    #the number of bytes sent
    numSent = 0

    #send the data
    while len(data) >  numSent: 
        numSent += socket.send(data[numSent:])

def receive_data(socket):
    #Receive the size header (first 10 bytes)
    size_header = socket.recv(10).decode('utf-8')

    #Convert the size header to an integer
    data_size = int(size_header)

    recvBuff = ""
    tmpBuff = ""

    #keep receiving till all is received
    while len(recvBuff) < data_size:
        #attempt to receive bytes
        tmpBuff = socket.recv(data_size).decode('utf-8')

        #the other side has closed the socket
        if not tmpBuff:
            break
        #add the received bytes to the buffer
        recvBuff += tmpBuff
    
    return recvBuff


while True:
    # Print ftp prompt
    command = input('ftp> ')
    if not command:
        continue
    s.send(command.encode('utf-8'))
    if command == 'quit':
        break  # Disconnect from the server
    elif command == 'ls':
        # List files on the server
        print(s.recv(BUFFER_SIZE).decode('utf-8'))
    elif command.startswith('get '):
        # Receive file from the server
        buffer = s.recv(BUFFER_SIZE)
        if buffer == b'File not found':
            print("File not found on server.")
            continue
        dataSocket = data_client(s)
        filename = command[4:]
        with open(filename, 'wb') as f:
            print('Receiving file!')
            f.write(receive_data(dataSocket).encode('utf-8'))
        print("File: " + filename + "\nSize (in bytes): " + str(os.stat(filename).st_size))
    elif command.startswith('put '):
        # Send file to the server
        filename = command[4:]
        fileData = ""
        try:
            with open(filename, 'rb') as f:
                fileData = f.read()
                s.send(b"File found!")
        except FileNotFoundError:
            print('File not found.')
            s.send(b"File not found")
            continue
        print("File: " + filename + "\nSize (in bytes): " + str(os.stat(filename).st_size))
        dataSocket = data_client(s)
        # dataSocket.send(fileData)
        # dataSocket.close
        send_data(dataSocket, fileData)

# Close the connection
s.close()
