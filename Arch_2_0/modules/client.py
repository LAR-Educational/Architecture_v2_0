import socket
import sys
import cv2
from thread import *

class Client(object):
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
			remote_ip = socket.gethostbyname(self.host)
		except socket.gaiaerror:
			print('Hostname could not be resolved. Exiting')
			sys.exit()
		print('Ip address of ' + self.host + ' is '+ remote_ip)
	
		self.sock.connect((remote_ip, port))
		print('Socket connected to ' + host + ' on ip '+ remote_ip)
	
	# Method that sends messages from client to server
	def send_message(self, message):
		try:
			self.sock.sendall(message.encode())
			data = self.sock.recv(2048)
		except socket.error:
			print('Failed')
		
		self.sock.close()
		
		return data.encode()
	
	# Method that sends a .txt file from client to server
	def send_txt(self, txt):
		try:
			self.sock.sendall(text.encode())
			data = self.sock.recv(2048)
		except socket.error:
			print('Failed')
		
		self.sock.close()
		
		return data.encode()
