import socket
import sys
import os


def send_data(socket, data):
    # get the size of the data as a header
    size_header = str(len(data))

    # prepend 0's to the size string
    # until the size is 10 bytes
    while len(size_header) < 10:
        size_header = "0" + size_header

    # prepend the size of the data to the file data
    data = size_header + data.decode('utf-8')
    data = data.encode('utf-8')
    # the number of bytes sent
    numSent = 0

    # send the data
    while len(data) > numSent:
        numSent += socket.send(data[numSent:])


def receive_data(socket):
    # Receive the size header (first 10 bytes)
    size_header = socket.recv(10).decode('utf-8')

    # Convert the size header to an integer
    data_size = int(size_header)

    recvBuff = ""
    tmpBuff = ""

    # keep receiving till all is received
    while len(recvBuff) < data_size:
        # attempt to receive bytes
        tmpBuff = socket.recv(data_size).decode('utf-8')

        # the other side has closed the socket
        if not tmpBuff:
            break
        # add the received bytes to the buffer
        recvBuff += tmpBuff

    return recvBuff
