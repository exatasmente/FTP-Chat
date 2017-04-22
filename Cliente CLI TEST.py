# telnet program example
import socket, select, sys
 
def prompt() :
    sys.stdout.write('')
    sys.stdout.flush()
 

#main function
if __name__ == "__main__":
     
     
    host = '127.0.0.1'
    port = 5000
    name = sys.argv[1]
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
        s.send(name.encode())

    except :
        print ('Não foi Possivél Conectar')
        sys.exit()
     
    print ('Concectado Ao Servidor')
    #s.send('Neto')
    prompt()
    
    try :
        while 1:
            socket_list = [sys.stdin, s]
         
             # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
            for sock in read_sockets:
                #incoming message from remote server
                if sock == s:
                    data = sock.recv(4096)
                    if not data :
                        print ('\nDesconectado')
                        sys.exit()
                    else :
                        #print data
                       sys.stdout.write(data.decode())
                       prompt()
                
                #use  r entered a message
                else :
                    msg = str(sys.stdin.readline()).encode()
                    s.send(msg)
                    prompt()
    except Exception as e:
        print(e)
        s.send("|sair|".encode())
    except KeyboardInterrupt as e:
        s.send("|sair|".encode())

