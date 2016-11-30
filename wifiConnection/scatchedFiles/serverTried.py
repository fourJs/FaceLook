import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.32.132', 1234)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


### new
data = ""
payload_size = struct.calcsize("H") 
while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()

	try:
		print >>sys.stderr, 'connection from', client_address

		# Receive the data in small chunks and retransmit it
		while True:
			while len(data) < payload_size:
					# data += conn.recv(4096)
					data += conn.recv(40)

			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack("H", packed_msg_size)[0]
			while len(data) < msg_size:
				# data += conn.recv(4096)
				print conn.recv(40)
				data += conn.recv(40)

			frame_data = data[:msg_size]
			data = data[msg_size:]
			###

			frame=pickle.loads(frame_data)
			print frame
			# cv2.imshow('frame',frame)		    
			# k = cv2.waitKey(1)
			# if k == ord('q'):
			# 	runFlag = False
			# 	cv2.destroyAllWindows()

			# # print >>sys.stderr, 'received "%s"' % data
			# if data:
			# #     print >>sys.stderr, 'sending data back to the client'
			# 	reply = "I got it"
			# 	connection.sendall(reply)
			# else:
			# 	print >>sys.stderr, 'no more data from', client_address
			# 	break
	except Exception as e:
		pass       

# Clean up the connection
connection.close()