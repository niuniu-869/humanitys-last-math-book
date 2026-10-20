"""独立核对 lesson.md 中例 1--27 的数值或结论。"""
import math
import sympy as sp

x, n, m, r, t, T = sp.symbols("x n m r t T", positive=True)


def ok_example(k, condition):
    print(f"{'PASS' if condition else 'FAIL'} 例{k}")


ok_example(1, sp.limit(x**2 + x, x, 1) == 2)
ok_example(2, sp.limit(sp.sqrt(x), x, 4) == 2)
ok_example(3, sp.limit((x**2 - 4) / sp.Abs(x - 2), x, 2, dir="-") == -4 and sp.limit((x**2 - 4) / sp.Abs(x - 2), x, 2, dir="+") == 4)
ok_example(4, sp.limit(1 / (1 + sp.exp(1 / x)), x, 0, dir="-") == 1 and sp.limit(1 / (1 + sp.exp(1 / x)), x, 0, dir="+") == 0)
ok_example(5, sp.limit((2 * x + 1) / (x + 3), x, sp.oo) == 2)
ok_example(6, sp.limit(sp.atan(x), x, sp.oo) == sp.pi / 2 and sp.limit(sp.atan(x), x, -sp.oo) == -sp.pi / 2)
xn = 1 / (1000 * math.pi)
yn = 1 / (2 * 1000 * math.pi + math.pi / 2)
ok_example(7, math.isclose(math.sin(1 / xn), 0.0, abs_tol=1e-12) and math.isclose(math.sin(1 / yn), 1.0, abs_tol=1e-12))
# 任意 x0：j=floor(N*x0)，theta=N*x0-j 属于 [0,1)。
# q=(j+1)/N、s=q+sqrt(2)/N 分别有理、无理，且都严格大于 x0。
N = sp.symbols("N", integer=True, positive=True)
j = sp.symbols("j", integer=True)
theta = sp.symbols("theta", real=True)
q = (j + 1) / N
s = q + sp.sqrt(2) / N
x0 = (j + theta) / N
q_gap = sp.simplify(N * (q - x0))
s_gap = sp.simplify(N * (s - x0))


def no_counterexample(conditions):
    return sp.reduce_inequalities(conditions, theta) == sp.false


unit_interval = [theta >= 0, theta < 1]
ok_example(8, q.is_rational is True and s.is_irrational is True
           and no_counterexample(unit_interval + [q_gap <= 0])
           and no_counterexample(unit_interval + [q_gap > 1])
           and no_counterexample(unit_interval + [s_gap <= 0])
           and no_counterexample(unit_interval + [s_gap > 1 + sp.sqrt(2)])
           and sp.limit((1 + sp.sqrt(2)) / N, N, sp.oo) == 0)
ok_example(9, sp.limit(sp.atan(n), n, sp.oo) == sp.pi / 2)
ok_example(10, sp.limit((x**2 - 4) / (x**2 - 3 * x + 2), x, 2) == 4)
ok_example(11, sp.limit((3 * x**2 + x) / (2 * x**2 - 5), x, sp.oo) == sp.Rational(3, 2))
ok_example(12, sp.limit(sp.sqrt(x**2 + x) - x, x, sp.oo) == sp.Rational(1, 2))
ok_example(13, sp.limit((sp.sqrt(1 + x) - 1) / x, x, 0) == sp.Rational(1, 2))
ok_example(14, sp.limit(1 / (1 + sp.exp(-x)), x, sp.oo) == 1 and sp.limit(1 / (1 + sp.exp(-x)), x, -sp.oo) == 0)
ok_example(15, sp.limit((1 - sp.cos(x)) / x**2, x, 0) == sp.Rational(1, 2))
ok_example(16, sp.limit(sp.sin(3 * x) / sp.sin(5 * x), x, 0) == sp.Rational(3, 5))
ok_example(17, sp.limit(n * sp.sin(sp.pi / n), n, sp.oo) == sp.pi)

e2a = sp.limit(x * sp.log(1 + 2 / x), x, sp.oo)
e2b = sp.limit(x * sp.log((x + 1) / (x - 1)), x, sp.oo)
ok_example(18, e2a == 2 and e2b == 2)
log19 = sp.limit(sp.log(sp.cos(x)) / x**2, x, 0)
ok_example(19, log19 == -sp.Rational(1, 2))
log20 = sp.limit(m * t * sp.log(1 + r / m), m, sp.oo)
ok_example(20, log20 == r * t and math.isclose(math.log(2) / 0.06, 11.55245300933242, rel_tol=1e-12))

# 正弦值的整个值域都在 [-1,1]，两式的绝对值分别不超过 |x|、1/|x|。
z = sp.symbols("z", real=True)
sine_range = sp.calculus.util.function_range(sp.sin(z), z, sp.S.Reals)
bounded = sine_range == sp.Interval(-1, 1)
near = sp.limit(sp.Abs(z), z, 0, dir="+") == 0 and sp.limit(sp.Abs(z), z, 0, dir="-") == 0
far = sp.limit(1/sp.Abs(z), z, sp.oo) == 0 and sp.limit(1/sp.Abs(z), z, -sp.oo) == 0
ok_example(21, bounded and near and far)

# 对任意 M,delta>0，令 Q=max(M,1/delta)，N=floor(Q/(2*pi))+1。
# 写 Q/(2*pi)=j+theta，则 2*pi*N+pi/2-Q=2*pi*(1-theta)+pi/2>0。
# 因此构造点同时满足 0<x_N<delta 和 f(x_N)>M，覆盖任意邻域。
x_high = 1 / (2 * N * sp.pi + sp.pi / 2)
x_zero = 1 / (N * sp.pi)
f = sp.sin(1/z) / z
high_value = sp.simplify(f.subs(z, x_high))
zero_value = sp.simplify(f.subs(z, x_zero))
excess = 2 * sp.pi * (1 - theta) + sp.pi / 2
ok_example(22, sp.simplify(high_value - (2*N*sp.pi + sp.pi/2)) == 0
           and zero_value == 0 and x_high.is_positive and x_zero.is_positive
           and sp.limit(x_high, N, sp.oo) == 0 and sp.limit(x_zero, N, sp.oo) == 0
           and sp.limit(high_value, N, sp.oo) == sp.oo
           and no_counterexample(unit_interval + [excess <= 0]))

p1 = 1 / (1 + sp.exp(-1 / T) + sp.exp(-2 / T))
p2 = sp.exp(-1 / T) / (1 + sp.exp(-1 / T) + sp.exp(-2 / T))
p3 = sp.exp(-2 / T) / (1 + sp.exp(-1 / T) + sp.exp(-2 / T))
large = [sp.limit(p, T, sp.oo) for p in (p1, p2, p3)]
small = [sp.limit(p, T, 0, dir="+") for p in (p1, p2, p3)]
ok_example(23, large == [sp.Rational(1, 3)] * 3 and small == [1, 0, 0])
ok_example(24, sp.limit((sp.sqrt(1 + x**2) - 1) / x**2, x, 0) == sp.Rational(1, 2))
ok_example(25, sp.limit((sp.tan(x) - sp.sin(x)) / x**3, x, 0) == sp.Rational(1, 2))
ok_example(26, sp.limit((sp.sin(x) + x**2) / (sp.tan(2 * x) + x**3), x, 0) == sp.Rational(1, 2))
root27 = (sp.sqrt(1 + sp.tan(x)) - sp.sqrt(1 + sp.sin(x))) / x**3
ok_example(27, sp.limit(root27, x, 0) == sp.Rational(1, 4))
