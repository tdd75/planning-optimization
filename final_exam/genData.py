import random
import math


n = 500
m = 50

c = [[0 for i in range(n)] for i in range(n)]
# number = random.randint(10000, 10000)
number = 50000
listS = [i for i in range(n)]
for i in range(number):
    coup = random.sample(set(listS), 2)
    c[coup[1]][coup[0]] = 1
    c[coup[0]][coup[1]] = 1
for i in range(n):
    c[i][i] = 1


with open('final_exam/input/20183515-1.txt', 'w') as f:
    f.writelines(str(n) + ' '+str(m)+' '+'\n')
    for i in range(n):
        f.write(str(random.randint(2, 5))+' ')
    f.write('\n')
    for i in range(m):
        f.write(str(int(random.randint(10, 24)*n/m))+' ')
    f.write('\n')
    gv = [int(i) for i in range(m)]
    for i in range(n):
        number = random.randint(0, m/5)
        listGV = random.sample(set(gv), number)
        f.write(str(number)+' ')
        for i in range(number):
            f.write(str(listGV[i])+' ')
        f.write('\n')

    for i in range(n):
        for j in range(n):
            f.write(str(c[i][j])+' ')
        f.write('\n')
