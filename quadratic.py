import cmath,math,sys

def get_float(msg,allow_zero):
    x=None
    while x is None:
        try:
            x=float(input(msg))
            if not allow_zero and abs(x)<sys.float_info.epsilon:
                print('不能是零')
                x=None
        except ValueError as err:
            print(err)
    return x
    
print('ax^2+bx+c=0')#print('ax\N{SUPERSCRIPT TWO}+bx+c=0'),windos中对平方号支持不好，用^2代替
a=get_float('输入参数a：',False)
b=get_float('输入参数b：',True)
c=get_float('输入参数c：',True) 
x1=None
x2=None
discriminant=(b**2)-(4*a*c)
if discriminant==0:
    x1=-(b/(2*a)) 
else:
    if discriminant > 0:
        root=math.sqrt(discriminant)
    else:
        root=cmath.sqrt(discriminant)#复数开根号
    x1=(-b+root)/(2*a) 
    x1=(-b+root)/(2*a)
equation=('{0}x^2+{1}x+{2}=0'
'>>> x={3}').format(a,b,c,x1)
if x2 is not None:
    equation+='or x={0}'.format(x2)
print(equation)
    
    
    
    