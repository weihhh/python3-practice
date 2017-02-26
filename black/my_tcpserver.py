import socket
import threading

bind_ip='0.0.0.0'#0.0.0.0代表整个本网络，能作为本网络所有地址
bind_port=9999

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))
server.listen(5)#maximum backlog of connections set to 5
print('[*]listening on {0}:{1}'.format(bind_ip,bind_port))

#client_handling thread
def handle_client(client_socket):
    request=client_socket.recv(1024)
    print('[*]recieved:{0}'.format(request))
    client_socket.send('ack!'.encode('utf-8'))
    client_socket.close()
    
while True:
    client,addr=server.accept()#receive the client socket into the client variable
    print('[*]accepted connection from :{0}:{1}'.format(addr[0],addr[1]))
    #spin up thread to handle incoming data
    client_handler=threading.Thread(target=handle_client,args=(client,))
    client_handler.start()