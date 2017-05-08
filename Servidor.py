import socket
import select
import Cliente
import utils
'''
Servidor Chat Baseado em Socket TCP  

Feito Com Amor em Python 3

Criado Por: Luiz Vieira Gonzaga Neto
Primeiro trabalho da disciplina Redes de Computadores 2017.1 UFC CAMPUS RUSSAS

'''


class Servidor:


    def __init__(self,IP,PORTA):
    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(0)
        self.socket.bind((IP, PORTA))
        self.socket.listen(1)

        self.listaCanais = dict()
        self.listaClientes = list()

           

    def getSock(self):
        return self.socket

    def getSelectSockets(self):
        s = [self.socket]+[ cli.getSock() for cli in self.listaClientes]
        return select.select(s,[],[])[0]
 
    def getListaClientes(self):
        return self.listaClientes

    def getListaCanais(self):
        return self.listaCanais



    def getData(self,cliente):
        try:
            POST = True
            data = cliente.get()
            if data:
                POST = self.getComando(cliente,data)
                if POST :
                    if cliente.getCanal(): 
                        self.post(cliente,cliente.getNome()+' : '+data)
                    else:
                       cliente.post('System : '+utils.SERVER_CLIENT_NOT_IN_CHANNEL+'\n')
        
        except Exception as e:
            print(e) 
            

            
    

    def post(self,cliente,msg):
        for cli in self.listaCanais[cliente.getCanal()]:
            if cli.getSock() != cliente.getSock():
               try:
                   cli.post(msg)
               except Exception as e:
                   print(e) 
                   self.remover(cli)



    def conectaCliente(self):
        sock,addr = self.socket.accept()
        cliente = Cliente.Cliente(None,addr,sock,None)
        cliente.setNome(cliente.get())
        self.listaClientes.append(cliente)


              

    def getCliente(self,socket):
        for cliente in self.listaClientes:
            if socket ==  cliente.getSock():
                return cliente

   
    def getComando(self,cliente,data):
        if data.startswith('/'):
            if data.__contains__('/exit'):
                self.sairCanal(cliente)
                return None
            if data.__contains__('/create'):
                if len(data.split())==2:
                    self.criarCanal(data.split()[1],cliente)
                    return False
                else:
                    cliente.post('System : '+utils.SERVER_CREATE_REQUIRES_ARGUMENT+'\n')
                    return False
            if data.__contains__('/join'):
                if len(data.split())==2:
                    self.entrarCanal(data.split()[1],cliente)
                    return False
                else:
                    cliente.post('System : '+utils.SERVER_JOIN_REQUIRES_ARGUMENT+'\n')
                    return False

            if data.__contains__('/list'):
                cliente.post(str(self.getCanais())+"\n")
                return False
            cliente.post('System : '+utils.SERVER_INVALID_CONTROL_MESSAGE.format(data)+'\n')
            return False
                        
        return True


    def sairCanal(self,cliente):
       if cliente.getCanal() == None:
           self.remover(cliente)
       else:
           cliente.post('System : You are in Limbo\n')
           self.post(cliente,'System : '+utils.SERVER_CLIENT_LEFT_CHANNEL.format(cliente.getNome())+'\n')
           if len(self.listaCanais[cliente.getCanal()]) == 1:
                del self.listaCanais[cliente.getCanal()]
           else:
               self.listaCanais[cliente.getCanal()].remove(cliente)
           cliente.setCanal(None)

     
        
    
    def entrarCanal(self,nomeCanal,cliente):
         if cliente.getCanal() == nomeCanal:
             cliente.post('System : You Are in Room '+ nomeCanal+ '\n')
         elif nomeCanal in self.listaCanais:
            if cliente.getCanal() != None :
                self.listaCanais[cliente.getCanal()].remove(cliente)
            cliente.setCanal(nomeCanal)
            self.listaCanais[nomeCanal].append(cliente)
            cliente.post('System : You are in Room '+ nomeCanal +'\n')
            self.post(cliente,'System : '+utils.SERVER_CLIENT_JOINED_CHANNEL.format(cliente.getNome()) +'\n')
         else:
              cliente.post('System : '+utils.SERVER_NO_CHANNEL_EXISTS.format(nomeCanal)+'\n')


  
    def criarCanal(self,nomeCanal,cliente):
        if not nomeCanal in self.listaCanais:
            self.listaCanais[nomeCanal]=list()
            cliente.post('Sistema : Você Criou o Canal '+nomeCanal+"\n")
            self.entrarCanal(nomeCanal,cliente)
        else:
            cliente.post("System : "+utils.SERVER_CHANNEL_EXISTS.format(nomeCanal)+'\n')
    


    def getCanais(self):
        retorno = "System :"
        for i in self.listaCanais:
            retorno += ' '+str(i)+'\n'
        return retorno


    def remover(self,cliente):
        cliente.disconnect()
        if cliente in self.listaClientes:
            self.listaClientes.remove(cliente)
            if cliente.getCanal():
                self.listaCanais[cliente.getCanal()].remove(cliente)

    def fechar(self):
        self.socket.close()
        
