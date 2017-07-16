# coding: utf8
from __future__ import print_function
import string
"""
https://py.checkio.org/mission/most-wanted-letter/
"""


def fun(a):
    letters = string.letters
    normalized = []
    for i in a:
        if i in letters:
            normalized.append(i.lower())
    normalized.sort()
    most_wanted = normalized[0]
    for k in range(len(normalized)-1):
        curr_letter = normalized.count(normalized[k]) #количество буквы
        next_letter = normalized.count(normalized[k+1])
        if next_letter > curr_letter:
            most_wanted = normalized[next_letter]

    return most_wanted


if __name__ == '__main__':
    a = 'Hello World!!@#$%^&**(*(***'
    print (fun(a))
