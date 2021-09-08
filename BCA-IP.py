import numpy as np
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


solver = pywraplp.Solver.CreateSolver('SCIP')

numCredits = sum(credits)

# Modeling with or-tools
x = [[solver.IntVar(0, 1, 'x(' + str(i) + ',' + str(j) + ')')
      for j in range(M)] for i in range(N)]
y = solver.IntVar(0, numCredits, 'y')
print('y:', y)

# constraint: 1 <= a1x1 + a2x2 + ... + anxn <= u
# Constraint between teacher and class
for i in range(M):
    for j in range(N):
        if tc[i][j] == 0:
            c = solver.Constraint(0, 0)
            c.SetCoefficient(x[j][i], 1)

# Conflict
for i in range(M):
    for j in range(N):
        if f[i][j] == 1:
            for k in range(M):
                c = solver.Constraint(0, 1)
                c.SetCoefficient(x[i][k], 1)
                c.SetCoefficient(x[j][k], 1)

for i in range(N):
    c = solver.Constraint(1, 1)
    for j in range(M):
        c.SetCoefficient(x[i][j], 1)

# Constraint on load of teachers
for j in range(M):
    c = solver.Constraint(-solver.infinity(), 0)
    c.SetCoefficient(y, -1)
    for i in range(N):
        c.SetCoefficient(x[i][j], credits[i])


obj = solver.Objective()
obj.SetCoefficient(y, 1)
obj.SetMinimization()

result_status = solver.Solve()
print('status', result_status)
# The problem has an optimal solution
assert result_status == pywraplp.Solver.OPTIMAL
print('objective = ', solver.Objective().Value())
for i in range(N):
    for j in range(M):
        if x[i][j].solution_value() > 0:
            print('Class ', i, 'assigned to teacher', j)

for j in range(M):
    info = ''
    for i in range(N):
        if x[i][j].solution_value() > 0:
            info = info + str(i) + ' '
    print('Teacher {}: {}'.format(j, info))
