import socket,sys,struct,pickle

Address=['localhost',9653]#115.159.4.205,9653

def main():
    if len(sys.argv)>1:
        Address[0]=sys.argv[1]
    call=dict(c=get_car_details,m=change_mileage,n=new_registration,s=stop_server,q=quit)
    menu="(C)ar (M)ileage (O)wner (N)ew car (S)top sever (Q)uit: "
    previous_license=None
    while True:
        action=input(menu).lower()
        print(action)
        previous_license=call[action](previous_license)

def get_car_details(previous_license):
    license,car=retrieve_car_details(previous_license)
    if car is not None:
        print('License:{0}\nSeat:{1}\nMileage:{2}\nOwner:{3}'.format(license,*car))
    return license
def retrieve_car_details(previous_license):
    license=input('please input license:') or previous_license
    if not license:
        return previous_license,None
    license=license.upper()
    status,*data=handle_request('GET_CAR_DETAILS',license)#服务器总是返回元组，用*data可以接收元组后面剩余的所有部分
    if not status:
        print(data[0])
        return previous_license,None
    return license,data

def change_mileage(previous_license):
    license,car=retrieve_car_details(previous_license)
    if car is None:
        return previous_license
    mileage=input('please input new mile') 
    if mileage is None:
        return license
    status,*data=handle_request('CHANGE_MILEAGE',license,mileage)
    if not status:
        print(data[0])
    else:
        print('Mileage successfully changed')
    return license

def new_registration(previous_license):
    license=input('please input new license:\n').upper()
    if license is None:
        license=input(' license must be provided\n').upper()
    seats=input('please input the seats:\n')
    mileage=input('please input new mile:\n')
    owner=input('please input the owner:\n')
    status,*data=handle_request('NEW_REGISTRATION',license,seats,mileage,owner)
    if not status:
        print(data[0])
    else:   
        print('successfully register the car')
    return license
    
    
def quit(*ignore):
    sys.exit()
def stop_server(*ignore):
    handle_request('SHUTDOWN',wait_for_reply=False)
    sys.exit()

def handle_request(*items,wait_for_reply=True):
    SizeStruct=struct.Struct('!l')
    data=pickle.dumps(items,3)
    try:
        with SocketManager(tuple(Address)) as sock:
            sock.sendall(SizeStruct.pack(len(data)))
            sock.sendall(data)
            if not wait_for_reply:
                return
            size_data=sock.recv(SizeStruct.size)
            size=SizeStruct.unpack(size_data)[0]
            result=bytearray()#因为是网络数据，事先定好用字节类型可以不断增加
            while True:
                data=sock.recv(4000)
                if not data:
                    break
                result.extend(data)
                if len(result)>=size:  
                    break
        return pickle.loads(result)
    except socket.error as err:
        print(err)
        sys.exit(1)

class SocketManager:
    def __init__(self,address):
        self.address=address
        
    def __enter__(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(self.address)
        return self.sock
    def __exit__(self,*ignore):
        self.sock.close()
            
    
    
if __name__=='__main__':
    main()