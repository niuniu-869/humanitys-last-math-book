#!/usr/bin/env python3
from fractions import Fraction


def lis(a):
    d = []
    for i, x in enumerate(a):
        d.append(1 + max([d[j] for j in range(i) if a[j] < x] or [0]))
    return d, max(d)


def lcs(x, y):
    c = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            c[i][j] = c[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else max(c[i - 1][j], c[i][j - 1])
    return c


def edit(x, y):
    e = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(len(x) + 1): e[i][0] = i
    for j in range(len(y) + 1): e[0][j] = j
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            e[i][j] = min(e[i - 1][j] + 1, e[i][j - 1] + 1,
                          e[i - 1][j - 1] + int(x[i - 1] != y[j - 1]))
    return e


def mcm(p):
    n = len(p) - 1
    m = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            m[i][j] = min(m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                           for k in range(i, j))
    return m


def max_subarray(a):
    g = []
    for x in a:
        g.append(x + max(0, g[-1] if g else 0))
    return g, max(g)


def nonadjacent(a):
    f = [0]
    if a:
        f.append(a[0])
    for x in a[1:]:
        f.append(max(f[-1], f[-2] + x))
    return f[-1]


def lps(s):
    n = len(s)
    p = [[0] * n for _ in range(n)]
    for i in range(n): p[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            p[i][j] = p[i + 1][j - 1] + 2 if s[i] == s[j] and length > 2 else (2 if s[i] == s[j] else max(p[i + 1][j], p[i][j - 1]))
    return p[0][-1]


def is_subsequence(s, t):
    it = iter(t)
    return all(ch in it for ch in s)


def check(example, ok):
    print(f"{'PASS' if ok else 'FAIL'} {example}")


check('例1', lis([5, 2, 8, 1, 9, 3])[1] == 3)
check('例2', lis([3, 1, 4, 1, 5, 9, 2, 6])[1] == 4)
check('例3', lcs('ACGTTA', 'AGTCA')[-1][-1] == 4)
check('例4', lcs('528193', '123589')[-1][-1] == 3)
check('例5', edit('kitten', 'sitting')[-1][-1] == 3)
check('例6', edit('the cat sat on the mat'.split(), 'the cat sat the mat now'.split())[-1][-1] == 2 and Fraction(2, 6) == Fraction(1, 3))
check('例7', lcs('ACGTTA', 'AGTCA')[-1][-1] == 4
      and is_subsequence('AGTA', 'ACGTTA')
      and is_subsequence('AGTA', 'AGTCA'))
check('例8', edit('kitten', 'sitting')[-1][-1] == 3)
check('例9', mcm([5, 10, 3, 12, 5])[0][-1] == 405)
check('例10', max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])[1] == 6)
check('例11', nonadjacent([2, 7, 9, 3, 1]) == 12)
check('例12', lps('BBABCBCAB') == 7)
