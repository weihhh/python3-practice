class person:
    def __init__(self,name):
        self.name=name
        pass
    @property   
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError('expected a string')
        self._name=value


class  subperson(person):
    """docstring for  subperson"""
    @property
    def name(self):
        print('get name')
        return super().name
    @name.setter
    def name(self,value):
        print('set name')
        super().name=value
        


a=subperson(1)
print(a.name)