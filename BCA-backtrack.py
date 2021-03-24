from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp


def input(filename):
    with open(filename, 'r') as f:
        [M, N] = [int(x) for x in f.readline().split()]
        c = [int(x) for x in f.readline().split()]
        list_class = []
        for g in range(M):
            list_class.append([int(x) for x in f.readline().split()])
        [K] = [int(x) for x in f.readline().split()]
        conflict = []
        for k in range(K):
            conflict.append([int(x) for x in f.readline().split()])
        return M, N, c, list_class, conflict


M, N, credits, list_class, conflict = input('BCA.txt')

tc = [[0 for c in range(N)] for g in range(M)]
for i in range(len(list_class)):
    for j in list_class[i]:
        tc[i][j] = 1


f = [[0 for i in range(N)] for j in range(N)]
for i in range(len(conflict)):
    c1 = conflict[i][0]
    c2 = conflict[i][1]
    f[c1][c2] = 1

x = [0 for i in range(N)]
load = [0 for g in range(M)]
f_best = 1000000

def Check(v, k):
    if tc[v][k] == 0:
        return False
    for i in range(0, k):
        if f[i][k] and v == x[i]:
            return False
    return True


def UpdateBest():
    global f_best
    max_load = max(load)
    if max_load < f_best:
        f_best = max_load
        print('update best', f_best)


def Try(k):
    for v in range(M):
        if Check(v, k):
            x[k] = v
            load[v] += credits[k]
            if k == N - 1:
                UpdateBest()
            else:
                Try(k+1)
            load[v] -= credits[k]


Try(0)
