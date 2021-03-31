import numpy as np
import time
import pandas as pd

cmin = 1e9


def input(filename):
    global N, c
    with open(filename) as f:
        for line in f:
            N = int(line)  # read the number of points
            print('N = ', N)
            break

        c = [[int(num) for num in line.split()]
             for line in f]  # read the whole distance matrix

    return N, c


N, c = input('TSP-4.txt')
print(N, c)

x = [0 for i in range(N)]
visited = [False for i in range(N)]
f = 0
f_best = 1e9


def SortedCandidates(cur):
    cand = []
    for v in range(N):
        if visited[v] == False:
            cand.append(v)

    # sort elements in cand in an increasing order of the distance from cur
    cand.sort(key=lambda x: c[cur][x])
    return cand


def updateBest():
    global f_best

    if f + c[x[N-1]][x[0]] < f_best:
        f_best = f + c[x[N-1]][x[0]]
        print('update best ', f_best)


# try all values for x[k], being aware x[0],x[1],...,x[k-1], length = f
def Try(k):
    global f, x, visited

    cand = SortedCandidates(x[k-1])
    #print('Try(',k,' cand = ',cand)
    for v in cand:
        x[k] = v
        f = f + c[x[k-1]][x[k]]
        visited[v] = True

        if k == N-1:
            updateBest()
        else:
            if f + cmin*(N-k) < f_best:
                Try(k+1)

        visited[v] = False  # recover when backtracking
        f = f - c[x[k-1]][x[k]]


for i in range(N):
    for j in range(N):
        if i != j and cmin > c[i][j]:
            cmin = c[i][j]

x[0] = 0
visited[0] = True
Try(1)

f = open('result.txt', 'w')
f.write(str(f_best))
f.close()
