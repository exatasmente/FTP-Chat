import socket, select, sys
from ModelCliente import Client
import utils
if __name__ == "__main__":
    try:
        cliente = Client(sys.argv[1],int(sys.argv[2]),sys.argv[3])
        cliente.connect()
        cliente.prompt()

    except IndexError:
        print('inform Host, Port and your Name')
        sys.exit()


    
    try :
 
        while 1:
            socklist = [sys.stdin,cliente.socket]
            read_sockets, write_sockets, error_sockets = select.select(socklist , [], [])
 
            for sock in read_sockets:
                if sock == cliente.socket:
                     cliente.getData(sock)
           
                else :
                    msg = str(sys.stdin.readline()).encode()
                    cliente.post(msg)
                    cliente.prompt()

    except Exception as e:
        print(e)
        print('Desconectado')
        cliente.disconnect()
        sys.exti()
    except KeyboardInterrupt as e:
        cliente.disconnect()
        print('Desconectado')
        sys.exit()

