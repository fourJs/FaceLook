import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.34.189', 5000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(10)

# Wait for a connection
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

data = ""

# try:

print >>sys.stderr, 'connection from', client_address

    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(16)
        print >>sys.stderr, 'received "%s"' % data

        # if data:
        #     print >>sys.stderr, 'sending data back to the client'
            # reply = "I got it"
            # connection.sendall(reply)
        # else:
            # print >>sys.stderr, 'no more data from', client_address
            # break

    # except Exception as e:
    #     pass       

# Clean up the connection
connection.close()