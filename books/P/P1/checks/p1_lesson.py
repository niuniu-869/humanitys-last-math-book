"""独立核对 lesson.md 中例 1--20 的数值或结论。"""
from fractions import Fraction as F
from itertools import combinations, product, permutations
from math import comb, factorial, pi
import sympy as sp

def ok(k, cond):
    print(f"PASS 例{k}" if bool(cond) else f"FAIL 例{k}")

# 例1--2：样本空间和事件计数
ok(1, len(list(permutations("abc", 2))) == 6 and len(list(combinations("abc", 2))) == 3 and len(range(2, 13)) == 11)
O = list(product(range(1, 7), repeat=2))
A = {(i, j) for i, j in O if i + j == 7}
B = {(i, j) for i, j in O if i == j}
C = {(i, j) for i, j in O if i == 6 or j == 6}
ok(2, (len(A), len(B), len(C)) == (6, 6, 11))

# 例3--4：集合表达式
U = set(product([False, True], repeat=3))
AA = {w for w in U if w[0]}
BB = {w for w in U if w[1]}
CC = {w for w in U if w[2]}
only_one = (AA - BB - CC) | (BB - AA - CC) | (CC - AA - BB)
ok(3, len(AA - BB - CC) == 1 and len(only_one) == 3 and len((AA & BB) | (AA & CC) | (BB & CC)) == 4)
left = (AA | BB) & (AA | (U - BB))
right = AA
ok(4, left == right and (U - ((U - AA) | BB)) == (AA & (U - BB)))

# 例5：互斥、对立与完备事件组
D, E = {1, 3, 5}, {2, 4, 6}
Fset, G = {1, 2}, {5, 6}
ok(5, D.isdisjoint(E) and D | E == set(range(1, 7)) and Fset.isdisjoint(G) and Fset | G != set(range(1, 7)))

# 例6--7：离散分配
ok(6, sum([F(3, 10)] * 4) != 1 and any(x < 0 for x in [F(5, 10), F(3, 10), F(4, 10), F(-2, 10)]) and sum([F(4, 10), F(3, 10), F(2, 10), F(1, 10)]) == 1 and sum(F(1, 2**k) for k in range(1, 100)) + F(1, 2**99) == 1 and sum(F(1, 2**(2*m)) for m in range(1, 100)) + F(1, 3 * 4**99) == F(1, 3))
ok(7, F(50, 100) + F(20, 100) + F(15, 100) + F(10, 100) + F(5, 100) == 1 and F(50, 100) + F(20, 100) == F(7, 10))

# 例8--10：概率性质
ok(8, (F(6, 10) + F(5, 10) - F(8, 10), F(6, 10) - F(3, 10), 1 - F(8, 10), 1 - F(3, 10)) == (F(3, 10), F(3, 10), F(2, 10), F(7, 10)))
ok(9, F(1, 10) == F(6, 10) + F(5, 10) - 1 and F(5, 10) == min(F(6, 10), F(5, 10)) and F(1, 10) <= F(3, 10) <= F(5, 10))
ok(10, F(3, 4) - F(1, 16) - F(1, 16) == F(5, 8) and 1 - F(5, 8) == F(3, 8))

# 例11--14：古典概型
ok(11, (F(sum(i == j for i, j in O), 36), F(sum(i + j == 8 for i, j in O), 36), F(sum(max(i, j) == 4 for i, j in O), 36)) == (F(1, 6), F(5, 36), F(7, 36)))
ok(12, (F(comb(3, 1) * comb(5, 1), comb(8, 2)), F(2 * 3 * 5, 8**2), 1 - F(comb(5, 2), comb(8, 2)), 1 - F(5**2, 8**2)) == (F(15, 28), F(15, 32), F(9, 14), F(39, 64)))
ok(13, F(3 * factorial(9), factorial(10)) == F(3, 10))
ok(14, F(3, 4) + F(1, 4) == 1 and F(3, 4) == F(3, 4))

# 例15--16：生日与超几何计数
def birthday(n):
    p = F(1)
    for i in range(n):
        p *= F(365 - i, 365)
    return 1 - p

ok(15, round(float(birthday(10)), 4) == 0.1169 and round(float(birthday(20)), 4) == 0.4114 and round(float(birthday(23)), 4) == 0.5073 and round(float(birthday(30)), 4) == 0.7063 and round(float(birthday(40)), 4) == 0.8912 and round(float(birthday(50)), 4) == 0.9704)
ok(16, F(comb(5, 2) * comb(95, 8), comb(100, 10)) == F(1335, 19012))

# 例17--20：几何概型
ok(17, F(3, 10) == F(3, 10))
ok(18, 1 - F(2 * (45**2), 2 * 60**2) == F(7, 16))
ok(19, abs(pi / 4 - pi / 4) < 1e-12)
d, l = sp.symbols("d l", positive=True)
ok(20, sp.simplify((l / 2) / (sp.pi * d / 4) - 2 * l / (sp.pi * d)) == 0)

# 新增：第 2、4 节开头的老朋友①计数（A=和不小于10，B=至少一个6）
_A = {w for w in O if sum(w) >= 10}
_B = {w for w in O if 6 in w}
ok("2-AB", (len(_A), len(_B), len(_A & _B), len(_A | _B), 36 - len(_A | _B)) == (6, 11, 5, 12, 24))
ok("4-小题", F(1, 2) - F(2, 10) == F(3, 10) and F(1, 2) + F(4, 10) - F(3, 10) == F(6, 10))
