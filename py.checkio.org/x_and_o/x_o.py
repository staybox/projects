# coding: utf8
from __future__ import print_function
import string
"""
https://py.checkio.org/mission/x-o-referee/
"""


def solve_it(a):
    for i in range(3): #lines
        j = 0
        if a[i][j] == a[i][j+1] == a[i][j+2]:
            return a[i][j]
    for j in range(3): #rows
        i = 0
        if a[i][j] == a[i+1][j] == a[i+2][j]:
            return a[i][j]
    k = 0
    if a[k][k] == a[k+1][k+1] == a[k+2][k+2]:  # diagonal_1
        return a[k+1][k+1]
    if a[k+2][k] == a[k+1][k+1] == a[k][k+2]: # diagonal_2
        return a[k+1][k+1]


if __name__ == '__main__':
    a = [
    "x.0",
    ".x.",
    "0xx"]
    print(solve_it(a))
