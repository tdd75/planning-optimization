from ortools.linear_solver import pywraplp
import numpy as np
import time

start_time = time.time()

with open('data_3_4_2.txt', 'r') as file:
    M, N, K = [int(x) for x in file.readline().split()]
    # Số hành khách
    p = [0]*(2*(M+N)+2*K+1)
    for i in range(1, M+1):
        p[i] = 1
    for i in range(M+N+1, M+N+1+M):
        p[i] = -1
    # Trọng lượng hàng
    q = [0]*(2*(M+N)+2*K+1)
    for index, X in enumerate(file.readline().split()):
        q[index+M+1] = int(X)
        q[index+2*M+N+1] = -int(X)
    # Trọng tải xe
    Q = [0] * (K+1)
    for index, X in enumerate(file.readline().split()):
        Q[index + 1] = int(X)
    # Quãng đường
    d = [[int(i) for i in file.readline().split()] for j in range(2*(M+N)+1)]


def expand_start(d):
    n = 2*(M+N)
    n_expand = 2*(M+N)+2*K
    d_expand = np.zeros((n_expand+1, n_expand+1), dtype=int)
    for i in range(1, n+1):
        for j in range(1, n+1):
            d_expand[i][j] = d[i][j]
    for i in range(n+1, n_expand+1):
        for j in range(1, n+1):
            d_expand[i][j] = d[0][j]
    for i in range(1, n+1):
        for j in range(n+1, n_expand+1):
            d_expand[i][j] = d[i][0]
    return d_expand


d = expand_start(d)
print(M, N, K)
print(p)
print(q)
print(Q)

# K = 1
# Q[1] = max(Q)
# for row in d:
#     print(row)

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = 10000

B = {i for i in range(1, 2*(M+N)+2*K+1)}

B_2d, F1, F2, F3, F4, F5, F6 = set(), set(), set(), set(), set(), set(), set()
for i in B:
    for j in B:
        B_2d.add((i, j))
# Điểm đón khách
for (i, j) in B_2d:
    if ((i in range(1, M+1))) and \
    (j in range(M+1, M+N+1) or j in range(2*M+N+1, 2*(M+N)+1) or j == i + M+N):
        F1.add((i, j))
# Điểm nhận hàng 
for (i, j) in B_2d:
    if ((i in range(M+1, M+N+1))) and (j in range(1, 2*(M+N)+1)):
        F2.add((i, j))
# Điểm trả khách
for (i, j) in B_2d:
    if (i in range(M+N+1, 2*M+N+1)) \
        and (j != i-N-M or (j in range(M+1, M+N+1)) \
        or (j in range(2*M+N+1, 2*(M+N)+1)) or (j in range(2*(M+N)+K+1, 2*(M+N)+2*K+1))):
        F3.add((i, j))
# Điểm trả hàng
for (i, j) in B_2d:
    if (i in range(2*M+N+1, 2*(M+N)+1)) and j!=i-M-N and (j not in range(2*(M+N)+1, 2*(M+N)+K+1)):
        F4.add((i, j))
# Điểm xuất phát
for (i, j) in B_2d:
    if (i in range(2*(M+N)+1, 2*(M+N)+K+1)) and ((j in range(1, (M+N)+1)) or j==i+K):
        F5.add((i, j))
# Đi tại chỗ
for i in B:
    F6.add((i, i))
A = F1.union(F2).union(F3).union(F4).union(F5)
A -= F6
# print(A)

Ap = [[] for i in range(len(A))]
Am = [[] for i in range(len(A))]
for (i, j) in A:
    Ap[i].append(j)
    Am[j].append(i)

X, L, P, W, Z, W_max = {}, {}, {}, {}, {}, {}
for (i, j) in A:
    X[i, j] = solver.BoolVar('X({},{})'.format(i, j))
for i in B:
    L[i] = solver.IntVar(0, INF, 'L({})'.format(i))
    P[i] = solver.BoolVar('P({})'.format(i))
    Z[i] = solver.IntVar(1, K, 'Z({})'.format(i))
    W_max[i] = solver.IntVar(0, INF, 'W_max({})'.format(i))

for k in range(1, K+1):
    for i in B:
        W[i] = solver.IntVar(0, INF, 'W({})'.format(i))

### Constraints
# Cân bằng luồng
for i in range(1, 2*(M+N)+1):
    c = solver.Constraint(1, 1)
    for j in Ap[i]:
        c.SetCoefficient(X[i, j], 1)

    c = solver.Constraint(1, 1)
    for j in Am[i]:
        c.SetCoefficient(X[j, i], 1)

for i in range(2*(M+N)+1, 2*(M+N)+K+1):
    c = solver.Constraint(1, 1)
    for j in Ap[i]:
        c.SetCoefficient(X[i, j], 1)
    
    c = solver.Constraint(1, 1)
    for j in Am[i+K]:
        c.SetCoefficient(X[j, i+K], 1)

    c = solver.Constraint(0, 0)
    for j in Am[i]:
        c.SetCoefficient(X[j, i], 1)

    c = solver.Constraint(0, 0)
    for j in Ap[i+K]:
        c.SetCoefficient(X[i+K, j], 1)

# Điểm đón và điểm trả cùng xe
for i in range(1, M+N+1):
    solver.Add(Z[i+(M+N)] == Z[i])

# Tồn tại đường đi
for (i, j) in A:
    solver.Add(INF*(1-X[i,j]) + Z[j] >= Z[i])
    solver.Add(INF*(1-X[i,j]) + Z[i] >= Z[j])
    solver.Add(INF*(1-X[i,j]) + W_max[j] >= W_max[i])
    solver.Add(INF*(1-X[i,j]) + W_max[i] >= W_max[j])
    solver.Add(INF*(1-X[i,j]) + L[j] >= L[i] + int(d[i][j]))
    solver.Add(INF*(1-X[i,j]) + L[i] + int(d[i][j]) >= L[j])
    solver.Add(INF*(1-X[i,j]) + P[j] >= P[i] + p[j])
    solver.Add(INF*(1-X[i,j]) + P[i] + p[j] >= P[j])
    solver.Add(INF*(1-X[i,j]) + W[j] >= W[i] + q[j])
    solver.Add(INF*(1-X[i,j]) + W[i] + q[j] >= W[j])
    
# Điều kiện điểm trả sau điểm đón
for i in range(1, M+N+1):
    solver.Add(L[i+(M+N)] >= L[i] + int(d[i][i+(M+N)]))

# Điều kiện tải trọng
for i in range(1, 2*(M+N)):
    solver.Add(W[i] <= W_max[i])

# Khởi tạo
for k in range(1, K+1):
    solver.Add(L[2*(M+N)+k] == 0)
    solver.Add(P[2*(M+N)+k] == 0)
    solver.Add(W[2*(M+N)+k] == 0)
    solver.Add(W_max[2*(M+N)+k] == Q[k])
    solver.Add(Z[2*(M+N)+k] == k)
    solver.Add(Z[2*(M+N)+K+k] == k)

# Objective
obj = solver.Objective()
for (i, j) in A:
    obj.SetCoefficient(X[i, j], int(d[i][j]))
obj.SetMinimization()

result_status = solver.Solve()
assert result_status == pywraplp.Solver.OPTIMAL

print('optimal objective value: %.2f' % solver.Objective().Value())

# print route
for k in range(1, K+1):
    print("Vehicle {}:".format(k))
    rs = [None] * (2*(M+N) + 2*K+1)
    for (i, j) in A:
        if X[i, j].solution_value() > 0 and Z[i].solution_value() == k:
            rs[i] = j
            print(i, j, P[j].solution_value(),
                  W[j].solution_value(), L[j].solution_value())
    start = 0
    for i in range(K+2*(M+N), 2*(M+N)-1, -1):
        if(rs[i] != None):
            start = i
            end = i+K
            break

    if(rs[start]):
        print('{} -> '.format(2*(M+N)+k), end="")
        cur_index = rs[start]
        while(rs[cur_index]):
            print('{} -> '.format(cur_index), end="")
            cur_index = rs[cur_index]
        print('{}'.format(2*(M+N)+k+K))
    else:
        print('{} -> {}'.format(2*(M+N)+k, 2*(M+N)+k+K))
print(time.time() - start_time)
