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


solver = pywraplp.Solver.CreateSolver('SCIP')

numCredits = sum(credits)

# Variables
model = cp_model.CpModel()

x = [model.NewIntVar(0, M-1, 'x[' + str(i) + ']') for i in range(N)]
obj = model.NewIntVar(0, numCredits, 'obj')
load = [model.NewIntVar(0, numCredits, 'load[' + str(g) + ']')
        for g in range(M)]
y = [[model.NewIntVar(0, 1, 'y[' + str(i) + ',' + str(g) + ']')
      for g in range(M)] for i in range(N)]

# Constraints
for i in range(N):
    model.Add(sum(y[i][g] for g in range(M)) == 1)

for g in range(M):
    model.Add(sum(y[i][g] * credits[i] for i in range(N)) == load[g])
    model.Add(obj >= load[g])

for k in range(len(conflict)):
    i = conflict[k][0]
    j = conflict[k][1]
    model.Add(x[i] != x[j])

for i in range(N):
    for g in range(M):
        model.Add(x[i] == g).OnlyEnforceIf(y[i][g])

for g in range(M):
    for i in range(N):
        if i not in list_class[g]:
            model.Add(x[i] != g)

model.Minimize(obj)
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("obj = %i" % solver.ObjectiveValue())
    for i in range(N):
        print('x[', i, '] = ', solver.Value(x[i]))
    for g in range(M):
        info = ''
        for i in range(N):
            if solver.Value(x[i]) == g:
                info += str(i) + ' '
        info += ' => load = ' + str(solver.Value(load[g]))
        print("class assigned to teacher", g , '=', info)
else:
    print('Not found')