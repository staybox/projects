# coding: utf8
from __future__ import print_function
"""
https://py.checkio.org/mission/fizz-buzz/
"""


def fbuzz(a):
    f = 'fizz'
    b = 'buzz'
    res = ''
    if a%3 == 0:
        res = f
    if a%5 == 0:
        res = res+b
    return res


if __name__ == '__main__':
    a = 15
    print (fbuzz(a))
