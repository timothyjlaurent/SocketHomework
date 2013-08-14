from socket import *
import os
# by Timothy Laurent
# Networking
# 8-13-2013

# usage: python ftserve.py 
# this program starts and initiates witht he creation of a listenSocket object listening on port 30021,
# when the remoteclient connects a commSocket object is created of for the new connection,
# the server waits on a "ready" signal from 
# the client, indicating that the client is listening on the data socket 30020
# The server then creates a new datasocket object socket to the client.
# The server waits for command on the comm socket and responds with the 
# different methods list(), errorMsg(), and get(); get() calls the 
# dataSocket push() command to read and send the file. Gets waits on confirmation
# before sending the file. If the server gets the quit command the commSocket Class __init__
# is returned from which returns the server to waitin for another connection.
# code for thei project adapted from the code examples in the lecture and from 
# the Python socket howto http://docs.python.org/2/howto/sockets.html

class listenSocket:
	'''Class for making new listening sockets
	'''
	
	def __init__(self, sock=None, port=30021):
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.port = port
		self.sock.bind(('',self.port))
		self.sock.listen(1)
		print "server is listening"
		while 1:
			commSock, addr = self.sock.accept()
			cs = commSocket(commSock, addr)
			print "The server is ready to receive Commands"

class commSocket:
	'''class for making communication sockets
	'''
	def __init__(self, commsock, addr ):
		dataport = 30020
		self.commsock = commsock
		if (self.commsock.recv(4096) == "ready"):
			self.ds = dataSocket(addr, dataport)
		else:
			self.commsock.send("connection error")
		while 1:
			# logic
			self.command = (self.commsock.recv(4096) ).strip()
			print "command\t" +self.command
			if self.command == "":
				print "empty String"
				self.errorMsg()
			elif self.command == "list":
				self.list()
			elif len(self.command.split()) >1 and self.command.split()[0] == "get" and len(self.command.split()) == 2:
				self.getReq = self.command
				self.get(self.command.split()[1])
			elif self.command == "quit":
				self.commsock.send("quit")
				return
			else:
				self.errorMsg()

			print "end of logic loop"

	def errorMsg(self):
		''' sends error message to the client
		'''
		msg = "Error Enter list, get <filename>, or quit"
		self.commsock.send(msg)

	def get (self, file ):
		'''method to check if the file exists, get the size of the
		file and have the datasocket object read the file and 
		send to client. waits for the 'transfer' command from the 
		client indicating that the client is ready to receive the file
		before calling the push command.
		'''
		print "in get command"
		try :
			size = os.path.getsize(file)
		except os.error:
			self.commock.send("Error File Not Found")
		else:
			self.commsock.send("Getting " + self.getReq.split()[1] + " size " + str(size))
			if (self.commsock.recv(4096) == "transfer"):
				self.ds.push(self.getReq.split()[1], size)
			else :
				self.commsock.send("connection Error")

	def list (self):
		'''handles the "list" command and sends
		the files in the current director to the 
		client
		'''
		files = os.listdir(os.curdir)
		msg = ""
		for file in files:
			msg = msg + file + "\n"
		self.commsock.send(msg)

class dataSocket:
	'''class for making data connections
	'''
	def __init__(self, addr, dataport ):
		print "addr " + str(addr)
		datasock = socket(AF_INET, SOCK_STREAM)
		datasock.connect((addr[0], dataport))
		self.datasock = datasock

	def push(self, file, size):
		'''reads and pushes the file to the client
		'''
		print "in push command"
		filestr = open(file, 'r').read()
		totalsent= 0 
		while totalsent < size:
			sent = self.datasock.send(filestr[totalsent:])
			print "Bytes sent\t" + str(sent)
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

if __name__ == "__main__":
	ls = listenSocket()








