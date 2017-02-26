#localhost和localport指的是本地应用应该发往的，remote是指原本将发往的
import sys
import socket
import threading

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.bind((local_host,local_port))
    except Exception as exc:
        print('failed!')
        print(str(exc))
        sys.exit(0)
    print('[*]listening on {0}:{1}'.format(local_host,local_port))
    server.listen()
    while True:
        client_socket,addr=server.accept()
        #print out the local connection information
        print('[>>>] received incoming connection from {0}:{1}'.format(addr[0],addr[1]))
        
        #start a thread to talk to the remote host
        proxy_thread=threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
        proxy_thread.start()
        
        

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    #connectto the remote host
    remote_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))
    #receive data from the remote end if neccessary，有时候我们一旦连接服务器，服务器就会先发送一些信息给我们
    if receive_first:
        
        remote_buffer=receive_from(remote_socket)
        if remote_buffer=='':
            print('err')
        #hexdump(remote_buffer)
        #send it to our response handler
        remote_buffer=response_handler(remote_buffer)
        #if we have data to send to our local client,send it
        if len(remote_buffer):
            print('[<<]sending {0} bytes to localhost.'.format(len(remote_buffer)))
            client_socket.send(remote_buffer.encode('utf-8'))
    #now lets loop and read from local,send to remote,send to local
    while True:
        
        #read from local host
        local_buffer=receive_from(client_socket)
        if len(local_buffer):
            print('[<<]received {0} chars from localhost:'.format(len(local_buffer)))
            #hexdump(local_buffer)
            print(local_buffer)
            #send it to our request handler
            local_buffer=request_handler(local_buffer)
            remote_socket.send(local_buffer.encode('utf-8'))
            print('[>>]sent to remote')
            
            #receive back response
        remote_buffer=receive_from(remote_socket)
        if len(remote_buffer):
            print('[<<]received {0} chars from remote:'.format(len(remote_buffer)))
            #hexdump(remote_buffer)
            print(remote_buffer)
            #send it to our response handler
            remote_buffer=response_handler(remote_buffer)
            #send the response to the local socket
            client_socket.send(remote_buffer.encode('utf-8'))
            print('[<<]sent to localhost')
            #if no more data on either side ,close the connection
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print('[*] no more data,close connection')
            break
            

            
def hexdump(src,length=16):#这个函数是python2的，在此处不能运行
    result=[]
    digits=4 if isinstance(src,str) else 2#python3 将unicode移除，替换为str
    for i in range(0,len(src),length):#python3将xrangge改名为range
        s=src[i:i+length]
        hexa=b''.join(["%0*X" % (digits, ord(x)) for x in s])
        text=b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i, length*(digits + 1), hexa,text))
        print(b'\n'.join(result))
        
def receive_from(connection):
    buffer=''
    #we set a 2second timeout,depending on your target ,this need to be adjusted
    #connection.settimeout(2)
    try:
        #keep reading into the buffer until,there is no more data or we time out
        while True:
            data=connection.recv(4096)
            
            if len(data) < 4096:
                buffer+=data.decode('utf-8')
                break
            buffer+=data
    
    except Exception as err:
        print(str(err))
    return buffer
    
def response_handler(buffer):
    #perform packet modifications
    return buffer
    
def request_handler(buffer):
    #perform packet modifications
    return buffer
    
    
        
        
        
        
def main():
    #no fancy commandline parsing here
    if len(sys.argv[1:])!=5:
        print('Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]')
        print('Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True')
        sys.exit(0)
        
    #setup local listening parameters
    local_host=sys.argv[1]
    local_port=int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    #this tell proxy to connect and receive data before sending to the remote host
    receive_first=sys.argv[5]
    if 'True' in receive_first:
        receive_first=True
    else:
        receive_first=False
        
    #NOW SPIN UP OUR LISTENING SOCKET
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)
   
   
main()   
    