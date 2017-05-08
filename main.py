import socket, select,sys
import Servidor
import Cliente


if __name__ == "__main__":
    try:
        servidor = Servidor.Servidor(sys.argv[1],int(sys.argv[2]))
        print('Servidor Criado')
    except IndexError:
        print('Por Favor informe o ip e a porta ')
        sys.exit()

    try:

        while 1:
            for sock in servidor.getSelectSockets():
                if sock == servidor.getSock():
                    servidor.conectaCliente()
                else:
                    servidor.getData(servidor.getCliente(sock))



    except KeyboardInterrupt as KI :
        servidor.fechar()
        

    except Exception as e:
        print(e) 
        servidor.fechar()

    
    
    
    
   
