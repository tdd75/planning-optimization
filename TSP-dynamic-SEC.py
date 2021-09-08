from ortools.linear_solver import pywraplp
import numpy as np
import random as rd

def genData(filename, n):
    f = open(filename, 'w')
    f.write(str(n) + '\n')
    for i in range(n):
        s = ''
        for j in range(n):
            x = rd.randint(1, 50)
            s = s+str(x) + ' '
        f.write(s+'\n')
    f.close()

def input(filename):
    with open(filename, 'r') as f:
        [n] = [int(x) for x in f.readline().split()]
        # print(f.readline())
        c = []
        for i in range(n):
            c.append([int(x) for x in f.readline().split()])
        return n, c


n, c = input('TSP-10.txt')

def CreateSolverAndVariable(n, c):
    solver = pywraplp.Solver.CreateSolver('CBC')
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = solver.IntVar(
                    0, 1, 'x(' + str(i) + ',' + str(j) + ')')
    return x, solver


def CreateFlowConstraint(n, solver, x):
    # flow balance CreateFlowConStraint
    for j in range(n):
        cstr = solver.Constraint(1, 1)
        for i in range(n):
            if i != j:
                cstr.SetCoefficient(x[i, j], 1)

        cstr = solver.Constraint(1, 1)
        for i in range(n):
            if i != j:
                cstr.SetCoefficient(x[j, i], 1)


def CreateSECConStraint(solver, x, SEC):
    # SEC
    for s in SEC:
        cstr = solver.Constraint(0, len(s)-1)
        for i in s:
            for j in s:
                if i != j:
                    cstr.SetCoefficient(x[i, j], 1)


def CreateObjective(n, c, solver, x):
    # objective
    obj = solver.Objective()
    for i in range(n):
        for j in range(n):
            if i != j:
                obj.SetCoefficient(x[i, j], c[i][j])
    obj.SetMinimization()


def SolveDynSEC(n, c, SEC):
    x, solver = CreateSolverAndVariable(n, c)
    CreateFlowConstraint(n, solver, x)
    CreateSECConStraint(solver, x, SEC)
    CreateObjective(n, c, solver, x)
    result_status = solver.Solve()

    assert result_status == pywraplp.Solver.OPTIMAL
    print('objective = ', solver.Objective().Value())

    y = np.array([[0 for i in range(n)]for j in range(n)])
    for i in range(n):
        for j in range(n):
            if i != j:
                y[i, j] = x[i, j].solution_value()
    return y


def FindNext(y, s):
    for i in range(n):
        if i != s and y[s, i] > 0:
            return i
    return -1


def ExtractCycle(x, s):
    S = set()
    C = []
    i = s
    C.append(s)
    S.add(s)
    while True:
        i = FindNext(x, i)
        if i == -1:
            return []
        if i in S:
            return C
        else:
            S.add(i)
            C.append(i)


def SolveTSPDynSEC(n, c):
    SEC = []
    while True:
        x = SolveDynSEC(n, c, SEC)
        mark = [False for v in range(n)]
        for s in range(n):
            if mark[s] == False:
                C = ExtractCycle(x, s)
                if len(C) == n:
                    return C
                else:
                    SEC.append(C)
                    for e in C:
                        mark[e] = True


cycle = SolveTSPDynSEC(n, c)
print('optimal tour TSP = ', cycle)