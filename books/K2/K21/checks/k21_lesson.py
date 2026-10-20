#!/usr/bin/env python3
"""独立核对 K2.1 讲义例题的数值与结论。"""
from pathlib import Path
import math
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
ok = True

def check(i, condition):
    global ok
    good = bool(condition)
    print(("PASS " if good else "FAIL ") + f"例{i}")
    ok &= good

# 例 1：爬楼梯。
a = [0, 1, 2]
for k in range(3, 11):
    a.append(a[-1] + a[-2])
check(1, a[10] == 89 and "a_{10}=89" in LESSON)

# 例 2：汉诺塔。
h = [0, 1]
for k in range(2, 7):
    h.append(2*h[-1] + 1)
check(2, h[1:7] == [1, 3, 7, 15, 31, 63] and "h_n=2h_{n-1}+1" in LESSON)

# 例 3：错排。
D = [0, 0, 1]
for k in range(3, 7):
    D.append((k-1)*(D[k-1] + D[k-2]))
check(3, D[3:7] == [2, 9, 44, 265] and "D_6=5\\times(44+9)=265" in LESSON)

# 例 4：一阶不动点法。
check(4, (2**3 - 1) == 7 and "h_n=2^n-1" in LESSON and "h_{64}=2^{64}-1" in LESSON)

# 例 5：等额本息。
rate = sp.Rational(101, 100)
x = sp.Rational(1000) * rate**12 / (rate**12 - 1)
check(5, abs(float(x) - 8884.88) < 0.01 and "8884.88" in LESSON and "106618.55" in LESSON)

# 例 6：直线分平面。
r = [1]
for k in range(1, 7):
    r.append(r[-1] + k)
check(6, r[6] == 22 and "r_n=1+\\frac{n(n+1)}2" in LESSON)

# 例 7：斐波那契通项。
F = [0, 1]
for _ in range(2, 11):
    F.append(F[-1] + F[-2])
check(7, F[10] == 55 and "F_n=\\frac{1}{\\sqrt5}" in LESSON)

# 例 8：由通项反求递推。
def a8(k):
    return 2*3**k + 5*(-1)**k
check(8, a8(2) == 23 and "a_{n+2}=2a_{n+1}+3a_n" in LESSON)

# 例 9：重根。
check(9, (1-2)*3**2 == -9 and "a_n=(1-n)\\,3^n" in LESSON)

# 例 10：递归调用次数。
F41 = [0, 1]
for _ in range(2, 42):
    F41.append(F41[-1] + F41[-2])
check(10, 2*F41[3]-1 == 3 and 2*F41[11]-1 == 177 and 2*F41[41]-1 == 331160281 and "c_{40}=2F_{41}-1" in LESSON)

# 例 11：非齐次递推。
a11 = [0, 0]
for k in range(2, 4):
    a11.append(3*a11[-1] - 2*a11[-2] + 1)
check(11, a11[2] == 1 and a11[3] == 4 and "a_n=2^n-n-1" in LESSON)

# 方法 4 随堂题：独立核对通项与首项。
check(12, 3**(1 + 1) - 3 * 2**1 == 3 and "a_n=3^{n+1}-3\\cdot2^n" in LESSON and "a_1=9-6=3" in LESSON)

raise SystemExit(0 if ok else 1)

