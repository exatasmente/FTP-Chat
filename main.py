import socket, select
import Servidor
import Cliente


if __name__ == "__main__":

    servidor = Servidor.Servidor('127.0.0.1',5000)
    print('Servidor Criado')

    try:
        while 1:
            read_sockets,write_sockets,error_sockets = select.select(servidor.SOCKLIST,[],[])
 
            for sock in read_sockets:

                if sock == servidor.socket:
                   
                    servidor.conecta_cliente()

                else:
                   
                    servidor.getData(sock)

    except KeyboardInterrupt as KI :
        servidor.fechar()
        

    except Exception as e:
        print('MAIN ERROR')
        print(e) 
 #       continue
#
    
    
    
    
   
