"""Recompute problem results from their defining functions, then compare with answers.

Expected values transcribe answers.md; anchors also detect edited answer text.
Symbolic recurrences, not just sampled orders, check the all-n assertions.
Only the induction proof is MANUAL. Run directly or through ../verify.py.
"""
import re
import sys
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"\*\*(C5-\d+)\*\*\n(.*?)(?=\n\*\*C5-|\Z)", ANSWERS, re.S
))
FAILURES = []
x, y, t, a, b, c = s.symbols("x y t a b c", real=True)
h = s.symbols("h", real=True, nonzero=True)
n = s.symbols("n", integer=True, nonnegative=True)
R = s.Rational


def same(actual, expected):
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            same(u, v) for u, v in zip(actual, expected)
        )
    if isinstance(expected, (bool, str)):
        return actual == expected
    return s.simplify(actual - expected) == 0


def check(pid, actual, expected, anchors=(), detail=""):
    base = pid.split("(")[0]
    ok = same(actual, expected) and all(token in BLOCKS[base] for token in anchors)
    print(f"{'PASS' if ok else 'FAIL'} {pid}{(' ' + detail) if detail else ''}")
    if not ok:
        FAILURES.append(pid)
        print(f"  got={actual!s}; expected={expected!s}; anchors={anchors!r}")


def choices(pid, actual_truths, expected_letter):
    for label, actual in zip("ABCD", actual_truths):
        check(f"{pid}({label})", bool(actual), label == expected_letter)
    selected = "".join(label for label, truth in zip("ABCD", actual_truths) if truth)
    check(pid, selected, expected_letter, [f"选 ({expected_letter})"])


# 01: Evaluate the actual increment and the differential separately.
f = x**2
actual = (s.diff(f, x).subs(x, 0)*h, f.subs(x, h)-f.subs(x, 0))
options = [(h**2, h**2), (0, 0), (2*h**2, h**2), (0, h**2)]
choices("C5-01", [same(actual, option) for option in options], "D")

# 02: Exact rational arithmetic checks both the approximation and its direction.
f = 1/x
estimate = f.subs(x, 1) + s.diff(f, x).subs(x, 1)*R(2, 100)
error = f.subs(x, R(102, 100)) - estimate
check("C5-02", [estimate, error, error > 0], [R(98, 100), R(1, 2550), True],
      ["0.98", "1/2550", "偏小"])

# 03: Differentiate the composite directly, independently of its stepwise answer.
actual = [s.diff(x**2, x).subs(x, 1)*h,
          s.diff(s.exp(x**2), x).subs(x, 1)*h]
options = [[2*h+h**2, s.E*(2*h+h**2)], [2*h, 2*s.E*h],
           [2*h, s.E*h], [2*h, 2*h]]
choices("C5-03", [same(actual, option) for option in options], "B")

f = (x+a)*s.exp(-x)
aval = s.solve(s.diff(f, x, 2).subs(x, 0), a)
check("C5-04", [aval, s.diff(f, x, 3).subs({x: 0, a: aval[0]})],
      [[2], 1], ["a=2", "f'''(0)=1"])

# 05: Compute both difference quotients and the proposed linear remainders.
f, g = s.Abs(x), x*s.Abs(x)
f_limits = [s.limit((f-f.subs(x, 0))/x, x, 0, dir=d) for d in ("-", "+")]
g_limits = [s.limit((g-g.subs(x, 0))/x, x, 0, dir=d) for d in ("-", "+")]
f_diff = same(*f_limits)
g_diff = same(*g_limits)
truths = [f_diff and g_diff,
          not f_diff and g_diff and same(g_limits[0], 0),
          not f_diff and not g_diff,
          not f_diff and g_diff and same(g_limits[0], 1)]
choices("C5-05", truths, "B")
remainders = [s.limit((g-g.subs(x, 0)-k*x)/x, x, 0, dir=d)
              for k in (0, 1) for d in ("-", "+")]
check("C5-05(差商与余项)", [f_limits, g_limits, remainders],
      [[-1, 1], [0, 0], [0, 0, -1, -1]],
      ["$f$ 在 $0$ 处不可微", "$g'(0)=0$", "$h|h|=o(h)$"])

# 06: Total differentiation of the defining relation; solve both constraints.
rel = x**2+a*x*y+y**2-b
parameters = s.solve([rel.subs({x: 1, y: 2}),
                      s.diff(rel, x).subs({x: 1, y: 2})], [a, b], dict=True)
rel = rel.subs(parameters[0])
d1 = -s.diff(rel, x)/s.diff(rel, y)
d2 = s.diff(d1, x)+s.diff(d1, y)*d1
check("C5-06", [parameters[0][a], parameters[0][b],
                 d1.subs({x: 1, y: 2}), d2.subs({x: 1, y: 2}),
                 s.diff(rel, y).subs({x: 1, y: 2})],
      [-1, 3, 0, -R(2, 3), 3], ["a=-1", "b=3", "y''(1)=-2/3"])

# 07: Work on the positive-base domain by substituting x=z-1/2, z>0.
z = s.symbols("z", positive=True)
f = (1+x)**(1+x)/(1+2*x)
claimed = f*(s.log(1+x)+1-2/(1+2*x))
derivative_residual = s.simplify((s.diff(f, x)-claimed).subs(x, z-R(1, 2)))
check("C5-07", [derivative_residual, f.subs(x, 0), s.limit((f-1)/x, x, 0)],
      [0, 1, -1], [r"\ln(1+x)+1-\dfrac2{1+2x}", "极限为 $-1$"])

xp, yp = t+1/t, t-1/t
slope = s.cancel(s.diff(yp, t)/s.diff(xp, t))
second = s.factor(s.diff(slope, t)/s.diff(xp, t))
roots = [root for root in s.solve(slope-3, t) if root > 1]
point = [expr.subs(t, roots[0]) for expr in (xp, yp)]
line_intercept = point[1]-3*point[0]
negative = s.factor(second.subs(t, z+1)).is_negative
check("C5-08", [roots, point, line_intercept, second, negative],
      [[s.sqrt(2)], [3/s.sqrt(2), 1/s.sqrt(2)], -4*s.sqrt(2),
       -4*t**3/(t**2-1)**3, True],
      [r"y=3x-4\sqrt2", r"-\frac{4t^3}{(t^2-1)^3}<0"])

r = 1/(s.cos(t)+s.sin(t))
xp, yp = r*s.cos(t), r*s.sin(t)
at = s.pi/4
# x=1/(1+tan t) spans [0,1] on the stated interval; y=1-x.
check("C5-09", [s.trigsimp(xp+yp-1),
                 [xp.subs(t, 0), yp.subs(t, 0)],
                 [xp.subs(t, s.pi/2), yp.subs(t, s.pi/2)],
                 [xp.subs(t, at), yp.subs(t, at)], s.diff(r, t).subs(t, at),
                 [s.diff(xp, t).subs(t, at), s.diff(yp, t).subs(t, at)],
                 (s.diff(yp, t)/s.diff(xp, t)).subs(t, at)],
      [0, [1, 0], [0, 1], [R(1, 2), R(1, 2)], 0,
       [-R(1, 2), R(1, 2)], -1],
      [r"x+y=1", r"x,y\ge0", r"r'(\pi/4)=0", "切线斜率是 $-1$"])

print("MANUAL C5-10 数学归纳法证明；人工核对基例、换下标和端点项")

# 11: Check all finite-slope roots AND the branch excluded by dividing by x'.
xp, yp = t**2, t**3-3*t
dx, dy = s.diff(xp, t), s.diff(yp, t)
vertical = s.solve(dx, t)
incidence = s.expand(dx*(yp-2)-dy*xp)
finite = [root for root in s.solve(incidence, t) if root.is_real and root != 0]
check("C5-11", [vertical, dy.subs(t, vertical[0]), xp.subs(t, vertical[0]),
                 finite, [xp.subs(t, -1), yp.subs(t, -1)],
                 (dy/dx).subs(t, -1),
                 s.discriminant(t**2-t+4, t)],
      [[0], -3, 0, [-1], [1, 2], 0, -15],
      ["共有两条切线", "$x=0$", "$y=2$", "$t=-1$", "$t=0$"])

# 12: Direct differentiation recovers the coefficients. The candidate all-n
# expression is verified by its base and derivative recurrence for symbolic n.
F = (a*x**2+b*x+c)*s.exp(x)
sol = s.solve([F.subs(x, 0)-1, s.diff(F, x, 2).subs(x, 0),
               s.diff(F, x, 3).subs(x, 0)], [a, b, c], dict=True)[0]
F = F.subs(sol)
candidate = s.exp(x)*(x**2/R(6)-2*x/R(3)+1+n*(x/R(3)-R(2, 3))+n*(n-1)/6)
all_n = (n-2)*(n-3)/6
checks = [s.diff(F, x, k).subs(x, 0)-all_n.subs(n, k) for k in range(11)]
check("C5-12", [list(sol[v] for v in (a, b, c)),
                 candidate.subs(n, 0)-F,
                 s.diff(candidate, x)-candidate.subs(n, n+1),
                 candidate.subs(x, 0)-all_n,
                 s.solve(all_n, n), checks],
      [[R(1, 6), -R(2, 3), 1], 0, 0, 0, [2, 3], [0]*11],
      ["a=1/6", "b=-2/3", "c=1", "F^{(n)}(0)=(n-2)(n-3)/6"])

g = (s.sqrt(1+x)-1)/x
value = s.limit(g, x, 0)
derivative = s.limit((g-value)/x, x, 0)
check("C5-13", [value, derivative], [R(1, 2), -R(1, 8)],
      ["a=1/2", r"\mathrm{d}g=-\frac18\mathrm{d}x"])

# 14: Obtain the inverse derivatives from f, independently of implicit work.
f = x+s.exp(x)
g1 = 1/s.diff(f, x)
g2 = s.diff(g1, x)/s.diff(f, x)
inverse_point = s.solve(f-1, x)
check("C5-14", [inverse_point, g1.subs(x, 0), g2.subs(x, 0)],
      [[0], R(1, 2), -R(1, 8)],
      ["g(1)=0", "g'(1)=1/2", "g''(1)=-1/8", "极限为 $1/2$"])

# 15: A genuine local path obeying the fixed-diagonal constraint gives all rates.
side_a = 2+R(3, 10)*t
side_b = s.sqrt(13-side_a**2)
rates = [s.diff(expr, t).subs(t, 0)
         for expr in (side_b, side_a*side_b, 2*(side_a+side_b))]
check("C5-15", rates, [-R(1, 5), R(1, 2), R(1, 5)],
      ["b'=-0.2", "面积变化率为 $0.5$", "周长变化率为 $0.2$"])

# 16: Eliminate the parameter, then use the definition at the singular parameter.
curve = s.resultant(x-t**3, y-t**6, t)
f = x**2
check("C5-16", [s.factor(curve), s.limit((f-f.subs(x, 0))/x, x, 0),
                 s.diff(f, x, 2), s.diff(t**3, t).subs(t, 0),
                 s.diff(t**6, t).subs(t, 0)],
      [(y-x**2)**3, 0, 2, 0, 0],
      ["切线为 $y=0$", r"\mathrm{d}^2y/\mathrm{d}x^2=2", "该断言错误"])

sys.exit(bool(FAILURES))
