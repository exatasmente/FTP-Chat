import socket, select, sys
from ModelCliente import Client

if __name__ == "__main__":
    cliente = Client(sys.argv[1])
    cliente.connect()
    cliente.prompt()
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
        cliente.disconnect()
    except KeyboardInterrupt as e:
        cliente.disconnect()

