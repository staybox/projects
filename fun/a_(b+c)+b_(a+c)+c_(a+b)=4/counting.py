# coding: utf8
from __future__ import print_function
import datetime
import numpy as np


def qwe():
    """
    https://www.quora.com/How-do-you-find-the-integer-solutions-to-frac-x-y+z-+-frac-y-z+x-+-frac-z-x+y-4/answer/Alon-Amit
    """
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    r1 = 0.1
    r2 = 200
    n = 4.0
    # for task with wholes values 10.0**8 is limit for np.arange.
    # We need to calculate r2 = 10.0**82
    for a in np.arange(r1, r2, 0.0001):
        for b in np.arange(r1, r2, 1.0):
            for c in np.arange(r1, r2, 1.0):
                check(a, b, c, n)
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def check(a,b,c, n):
    a = float(a)
    b = float(b)
    c = float(c)
    x = a / (b + c) + b/(a+c) + c/(a+b)
    if x > n and x < n+0.0001:
        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        assert False, 'x = {}, a = {}, b = {}, c = {}'.format(x,a,b,c)

# for not wholes answer is :
#x = 4.00009417114, a = 0.1, b = 51.1, c = 191.1

if __name__ == '__main__':
    qwe()
