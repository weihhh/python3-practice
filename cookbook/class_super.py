class base:
    def __init__(self):
        print('base_init')

class A(base):
    def __init__(self):
        super().__init__()
        print('A.init')
class B(base):
    def __init__(self):
        super().__init__()
        print('B.init')
class C(A,B):
    def __init__(self):
        super().__init__()
        print('C.init')

c=C()