import os
'''
得到指定目录下的所有文件列表，递归或者不递归
'''
def get_files(path,recurse=False):
    files=[]
    if not recurse:
        for name in os.listdir(path) :
            fullname=os.path.join(path,name)
            if os.path.isfile(fullname):
                files.append(fullname)
        return files   
    else:
        for root ,dirs,names in os.walk(path) :
            for name in names:
                fullname=os.path.join(root,name)
                files.append(fullname)
        return files   
            
# x=get_files('D:\Documents\GitHub\python3-practice')
# with open(x[0]) as f:
#     result=f.read()
#     print(x[0])
#     print(x) 
