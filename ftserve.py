from socket import *
import os

class ftserver:
    '''This class creates a command connection
    for the server. It allows the server to 
    respond to commands and initiated a new 
    file transfer socket when asked to do so.
    '''

    def __init__(self, sock=None, port=30021):
        if sock is None:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = sock
        self.port = port
        self.socklisten()

    def socklisten(self):
        self.sock.bind(('',self.port))
        self.sock.listen(1)
        print "The server is ready to receive"
        self.commSocket = 1
        while(self.commSocket):
            self.commSocket, addr = self.sock.accept();
            while(self.commSocket):
                command = (self.commSocket.recv(4096) ).strip()
                print command
                if command == "list":
                    msg = self.list()
                    self.commSocket.send("\nDirectory Listings:\n\n" + msg)
                elif command.split()[0] == "get" and len(command.split()) == 2:
                    rfile = command.split()[1]
                    print "rfile = " + rfile
                    self.get( rfile)
                elif command == "quit":
                    self.quit()
                else:
                    msg = "Error Enter list, get <filename>, or quit"
                    self.commSocket.send(msg)
        

    def list(self):
        files = os.listdir(os.curdir)
        msg = ""
        for file in files:
            msg = msg + file + "\n"
        return msg

    def quit(self):
        self.commSocket.send("quit")
        self.commSocket = 0

    def get(self, file):
       
        try :
            size = os.path.getsize(file)
        except os.error:
            self.commSocket.send("Error File Not Found")
        else:
            transferPort = 30021
            self.commSocket.send("incomingFileSize " + str(size) + " port " + str(transferPort + " filename " + file))
            openTransferSocket(self, size, 10044,file)

    def PushFile(self, size, port, file )

if __name__=="__main__":
    server = ftserver()

