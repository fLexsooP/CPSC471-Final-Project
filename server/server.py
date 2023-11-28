import socket
import sys
import subprocess


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
            files = subprocess.getstatusoutput('ls -l')
            c.send('\n'.join(files[1:]).encode('utf-8'))
        elif command.startswith('get '):
            # Send file to the client
            filename = command[4:]
            try:
                with open(filename, 'rb') as f:
                    c.send(f.read())
            except FileNotFoundError:
                c.send(b'File not found')
        elif command.startswith('put '):
            # Receive file from the client
            filename = command[4:]
            with open(filename, 'wb') as f:
                f.write(c.recv(BUFFER_SIZE))
        elif command == 'quit':
            break  # Client has requested to disconnect

    # Close the connection with the client
    c.close()