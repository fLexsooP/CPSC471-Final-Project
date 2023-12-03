import socket
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), './utils'))
from ftp import send_data, receive_data

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


while True:
    # Print ftp prompt
    command = input('ftp> ')
    if not command:
        continue
    s.send(command.encode('utf-8'))
    if command == 'quit':
        print(s.recv(BUFFER_SIZE).decode('utf-8'))
        break  # Disconnect from the server
    elif command == 'ls':
        # List files on the server
        print(s.recv(BUFFER_SIZE).decode('utf-8'))
    elif command.startswith('get '):
        # Receive file from the server
        buffer = s.recv(BUFFER_SIZE)
        # Check if there is a file
        if buffer.startswith(b'550'):
            print(buffer.decode('utf-8'))
            continue
        # Get file and store
        dataSocket = data_client(s)
        filename = command[4:]
        with open(filename, 'wb') as f:
            print(buffer.decode('utf-8'))
            f.write(receive_data(dataSocket).encode('utf-8'))
        # Wait for tranfer complete
        buffer = s.recv(BUFFER_SIZE)
        print(buffer.decode('utf-8'))
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
