#程序存在一个bug，发送一个命令后应该是返回结果，紧接着是提示符，然后等待下一条命令，但实际情况是结果后面没有提示符，直接等待下一条命令，漏掉一个提示符
import sys,time
import socket
import getopt
import threading
import subprocess

#define global variables
listen=False
command=False
upload=False
execute=''
target=''
upload_destination=''
prot=0


def usage():
    '''   
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen - listen on [host]:[port] for ¬
    incoming connections"
    print "-e --execute=file_to_run - execute the given file upon ¬
    receiving a connection"
    print "-c --command - initialize a command shell"
    print "-u --upload=destination - upon receiving connection upload a ¬
    file and write to [destination]"
    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    '''    
    print('use not right')
    sys.exit(0)
    
def client_sender(buffer):#最后加上这个脚本使用者的输入，使得这个程序和命令行的操作更加的像
    
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
    #connect to our target host
            
        client.connect((target,port))
        
        if len(buffer):
            client.send(buffer.encode('utf-8'))
        while True:
            #now wait for data back until there is no more data to receive
            recv_len =1
            response=''
                
            while recv_len:
                data=client.recv(4096).decode('utf-8')
                recv_len=len(data)
                response+=data
                if recv_len<4096:#收到为空或者收到不足四个字节（收取完毕），则跳出当前循环，重新一轮收取，否则继续收取加到response上
                    break
            print(response)
                #wait for more input
            
            buffer=input('')
            buffer += '\n'
            #send it off
            client.send(buffer.encode('utf-8'))
    except Exception as err:
        print('Exception !exiting!')
        print(str(err))
            #tear down the connection
        client.close()
            
def server_loop():
    global target
    #if no target is defined ,we listen on all interfaces
    if not len(target):
        target='0.0.0.0'
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    print('[*]recieving at {0}:{1}'.format(target,port))
    server.listen(5)
    while True:
        client_socket,addr =server.accept()
        client_thread=threading.Thread(target=client_handler,args=(client_socket,))
        print('from {0}:{1}'.format(addr[0],addr[1]))
        client_thread.start()

def run_command(command):
    
    #trim the newline
    command=command.rstrip()
    #run the command and get the output back
    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True,universal_newlines=True)
        #原先这里没有universal_newlines=True，subprocess.check_output返回的是bytes对象，加上后返回字符串，这里的shell，和这个univer_newlines都还需进一步熟悉
    except:
        output='Failed to execute command. \r\n'
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    #check for upload
    if len(upload_destination):
        #read in all of the bytes and write to our destination 
        file_buffer=''
        #keep reading data until none is available
        while True: 
            data=client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        #now we take these bytes and try to write them out
        try:
            file_descriptor=open(upload_destination,'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            #acknowledge that we wrote the file out
            client_socket.send('successfully saved file to{0}'.format(upload_destination).encode('utf-8'))
        except:
            client_socket.send('failed save file'.encode('utf-8'))
     
    if command:#就在这里开始无限循环，一直读取远端传来的命令，直到换行符，然后接着下一条，
        i=0
        while True:
            client_socket.send('<BHP:#{0}>'.format(i).encode('utf-8'))
            print('another command')
            cmd_buffer=''
            while  '\n' not in cmd_buffer:
                
                cmd_buffer +=(client_socket.recv(1024).decode('utf-8'))#缓存中有数据才运行
                
            response=run_command(cmd_buffer) 
            #print(type(response))
            client_socket.send(response.encode('utf-8'))            
            i+=1
            #time.sleep(3) 
     
     
     
     
     
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args=getopt.getopt(sys.argv[1:],'hle:t:p:cu:',['help','listen','execute','target','port','command','upload'])
        #后面的冒号和等号表示带不带参数,opts为二元组的列表，args为剩余没有读取的命令行参数
    except getopt.GetoptError as err:
        print(str(err))
        usage()
         
    for o,a in opts:
        if o in ('-h','--help'):
            usage()
        elif o in ('-l','--listen'):
            listen=True
        elif o in ('-u','--upload'):
            upload_destination=a
        elif o in ('-c','--command'):
            command=True
        elif o in ('-e','--execute'):
            execute=True
        elif o in ('-t','--target'):
            target=a
        elif o in ('-p','--port'):
            port=int(a)
        else:
            assert False,'unhandled option'
            
    #listen or just send data from stdin        
    if not listen and len(target) and port > 0:
        #read in the buffer from the commandline
        #this will block, so send ctrl-d if not sending input to stdin
        #ctrl-d 关闭当前shell，win下面是ctrl_z
        
        buffer =sys.stdin.read()
        #send data off
        
        client_sender(buffer)
        
        
    #listen and potentially upload things,execute commands, and drop a shell back depend on our command line options above
    if listen:
        server_loop()

main()        