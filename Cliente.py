import socket

class Cliente:

    def __init__(self,nome = None,addr = None,socket = None,canal = None):
    
        self.nome = nome
        self.addr = addr
        self.socket = socket
        self.canal = canal
    
    def __eq__(self,other):
        
        return self.addr ==  other.addr and self.socket == other.socket 

    def getSock(self):
        return self.socket
    def setSock(self,socket):
        self.socket = socket
        
    def getaddr(self):
        return self.addr
    def setSock(self,addr):
        self.addr = addr
        
      
    
    def post(self,msg):
        print('POST')
        self.socket.send(msg.encode())  


    def disconnect(self):
        self.socket.close()
        
