"""Independent symbolic/numeric checks for all 22 numbered lesson examples.

Example 11: besides the derivative, an early draft claimed a point with y=1;
the check proves no such point exists (the lesson no longer makes that claim).
"""
import sys

import numpy as np
import sympy as s

x, y, t = s.symbols("x y t", real=True)
z = s.symbols("z", positive=True)
n = s.symbols("n", integer=True, positive=True)
R = s.Rational
FAILURES = []


def eq(actual, expected):
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(eq(a, b) for a, b in zip(actual, expected))
    if isinstance(expected, bool):
        return bool(actual) == expected
    # Equal infinities must be compared before subtraction, which gives nan.
    if actual == expected:
        return True
    return s.simplify(actual-expected) == 0


def check(k, actual, expected, note=""):
    ok = eq(actual, expected)
    print(f"{'PASS' if ok else 'FAIL'} 例{k}{(' ' + note) if note else ''}")
    if not ok:
        FAILURES.append(k)
        print(f"  got={actual!s}; expected={expected!s}")


def rounded(expr, expected, digits):
    return bool(np.isclose(float(s.N(expr)), expected, rtol=0, atol=0.51*10**(-digits)))


def implicit(F):
    first = -s.diff(F, x)/s.diff(F, y)
    second = s.diff(first, x)+s.diff(first, y)*first
    return first, second


def parametric(X, Y):
    first = s.diff(Y, t)/s.diff(X, t)
    return s.simplify(first), s.simplify(s.diff(first, t)/s.diff(X, t))


f = x**3-2*x
dy = s.diff(f, x).subs(x, 2)*R(1, 10)
delta = f.subs(x, R(21, 10))-f.subs(x, 2)
check(1, [dy, delta, delta-dy], [1, R(1061, 1000), R(61, 1000)])

f = z**R(1, 3)
approx_cube = f.subs(z, 1)+s.diff(f, z).subs(z, 1)*R(3, 100)
angle = s.pi/6
approx_sin = s.sin(angle)+s.diff(s.sin(x), x).subs(x, angle)*s.pi/180
check(2, [approx_cube, approx_sin,
          rounded(R(103, 100)**R(1, 3), 1.009902, 6),
          rounded(approx_sin, .515115, 6), rounded(s.sin(31*s.pi/180), .515038, 6)],
      [R(101, 100), R(1, 2)+s.sqrt(3)*s.pi/360, True, True, True])

volume = s.pi*x**3/6
v0 = volume.subs(x, 20)
error = s.diff(volume, x).subs(x, 20)*R(1, 5)
check(3, [error, v0, error/v0, rounded(error, 125.7, 1), rounded(v0, 4188.8, 1)],
      [40*s.pi, 4000*s.pi/3, R(3, 100), True, True])

loss = (x-1)**2
step = -R(1, 100)*s.diff(loss, x).subs(x, 3)
prediction = s.diff(loss, x).subs(x, 3)*step
new_loss = loss.subs(x, 3+step)
actual = new_loss-loss.subs(x, 3)
check(4, [step, 3+step, prediction, new_loss, actual, actual-prediction],
      [-R(4, 100), R(296, 100), -R(16, 100), R(38416, 10000),
       -R(1584, 10000), R(16, 10000)])

check(5, s.diff(s.log(1+s.exp(2*x)), x), 2*s.exp(2*x)/(1+s.exp(2*x)))
check(6, s.diff(s.log(z), z)/s.diff(s.sqrt(z), z), 2/s.sqrt(z))

primitives = [x**2/2, s.sin(x), s.log(z), s.exp(3*x)/3, s.atan(x)]
derivatives = [s.diff(expr, z if expr == s.log(z) else x) for expr in primitives]
check(7, [derivatives, s.diff(s.log(-x), x)],
      [[x, s.cos(x), 1/z, s.exp(3*x), 1/(1+x**2)], 1/x])

F = s.exp(y)+x*y-s.E
d1, _ = implicit(F)
check(8, [F.subs({x: 0, y: 1}), d1, d1.subs({x: 0, y: 1})],
      [0, -y/(s.exp(y)+x), -1/s.E])

F = x**3+y**3-6*x*y
d1, _ = implicit(F)
check(9, [F.subs({x: 3, y: 3}), d1, d1.subs({x: 3, y: 3}),
          3-d1.subs({x: 3, y: 3})*3],
      [0, (2*y-x**2)/(y**2-2*x), -1, 6])

F = x**2+y**2-25
d1, d2 = implicit(F)
check(10, [s.factor(d2*y**3), d2.subs({x: 3, y: 4}),
           s.expand(d2*y**3+25)+F],
      [-x**2-y**2, -R(25, 64), 0])

F = x*y-s.exp(x+y)
d1, _ = implicit(F)
formula = (s.exp(x+y)-y)/(x-s.exp(x+y))
reduced = s.factor(d1.subs(s.exp(x+y), x*y))
# y=1 would require x*exp(-x)=e and x>0. The derivative changes from
# positive to negative at x=1; the global maximum is 1/e, strictly below e.
q = z*s.exp(-z)
critical = s.solve(s.diff(q, z), z)
no_y1 = (critical == [1] and s.simplify(q.subs(z, 1)-s.E).is_negative
         and s.limit(q, z, 0, dir="+") == 0 and s.limit(q, z, s.oo) == 0)
check(11, [d1-formula, reduced-y*(x-1)/(x*(1-y)), no_y1], [0, 0, True],
      "导数公式通过；并核对曲线上不存在 y=1 的点")

f = (x+1)**2*s.sqrt(x-2)/(x+3)**3
check(12, [f.subs(x, 3), s.diff(f, x).subs(x, 3),
           s.simplify(s.diff(f, x)/f).subs(x, 3)],
      [R(2, 27), R(1, 27), R(1, 2)])

f = z**s.sin(z)
check(13, s.diff(f, z), f*(s.cos(z)*s.log(z)+s.sin(z)/z))

first, second = parametric(t**2, t**3)
check(14, [first, second], [3*t/2, 3/(4*t)])

X, Y = t-s.sin(t), 1-s.cos(t)
first, second = parametric(X, Y)
check(15, [s.trigsimp(first-s.sin(t)/(1-s.cos(t))),
           s.trigsimp(second+1/(1-s.cos(t))**2),
           first.subs(t, s.pi/2), second.subs(t, s.pi/2),
           s.diff(X, t).subs(t, 0), s.diff(Y, t).subs(t, 0),
           s.limit(first, t, 0, dir="-"), s.limit(first, t, 0, dir="+")],
      [0, 0, 1, -1, 0, 0, -s.oo, s.oo])

control = [(0, 0), (1, 2), (3, 2), (4, 0)]
coords = [s.expand(sum(s.binomial(3, k)*(1-t)**(3-k)*t**k*control[k][j]
                      for k in range(4))) for j in (0, 1)]
first, _ = parametric(*coords)
check(16, [coords, [first.subs(t, v) for v in (0, R(1, 4), R(1, 2))],
           [coord.subs(t, R(1, 4)) for coord in coords],
           s.solve(s.diff(coords[1], t), t), s.diff(coords[1], t, 2), first.subs(t, 1)],
      [[3*t+3*t**2-2*t**3, 6*t-6*t**2], [2, R(8, 11), 0],
       [R(29, 32), R(9, 8)], [R(1, 2)], -12, -2])

r = 2*s.cos(t)
X, Y = r*s.cos(t), r*s.sin(t)
check(17, [s.trigsimp((X-1)**2+Y**2-1),
           [X.subs(t, s.pi/2), Y.subs(t, s.pi/2)],
           s.simplify(s.sec(t)*s.cos(t))], [0, [0, 0], 1])

r = 1+s.cos(t)
X, Y = r*s.cos(t), r*s.sin(t)
first, _ = parametric(X, Y)
check(18, [[expr.subs(t, s.pi/2) for expr in (r, s.diff(r, t), X, Y)],
           [s.diff(expr, t).subs(t, s.pi/2) for expr in (X, Y)],
           first.subs(t, s.pi/2), (Y-first*X).subs(t, s.pi/2)],
      [[1, -1, 0, 1], [-1, -1], 1, 1])

height = s.symbols("height", positive=True)
radius = height*R(2, 4)
volume = s.pi*radius**2*height/3
rate = 2/s.diff(volume, height).subs(height, 1)
check(19, [volume, rate, rounded(rate, 2.55, 2)], [s.pi*height**3/12, 8/s.pi, True])

distance = s.sqrt(z**2+z**4)
rate = s.diff(distance, z).subs(z, 1)*3
check(20, [rate, rounded(rate, 6.36, 2)], [9/s.sqrt(2), True])

# An all-n derivative formula follows from a base case and this identity.
f = x**2*s.exp(2*x)
formula = 2**(n-2)*s.exp(2*x)*(4*x**2+4*n*x+n*(n-1))
check(21, [formula.subs(n, 2)-s.diff(f, x, 2),
           s.diff(formula, x)-formula.subs(n, n+1),
           [s.diff(f, x, k)-formula.subs(n, k) for k in range(2, 10)]],
      [0, 0, [0]*8])

m = s.symbols("m", integer=True, positive=True)
log_derivative = (-1)**(m-1)*s.factorial(m-1)/(1+x)**m
claimed = (-1)**(n-1)*s.factorial(n)/(n-2)
leibniz_value = n*(n-1)*log_derivative.subs({m: n-2, x: 0})
f = x**2*s.log(1+x)
check(22, [log_derivative.subs(m, 1)-s.diff(s.log(1+x), x),
           s.diff(log_derivative, x)-log_derivative.subs(m, m+1),
           s.combsimp(leibniz_value-claimed),
           [s.diff(f, x, k).subs(x, 0)-claimed.subs(n, k) for k in range(3, 11)]],
      [0, 0, 0, [0]*8])

sys.exit(bool(FAILURES))
