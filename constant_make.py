class  Constantnum:
    def __setattr__(self,name,value):
        if name in self.__dict__:
            raise ValueError('no')
        self.__dict__[name]=value
        
        
con=Constantnum()
con.wei=1
print(con.wei)
#con.wei=2
com=type(con)()
com.wei=9
