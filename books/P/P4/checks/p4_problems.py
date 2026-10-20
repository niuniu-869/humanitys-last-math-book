"""独立积分、解方程与集合运算核对习题；仅纯证明题标 MANUAL。"""
import math

import numpy as np
import sympy as sp
from scipy import integrate, optimize, stats


def ok(pid, cond):
    print(f"{'PASS' if bool(cond) else 'FAIL'} {pid}")


def close(a, b, tol=1e-10):
    return bool(np.isclose(float(a), float(b), atol=tol, rtol=0))


def options(pid, values, target, correct):
    for letter, value in zip("ABCD", values):
        ok(f"{pid}-{letter}", close(value, target) == (letter == correct))


x = sp.symbols("x", real=True)
c = sp.symbols("c", positive=True)
half = sp.Rational(1, 2)

coefficient = sp.solve(sp.integrate(c * (2*x + 1), (x, 0, 1)) - 1, c)[0]
f01 = coefficient * (2*x + 1)
F01 = sp.integrate(f01, (x, 0, x))
ok("P4-01", coefficient == half
   and sp.integrate(f01, (x, sp.Rational(1, 4), sp.Rational(3, 4))) == half
   and sp.simplify(F01 - (x*x + x)/2) == 0
   and F01.subs(x, 0) == 0 and F01.subs(x, 1) == 1)

middle02 = (x + 1)**2/4
f02 = sp.diff(middle02, x)
left_join = sp.limit(middle02/(x + 1), x, -1, dir="+")
right_join = sp.limit((middle02 - 1)/(x - 1), x, 1, dir="-")
ok("P4-02-端点", left_join == 0 and right_join == 1)
ok("P4-02-A", f02.subs(x, 2) != 0)  # 区间外真实密度为 0。
ok("P4-02-B", sp.limit(middle02, x, 0, dir="+")
   - sp.limit(middle02, x, 0, dir="-") != sp.Rational(1, 4))
ok("P4-02-C", sp.integrate(f02, (x, -1, 0)) == sp.Rational(1, 4))
ok("P4-02-D", sp.integrate(f02, (x, -1, 1)) == 1
   and middle02.subs(x, -1) == 0 and middle02.subs(x, 1) == 1
   and sp.minimum(f02, x, sp.Interval(-1, 1)) >= 0)

negative03 = sp.solve_univariate_inequality(-x <= 1, x, relational=False)
positive03 = sp.solve_univariate_inequality(x/4 <= 1, x, relational=False)
event03 = ((negative03 & sp.Interval.open(-sp.oo, 0))
           | (positive03 & sp.Interval(0, sp.oo))) & sp.Interval.open(-2, 3)
ok("P4-03", event03.measure / 5 == sp.Rational(4, 5))

solution04 = optimize.root(
    lambda v: [stats.expon(scale=1/v[0]).sf(v[1]) - 1/3,
               stats.expon(scale=1/v[0]).sf(v[1] + 2) - 1/12],
    [0.7, 1.6])
lam04, boundary04 = solution04.x
ok("P4-04", solution04.success and close(lam04, math.log(2), 1e-8)
   and close(boundary04, math.log(3)/math.log(2), 1e-8))

Phi = stats.norm.cdf
target05 = integrate.quad(lambda v: stats.norm(-2, 4).pdf(v), 2, np.inf)[0]
options("P4-05", [1-Phi(1/4), 1-Phi(1), Phi(1), 1-Phi(1/2)], target05, "B")

F06_low = sp.integrate(x, (x, 0, x))
F06_high = sp.integrate(x, (x, 0, 1)) + sp.integrate(2-x, (x, 1, x))
numerator06 = sp.integrate(x, (x, half, 1)) + sp.integrate(2-x, (x, 1, 3*half))
denominator06 = sp.integrate(x, (x, half, 1)) + sp.integrate(2-x, (x, 1, 2))
ok("P4-06", sp.simplify(F06_low - x*x/2) == 0
   and sp.simplify(F06_high - (2*x - x*x/2 - 1)) == 0
   and F06_low.subs(x, 0) == 0 and F06_low.subs(x, 1) == F06_high.subs(x, 1)
   and F06_high.subs(x, 2) == 1 and numerator06/denominator06 == sp.Rational(6, 7))

absolute07 = sp.solve_univariate_inequality(sp.Abs(x) >= half, x, relational=False)
quadratic07 = sp.solve_univariate_inequality(x*(2-x) >= 0, x, relational=False)
support07 = sp.Interval.open(-1, 2)
event07 = absolute07 & quadratic07 & support07
target07 = event07.measure / support07.measure
options("P4-07", [sp.Rational(2, 3), sp.Rational(1, 6), half, sp.Rational(3, 4)], target07, "C")
wrong_absolute = sp.solve_univariate_inequality(sp.Abs(x) <= half, x, relational=False)
ok("P4-07-错项来源", (quadratic07 & support07).measure/3 == sp.Rational(2, 3)
   and (wrong_absolute & quadratic07 & support07).measure/3 == sp.Rational(1, 6)
   and event07.measure/(absolute07 & support07).measure == sp.Rational(3, 4))

print("MANUAL P4-08 无记忆性证明：检查分母为正、事件包含及约分")

uniform09 = stats.uniform(0, 10)
ok("P4-09", close(uniform09.sf(4)/uniform09.sf(2), 3/4)
   and close(uniform09.sf(8)/uniform09.sf(6), 1/2)
   and close(uniform09.sf(2), 4/5))

a = sp.symbols("a", positive=True)
exponent10 = -a*(x-1)**2 + 2*(x-1)
mu10 = sp.solve(sp.diff(exponent10, x), x)[0]
variance10 = -1/sp.diff(exponent10, x, 2)
integral10 = sp.integrate(sp.exp(exponent10), (x, -sp.oo, sp.oo))
constant10 = sp.sqrt(a/sp.pi)*sp.exp(-1/a)
ok("P4-10-参数", sp.simplify(mu10 - (1+1/a)) == 0
   and sp.simplify(variance10 - 1/(2*a)) == 0
   and sp.simplify(constant10*integral10 - 1) == 0
   and sp.solve(mu10-2, a) == [1])
ok("P4-10-非正参数", sp.limit(sp.exp(exponent10.subs(a, 0)), x, sp.oo) == sp.oo
   and sp.limit(sp.exp(exponent10.subs(a, -a)), x, sp.oo) == sp.oo)
ok("P4-10-中点", close(integrate.quad(
    lambda v: math.exp(-(v-2)**2)/math.sqrt(math.pi), -np.inf, 2)[0], 0.5))

interval11 = Phi(2)-Phi(-1)
tail11 = stats.norm.sf(2)
solution11 = optimize.root(
    lambda v: [stats.norm(v[0], v[1]).cdf(5)-stats.norm(v[0], v[1]).cdf(-1)-interval11,
               stats.norm(v[0], v[1]).sf(5)-tail11], [0, 3])
mu11, sigma11 = solution11.x
ok("P4-11", solution11.success and close(mu11, 1, 1e-8) and close(sigma11, 2, 1e-8)
   and close(stats.norm(mu11, sigma11).cdf(-1), 0.1587, 5e-5))

lam12 = optimize.brentq(lambda v: stats.poisson(v).pmf(0)-1/5, 0.01, 10)
poisson_tail = lambda t: stats.poisson(lam12*t).pmf(0)
ok("P4-12", close(lam12, math.log(5))
   and close(poisson_tail(1)-poisson_tail(3), 24/125)
   and close(poisson_tail(3)/poisson_tail(1), 1/25))
rate, duration = sp.symbols("rate duration", positive=True)
ok("P4-12-零次公式", sp.simplify(
    sp.exp(-rate*duration)*(rate*duration)**0/sp.factorial(0)
    - sp.exp(-rate*duration)) == 0)

kernel13 = lambda v: math.exp(-(v+1)**2/8)
c13 = 1/integrate.quad(kernel13, -np.inf, np.inf)[0]
prob13 = lambda lo, hi: c13*integrate.quad(kernel13, lo, hi)[0]
ok("P4-13-归一化与分布函数", close(c13, 1/(2*math.sqrt(2*math.pi)))
   and all(close(prob13(-np.inf, v), Phi((v+1)/2)) for v in [-4, -1, 0, 3]))
pA13, pB13, intersection13 = prob13(-3, 2), prob13(-2, 3), prob13(-2, 2)
tableA13 = 0.9332 - (1-0.8413)
tableB13 = 0.9772 - (1-0.6915)
tableIntersection13 = 0.9332 - (1-0.6915)
ok("P4-13-区间", close(tableA13, 0.7745) and close(tableB13, 0.6687)
   and close(pA13, tableA13, 1e-4) and close(pB13, tableB13, 1e-4) and pA13 > pB13)
ok("P4-13-条件概率", close(tableIntersection13/tableB13, 0.9342, 5e-5)
   and close(intersection13/pB13, tableIntersection13/tableB13, 1e-4))

ok("P4-14", close(stats.poisson(6).pmf(0), math.exp(-6)))

cut_a, cut_b = sp.symbols("cut_a cut_b")
solution15 = sp.solve([cut_b-sp.Rational(11, 20), cut_a-(sp.Rational(4, 5)-cut_b)], [cut_a, cut_b])
cuts15 = [0, solution15[cut_a], solution15[cut_b], sp.Rational(4, 5), 1]
lengths15 = [right-left for left, right in zip(cuts15, cuts15[1:])]
ok("P4-15", solution15 == {cut_a: sp.Rational(1, 4), cut_b: sp.Rational(11, 20)}
   and lengths15 == [sp.Rational(1, 4), sp.Rational(3, 10), sp.Rational(1, 4), sp.Rational(1, 5)]
   and all(length > 0 for length in lengths15) and sum(lengths15) == 1)

A16 = sp.Interval.open(0, sp.Rational(3, 5))
B16 = sp.Interval.open(sp.Rational(1, 5), 1)
intersection16 = (A16 & B16).measure
ok("P4-16", intersection16 == sp.Rational(2, 5) and intersection16/B16.measure == half
   and intersection16 != A16.measure*B16.measure)

pmf17 = stats.poisson(1).pmf([0, 1])
cuts17 = np.cumsum(pmf17)
lengths17 = np.diff([0, *cuts17, 1])
ok("P4-17-切点", close(cuts17[0], math.exp(-1)) and close(cuts17[1], 2*math.exp(-1))
   and np.allclose(lengths17, [*pmf17, stats.poisson(1).sf(1)], atol=1e-12)
   and np.all(lengths17 > 0) and close(sum(lengths17), 1))
ok("P4-17-判类", np.searchsorted(cuts17, 0.6, side="right") == 1
   and np.searchsorted(cuts17, cuts17[0], side="right") == 1
   and np.searchsorted(cuts17, cuts17[1], side="right") == 2)
wrong_lengths17 = np.diff([0, math.exp(-1), math.exp(-1), 1])
ok("P4-17-原规则错误", not close(wrong_lengths17[1], pmf17[1]))
