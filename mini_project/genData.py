import random
# import math
import numpy as np

print('nhap n,m,k: ')
n=int(input())
m=int(input())
K=int(input())

# const
min_q= int((n+m)*random.uniform(1, 1.2))  # min max mỗi điểm nhận/ trả hàng 
max_q= int((n+m)*random.uniform(1.8, 2.5)) 

min_Q= min_q * int((m/K) + random.randint(-1, 1)) + random.randint(-2,2)  
min_Q = max(min_Q, min_q)
max_Q= max_q * int((m/K) + random.randint(1, 3)) + random.randint(-2,2)
R = n*2+m*2+random.randint(1,5)

def distance(point1, point2):
	return int(np.linalg.norm(point1-point2))

point = [np.array([0,0]) ]
while len(point) != 2*n+2*m+1:
    p = np.array([random.uniform(2, R), random.uniform(2, R)])
    verify = 0 # xac nhan các điểm không quá gần
    for p1 in point:
        if distance(p, p1) < 1:
            verify += 1
    if verify == 0: 
        point.append(p)

d=[[0 for i in range(2*n+2*m+1)] for j in range(2*n+2*m+1)]
for i in range(2*n+2*m+1):
	for j in range(2*n+2*m+1):
		if j!=i:
			d[i][j]=distance(point[i], point[j]) 
q=[random.randint(min_q, max_q+1) for i in range(m) ]
Q=[random.randint(min_Q, max_Q+1) for i in range(K) ]


with open('project/data_{}_{}_{}.txt'.format(n,m,K), 'w') as f:
	f.writelines(str(n)+ ' '+str(m)+ ' '+str(K)+' '+'\n')
	for i in range(m):
		f.write(str(q[i])+' ')
	f.write('\n')
	for i in range(K):
		f.write(str(Q[i])+' ')
	f.write('\n')
	for i in range(2*n+2*m+1):
		for j in range(2*n+2*m+1):
			f.write(str(d[i][j])+' ')
		f.write('\n')

print('done')