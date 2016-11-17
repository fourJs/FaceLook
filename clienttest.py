import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('192.168.33.237', 1234)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
data = " "
while True:
    try:
        
        # Send data
        message = 'This is the message.  It will be repeated.'
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)       
        while data!="I got it":
            data = sock.recv(8) 
            print >>sys.stderr, 'received "%s"' % data
    except Exception as e:
        pass

    data = ""
print >>sys.stderr, 'closing socket'
sock.close()
