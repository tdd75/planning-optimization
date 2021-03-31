def check(v, k):
    # check if v can be assigned to x[k] without violating the constraints
    return mr[v] == False and md1[v + k] == False and md2[v - k + n - 1] == False

def Solution():
    global found
    found = True
    print('FOUND')
    print(x)


def Try(k):
    if found:
        return
    for v in range(n):
        if check(v, k):
            x[k] = v
            mr[v] = True
            md1[x[k] + k] = True
            md2[x[k] - k + n - 1] = True
            if k == n - 1:
                Solution()
            else:
                Try(k + 1)
            # recover then backtracking
            mr[v] = False
            md1[x[k] + k] = False
            md2[x[k] - k + n - 1] = False

found = False
n = 6
x = [0 for i in range(n)]
mr = [False for i in range(n)]
md1 = [False for i in range(0, 2 * n - 1)]
md2 = [False for i in range(0, 2 * n - 1)]

Try(0)