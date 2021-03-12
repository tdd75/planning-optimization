from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('CBC')
print('create solver OK')

INF = solver.infinity()

x1 = solver.NumVar(0, 14, 'x1')
x2 = solver.IntVar(0, 20, 'x2')

# constraint: -INF <= x1 - 10x2 <= 7
c1 = solver.Constraint(-INF, 7)
c1.SetCoefficient(x1, 1)
c1.SetCoefficient(x2, -10)

# constraint: -INF <= 2x1 + 3x2 <= 20
c2 = solver.Constraint(-INF, 20)
c2.SetCoefficient(x1, 2)
c2.SetCoefficient(x2, 3)

# 
obj = solver.Objective()
obj.SetCoefficient(x1, 1)
obj.SetCoefficient(x2, 1)
obj.SetMaximization()

result_status = solver.Solve()

# The problem has an optimal solution
assert result_status == pywraplp.Solver.OPTIMAL
print('Optimal objective value = %f ' % solver.Objective().Value())

print('x1 =', x1.solution_value())
print('x2 =', x2.solution_value())

