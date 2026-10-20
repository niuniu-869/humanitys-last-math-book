"""P.6 讲义例题的独立数值核对。"""
from fractions import Fraction as F
import math
import sympy as sp


def check(num, condition):
    print(("PASS " if condition else "FAIL ") + f"例{num}")
    return condition


ok = True
T = {(0, 1): F(20, 100), (0, 2): F(15, 100), (0, 3): F(5, 100),
     (1, 1): F(10, 100), (1, 2): F(25, 100), (1, 3): F(25, 100)}
ok &= check(1, sum(v for (x, y), v in T.items() if y >= 2) == F(7, 10) and sum(v for (x, y), v in T.items() if x == 1 and y >= 2) == F(1, 2) and sum(v for (x, y), v in T.items() if x < y) == F(9, 10))

cnt = {(m, u): (1 if u == m else 2) for m in range(1, 7) for u in range(1, m + 1)}
ok &= check(2, sum(v for (m, u), v in cnt.items() if m - u >= 3) == 12)

x, y = sp.symbols("x y", real=True)
c = sp.symbols("c")
cc = sp.solve(sp.integrate(sp.integrate(c * (x + y), (y, 0, 1)), (x, 0, 1)) - 1, c)[0]
ok &= check(3, cc == 1 and sp.integrate(sp.integrate(x + y, (y, 0, 1 - x)), (x, 0, 1)) == sp.Rational(1, 3))

xp, yp = sp.symbols("xp yp", positive=True)
f4 = 6 * sp.exp(-2 * xp - 3 * yp)
a, b = sp.symbols("a b", positive=True)
Fxy = sp.integrate(sp.integrate(f4, (xp, 0, a)), (yp, 0, b))
ok &= check(4, sp.integrate(sp.integrate(f4, (yp, xp, sp.oo)), (xp, 0, sp.oo)) == sp.Rational(2, 5) and sp.simplify(Fxy - (1 - sp.exp(-2 * a)) * (1 - sp.exp(-3 * b))) == 0)

ok &= check(5, sp.integrate(sp.integrate(2, (y, 1 - x, x)), (x, sp.Rational(1, 2), 1)) == sp.Rational(1, 2))
p_x = {a0: sum(v for (a1, b0), v in T.items() if a1 == a0) for a0 in (0, 1)}
p_y = {b0: sum(v for (a0, b1), v in T.items() if b1 == b0) for b0 in (1, 2, 3)}
ok &= check(6, p_x == {0: F(2, 5), 1: F(3, 5)} and p_y == {1: F(3, 10), 2: F(2, 5), 3: F(3, 10)})
ok &= check(7, sp.integrate(x + y, (y, 0, 1)) == x + sp.Rational(1, 2))
ok &= check(8, sp.integrate(2, (y, 0, x)) == 2 * x and sp.integrate(2, (x, y, 1)) == 2 * (1 - y))
ok &= check(9, [T[(1, j)] / p_x[1] for j in (1, 2, 3)] == [F(1, 6), F(5, 12), F(5, 12)] and [T[(0, j)] / p_x[0] for j in (1, 2, 3)] == [F(1, 2), F(3, 8), F(1, 8)])
ok &= check(10, sp.integrate((sp.Rational(1, 4) + y) / sp.Rational(3, 4), (y, sp.Rational(1, 2), 1)) == sp.Rational(2, 3))
ok &= check(11, sp.simplify(sp.integrate(1 / xp, (xp, sp.Symbol("q", positive=True), 1)) + sp.log(sp.Symbol("q", positive=True))) == 0)
ok &= check(12, T[(0, 1)] != p_x[0] * p_y[1])
ok &= check(13, sp.integrate(sp.integrate(4 * x * y, (x, 0, 1)), (y, 0, 1)) == 1 and sp.integrate(sp.integrate(8 * x * y, (x, 0, y)), (y, 0, 1)) == 1)
ok &= check(14, sp.integrate(2 * sp.exp(-2 * xp) * sp.exp(-3 * xp), (xp, 0, sp.oo)) == sp.Rational(2, 5))
ok &= check(15, abs(0.5 - 0.5) < 1e-12 and abs((1 - 0.7929) - 0.2071) < 1e-4)
L = sp.Matrix([[sp.sqrt(2), 0], [1 / sp.sqrt(2), sp.sqrt(sp.Rational(3, 2))]])
ok &= check(16, L * L.T == sp.Matrix([[2, 1], [1, 2]]))
ok &= check(17, all(sum(F(1, 36) for i in range(1, 7) if 1 <= s - i <= 6) == F(6 - abs(s - 7), 36) for s in range(2, 13)))
z = sp.symbols("z", real=True)
ok &= check(18, sp.integrate(z, (z, 0, 1)) + sp.integrate(2 - z, (z, 1, 2)) == 1)

def pp(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)

ok &= check(19, all(abs(sum(pp(i, 1.5) * pp(k - i, 1.5) for i in range(k + 1)) - pp(k, 3)) < 1e-12 for k in range(7)))
s1, s2 = sp.symbols("s1 s2", positive=True)
ok &= check(20, sp.simplify(x**2 / s1**2 + (z - x)**2 / s2**2 - ((s1**2 + s2**2) / (s1**2 * s2**2) * (x - s1**2 * z / (s1**2 + s2**2))**2 + z**2 / (s1**2 + s2**2))) == 0)
f21 = 1 / (2 * sp.pi * sp.sqrt(3)) * sp.exp(-(x**2 - x * (z - x) + (z - x)**2) / 3)
fz21 = sp.integrate(f21, (x, -sp.oo, sp.oo))
ok &= check(21, sp.simplify(fz21 - sp.exp(-z**2 / 12) / sp.sqrt(12 * sp.pi)) == 0)
ok &= check(22, sp.simplify(sp.diff(z / (1 + z), z) - 1 / (1 + z)**2) == 0)
ok &= check(23, sp.simplify(sp.integrate(9 * z * sp.exp(-3 * z), (z, 1, sp.oo)) - 4 * sp.exp(-3)) == 0)
ok &= check(24, all(F(m * m - (m - 1) ** 2, 36) == F(2 * m - 1, 36) for m in range(1, 7)))
ok &= check(25, sp.integrate(3 * z**2, (z, 0, 1)) == 1 and sp.integrate(3 * (1 - z)**2, (z, 0, 1)) == 1)
ok &= check(26, sp.simplify((1 - sp.exp(-5 * z)) - (1 - sp.exp(-2 * z) * sp.exp(-3 * z))) == 0)

raise SystemExit(0 if ok else 1)
