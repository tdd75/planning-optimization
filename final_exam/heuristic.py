from ortools.linear_solver import pywraplp
import time

start = time.time()


def input(filename):
    with open(filename, 'r') as f:
        n, m = [int(i) for i in f.readline().split()]
        d = [float(i) for i in f.readline().split()]
        t = [float(i) for i in f.readline().split()]
        D = []
        for i in range(n):
            D.append([int(i) for i in f.readline().split()[1:]])
        c = []
        for i in range(n):
            c.append([int(i) for i in f.readline().split()])
        return n, m, d, t, D, c


n, m, d, t, D, c = input('final_exam/input/3.txt')

for i in range(n):
    print('{}:'.format(i), end=' ')
    for j in range(n):
        if c[i][j] == 1 and i != j:
            print(j, end=' ')
    print()

tc = [[0 for j in range(m)] for i in range(n)]
for i in range(len(D)):
    for j in D[i]:
        tc[i][j] = 1

x = [[solver.IntVar(0, 1, 'x({}, {})'.format(i, j))
      for j in range(m)] for i in range(n)]


print('Time = {}s'.format(round(time.time() - start, 2)))
