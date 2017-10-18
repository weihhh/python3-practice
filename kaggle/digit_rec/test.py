import numpy as np
import csv,sys

def toInt(array):
    array=array.astype(np.int8)
    return array
def a():
    print('b: ')
    b()
a()
def b():
    print('here')



# a=[[1,3,4,5],[1,128,2,7]]
# b=[[6,8,2,3],[2,3,7,3]]
# a=np.array(a)
# b=np.array(b)
# a[a<3]=0
# print(a)
# data=np.mat(a[0])
# x=toInt(a)
# print(x)
# for i in range(100):
#     percent = 1.0 * i / 100 * 100  
#     sys.stdout.write('\r' + str(percent))
    # print('\r','complete percent:%10.8s%s'%(str(percent),'%'),end='')
# c=np.array([4,5,7,2,1,8])
# d=np.array(['1','5','7','2'])
# print(c)
# print(np.array(data-b)**2)
# print((np.array(data-b)**2).sum(axis=1)**0.5)
# print(sorted(c),c.argsort()[0],c)
# d=d.astype(np.int8)
# d=np.where(d>2,8,0)
# print(d)
# with open('result.csv','w') as myFile:
#     myWriter=csv.writer(myFile,lineterminator='\n')
#     for i in range(6): 
#         tmp=c[3]
#         myWriter.writerow([tmp])