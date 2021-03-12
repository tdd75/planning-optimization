n = 0
c = [0][0] * 100
mark = []
cmin = 999999999
best = 999999999
curr = 0
mark = [0] * 100
x = [0] * 100

def TRY(k):
    if k > n:
        best = min(best, curr + c[x[k-1][1]])
        return
    for i in range(2, n + 1):
        if not(mark[i]) and c[x[k-1]][i]:
            x[k] = i
            mark[i] = 1
            curr += c[x[k - 1]][i]
            if curr + cmin * (n - k + 1) < best:
                TRY(k+1)
            curr -= c[x[k - 1]][i]
            mark[i] = 0


with open('input.txt') as f:
    n = int(next(f))
    for line in f:
        c.append([int(x) for x in line.split()])


# x[1] = 1
TRY(2)
print(best);
# f = open('result.txt', 'w+')
# f.write(str(a+b))
# f.close()