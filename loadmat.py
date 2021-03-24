# a = "1, 2, 3, 4, 5"
# [n] = [int(x) for x in a.split(",")]
# for cha in n:
#     print(cha)

with open(filename, 'r') as f:
    [n] = [int(x) for x in f.readline().split()]
    # print(f.readline())
    c = []
    for i in range(n):
        c.append([int(x) for x in f.readline().split()])
