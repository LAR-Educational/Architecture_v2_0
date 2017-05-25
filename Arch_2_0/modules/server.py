import socket
import sys
import emotion
from thread import *

class Server(object):
	def __init__(self, host='localhost', port=12345):
		self.host = host
		self.port = port
		
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as msg:
			print('Failed to create socket. Error code: ' + str(msg[0]) + ', Error message: ' + msg[1])
			sys.exit()
		print('Socket Created')
	
		try:
			self.sock.bind((host, port))
		except socket.error as e:
			print(str(e))
			sys.exit()
		
		self.sock.listen(5)

		self.start()

	# Method that implements a client-server connection
	def threaded_client(self, conn, data_number):	
		while True:
			data = conn.recv(2048)
	
			filetype = data[0:3].decode()
			data = data[4:].decode()
	
			if data:
				if(filetype == 'msg'):
					print(data)
					if(data == 'end of part'):
						emotion.command = 'write'
						conn.send('Data successfuly stored')
					if(data == 'end of execution'):
						emotion.command = 'end'
						conn.send('end')
					else:
						conn.send(data)


				elif(filetype == 'txt'):
					file = open(str(data_number)+'.txt', 'wb')
					file.write(data.encode())
					file.close()
					conn.send('Data received and succesfully stored')
				else:
					conn.send('Failed to store/receive data')
					break
				
				data_number = data_number + 1
		conn.close()
	
	# Initializes the server (called on init)
	def start(self):
		data_number = 0
		
		while True:
			conn, addr = self.sock.accept()
			print('connected to: ' + addr[0] + ' : ' + str(addr[1]))
			
			#runs the server a different thread for each client connectedss
			start_new_thread(self.threaded_client,(conn,data_number))
