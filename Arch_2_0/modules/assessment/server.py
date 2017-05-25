from thread import *
import socket
import time
import sys

import emotion
import disatention
import settings

isRunning = True

class Server(object):
	def __init__(self, host='localhost', port=12345):
		self.host = host
		self.port = port
		self.max_retries = 5
		self.retries = 0

		while True:
			try:
				self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				break
			except socket.error as msg:
				settings.info('Server failed to create socket. Error code: ' + str(msg[0]) + '. Error message: ' + msg[1] + '\n', 2)
				if(self.retries < self.max_retries):
					self.retries += 1
				else:
					emotion.setCommand('end')
					disatention.desv_end('sair')
					sys.exit()
				time.sleep(4)
				settings.info("Retrying connection")
				pass
		settings.info('Server socket Created\n')
	
		try:
			self.sock.bind((host, port))
		except socket.error as e:
			settings.info(str(e), 2)
			sys.exit()
		
		self.sock.listen(5)

		self.start()

	# Method that implements a client-server connection
	def threaded_client(self, conn, data_number):	
		global isRunning
		while isRunning:
			data = conn.recv(2048).decode()

			if data:
				settings.info("Server received: " + data)
				if(data == 'end of part'):
					emotion.setCommand('write')
					conn.send('Data successfuly stored\n')
				elif(data == 'end of execution'):
					emotion.setCommand('end')
					disatention.desv_end('sair')
					conn.send('end')
					isRunning = False
					settings.info('Server: Finishing execution')
				else:
					conn.send('Failed to store/receive data\n')
					settings.info('Server: Failed to store/receive data', 1)
					isRunning = False
				data_number += 1
		conn.close()
	
	# Initializes the server (called on init)
	def start(self):
		global isRunning
		data_number = 0
		
		while True:
			conn, addr = self.sock.accept()
			settings.info('Server connected to: ' + addr[0] + ' : ' + str(addr[1]))

			#runs the server a different thread for each client connectedss
			start_new_thread(self.threaded_client,(conn,data_number))
			exit()
			break
		self.sock.close()
		settings.info('Server closed')
