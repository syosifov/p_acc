import enum
import os
# from django import setup
# from acc.c import A411
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p_acc.core.settings')
# setup()
# import acc.con as c

# from math import pi
import math


def t1():
    n = 3
    i = 1
    s1 = str(i)
    print(s1)
    # s1 = 'aa'
    s = s1.zfill(n)
    print(s)
    
    
def t2():
    math.pi = 222
    print(math.pi)
    
t2()    
