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
        
    def getAddr(self):
        return self.addr
    def setAddr(self,addr):
        self.addr = addr
        
    def getNome(self):
        return self.nome
    def setNome(self,nome):
        self.nome = nome
              
    def getCanal(self):
        return self.canal
    def setCanal(self,canal):
        self.canal = canal
        
    
    def post(self,msg):
        self.socket.send(msg.encode())  


    def disconnect(self):
        self.socket.close()
        
