from socket import *
import sys

class ftclient:
	'''This client makes a command connection to 
	the server host and displays the messages sent 
	back by the server. If it detects a file size argument
	the client listens on a port and saves the incoming file
	'''

	def __init__(self, addr='localhost', port= 30021 ):
		self.commSocket  =socket(AF_INET, SOCK_STREAM)
		self.commSocket.connect((addr, port))
		self.commandSession();

	def commandSession(self):
		# while(1):
		while self.commSocket:
			comm = raw_input('Enter Command\n>')
			self.commSocket.send(comm)
			resp = self.commSocket.recv(4096)
			if resp == "quit":
				self.commSocket.close()
				self.commSocket = 0
				print "connection closed"
				# sys.exit()
			elif resp.split()[0] == "incomingFileSize":
				print 'from server:', resp
			else:
				print resp

	def openTransferSocket( self, size, port,file ):
		self.transferSocket = socket(AF_INET, SOCK_STREAM)
		self.transferSocket.bind(("", port))
		self.transferSocket.listen(1)
		print "ready to receive file"
		msg = ''
		while len(msg) < size:
			chunk = self.sock.recv(size-len(msg))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			msg = msg + chunk


if __name__=="__main__":
	client = ftclient()