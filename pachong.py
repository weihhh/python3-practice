import urllib.request  
import socket  
import re  
import sys  
import os  
targetDir = r'F:\\python pro\\'  #文件保存路径
def destFile(path):  
    if not os.path.isdir(targetDir):  
        os.mkdir(targetDir)  
    pos = path.rindex('/')  
    t = os.path.join(targetDir, path[pos+1:])  
    return t  
for i in range(1):  #程序运行入口
    weburl = 'http://www.hdu.edu.cn/'
    webheaders = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
    req = urllib.request.Request(url=weburl, headers=webheaders)  #构造请求报头
    webpage = urllib.request.urlopen(req)  #发送请求报头
    contentBytes = webpage.read()  
    #print(str(contentBytes))
    for link in re.findall(' <li style=\"background-image:url\((http:\//www.hdu.edu.cn/uploads/images/\d{8}/(.*?))\)', str(contentBytes)):  #正则表达式查找所有的图片
        #print(type(link))
        print(link[0],link[1])
        print('F:\\python pro\\'+link[1])
        try: 
            urllib.request.urlretrieve(link[0],'F:\\python pro\\'+link[1]) #下载图片
        except:
            print('失败') #异常抛出
