import socket
import Cliente

RECV_BUFFER = 4096

class Servidor:
    
    def __init__(self,IP,PORTA):
    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((IP, PORTA))
        self.socket.listen(10)
        self.C_LISTA = dict()
        self.C_LISTA['0'] = list()
        self.SOCKLIST=list()
        self.SOCKLIST.append(self.socket)
        self.COMANDO = ['/sair','/entrar','/trocar','/criar']
        
    def remover(self,cliente):
        print('DEL')
        cliente.disconnect()
        self.SOCKLIST.remove(cliente.socket)


    #Func1 seleciona o canal
    def enviar_msg(self,cliente,msg):

        for cli in self.C_LISTA[cliente.canal]:
            if cli.socket != cliente.socket and cli.socket != self.socket:
                try:
                    print(str(cliente.nome+" : "+msg))
                    cli.post(str(cliente.nome+" : "+msg))
                except Exception as e:
                    print('ERRO ENVIA MSG')
                    print(e) 
                    self.remover(cli)
                    self.C_LISTA[cliente.canal].remove(cli)
                    continue

    # Func5 Sair Canal
    def sair_canal(self,nome_canal,cliente):
        self.enviar_msg(cliente,'Saiu do canal\n')
        print(cliente.nome,'Saiu do Canal : ',cliente.canal)
        self.C_LISTA[nome_canal].remove(cliente)
        

    # Func4 Entra Canal
    def entrar_canal(self,nome_canal,cliente):
        if nome_canal in self.C_LISTA:
            if not cliente in self.C_LISTA[nome_canal]:
                cliente.canal = nome_canal
                self.C_LISTA[nome_canal].append(cliente)
                self.C_LISTA['0'].remove(cliente)
                self.enviar_msg(cliente,'Entrou\n')
                cliente.post('Você Está No Canal: '+nome_canal+"\n")
                print(cliente.nome,'Entrou no Canal : ',cliente.canal,"\n")
        else:
            cliente.post('§Error03§\n')
        
                            

                    
    # Func3 Cria um canal
    def criar_canal(self,nome_canal,cliente):
        if not nome_canal in self.C_LISTA:
            print('Criar Canal Com Nome: ',nome_canal)
            self.C_LISTA[nome_canal]=list()
            cliente.post('Você Criou o Canal: '+nome_canal+"\n")
            self.entrar_canal(nome_canal,cliente)
        else:
            cliente.post('§Error02§\n')
    
    def getNomeCliente(sock):
     data = sock.recv(RECV_BUFFER).decode()
     return data


    def conecta_cliente(self):

        c = None
        print('Connecta')

        sock,addr = self.socket.accept()

        cliente = Cliente.Cliente(None,addr,sock,'0')
        self.SOCKLIST.append(cliente.socket)
        self.C_LISTA['0'].append(cliente)
        print(self.C_LISTA)
      
        

    def getCliente(self,socket):

        for canal in self.C_LISTA:
            for cliente in self.C_LISTA[canal]:
                if socket ==  cliente.socket:
                      return cliente

    def setNomeCliente(self,nome,cliente):
       print('Set Nome')
       if cliente:
           if cliente.nome == None:
               cliente.nome = nome
               return False
       return True
    
               
   
    def getComando(self,data,cliente):
        if data == self.COMANDO[0]:
            self.remover(cliente)
        if data == self.COMANDO[1]:
            data = data.replace(self.COMANDO[1],"")
            self.entrar_canal(data,cliente)
    def getCanais(self):
        return [i for i in self.C_LISTA]

    def getData(self,s):
#        print('DATA')
        try:
            name = True
            criar = -1
            data = s.recv(RECV_BUFFER).decode()
            if data:
                cliente = self.getCliente(s)
                if cliente.nome == None:
                     name =  self.setNomeCliente(data,cliente)

                if str(data).find('|sair|') >-1:
                      self.remover(cliente)
                      self.sair_canal(cliente.canal,cliente)
                      name = False

                if str(data).find('/criar')>-1:
                    self.criar_canal(data.split()[1],cliente)
                    name = False

                if str(data).find('/entrar')>-1:
                    self.entrar_canal(data.split()[1],cliente)
                    name = False
                if str(data).find('/listar')>-1:
                    cliente.post(str(self.getCanais())+"\n")
                    name = False
                if name :
                     self.enviar_msg(cliente,data)        
        except Exception as e:
            print('DATA ERROR')
            print(e) 
            cliente  = self.getCliente(s)
            self.sair_canal(cliente.canal,cliente)
            print ("O Cliente saiu")
            self.remover(cliente)
            self.C_LISTA[cliente.canal].remove(cliente)
            pass
            


        
    def getConn(self):
        return self.C_LISTA
    def fechar(self):
        self.socket.close()
        
   


