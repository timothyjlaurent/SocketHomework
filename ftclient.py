from socket import *
import sys
import os
# by Timothy Laurent
# Networking
# 8-13-2013

# usage : python ftclient.py
## Ft client initiates a ftclient object whick creates the
# conncetion socket and connects to the server.
# Upon connection, the client calls listenDataSocket() to open a 
# dsock datasocket class attribute listening on the dataport, 30020, and then sends
# the 'ready' signal to the server. The client calls a commandSession() logic
# method in a forever loop. In the commandSession, the user is prompted
# to input a command. The possible commands are 'list', 'get <file>', or quit.
# The client send all entered commends to the server and displays the server's
# response. If the response is 'quit' the client closes the sockets and 
# quits. If the recieves the "getting <filename> size x" string, the client send a confirmation 
# message "transfer" and then copys the file from the sdata socket to the current directory. 
# if the there is another file by that name in the dircectory, the user will be 
# asked whether to overwrite or cancel the transfer.



class ftclient:
	'''This client makes a command connection to 
	the server host and displays the messages sent 
	back by the server. If it detects a file size argument
	the client listens on a port and saves the incoming file
	'''

	def __init__(self, addr='localhost', port= 30021 ):
		'''Connects to server then sets up a listening 
		socket for the data connection before signalling
		to the server that it is ready to initialize the data
		connection
		'''
		self.commSocket  =socket(AF_INET, SOCK_STREAM)
		self.commSocket.connect((addr, port))
		self.listenDataSocket()
		self.commSocket.send("ready")
		self.dsock, self.daddr = self.dlsock.accept()
		self.connection = 1
		while self.connection == 1:
			self.commandSession();

	def listenDataSocket(self, port = 30020):
		'''opens a listening socket
		'''
		self.dlsock = socket(AF_INET, SOCK_STREAM)
		self.dlsock.bind(('', port))
		self.dlsock.listen(1)
		
	def commandSession(self):
		'''this is the command session interface
		'''
		comm = raw_input('Enter Command\n>')
		if comm == "":
			comm = "emptyString" 

		self.commSocket.send(comm)
		if self.connection ==1 :
			resp = self.commSocket.recv(4096)
		# print "resp " + resp
		if resp == "quit":
			self.commSocket.close()
			self.connection = 0
			self.dsock.close()
			print "connection closed"
			sys.exit()
		
		elif len(resp) > 1 and resp.split()[0] == "Getting" and resp.split()[2] == "size":
			# print 'from server:', resp
			self.commSocket.send("transfer")
			file = resp.split()[1]
			# print "file\t"+file
			size = resp.split()[3]
			# print "size\t"+ str(size)
			self.receiveFile(file , size)
		else:
			print resp
		


	def receiveFile ( self , file, size):
		'''this recieves the file and checks for file duplication 
		allowin the user to cancel duplicate saves
		'''
		print "ready to receive file"
		msg = ''
		size = int(size)
		while len(msg) < size:
			chunk = self.dsock.recv(size-len(msg))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			msg = msg + chunk
		# print msg
		if os.path.isfile(file):
			res= raw_input(file + " exists. Overwrite??\n\n(y/n):  ")
			if res != 'y':
				print "Cancelled file save"
				return
			with open(file, 'w') as out:
				out.write(msg)
			print "Transfer Complete!!!"

if __name__=="__main__":
	client = ftclient()