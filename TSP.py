from ortools.linear_solver import pywraplp

class SubSetGeneration:
    def __init__(self, n):
        self.n = n
        self.x = [0 for i in range(n)]

    def solution(self):
        s = []
        for i in range(self.n):
            if self.x[i] == 1:
                s.append(i)
        self.subset.append(s)

    def Try(self, k):
        for v in range(2):
            self.x[k] = v
            if k == self.n-1:
                self.solution()
            else:
                self.Try(k+1)

    def generate(self):
        self.subset = []
        self.Try(0)
        return self.subset


c = [[0,6,4,2],[5,0,6,1],[1,2,0,8],[3,2,5,0]]
n = len(c)

SG = SubSetGeneration(n)
subsets = SG.generate()
for s in subsets:
    print(s)

solver = pywraplp.Solver.CreateSolver('CBC')
x = {}
for i in range(n):
    for j in range(n):
        if i != j:
            x[i, j] = solver.IntVar(0, 1, 'x(' + str(i) + ',' + str(j) + ')')

for j in range(n):
    cstr = solver.Constraint(1, 1)
    for i in range(n):
        if i != j:
            cstr.SetCoefficient(x[j, i], 1)


for s in subsets:
    if len(s) >= 2 and len(s) < n:
        cstr = solver.Constraint(0, len(s)-1)
        for i in s:
            for j in s:
                if i != j:
                    cstr.SetCoefficient(x[i, j], 1)

obj = solver.Objective()
for i in range(n):
    for j in range(n):
            if i != j:
                obj.SetCoefficient(x[i, j], c[i][j])
obj.SetMinimization()

result_status = solver.Solve()

assert result_status == pywraplp.Solver.OPTIMAL
print('objective = ', solver.Objective().Value())

for i in range(n):
	for j in range(n):
		if i !=j and x[i, j].solution_value() > 0:
			print(i,j)