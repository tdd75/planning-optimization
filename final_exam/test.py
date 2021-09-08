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


filename = '20183515-1'
n, m, d, t, D, c = input('final_exam/input/{}.txt'.format(filename))
index_file = filename[-1]

solver = pywraplp.Solver.CreateSolver('SCIP')

# Variables
x = [[solver.IntVar(0, 1, 'x({}, {})'.format(i, j))
      for j in range(m)] for i in range(n)]

# Constraints
for i in range(n):
    for j in range(m):
        if j not in D[i]:
            solver.Add(x[i][j] == 0)

for i in range(n):
    for j in range(n):
        if c[i][j] == 1 and j > i:
            for k in range(m):
                if k in D[i] and k in D[j]:
                    solver.Add(x[i][k] + x[j][k] <= 1)

for j in range(m):
    c = solver.Constraint(0, t[j])
    for i in range(n):
        if j in D[i]:
            c.SetCoefficient(x[i][j], d[i])

for i in range(n):
    c = solver.Constraint(0, 1)
    for j in D[i]:
        c.SetCoefficient(x[i][j], 1)

# Objectives
obj = solver.Objective()
for i in range(n):
    for j in D[i]:
        obj.SetCoefficient(x[i][j], 1)
obj.SetMaximization()

result_status = solver.Solve()
assert result_status == pywraplp.Solver.OPTIMAL

# Print output
for j in range(m):
    info = ''
    for i in range(n):
        if x[i][j].solution_value() > 0:
            info = info + str(i) + ' '
    print('Teacher {}: {}'.format(j, info))

# Write output to file
with open('final_exam/20183515-{}-out.txt'.format(index_file), 'w') as f_out:
    for i in range(n):
        check = False
        for j in range(m):
            if x[i][j].solution_value() > 0:
                f_out.write('{} {}\n'.format(i, j))
                check = True
                break
        if check == False:
            f_out.write('{} {}\n'.format(i, -1))
    f_out.write('{}\n'.format(int(solver.Objective().Value())))

print('Objective = {}'.format(int(solver.Objective().Value())))

print('Time = {}s'.format(round(time.time() - start, 2)))
