# coding: utf8
import ConfigParser
import ast
from itertools import product
import itertools


def go(lab_values, i, j):
    if i < 4 and j < 4:
        if lab_values[i][j+1] == 0 or lab_values[i][j+1] == 7: #right
            print '>'
            return i, j+1
        elif lab_values[i+1][j] == 0 or lab_values[i+1][j] == 7: #down
            print 'v'
            return i+1, j
        elif lab_values[i][j-1] == 0 or lab_values[i][j-1] == 7: #left
            print '<'
            return i, j-1
        elif lab_values[i-1][j] == 0 or lab_values[i-1][j] == 7: #up
            print '^'
            return i-1, j
        else:
            return False
    else:
        return False


def check_bad_cells(lab_values):
    print lab_values
    counter = 0
    while counter < 100:
        i = 1
        while i < len(lab_values)-1: # number of string
            k = lab_values[i]
            j = 1
            while j < len(k)-1: # number of rows
                P = lab_values[i][j]
                if P == 0:
                    l = lab_values[i][j - 1]
                    r = lab_values[i][j + 1]
                    u = lab_values[i - 1][j]
                    d = lab_values[i + 1][j]
                    summ = l+r+u+d
                    if summ ==3:
                        lab_values[i][j] = 1
                j += 1
            i += 1
        counter += 1
    print lab_values
    return lab_values

# далее найти все перекрёстки
# рандомно выбирая направление пути из 4х идти куда-либо, если дойти до финиша, то запомнить путь

def solve_it():
    """
    It takes labirint file from config and prints the way from point 1,1 to 10,10
    https://py.checkio.org/mission/open-labyrinth/
    """

configFilePath = 'input.ini'
config = ConfigParser.ConfigParser()
config.read(configFilePath)
a = config.get('1', 'b')  # take labirint number 1

lab_values = ast.literal_eval(a)  # make list from string

start = 5
finish = 7
cur_pos = start

lab_values_checked = check_bad_cells(lab_values)
i = 1
j = 1
while cur_pos != finish:
    i,j = go(lab_values, i, j)
    cur_pos = lab_values[i][j]


if __name__ == '__main__':
    solve_it()
