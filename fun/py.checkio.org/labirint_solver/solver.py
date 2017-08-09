# coding: utf8
import ConfigParser
import ast
import locale

def print_lab(lab_values):
    for i in lab_values:
        b = []
        for j in i:
            if j == 1:
                j='\xe2\x96\xa0'#''■'
            if j == 0:
                j='\xe2\x96\xa1' #'□'
            if j == 7:
                j='\xe2\x96\xa1' #'□'
            b.append(j)
            #print (j)
        print locale.getlocale()
        print b


def go(lab_values, i, j, prev_direction):
    if i < len(lab_values)-1 and j < len(lab_values[i])-1:
        if lab_values[i][j+1] != 1 and prev_direction != '<': #right
            return i, j+1, '>'
        elif (lab_values[i+1][j] != 1) and prev_direction != '^': #down
            return i+1, j, 'v'
        elif lab_values[i][j-1] != 1 and prev_direction != '>': #left
            return i, j-1, '<'
        elif lab_values[i-1][j] != 1 and prev_direction != 'v': #up
            return i-1, j, '^'
        else:
            return False
    else:
        return False


def check_bad_cells(lab_values):
    counter = 0
    while counter < 100:
        i = 1
        while i < len(lab_values)-1: # number of string
            k = lab_values[i]
            j = 2
            while j < len(k)-1: # number of rows
                P = lab_values[i][j]
                if P == 0:
                    # find dead one end
                    l = lab_values[i][j - 1]
                    r = lab_values[i][j + 1]
                    u = lab_values[i - 1][j]
                    d = lab_values[i + 1][j]
                    summ = l+r+u+d
                    if summ ==3:
                        lab_values[i][j] = 1
                    # find dead one couple
                    if i < len(lab_values)-2 and j< len(k)-2:
                        ld = lab_values[i+1][j - 1]
                        dd = lab_values[i+2][j]
                        summ2 = u+l+ld+dd
                        if d ==0 and summ2 == 4:
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

finish = 7
cur_pos = 0
#print_lab(lab_values)
lab_values_checked = check_bad_cells(lab_values)
i = 1
j = 1
way = []
prev_direction = '>'
while cur_pos != finish:
    i,j, direction = go(lab_values, i, j, prev_direction)
    cur_pos = lab_values[i][j]
    prev_direction = direction
    way.append(direction)
print way


if __name__ == '__main__':
    solve_it()
