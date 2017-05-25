import socket
import time
import sys
import cv2
import settings
import emotion
import disatention
from thread import *

class Client(object):
	def __init__(self, host='localhost', port=12345):
		self.host = host
		self.port = port
		self.max_retries = 10
		self.retries = 0
		
		while True:
			try:
				self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				break
			except socket.error as msg:
				settings.info('Client failed to create socket. Error code: ' + str(msg[0]) + ', Error message: ' + msg[1], 1)
				if(self.retries < self.max_retries):
					self.retries += 1
				else:
					emotion.setCommand('end')
					disatention.desv_end('sair')
					sys.exit()
				time.sleep(2)
				settings.info("Retrying connection")
				pass
		settings.info('Client socket Created')
		
		self.retries = 0
		while True:
			try:
				remote_ip = socket.gethostbyname(self.host)
				break
			except socket.gaiaerror:
				settings.info('Client hostname could not be resolved. Exiting', 3)
				if(self.retries < self.max_retries):
					self.retries += 1
				else:
					emotion.setCommand('end')
					disatention.desv_end('sair')
					sys.exit()
				time.sleep(2)
				settings.info("Retrying connection")
				pass	
		settings.info('Client: IP address of ' + self.host + ' is '+ remote_ip)
	
		self.retries = 0
		while True:
			try:
				self.sock.connect((remote_ip, port))
				break
			except socket.error as msg:
				settings.info('Client failed to connect to server. Error code: ' + str(msg[0]) + ', Error message: ' + msg[1], 1)
				if(self.retries < self.max_retries):
					self.retries += 1
				else:
					emotion.setCommand('end')
					disatention.desv_end('sair')
					sys.exit()
				time.sleep(2)
				settings.info("Retrying connection")
				pass
		settings.info('Client socket connected to ' + host + ' on IP '+ remote_ip)
	
	# Method that sends messages from client to server
	def sendMessage(self, message):
		try:
			self.sock.sendall(message.encode())
			data = self.sock.recv(2048)
			settings.info('Client ' + data.decode())
		except socket.error as msg:
			settings.info('Client send failed. Error code: ' + str(msg[0]) + '. Error message: ' + msg[1] + '\n', 1)

		return data.encode()
