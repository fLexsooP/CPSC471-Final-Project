import socket
import sys

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
port = int(sys.argv[2])  # Get port number from command line arguments
server_machine = sys.argv[1]  # Get server machine from command line arguments

# Define buffer size
BUFFER_SIZE = 1024

# Connect to the server on local computer
s.connect((server_machine, port))

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

        filename = command[4:]
        with open(filename, 'wb') as f:
            f.write(buffer)
    elif command.startswith('put '):
        # Send file to the server
        filename = command[4:]
        try:
            with open(filename, 'rb') as f:
                s.send(f.read())
        except FileNotFoundError:
            print('File not found.')

# Close the connection
s.close()