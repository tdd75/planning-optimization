from ortools.sat.python import cp_model

n = 8
model = cp_model.CpModel()

# decision variables
x = [model.NewIntVar(0, n-1, 'x[' + str(i) + ']') for i in range(n)]
y1 = [model.NewIntVar(0, 2*n-2, 'y1[' + str(i) + ']') for i in range(n)]
y2 = [model.NewIntVar(0, 2*n-2, 'y2[' + str(i) + ']') for i in range(n)]

# state constraints of the problem
for i in range(n):
    model.Add(y1[i] == x[i] + i)
for i in range(n):
    model.Add(y2[i] == x[i] - i + n - 1)

model.AddAllDifferent(x)
model.AddAllDifferent(y1)
model.AddAllDifferent(y2)

# backtracking search
solver = cp_model.CpSolver()
status = solver.Solve(model)

for i in range(n):
    print('x[', i, '] =', solver.Value(x[i]))