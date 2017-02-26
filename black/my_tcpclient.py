import socket
target_host='127.0.0.31'#如果服务器设置为0.0.0.0则这里最后一个网段随意都可以
target_port=9999

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))
client.send('hello'.encode('utf-8'))
response=client.recv(4096)
print(response)