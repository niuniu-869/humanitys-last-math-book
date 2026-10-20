import itertools


def out(ok, label):
    print(("PASS " if ok else "FAIL ") + label)


# K12-01
counts = []
for x in range(1, 5):
    counts.append(sum([x == 1, x == 2, x in (1, 2), x in (1, 3)]))
out(counts == [3, 2, 1, 0], "K12-01")

# K12-02
sol = []
for bits in itertools.product([0, 1], repeat=4):
    a, b, c, d = bits
    if sum(bits) == 1 and sum([a == 1, a == 0, b == 1, c == 1]) == 2:
        sol.append(bits)
out(sol == [(0, 0, 1, 0), (0, 1, 0, 0)], "K12-02")

# K12-03
sol = []
for a, b, c in itertools.product([0, 1], repeat=3):
    truth = [b == 1, c == 0, a == b]
    if truth == [bool(a), bool(b), bool(c)]:
        sol.append((a, b, c))
out(sol == [(0, 0, 1)], "K12-03")

# K12-04
sol = []
for a, b, c, d in itertools.permutations(range(1, 5)):
    pairs = [[b == 1, c == 3], [b == 1, d == 4],
             [a == 2, d == 4], [a == 2, c == 1]]
    if all(sum(x) == 1 for x in pairs):
        sol.append((a, b, c, d))
out(sol == [(2, 1, 4, 3)], "K12-04")

# K12-05
sol = []
counts = []
for x in range(5):
    truth = [x < 2, x > 2, x != 2]
    counts.append(sum(truth))
    if sum(truth) == 2:
        sol.append(x)
out(sol == [0, 1, 3, 4] and counts == [2, 2, 0, 2, 2], "K12-05 全部取值")
options = [[x < 2, x > 2, x != 2, x == 0] for x in sol]
for i, expected in enumerate([False, False, True, False]):
    out(bool(sol) and all(row[i] for row in options) == expected,
        f"K12-05 选项 {'ABCD'[i]}")

# K12-06
counts = []
for p, q, r in itertools.product([0, 1], repeat=3):
    counts.append(sum([not p or q, not q or r, not r or p]))
out(counts == [3, 2, 2, 2, 2, 2, 2, 3], "K12-06 完整计数")
for label, value, expected in zip("ABCD", [0, 1, 2, 4], [False, False, True, False]):
    out((value in counts) == expected, f"K12-06 选项 {label}")

# K12-07
sol = []
for a, b, c, d in itertools.permutations(range(1, 5)):
    truth = [a != 1, d != 1, c < b, c != 1, d < c]
    if sum(truth) == 2:
        sol.append(((a, b, c, d), truth))
out(sol == [((1, 2, 3, 4), [False, True, False, True, False])], "K12-07")

# K12-08
sol = []
for bits in itertools.product([0, 1], repeat=4):
    a, b, c, d = bits
    k = sum(bits)
    truth = [k == 2, k == 1, k == 3, a == b]
    if truth == [bool(a), bool(b), bool(c), bool(d)]:
        sol.append(bits)
out(sol == [(0, 1, 0, 0)], "K12-08")

# K12-09
sol = []
for a, b, c, d in itertools.permutations(range(1, 5)):
    truth = [a == 1, b == 1, c != 4, d != 4]
    if sum(truth) == 1:
        sol.append((a, b, c, d))
out(sol == [(2, 3, 1, 4), (2, 3, 4, 1), (3, 2, 1, 4), (3, 2, 4, 1)],
    "K12-09 全部解")
options = [all(a == 1 for a, b, c, d in sol),
           all(b == 1 for a, b, c, d in sol),
           all(c != 4 for a, b, c, d in sol), len(sol) > 1]
for label, actual, expected in zip("ABCD", options, [False, False, False, True]):
    out(bool(sol) and actual == expected, f"K12-09 选项 {label}")

# K12-10 is a proof task.
print("MANUAL K12-10")

# K12-11
sol = []
for p, q, r in itertools.product([0, 1], repeat=3):
    truth = [(not p) or q, p and (not q), q or r, not r]
    if sum(truth) == 2:
        sol.append((p, q, r))
expected = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 1)]
out(sol == expected, "K12-11")

# K12-12
sol = []
for a, b, c, d in itertools.permutations(range(1, 5)):
    pairs = [[b == 1, b == 4], [b == 1, d == 4], [b == 1, a == 1]]
    if all(sum(x) == 1 for x in pairs):
        sol.append((a, b, c, d))
out(sol == [(2, 1, 4, 3), (3, 1, 4, 2), (4, 1, 2, 3), (4, 1, 3, 2)],
    "K12-12 原始解集")
retained = [[], [], [], []]
for a, b, c, d in sol:
    for i, holds in enumerate([a < c, d < c, a > c, c == 3]):
        if holds:
            retained[i].append((a, b, c, d))
for label, rows, expected in zip("ABCD", retained, [2, 3, 2, 1]):
    out(len(rows) == expected, f"K12-12 选项 {label} 保留解数")
out(retained[3] == [(4, 1, 3, 2)], "K12-12 补充后的唯一解")

# K12-13
sol = []
for a, b, c, d in itertools.product([0, 1], repeat=4):
    liars = sum(x == 0 for x in (a, b, c, d))
    truth = [b == 1 and c == 0, a == d, liars == 2, b == 1]
    if truth == [bool(a), bool(b), bool(c), bool(d)]:
        sol.append((a, b, c, d))
out(sol == [(1, 1, 0, 1)], "K12-13")

# K12-14
sol = []
for a, b, c, d in itertools.permutations(range(1, 5)):
    truth = [a != 4 or b < a, c != 1 or d < a, d == 4, c < a, a < c]
    if sum(truth) == 2:
        sol.append(((a, b, c, d), truth))
out(sol == [((2, 4, 1, 3), [True, False, False, True, False])], "K12-14")
