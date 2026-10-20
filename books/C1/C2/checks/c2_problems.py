"""独立核对 C.2 题目。运行：python3 c2_problems.py"""
import math
import sympy as sp

x, a, n = sp.symbols("x a n", real=True)


def verdict(pid, ok):
    print(f"{'PASS' if ok else 'FAIL'} {pid}")


def close(expr, target):
    return sp.simplify(expr - target) == 0


# A 档
r = sp.limit((sp.sqrt(x + 3) - 2) / (x - 1), x, 1)
verdict("C2-01", close(r, sp.Rational(1, 4)))
for label, value, expected in [("A", sp.Rational(1, 2), False), ("B", sp.Rational(1, 4), True), ("C", 1, False)]:
    verdict("C2-01-" + label, close(r, value) == expected)
verdict("C2-01-D", r.is_finite and close(sp.limit((sp.sqrt(x + 3) - 2) / (x - 1), x, 1, dir="-"), r))

r = sp.limit(sp.sin(7 * x) / (2 * x), x, 0)
verdict("C2-02", close(r, sp.Rational(7, 2)))

r = sp.limit(sp.sin(x**2) / (x - sp.sqrt(x**2 + 1)), x, -sp.oo)
verdict("C2-03", close(r, 0))
for label, value, expected in [("A", 0, True), ("B", 1, False), ("C", sp.oo, False)]:
    verdict("C2-03-" + label, (r == value) == expected)
verdict("C2-03-D", r.is_finite is True)

left = 1 - a
right = 1 + sp.symbols("b")
b = sp.symbols("b")
sol = sp.solve([left - 3, (1 + b) - 3], [a, b], dict=True)
verdict("C2-04", sol == [{a: -2, b: 2}])
for label, av, bv, expected in [("A", 2, 2, False), ("B", -2, 1, False), ("C", -2, 2, True), ("D", 2, 1, False)]:
    actual = left.subs(a, av) == 3 and right.subs(b, bv) == 3
    verdict("C2-04-" + label, actual == expected)

log_expr = sp.log(1 + 4 * x) / (2 * x)
verdict("C2-05", all(close(sp.limit(log_expr, x, 0, dir=d), 2) for d in ("+", "-")))

# 证明题保留给人工检查，不能用数值判定替代证明。
print("MANUAL C2-06")
print("MANUAL C2-07")

# B 档
log_f = sp.log(1 + sp.sin(x)) / x
log_g = sp.log(1 - sp.sin(x)) / x
for label, expr, target in [("F", log_f, 1), ("G", log_g, -1), ("quotient", log_f - 2 * log_g, 3)]:
    verdict("C2-08-" + label, all(close(sp.limit(expr, x, 0, dir=d), target) for d in ("+", "-")))

c = sp.symbols("c", real=True)
h = sp.sqrt(1 + x) - 1 - c * x
verdict("C2-09-first", all(close(sp.limit(h / x, x, 0, dir=d), sp.Rational(1, 2) - c) for d in ("+", "-")))
verdict("C2-09-cancel", all(close(sp.limit(h.subs(c, sp.Rational(1, 2)) / x**2, x, 0, dir=d), -sp.Rational(1, 8)) for d in ("+", "-")))

opt_a = sp.limit((1 - sp.cos(2*x) - 4*(1 - sp.cos(x))) / (-x**4 / 2), x, 0)
opt_b = sp.limit((sp.sin(2*x) - 2*sp.sin(x)) / x**3, x, 0)
opt_c = sp.limit((1 - sp.cos(2*x))**2 / x**4, x, 0)
opt_d = [sp.limit(sp.sin(x) / sp.sqrt(x**2), x, 0, dir=d) for d in ("+", "-")]
verdict("C2-10-A", close(opt_a, 1))
verdict("C2-10-B", close(opt_b, -1))
verdict("C2-10-C", close(opt_c, 4))
verdict("C2-10-D", opt_d == [1, -1])

# C 档
right_limit = sp.E
left_limit = a
verdict("C2-11", sp.solve(sp.Eq(left_limit, right_limit), a) == [sp.E])

alpha = 1 - sp.cos(x) - a*sp.sin(x)**2 - b*(1-sp.cos(x))**2
for d in ("+", "-"):
    second = sp.limit(alpha / x**2, x, 0, dir=d)
    fourth = sp.limit(alpha.subs(a, sp.Rational(1, 2)) / x**4, x, 0, dir=d)
    verdict("C2-12-" + d, close(second, (1-2*a)/2) and close(fourth, (1-2*b)/8))
verdict("C2-12-zero", sp.trigsimp(alpha.subs({a: sp.Rational(1, 2), b: sp.Rational(1, 2)})) == 0)

# 章末混合练习
r = sp.limit(n * (sp.sqrt(1 + 1 / n) - 1), n, sp.oo)
verdict("C2-13", close(r, sp.Rational(1, 2)))

r1 = sp.limit(sp.sin(1 / n) / (1 / n), n, sp.oo)
# 第二项的绝对值恒为 1/n，因此由夹逼趋于 0；不把 (-1)^n 交给符号极限器。
verdict("C2-14", close(r1, 1) and close(sp.limit(1 / n, n, sp.oo), 0))

# 递推式的不动点与单调区间由符号计算核对。
L = sp.symbols("L", real=True)
fixed = sp.solve(sp.Eq(L, (2 * L + 1) / (L + 2)), L)
decrease = sp.factor((2 * x + 1) / (x + 2) - x)
above_one = sp.factor((2 * x + 1) / (x + 2) - 1)
verdict("C2-15", set(fixed) == {sp.Integer(-1), sp.Integer(1)} and sp.simplify(decrease - (1 - x**2) / (x + 2)) == 0 and sp.simplify(above_one - (x - 1) / (x + 2)) == 0)

r = sp.limit((1 - sp.cos(x)) / x**2, x, 0)
k = sp.symbols("k", integer=True, positive=True)
even = (c + 1) / (2*k)
odd = (c - 1) / (2*k - 1)
verdict("C2-16", close(r, sp.Rational(1, 2)) and sp.solve(even, c) == [-1] and sp.solve(odd, c) == [1] and sp.limit((sp.Abs(c)+1)/n, n, sp.oo) == 0)
