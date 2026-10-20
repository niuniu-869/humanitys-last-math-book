#!/usr/bin/env python3
import sympy as sp


def lis(a):
    d = []
    for i, x in enumerate(a):
        prev = [d[j] for j in range(i) if a[j] < x]
        d.append(1 + (max(prev) if prev else 0))
    return d, max(d)


def lcs(x, y):
    m, n = len(x), len(y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            c[i][j] = c[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else max(c[i - 1][j], c[i][j - 1])
    return c


def edit(x, y):
    m, n = len(x), len(y)
    e = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        e[i][0] = i
    for j in range(n + 1):
        e[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            e[i][j] = min(e[i - 1][j] + 1, e[i][j - 1] + 1,
                          e[i - 1][j - 1] + int(x[i - 1] != y[j - 1]))
    return e


def weighted_edit(x, y, insert=1, delete=1, replace=1):
    m, n = len(x), len(y)
    e = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        e[i][0] = e[i - 1][0] + delete
    for j in range(1, n + 1):
        e[0][j] = e[0][j - 1] + insert
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            e[i][j] = min(e[i - 1][j] + delete, e[i][j - 1] + insert,
                          e[i - 1][j - 1] + (0 if x[i - 1] == y[j - 1] else replace))
    return e


def mcm(p):
    n = len(p) - 1
    m = [[sp.Integer(0)] * n for _ in range(n)]
    split = [[None] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            choices = [(m[i][k] + m[k + 1][j] + sp.Integer(p[i]) * p[k + 1] * p[j + 1], k)
                       for k in range(i, j)]
            m[i][j], split[i][j] = min(choices)
    return m, split


def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[sp.Integer(0)] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    return dp


def longest_common_substring(x, y):
    d = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    best = 0
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            d[i][j] = d[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else 0
            best = max(best, d[i][j])
    return best


def is_subsequence(s, t):
    it = iter(t)
    return all(ch in it for ch in s)


def check(pid, ok):
    print(f"{'PASS' if ok else 'FAIL'} {pid}")


d, best = lis([3, 1, 4, 2, 5])
check('K35-01', d == [1, 1, 2, 2, 3] and best == 3)

c = lcs('ABCA', 'ACBA')
check('K35-02', c[-1][-1] == 3 and c[3][2] == 2)

e = weighted_edit('abc', 'adc', replace=2)
check('K35-03', e[-1][-1] == 2)

d, best = lis([2, 2, 1, 3])
options = [False,
           d == [1, 1, 1, 2] and best == 2,
           False,
           False]
check('K35-04', options == [False, True, False, False])

e = edit('ab', 'ac')
options = [e[2][0] == 0, e[0][2] == 2 and e[2][2] == 1,
           e[2][2] == 2, e[2][2] == 2]
check('K35-05', options == [False, True, False, False])

c = lcs('ABCBDAB', 'BDCABA')
check('K35-06', c[-1][-1] == 4
      and is_subsequence('BCBA', 'ABCBDAB') and is_subsequence('BCBA', 'BDCABA')
      and is_subsequence('BDAB', 'ABCBDAB') and is_subsequence('BDAB', 'BDCABA'))

e = edit('abc', 'ab')
terms = [e[2][2] + 1, e[3][1] + 1, e[2][1] + int('c' != 'b')]
options = [False, min(terms) == e[3][2],
           False, False]
check('K35-07', options == [False, True, False, False])

print('MANUAL K35-08')

m, s = mcm([6, 2, 8, 3, 5])
check('K35-09', m[0][-1] == 138 and m[0][2] == 84 and m[1][3] == 78
      and 138 == m[0][0] + m[1][3] + 6 * 2 * 5
      and 174 == m[0][2] + m[3][3] + 6 * 3 * 5
      and 456 == m[0][1] + m[2][3] + 6 * 8 * 5)

check('K35-10', lcs('ABCA', 'BCDA')[-1][-1] == 3 and longest_common_substring('ABCA', 'BCDA') == 2)

dp = knapsack([2, 3, 4, 5], [3, 4, 5, 7], 7)
chosen = []
w = 7
for i in range(4, 0, -1):
    if dp[i][w] != dp[i - 1][w]:
        chosen.append(i)
        w -= [2, 3, 4, 5][i - 1]
chosen_ok = dp[-1][-1] == 10 and chosen == [4, 1] and w == 0
check('K35-11', chosen_ok)

a = [3, 1, 4, 2, 5]
sums = []
for i, x in enumerate(a):
    sums.append(x + max([sums[j] for j in range(i) if a[j] < x] or [0]))
check('K35-12', sums == [3, 1, 7, 3, 12] and max(sums) == 12)

print('MANUAL K35-13')

m, s = mcm([4, 3, 6, 2, 5, 7])
check('K35-14', m[0][-1] == 186 and m[0][3] == 100 and m[1][4] == 148
      and m[0][2] == 60 and m[1][3] == 66 and m[2][4] == 154
      and s[0][2] == 0 and s[1][3] == 2 and s[2][4] == 2
      and s[0][3] == 2 and s[1][4] == 2 and s[0][-1] == 2)
