import sys,time,msvcrt
def timedInput(caption, default, timeout=5):
    start_time = time.time()
    sys.stdout.write('%s(%d秒自动跳过):' % (caption,timeout))
    sys.stdout.flush()
    input = ''
    while True:
        ini=msvcrt.kbhit()
        try:
            if ini:
                chr = msvcrt.getche()
                if ord(chr) == 13 :  # enter_key
                    break
                elif ord(chr) >= 32:
                    input += chr.decode()
        except Exception as e:
            pass
        if len(input) == 0 and time.time() - start_time > timeout:
            break
    print ('')  # needed to move to next line
    if len(input) > 0:
        return input+''
    else:
        return default
 
 
#使用方法
iscaiji=timedInput('请输入你的名字','y')
if iscaiji==('y' or 'yes'):
    print('进行---> ')