import random as rd


def violations():
    v = 0
    for i in range(n-1):
        for j in range(i + 1, n):
            if x[i] == x[j]:
                v += 1
            if x[i] + i == x[j] + j:
                v += 1
            if x[i] - i == x[j] - j:
                v += 1
    return v


def generate_initial_solution():
    for i in range(n):
        x[i] = 0


def violations_q(q):
    v = 0
    for i in range(n):
        if i != q:
            if x[i] == x[q]:
                v += 1
            if x[i] + i == x[q] + q:
                v += 1
            if x[i] - i == x[q] - q:
                v += 1
    return v


def select_most_violating_queen():
    sel_q = 1
    max_violations = 0
    cand = []
    for q in range(n):
        vq = violations_q(q)
        if max_violations < vq:
            max_violations = vq
            cand.clear()
            cand.append(q)
        elif max_violations == vq:
            cand.append(q)

    idx = rd.randint(0, len(cand) - 1)
    sel_q = cand[idx]
    return sel_q


def violations_q_r(q, r):
    # return the violations if x(q) is assigned to r
    old = x[q]
    x[q] = r
    v = violations()
    x[q] = old
    return v


def select_most_promissing_row(q):
    min_violations = 1e9
    sel_r = -1
    cand = []
    for r in range(n):
        vr = violations_q_r(q, r)
        if min_violations > vr:
            min_violations = vr
            cand.clear()
            cand.append(r)
        elif min_violations == vr:
            cand.append(r)

    idx = rd.randint(0, len(cand) - 1)
    sel_r = cand[idx]
    return sel_r


def solve():
    generate_initial_solution()

    for k in range(10000):
        q = select_most_violating_queen()
        v = select_most_promissing_row(q)
        x[q] = v
        v = violations()
        print('step', k, 'assign x[', q, '] = ',
              v, 'violations = ', violations())
        if v == 0:
            print(x)
            break


n = 10
x = [0 for i in range(n)]
solve()