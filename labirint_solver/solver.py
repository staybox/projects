# coding: utf8
import ConfigParser
import ast
from itertools import product


def stencil(dim):
    stencils = list(product([-1,0,1], repeat=dim))
    zero = ((0,) * dim)
    stencils.remove(zero) #(0, 0)
    # we need only horizontal neighbors, not diagonals
    for i in stencils:
        i1 = []
        for k in i:
            i1.append(abs(k))
        if sum(i1) == dim:
            stencils.remove(i)

    return stencils # cross 3x3


def neighbours(P):
    stencils = stencil(len(P))
    return [tuple([sum(x) for x in zip(P,s)]) for s in stencils]

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





def solve_it():
    """
    It takes labirint file from config and prints the way from point 1,1 to 10,10
    https://py.checkio.org/mission/open-labyrinth/
    """
configFilePath = 'input.ini'
config = ConfigParser.ConfigParser()
config.read(configFilePath)
a = config.get('1', 'a') # take labirint number 1

lab_list = ast.literal_eval(a) # make list from string

start = lab_list[1][1] #start position #<type 'list'>

cur_pos = start # current position
finish = lab_list[10][10] #final position

P = (10, 10) # coordinate of current position
n = neighbours(P) # <type 'list'>
print(n) # coordinates of the neighbors

for i in n:
    x = i[0]
    y = i[1]
    print lab_list[x][y]
    

if __name__ == '__main__':
    solve_it()