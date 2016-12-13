import os,socketserver,contextlib,threading,pickle,gzip,struct,copy,sys


def main():
    filename=os.path.join(os.path.dirname(__file__),'car_registrations.dat')
    cars=load(filename)
    print('load {0} car registrations'.format(len(cars)))
    RequestHandler.Cars=cars
    server=None
    try:
        server=CarRegistrationServer(('',9653),RequestHandler)#服务器上只需要空着
        server.serve_forever()
    except Exception as err:
        print('ERROR',err)
    finally:
        if server is not None:  
            server.shutdown()
            save(filename,RequestHandler.Cars)
            print('save {0} car registrations'.format(len(RequestHandler.Cars)))
            
class Car:
    def __init__(self,seats,mileage,owner):
        self.seats=seats
        self.mileage=mileage
        self.owner=owner


            
def load(filename):
    try:
        with contextlib.closing(gzip.open(filename,'rb')) as fh:
            return pickle.load(fh)#为什么只能是load？
    except (EnvironmentError,pickle.UnpicklingError) as err:
        print('sever cannot load data :{0}'.format(err))
        sys.exit(1)
       
def save(filename,cars):
    try: 
        with contextlib.closing(gzip.open(filename,'wb')) as fh:
            pickle.dump(cars,fh,pickle.HIGHEST_PROTOCOL)
    except (EnvironmentError,pickle.UnpicklingError) as err:
        print('sever cannot save data :{0}'.format(err))
        sys.exit(1)       

#自定义服务器类,继承socketserver.ForkingMixin 则是使用进程，            
class CarRegistrationServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

    
class Finish(Exception):
        pass
    
class RequestHandler(socketserver.StreamRequestHandler):#tcp对应StreamRequestHandler，udp对应datagramRequestHandler
    CarsLock=threading.Lock()
    CallLock=threading.Lock()
    Call=dict(
        GET_CAR_DETAILS=(lambda self,*args:self.get_car_details(*args)),
        CHANGE_MILEAGE=(lambda self,*args:self.change_mileage(*args)),
        NEW_REGISTRATION=(lambda self,*args:self.new_registration(*args)),
        SHUTDOWN=lambda self,*args:self.shutdown(*args)
        )
    def handle(self):
        SizeStruct=struct.Struct('!l')
        size_data=self.rfile.read(SizeStruct.size)
        size=SizeStruct.unpack(size_data)[0]#unpack得到的是元组
        data=pickle.loads(self.rfile.read(size))
        
        try:
            with self.CallLock:
                function=self.Call[data[0]]#客户端传输过来数据data的是元组，第一个为命令名
            reply=function(self,*data[1:])
        except Finish:
            return
        data=pickle.dumps(reply,3)
        self.wfile.write(SizeStruct.pack(len(data)))
        self.wfile.write(data)
            
    def get_car_details(self,license):
        print(license)
        with self.CarsLock:
            car=copy.copy(self.Cars.get(license,None))
            if car is not None:
                return (True,car.seats,car.mileage,car.owner)#服务器回复的标准格式，一个元组
            return (False,'this lecense is not registered')
    
    def change_mileage(self,license,mileage):
        mileage=int(mileage)
        if mileage<0:
            return (False,'cannot set a negtive mileage')
        with self.CarsLock:
            car=self.Cars.get(license,None)
            if car is not None:
                if car.mileage <mileage:   
                    car.mileage=mileage
                    return (True,None)
                return (False,'not back')
            return (False,'this license is not registered')                
    def new_registration(self,license,seats,mileage,owner):
        mileage=int(mileage)
        if not license:
            return (False,'no license')
        if int(seats) not in {2,4,5,6,7}:    
            return (False,'seats not right')
        if mileage <0:
            return (False,'mileage cannot below zero')
        if not owner:
            return (False,'no owner')
        with self.CarsLock:
            if license not in self.Cars:
                self.Cars[license]=Car(seats,mileage,owner)
                return (True,None)
        return (False,'this license have been registered')  

    def shutdown(self,*ignore):
        self.server.shutdown()
        raise Finish()
             

if __name__=='__main__':
    main()             
    
        