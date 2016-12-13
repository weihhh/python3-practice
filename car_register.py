import pickle,gzip,os

def main():
    cars={'SC111':Car(3,344,'wei'),'SC211':Car(4,213,'hao')}#全部牌照为大写，客户端全部转换为大写
    save(cars,'car_registrations.dat')

class Car:
    def __init__(self,seats,mileage,owner):
        self.seats=seats
        self.mileage=mileage
        self.owner=owner

def save(cars,filename):
        try:
            with gzip.open(os.path.join(os.path.dirname(__file__),filename),'wb') as fh:
                pickle.dump(cars,fh,pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError,pickle.PicklingError) as err:
            print(err)        
    
if __name__=='__main__':
    main()         