# coding: utf8
from __future__ import print_function

"""
когда не нужно изменять функцию, используем декораторы
"""


def make_bold(fn):
    def wrapped():
        return '<b>' + fn() + '</b>'
    return wrapped


def make_italic(fn):
    def wrapped():
        return '<i>' + fn() + '</i>'
    return wrapped


@make_italic
@make_bold
def try_decorators():
    return 'hello world'


if __name__ == '__main__':
    print(try_decorators())
