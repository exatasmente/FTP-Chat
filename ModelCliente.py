
import socket, select, sys
import utils


class Client:
     
    def __init__(self,host,port,name):
        self.host = host
        self.port = port
        self.name = name
    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)

        

    def prompt(self,data=None) :
        if data:

            sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX.format(data[0])+ ' ' +  data[1])
        else:
            sys.stdout.write('')
        sys.stdout.flush()
 


 
    def getData(self,s):
        data = s.recv(400).decode()
        if data :
            if len(data.split(':')) > 1:
                self.prompt(data.split(':'))
            else:
                self.prompt()
        else:
            print(utils.CLIENT_SERVER_DISCONNECTED.format(self.host,self.port))
            sys.exit()
           
    def disconnect(self):
        self.socket.close()
        sys.exit()

    def connect(self):
        try :
            self.socket.connect((self.host, self.port))
            self.socket.send(self.name.encode())

        except :
            print(utils.CLIENT_CANNOT_CONNECT.format(sys.argv[1],sys.argv[2]))
            sys.exit()
     
        print ('Connected')

    def post(self,msg):
        self.socket.send(msg)



