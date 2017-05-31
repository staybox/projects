# coding: utf8
import ConfigParser
import ast
from itertools import product
import itertools


def stencil(dim):
    stencils = list(product([-1, 0, 1], repeat=dim))
    zero = ((0,) * dim)
    stencils.remove(zero)  # (0, 0)
    # we need only horizontal neighbors, not diagonals
    for i in stencils:
        i1 = []
        for k in i:
            i1.append(abs(k))
        if sum(i1) == dim:
            stencils.remove(i)

    return stencils  # cross 3x3


def neighbour_coordinates(P):
    stencils = stencil(len(P))
    n = [tuple([sum(x) for x in zip(P, s)]) for s in stencils]
    return n

    # stencils = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] # cube 3x3
    # P = (1, 1)

    # s = (-1, -1)
    # zip(P,s) = [(1, -1), (1, -1)]
    # x = (1, -1)
    # sum(x) = 0
    # x = (1, -1)
    # sum(x) = 0

    # s = (-1, 0)
    # zip(P,s) = [(1, -1), (1, 0)]
    # x = (1, -1)
    # sum(x) = 0
    # x = (1, 0)
    # sum(x) = 1

    # ...

    # neighbours = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def neighbour_values(lab_values, n):
    neighbour_values = []
    for i in n:
        x = i[0]
        y = i[1]
        # print lab_list[x][y]
        neighbour_values.append(lab_values[x][y])
    return neighbour_values


def check_bad_cells(lab_values):
    print lab_values
    counter = 0
    while counter < 100:
        i = 1
        while i < len(lab_values)-1: # number of string
            k = lab_values[i]
            j = 1
            while j < len(k)-1:
                P = lab_values[i][j]
                if P == 0:
                    l = lab_values[i][j - 1]
                    r = lab_values[i][j + 1]
                    u = lab_values[i + 1][j]
                    d = lab_values[i - 1][j]
                    summ = l+r+u+d
                    if summ >=3:
                        lab_values[i][j] = 1
                j += 1
            i += 1
        counter += 1

    return lab_values


def solve_it():
    """
    It takes labirint file from config and prints the way from point 1,1 to 10,10
    https://py.checkio.org/mission/open-labyrinth/
    """


configFilePath = 'input.ini'
config = ConfigParser.ConfigParser()
config.read(configFilePath)
a = config.get('1', 'a')  # take labirint number 1

lab_values = ast.literal_eval(a)  # make list from string

start = lab_values[1][1]  # start position #<type 'list'>
# 5 = start
# 7 = finish
cur_pos = start  # current position
finish = lab_values[10][10]  # final position

P = (10, 10)  # coordinate of current position
# n = neighbour_coordinates(P) # <type 'list'>
# print(n) # coordinates of the neighbors

# print lab_surface # print all the values of the neighbors (wall or way)
lab_values_checked = check_bad_cells(lab_values)


if __name__ == '__main__':
    solve_it()
