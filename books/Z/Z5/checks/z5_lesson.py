"""独立核对 lesson.md 中 16 道例题的数值或可检验结论。"""
from itertools import combinations, product
from math import factorial
import sympy as sp

FAIL = 0


def check(k, condition):
    global FAIL
    if condition:
        print(f"PASS 例{k}")
    else:
        FAIL += 1
        print(f"FAIL 例{k}")


# 例 1、2：受限排列与两颗骰子。
z1a = sum(1 for p in product(range(10), repeat=3) if p[0] != 0 and len(set(p)) == 3)
z1b = sum(1 for p in product(range(10), repeat=3) if p[0] != 0 and len(set(p)) == 3 and p[2] % 2 == 0)
check(1, (z1a, z1b) == (648, 328))
check(2, sum(1 for a in range(1, 7) for b in range(1, 7) if (a + b) % 2 == 0) == 18)

# 例 3、4：组合与恰好一个对子。
check(3, sp.binomial(10, 4) - sp.binomial(6, 4) == 195)
z4 = 13 * sp.binomial(4, 2) * sp.binomial(12, 3) * 4**3
check(4, z4 == 1098240)

# 例 5、6：捆绑插空、不同书分给有名字的人。
check(5, 2 * factorial(3) * (4 * 3) == 144)
z6 = (sp.factorial(6) / (sp.factorial(4) * sp.factorial(1) * sp.factorial(1)) / 2
      + sp.factorial(6) / (sp.factorial(3) * sp.factorial(2) * sp.factorial(1))
      + sp.factorial(6) / (sp.factorial(2) ** 3) / factorial(3)) * factorial(3)
check(6, z6 == 540)

# 例 7、8：带下限隔板与格路。
check(7, sp.binomial(7, 2) == 21)
check(8, (sp.binomial(7, 3), sp.binomial(3, 1) * sp.binomial(4, 2)) == (35, 18))

# 例 9、10：二项式系数与双计数恒等式。
z9 = sp.expand((sp.Symbol("x") ** 2 - 1 / sp.Symbol("x")) ** 6).coeff(sp.Symbol("x"), 0)
check(9, z9 == 15)
check(10, all(sum(k * sp.binomial(n, k) for k in range(1, n + 1)) == n * 2 ** (n - 1) for n in range(1, 9)))

# 例 11、12、13：容斥和错排。
z11 = 100 - (50 + 33 + 20 - 16 - 10 - 6 + 3)
check(11, z11 == 26)
check(12, 3**4 - (3 * 2**4 - 3) == 36)
z13 = factorial(4) - sum((-1) ** (j + 1) * sp.binomial(4, j) * factorial(4 - j) for j in range(1, 5))
check(13, z13 == 9)

# 例 14：穷举所有 6 元子集，核对必有和为 11 的一对。
z14 = all(any(a + b == 11 for a, b in combinations(s, 2)) for s in combinations(range(1, 11), 6))
check(14, z14)

# 例 15：8 个时可以每类 2 个，9 个时由鸽巢保证至少一类 3 个。
check(15, (sp.ceiling(sp.Rational(9, 4)) >= 3) and sp.ceiling(sp.Rational(8, 4)) < 3)

# 例 16：对小 n 穷举整数列，核对总有一段和被 n 整除。
def has_divisible_segment(seq, n):
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += seq[j]
            if total % n == 0:
                return True
    return False


z16 = all(has_divisible_segment(seq, n) for n in range(1, 7) for seq in product(range(-2, 3), repeat=n))
check(16, z16)

raise SystemExit(1 if FAIL else 0)
