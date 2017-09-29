import sys,time,msvcrt

ch=msvcrt.getch()
if ch==b'y':#或ord(ch)=97
    print('ok')
else:
    print('err')
