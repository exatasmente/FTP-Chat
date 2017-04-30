# telnet program example
import socket, select, sys
 


class Client:
     
    def __init__(self,nome):
        self.host = '127.0.0.1'
        self.port = 500
        self.name = nome
    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(2)
        

    def prompt(self) :
        sys.stdout.write('')
        sys.stdout.flush()
 


 
    def getData(self,s):
        try:
            data = s.recv(4096).decode()
            if data:
                sys.stdout.write(data)
                self.prompt()

        except Exception as e:
            print(e) 
            self.disconnect()
            pass
            
    def disconnect(self):
        self.socket.send("|sair|".encode())
        self.socket.close()
        sys.exit()

    def connect(self):
        try :
            self.socket.connect((self.host, self.port))
            self.socket.send(self.name.encode())

        except :
            print ('Não foi Possivél Conectar')
            sys.exit()
     
        print ('Conectado Ao Servidor')

    def post(self,msg):
        self.socket.send(msg)



