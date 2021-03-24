from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
print('create solver OK')

INF = solver.infinity()

x1 = solver.NumVar(0, INF, 'x1')
x2 = solver.NumVar(0, INF, 'x2')
x3 = solver.NumVar(0, INF, 'x3')
x4 = solver.NumVar(0, INF, 'x4')
x5 = solver.NumVar(0, INF, 'x5')
x6 = solver.NumVar(0, INF, 'x6')
x7 = solver.NumVar(0, INF, 'x7')


# constraint: x1 + x4 + 6x6 = 9
c1 = solver.Constraint(9, 9)
c1.SetCoefficient(x1, 1)
c1.SetCoefficient(x4, 1)
c1.SetCoefficient(x6, 6)

# constraint: 3x1 + x2 - 4x3 + 2x6 + x7 = 2
c2 = solver.Constraint(2, 2)
c2.SetCoefficient(x1, 3)
c2.SetCoefficient(x2, 1)
c2.SetCoefficient(x3, -4)
c2.SetCoefficient(x6, 2)
c2.SetCoefficient(x7, 1)

# constraint: x1 + 2x2 + x5 + 2x6 = 6
c3 = solver.Constraint(6, 6)
c3.SetCoefficient(x1, 1)
c3.SetCoefficient(x2, 2)
c3.SetCoefficient(x5, 1)
c3.SetCoefficient(x6, 2)

# 
obj = solver.Objective()
obj.SetCoefficient(x1, 1)
obj.SetCoefficient(x2, -6)
obj.SetCoefficient(x3, 32)
obj.SetCoefficient(x4, 1)
obj.SetCoefficient(x5, 1)
obj.SetCoefficient(x6, 10)
obj.SetCoefficient(x7, 100)

result_status = solver.Solve()

# The problem has an optimal solution
assert result_status == pywraplp.Solver.OPTIMAL
print('Optimal objective value = %f ' % solver.Objective().Value())

print('x1 =', x1.solution_value())
print('x2 =', x2.solution_value())
print('x3 =', x3.solution_value())
print('x4 =', x4.solution_value())
print('x5 =', x5.solution_value())
print('x6 =', x6.solution_value())
print('x7 =', x7.solution_value())

