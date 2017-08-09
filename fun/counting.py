# coding: utf8
import datetime
import numpy as np


def qwe():
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    r = 1000000.0
    n = 4.0
    for a in np.arange(1.0, r, 1.0):
        print a
        for b in np.arange(1.0, r, 1.0):
            print b
            for c in np.arange(1.0, r, 1.0):
                check(a, b, c, n)
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check(a,b,c, n):
    a = float(a)
    b = float(b)
    c = float(c)
    x = a / (b + c) + b/(a+c) + c/(a+b)
    if x == n:
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        assert False, 'x = {}, a = {}, b = {}, c = {}'.format(x,a,b,c)




if __name__ == '__main__':
    qwe()
