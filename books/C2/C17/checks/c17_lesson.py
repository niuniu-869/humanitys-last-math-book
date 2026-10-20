"""Check all twelve worked examples and the short exercises in lesson.md.

Example 6's displayed branches are valid but omit glued solutions. Verify an
explicit counterexample below and keep the defect visible in the PASS label
and author notes. It is not silently counted as a complete solution family.
"""

from pathlib import Path
import sys

import numpy as np
import sympy as s


x = s.Symbol("x", positive=True)
t, C, y = s.symbols("t C y", real=True)
failures = 0


def eq(a, b):
    return s.simplify(a-b) == 0


def near(a, b, tolerance):
    return abs(float(s.N(a))-b) <= tolerance


def report(label, condition, detail=""):
    global failures
    ok = bool(condition)
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} {label}" + (f" {detail}" if detail else ""))


def euler(f, x0, y0, h, n):
    values = [s.sympify(y0)]
    xi = s.sympify(x0)
    for _ in range(n):
        values.append(s.simplify(values[-1]+h*f(xi, values[-1])))
        xi += h
    return values


# Example 1: both complete recurrences, rounded numbers, and the error ordering.
half = euler(lambda a, b: b, 0, 1, s.Rational(1, 2), 2)
quarter = euler(lambda a, b: b, 0, 1, s.Rational(1, 4), 4)
h = s.Symbol("h", positive=True)
g = s.exp(h)-1-h
report("例1", half == [1, s.Rational(3, 2), s.Rational(9, 4)]
       and quarter[:3] == [1, s.Rational(5, 4), s.Rational(25, 16)]
       and near(quarter[3], 1.953, .0005) and near(quarter[4], 2.441, .0005)
       and near(s.E, 2.718, .0005) and near(s.E-half[-1], .47, .005)
       and near(s.E-quarter[-1], .28, .005) and half[-1] < quarter[-1] < s.E
       and eq(g.subs(h, 0), 0) and eq(s.diff(g, h).subs(h, 0), 0)
       and s.diff(g, h, 2).is_positive
       and eq(s.diff(s.exp(x), x), s.exp(x)))

# Example 2: derive the gradient from L and solve the stability inequality.
theta = s.Symbol("theta", real=True)
eta = s.Symbol("eta", real=True)
gradient = s.diff(2*theta**2, theta)
sequences = [euler(lambda a, b: -gradient.subs(theta, b), 0, 1, rate, 3)[1:]
             for rate in [s.Rational(1, 10), s.Rational(3, 5)]]
q = s.simplify((theta-eta*gradient)/theta)
stable = s.solve_univariate_inequality(q**2 < 1, eta, relational=False)
continuous = s.exp(-4*t)
report("例2", sequences == [[s.Rational(3, 5), s.Rational(9, 25), s.Rational(27, 125)],
                           [-s.Rational(7, 5), s.Rational(49, 25), -s.Rational(343, 125)]]
       and stable == s.Interval.open(0, s.Rational(1, 2))
       and eq(s.diff(continuous, t), -gradient.subs(theta, continuous))
       and continuous.subs(t, 0) == 1 and s.limit(continuous, t, s.oo) == 0)

# Example 3: integrate after w=ln(y); substitute back, including C=0.
w = s.Symbol("w", nonzero=True)
primitive = s.integrate(1/w, w)
candidate = s.exp(C*x)
report("例3", eq(s.diff(primitive, w), 1/w)
       and eq(x*s.diff(candidate, x), candidate*(C*x))
       and eq(s.log(candidate), C*x) and candidate.subs(C, 0) == 1
       and s.solve(C-1, C) == [1] and eq(candidate.subs(C, 1), s.exp(x)))

# Example 4: derive the logistic solution algebraically and maximize its rate.
partial = s.apart(4/(y*(4-y)), y)
candidate = s.solve(s.Eq(y/(4-y), s.exp(t)/3), y)[0]
rate = y*(1-y/4)
fastest = s.solve(s.diff(rate, y), y)[0]
time = s.solve(candidate-fastest, t)[0]
report("例4", eq(partial, 1/y+1/(4-y))
       and eq(s.diff(s.log(y)-s.log(4-y), y), 4/(y*(4-y)))
       and eq(candidate, 4/(1+3*s.exp(-t)))
       and eq(s.diff(candidate, t), rate.subs(y, candidate)) and candidate.subs(t, 0) == 1
       and set(s.solve(rate, y)) == {0, 4} and fastest == 2 and s.diff(rate, y, 2) < 0
       and eq(time, s.log(3)))

# Example 5: integrate u du=dx/x, impose the initial value and find the domain.
u2 = 2*s.integrate(1/x, x)+C
constant = s.solve(u2.subs(x, 1)-4, C)[0]
candidate = x*s.sqrt(u2.subs(C, constant))
domain = s.solve_univariate_inequality(u2.subs(C, constant) > 0, x, relational=False)
report("例5", eq(candidate, x*s.sqrt(2*s.log(x)+4)) and candidate.subs(x, 1) == 2
       and eq(s.diff(candidate, x), (x**2+candidate**2)/(x*candidate))
       and domain == s.Interval.open(s.exp(-2), s.oo))

# Example 6: the unsquared sign condition is essential. Check cos(v)>=0
# over the stated phase interval, then use it to remove the absolute value.
phase = s.Symbol("phase", real=True)
allowed = s.Interval(-s.pi/2, s.pi/2)
cos_range = s.calculus.util.function_range(s.cos(phase), phase, allowed)
candidate = x*s.sin(s.log(x)+C)
lhs = s.simplify(x*s.diff(candidate, x)-candidate)
root = s.simplify(x*s.sqrt(1-s.sin(phase)**2))
branch_ok = cos_range.is_subset(s.Interval(0, s.oo)) and eq(
    lhs.subs(s.log(x)+C, phase), root.replace(s.Abs(s.cos(phase)), s.cos(phase)))
constant_branches = [x, -x]
boundary_ok = all(eq(x*s.diff(f, x)-f, s.sqrt(x**2-f**2)) for f in constant_branches)
report("例6", branch_ok and boundary_ok, "已列公式成立；拼接解见下项")

# A genuine additional C^1 solution: -x, then -x*cos(ln x), then x.
pieces = [-x, -x*s.cos(s.log(x)), x]
join_ok = all(eq(left.subs(x, point), right.subs(x, point))
              and eq(s.diff(left, x).subs(x, point), s.diff(right, x).subs(x, point))
              for left, right, point in [(pieces[0], pieces[1], 1),
                                          (pieces[1], pieces[2], s.exp(s.pi))])
mid_lhs = s.simplify((x*s.diff(pieces[1], x)-pieces[1])/x).subs(s.log(x), phase)
mid_rhs = s.simplify(s.sqrt(1-s.cos(phase)**2)).replace(s.Abs(s.sin(phase)), s.sin(phase))
mid_sign = s.Interval(0, s.pi).is_subset(
    s.solve_univariate_inequality(s.sin(phase) >= 0, phase, relational=False))
grid = np.exp(np.linspace(.01, float(s.pi)-.01, 200))
mid_f = s.lambdify(x, pieces[1], "numpy")
mid_df = s.lambdify(x, s.diff(pieces[1], x), "numpy")
numeric_ok = np.allclose(grid*mid_df(grid), mid_f(grid)+np.sqrt(grid**2-mid_f(grid)**2))
f_y = s.diff(y/x+s.sqrt(1-(y/x)**2), y)
derivative_limit = s.limit(f_y.subs(x, 1), y, 1, dir="-")
report("例6-漏解反例", join_ok and boundary_ok and eq(mid_lhs, mid_rhs) and mid_sign
       and numeric_ok and derivative_limit == -s.oo,
       "已证实拼接解；第1节称所有例子满足唯一性条件也不适用于例6边界")

# Example 7: derive the balance using the integrating factor and integrate deposits.
P, Q = -s.Rational(5, 100), s.Rational(6, 5)*s.exp(s.Rational(3, 100)*t)
mu = s.exp(s.integrate(P, t))
general = (s.integrate(mu*Q, t)+C)/mu
balance = s.simplify(general.subs(C, s.solve(general.subs(t, 0), C)[0]))
principal = s.integrate(Q, (t, 0, 10))
report("例7", eq(balance, 60*(s.exp(t/20)-s.exp(3*t/100)))
       and eq(s.diff(balance, t)+P*balance, Q) and balance.subs(t, 0) == 0
       and near(balance.subs(t, 10), 17.93, .005) and near(principal, 13.99, .005))

# Example 8: independent integrating-factor construction, plus variation of constants.
mu = s.exp(s.integrate(1/x, x))
candidate = (s.integrate(mu*x**2, x)+C)/mu
cf = s.Function("c")(x)
variation = s.diff(cf/x, x)+(cf/x)/x
cprime = s.solve(variation-x**2, s.diff(cf, x))[0]
report("例8", eq(candidate, x**3/4+C/x)
       and eq(s.diff(candidate, x)+candidate/x, x**2) and eq(cprime, x**3)
       and eq(s.diff(C/x, x)+(C/x)/x, 0))

# Example 9: compute the integrating factor rather than copying the solution.
mu = s.exp(s.integrate(s.cos(x), x))
candidate = (s.integrate(s.simplify(mu*s.exp(-s.sin(x))), x)+C)/mu
report("例9", eq(candidate, (x+C)*s.exp(-s.sin(x)))
       and eq(s.diff(candidate, x)+candidate*s.cos(x), s.exp(-s.sin(x))))

# Example 10: solve for z=1/y, then substitute into the ORIGINAL equation.
mu = s.exp(s.integrate(-1/x, x))
z = (s.integrate(mu*(-x), x)+C)/mu
candidate = 1/z
report("例10", eq(z, C*x-x**2) and eq(candidate, 1/(C*x-x**2))
       and eq(s.diff(candidate, x)+candidate/x, x*candidate**2)
       and eq(s.diff(s.S.Zero, x)+s.S.Zero/x, x*s.S.Zero**2))

# Example 11: verify both the transformed equation and the original one.
candidate = s.tan(x+C)-x
u = x+candidate
report("例11", eq(s.diff(u, x), 1+u**2)
       and eq(s.diff(candidate, x), (x+candidate)**2)
       and eq(s.diff(s.atan(y), y), 1/(1+y**2)))

# Example 12: solve the linear equation for x(y) on either nonzero sign interval.
mu = y**-3
inverse = s.simplify((s.integrate(mu*(-y/2), y)+C)/mu)
dxdy = s.diff(inverse, y)
report("例12", eq(inverse, y**2/2+C*y**3)
       and eq(dxdy-3*inverse/y, -y/2)
       and eq((y**2-6*inverse)/dxdy+2*y, 0)
       and eq((0-6*x)*0+2*0, 0))

# Short in-text exercises and numerical claims are checked in addition to examples.
report("随堂-解与初值", eq(x*s.diff(C*x**2, x), 2*C*x**2)
       and s.solve(C*1**2-3, C) == [3])
vals = euler(lambda a, b: a+b, 0, 1, s.Rational(1, 2), 2)
exact = 2*s.exp(x)-x-1
report("随堂-欧拉", vals == [1, s.Rational(3, 2), s.Rational(5, 2)]
       and eq(s.diff(exact, x), x+exact) and exact.subs(x, 0) == 1
       and near(exact.subs(x, 1), 3.44, .005) and vals[-1] < exact.subs(x, 1))
candidate = 3*s.exp(x**2)
report("随堂-分离", eq(s.diff(candidate, x), 2*x*candidate) and candidate.subs(x, 0) == 3)
uf = s.Function("u")(x)
implicit_derivative = s.diff(s.sin(uf)-C*x, x).subs(s.diff(uf, x), s.tan(uf)/x)
report("随堂-齐次", eq(implicit_derivative.subs(C, s.sin(uf)/x), 0)
       and eq(s.diff(s.log(s.sin(y)), y), s.cos(y)/s.sin(y)))
candidate = (s.exp(x)+2*s.exp(-2*x))/3
report("随堂-线性", eq(s.diff(candidate, x)+2*candidate, s.exp(x))
       and candidate.subs(x, 0) == 1)
candidate = 1/(1+s.exp(-x))
report("随堂-伯努利", eq(s.diff(candidate, x)-candidate, -candidate**2)
       and candidate.subs(x, 0) == s.Rational(1, 2))
drug = 200*s.exp(-t/10)
infusion = 200*(1-s.exp(-t/10))
half_time = s.solve(s.exp(-t/10)-s.Rational(1, 2), t)[0]
report("正文-药量", eq(s.diff(drug, t), -drug/10) and drug.subs(t, 0) == 200
       and near(drug.subs(t, 6), 109.8, .05)
       and eq(s.diff(infusion, t)+infusion/10, 20) and infusion.subs(t, 0) == 0
       and eq(half_time, 10*s.log(2)) and near(half_time, 6.9, .05))

lesson = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")
report("例6-讲义写出拼接解", r"-x\cos(\ln x)" in lesson and "分段函数" in lesson)
sys.exit(bool(failures))
