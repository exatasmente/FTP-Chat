import socket
import select
import Cliente
'''
Servidor Chat Baseado em Socket Stream  

Feito Com Amor em Python 3

Criado Por: Luiz Vieira Gonzaga Neto
Primeiro trabalho da disciplina Redes de Computadores 2017.1 UFC CAMPUS RUSSAS

'''
RECV_BUFFER = 4096

class Servidor:


    def __init__(self,IP,PORTA):
    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((IP, PORTA))
        self.socket.listen(10)
        self.listaCanais = dict()
        self.listaCanais['0'] = list()
        self.listaSockets=list()
        self.listaSockets.append(self.socket)
           

    def getSock(self):
        return self.socket

    def getSelectSockets(self):
        return select.select(self.getListaSockets(),[],[])
 
    def getListaSockets(self):
        return self.listaSockets

    def getListaCanais(self):
        return self.listaCanais



    def getData(self,s):
        try:
            POST = True
            data = s.recv(RECV_BUFFER).decode()
            if data:
                cliente = self.__getCliente__(s)
                if cliente.getNome() == None:
                    POST =  self.__setNomeCliente__(data,cliente)
                if POST:
                    POST = self.__getComando__(cliente,data)
                if POST : 
                    self.__post__(cliente,data)        
        except Exception as e:
            print(e) 
            cliente  = self.__getCliente__(s)
            self.__sairCanal__(cliente)
            self.__remover__(cliente)
            self.listaCanais[cliente.getCanal()].remove(cliente)
            pass
            
    
    def __post__(self,cliente,msg):

        for cli in self.listaCanais[cliente.getCanal()]:
            if cli.getSock() != cliente.getSock() and cli.getSock() != self.socket:
                try:
                    cli.post(str(cliente.getNome()+" : "+msg))
                except Exception as e:
                    print(e) 
                    self.__remover__(cli)
                    self.listaCanais[cliente.getCanal()].remove(cli)
                    continue



    def conectaCliente(self):
        sock,addr = self.socket.accept()
        cliente = Cliente.Cliente(None,addr,sock,'0')
        self.listaSockets.append(cliente.getSock())
        self.listaCanais['0'].append(cliente)

              

    def __getCliente__(self,socket):

        for canal in self.listaCanais:
            for cliente in self.listaCanais[canal]:
                if socket ==  cliente.getSock():
                      return cliente


    def __getNomeCliente__(sock):
     data = sock.recv(RECV_BUFFER).decode()
     return data


    def __setNomeCliente__(self,nome,cliente):
       if cliente:
           if cliente.getNome() == None:
               cliente.setNome(nome)
               return False
       return True
                   
   
    def __getComando__(self,cliente,data):
        if str(data).find('//sair') >-1:
            self.__sairCanal__(cliente)
            return False
        if str(data).find('|sair|') >-1:
            cliente.setCanal('0')
            self.__sairCanal__(cliente)
            return False
        if str(data).find('//criar')>-1 and len(data.split())==2:
            self.__criarCanal__(data.split()[1],cliente)
            return False
        if str(data).find('//entrar')>-1 and len(data.split())==2:
            self.__entrarCanal__(data.split()[1],cliente)
            return False
        if str(data).find('//listar')>-1:
            cliente.post(str(self.__getCanais__())+"\n")
            return False

        return True

    def __trocarCanal__(self,novoCanal,cliente):
         if novoCanal in self.listaCanais:
              if not cliente in self.listaCanais[novoCanal]:
                  canalAntigo = cliente.getCanal()
                  if cliente in self.listaCanais[canalAntigo]:
                      self.listaCanais[canalAntigo].remove(cliente)
                  self.listaCanais[novoCanal].append(cliente)
                  cliente.setCanal(novoCanal)
                  cliente.post('Você Está No Canal: '+nomeCanal+"\n")
                  self.__post__(cliente,str('Trocou do Canal '+canalAntigo+' Para o Canal '+cliente.getCanal()+'\n'))
         else:
            cliente.post('§Error04§\n')


    def __sairCanal__(self,cliente):
        if cliente.getCanal() == '0':
            self.__remover__(cliente)
            self.listaCanais[cliente.getCanal()].remove(cliente)
            self.__post__(cliente,'Saiu \n')
        else:
            self.__post__(cliente,'Saiu do canal\n')
            self.listaCanais[cliente.getCanal()].remove(cliente)
            self.__entrarCanal__('0',cliente)
     
        
    
    def __entrarCanal__(self,nomeCanal,cliente):
        if nomeCanal in self.listaCanais:
            if not cliente in self.listaCanais[nomeCanal]:
                if cliente.getCanal() == '0':
                     self.listaCanais[cliente.getCanal()].remove(cliente)
                     cliente.setCanal(nomeCanal)
                     self.listaCanais[nomeCanal].append(cliente)
                     self.__post__(cliente,'Entrou\n')
                     cliente.post('Você Está No Canal: '+nomeCanal+"\n")
                else:
                     self.__trocarCanal__(nomeCanal,cliente)
        else:
            cliente.post('§Error03§\n')


    def __criarCanal__(self,nomeCanal,cliente):
        if not nomeCanal in self.listaCanais:
            self.listaCanais[nomeCanal]=list()
            cliente.post('Você Criou o Canal: '+nomeCanal+"\n")
            self.__entrarCanal__(nomeCanal,cliente)
        else:
            cliente.post('§Error02§\n')
    


    def __getCanais__(self):
        return [i for i in self.listaCanais]

        
    def __remover__(self,cliente):
        cliente.disconnect()
        self.listaSockets.remove(cliente.getSock())


    def fechar(self):
        self.socket.close()
        
