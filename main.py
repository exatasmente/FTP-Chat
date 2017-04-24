import socket, select
import Servidor
import Cliente


if __name__ == "__main__":

    servidor = Servidor.Servidor('192.168.1.5',5000)
    print('Servidor Criado')

    try:
        while 1:
            
 
 
            for sock in servidor.getSelectSockets()[0]:

                if sock == servidor.getSock():
                   
                    servidor.conectaCliente()

                else:
      
                    servidor.getData(sock)

    except KeyboardInterrupt as KI :
        servidor.fechar()
        

    except Exception as e:
        print('MAIN ERROR')
        print(e) 

    
    
    
    
   
