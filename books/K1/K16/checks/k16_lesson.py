"""独立核对 lesson.md 中例 1--7 的数值和结论。"""
from itertools import product
from math import comb


def report(i, ok):
    print(f"{'PASS' if ok else 'FAIL'} 例{i}")


def sat(clauses, a):
    return all(any((a[v] if sign else not a[v]) for v, sign in c) for c in clauses)


# 例 1：枚举八种取值，验证唯一解。
clauses1 = [[("x1", True), ("x2", True)], [("x1", False), ("x2", False)],
            [("x2", True), ("x3", True)], [("x2", False), ("x3", False)],
            [("x1", False), ("x3", True)], [("x1", True), ("x3", False)], [("x1", False)]]
models1 = []
for bits in product([False, True], repeat=3):
    a = dict(zip(["x1", "x2", "x3"], bits))
    if sat(clauses1, a):
        models1.append(bits)
report(1, models1 == [(False, True, False)])

# 例 2：回溯后给出的模型逐项代入五个子句。
a, b, c, d = False, True, True, False
ok2 = ((not a) or b) and ((not b) or c) and ((not a) or (not c) or d) and ((not b) or (not d)) and (a or b)
report(2, ok2)

# 例 3：前向链闭包。
facts3 = {"p", "a", "s", "d"}
rules3 = [({"p", "a"}, "c"), ({"c", "s"}, "f"), ({"c", "d"}, "m"), ({"m", "s"}, "g"), ({"e", "c"}, "r")]
changed = True
while changed:
    changed = False
    for body, head in rules3:
        if body <= facts3 and head not in facts3:
            facts3.add(head)
            changed = True
report(3, facts3 == {"p", "a", "s", "d", "c", "f", "m", "g"} and "r" not in facts3)

# 例 4：g 在闭包中，r 不在闭包中。
report(4, "g" in facts3 and "r" not in facts3)

# 例 5：独立连乘。
ok5 = round(0.95**5, 3) == 0.774 and round(0.95**10, 3) == 0.599 and round(0.95**20, 3) == 0.358 and round(0.99**20, 3) == 0.818
report(5, ok5)


def majority(k, q):
    return sum(comb(k, i) * q**i * (1-q)**(k-i) for i in range(k//2 + 1, k+1))


# 例 6：多数票。
ok6 = abs(majority(1, .6)-.6) < 1e-12 and abs(majority(5, .6)-.68256) < 1e-12 and abs(majority(11, .6)-.75349813248) < 1e-12 and abs(majority(21, .6)-.8256221336382272) < 1e-12
report(6, ok6)

# 例 7：至少一个候选正确。
ok7 = all(abs((1-.7**k)-expected) < 1e-12 for k, expected in [(1, .3), (5, .83193), (10, .9717524751)])
report(7, ok7)
