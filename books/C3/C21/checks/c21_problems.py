"""Recompute answers with symbolic derivatives, limits and local expansions.

Expected values are transcribed from answers.md. Local polynomial jets use
independent coefficients, so abstract derivative checks cover every C2 jet.
Only the general proof C21-10 is left for manual review.
"""

import re
import sys
from pathlib import Path

import sympy as s

x, y, z, t, u, v = s.symbols("x y z t u v", real=True)
failed = 0
covered = set()


def equal(actual, expected):
    if isinstance(actual, (list, tuple, s.MatrixBase)):
        return len(actual) == len(expected) and all(
            equal(a, b) for a, b in zip(actual, expected)
        )
    if isinstance(actual, (bool, s.logic.boolalg.BooleanAtom)):
        return bool(actual) == bool(expected)
    return s.simplify(actual - expected) == 0


def check(number, actual, expected, detail=""):
    global failed
    pid = f"C21-{number:02d}"
    covered.add(pid)
    ok = equal(actual, expected)
    print(f"{'PASS' if ok else 'FAIL'} {pid}{detail}")
    if not ok:
        failed += 1
        print(f"  computed: {actual}; answer: {expected}")


def choices(number, actual, correct):
    for i, truth in enumerate(actual):
        check(number, truth, i == correct, f" 选项 {'ABCD'[i]}")
    check(number, [i for i, truth in enumerate(actual) if truth], [correct])


# 01: arbitrary first-order path, differentiated after substitution.
b = s.symbols("b", real=True)
velocity = s.diff(s.log((1 + 3*t) + (1 + b*t)), t).subs(t, 0)
check(1, s.solve(s.Eq(velocity, 2), b), [1])

# 02: an arbitrary affine outer function with the prescribed first jet.
outer = 2*(u-3) - (v-1)
composed = outer.subs({u: x+y, v: x-y}, simultaneous=True)
actual = [s.diff(composed, q).subs({x: 2, y: 1}) for q in (x, y)]
options = [(2, -1), (1, 3), (3, 1), (1, 1)]
choices(2, [equal(actual, option) for option in options], 1)

# 03: differentiate a representative with the given differential.
outer = 3*(u-1) - 2*v
composed = outer.subs({u: x*s.exp(y), v: x-y-1}, simultaneous=True)
check(3, [s.diff(composed, q).subs({x: 1, y: 0}) for q in (x, y)], [1, 5])

# 04: let SymPy differentiate the original identity before solving for y'.
Y = s.Function("Y")(x)
identity = Y + s.sin(Y) - x**2
dY = s.solve(s.diff(identity, x), s.diff(Y, x))[0]
check(4, [dY.subs(Y, y), dY.subs({x: 0, Y: 0}),
          s.diff(y+s.sin(y)-x**2, y).subs({x: 0, y: 0})],
      [2*x/(1+s.cos(y)), 0, 2])

# 05: solve the equation itself; check cancellation on its entire solution set.
F = (y-x)**3
branches = s.solve(F, y)
slope = s.diff(branches[0], x).subs(x, 0)
denominator_on_branch = s.diff(F, y).subs(y, branches[0])
fx0 = s.diff(F, x).subs({x: 0, y: 0})
choices(5, [len(branches) != 1, equal(fx0, 0) and equal(slope, 0),
            denominator_on_branch != 0,
            equal(branches[0], x) and equal(slope, 1)
            and equal(denominator_on_branch, 0)], 3)

# 06: the derivative definition requires BOTH one-sided difference quotients.
f = s.Abs(x*y)/s.sqrt(x**2+y**2)
g = s.simplify(f.subs({x: t, y: t}))
right = s.limit(g/t, t, 0, dir="+")
left = s.limit(g/t, t, 0, dir="-")
px = s.limit(f.subs(y, 0)/x, x, 0)
py = s.limit(f.subs(x, 0)/y, y, 0)
a, b = s.symbols("a b", nonnegative=True)
bound = equal(a*a+b*b-2*a*b, (a-b)**2) and ((a-b)**2).is_nonnegative
r = s.symbols("r", positive=True)
continuous = bool(bound) and equal(s.limit(r/2, r, 0, dir="+"), 0)
exists = equal(left, right)
choices(6, [exists and equal(right, px+py),
            exists and equal(right, 1/s.sqrt(2)),
            not exists, not continuous], 2)
check(6, [px, py, left, right], [0, 0, -1/s.sqrt(2), 1/s.sqrt(2)], " 单侧导数")

# 07: recover the outer first jet by differentiating a symbolic affine model.
a, b = s.symbols("a b")
model = a*(u-1)+b*(v-3)
H = model.subs({u: x, v: x+y}, simultaneous=True)
jet = s.solve([s.diff(H, x)-4, s.diff(H, y)+2], (a, b))
g = model.subs(jet).subs({u: t**2, v: 3*t}, simultaneous=True)
check(7, [jet[a], jet[b], s.diff(g, t).subs(t, 1)], [6, -2, 6])

# 08: compose an arbitrary second jet, then recover its unknown coefficients.
c0, c1, c2, A, B, C = s.symbols("c0 c1 c2 A B C")
model = c0+c1*u+c2*v+A*u*u/2+B*u*v+C*v*v/2
H = model.subs({u: x+y, v: x-y}, simultaneous=True)
derivatives = [s.diff(H, x, 2), s.diff(H, y, 2), s.diff(H, x, y)]
relations = [value.subs({x: 0, y: 0}) for value in derivatives]
jet = s.solve([value-given for value, given in zip(relations, [10, 2, 2])],
              (A, B, C), dict=True)
check(8, len(jet), 1, " 唯一解")
check(8, [jet[0][coefficient] for coefficient in (A, B, C)], [4, 2, 2])

# 09: solve coefficients of the local two-variable expansion of the equation.
h, k = s.symbols("h k")
a, b, c = s.symbols("a b c")
Z = a*h+b*k+c*h*k
# A common scaling parameter extracts all terms through total degree two.
residual = s.exp(Z)+h*Z-(1+k)
poly = s.series(residual.subs({h: t*h, k: t*k}), t, 0, 3).removeO().subs(t, 1).expand()
jet = s.solve([poly.coeff(h, 1).coeff(k, 0),
               poly.coeff(k, 1).coeff(h, 0), poly.coeff(h, 1).coeff(k, 1)], (a, b, c))[0]
check(9, list(jet), [0, 1, -1])

covered.add("C21-10")
print("MANUAL C21-10 证明：全微分消元与路径上的中值定理论证")

# 11: independent coefficients represent every possible second-order outer jet.
c0, c1, c2, c11, c12, c22 = s.symbols("c0 c1 c2 c11 c12 c22")
model = c0+c1*u+c2*v+c11*u*u/2+c12*u*v+c22*v*v/2
Z = model.subs({u: x+y, v: x-y}, simultaneous=True)
operator = s.diff(Z, x, 2)-2*s.diff(Z, x, y)+s.diff(Z, y, 2)
candidate = s.exp(s.sqrt(2)*v)*s.sin(u)
candidate_xy = candidate.subs({u: x+y, v: x-y}, simultaneous=True)
check(11, [operator, s.diff(candidate, v, 2)-2*candidate,
           s.diff(candidate_xy, x, 2)-2*s.diff(candidate_xy, x, y)
           +s.diff(candidate_xy, y, 2)-8*candidate_xy], [4*c22, 0, 0])

# 12: substitute unknown quadratic series into both ORIGINAL equations.
a, b, c, d = s.symbols("a b c d")
Y, Z = a*x+b*x*x, c*x+d*x*x
equations = [Y+Z**2-x, s.exp(Y)+Z-1]
coefficients = []
for equation in equations:
    polynomial = s.series(equation, x, 0, 3).removeO().expand()
    coefficients.extend([polynomial.coeff(x, power) for power in (1, 2)])
jet = s.solve(coefficients, (a, b, c, d), dict=True)[0]
result = [jet[a], jet[c], 2*jet[b], 2*jet[d],
          s.diff((Y*Y+Z).subs(jet), x, 2).subs(x, 0)]
matrix = s.Matrix([y+z*z-x, s.exp(y)+z-1]).jacobian([y, z])
check(12, result+[matrix.det(), matrix.det().subs({y: 0, z: 0})],
      [1, -1, -2, 1, 3, 1-2*z*s.exp(y), 1])

# 13: solve the linear terms, then independently solve the nonlinear equation.
a, b = s.symbols("a b")
Z = 1+a*x+b*y
F = s.log(Z)+x*Z+y
jet = s.solve([s.diff(F, x).subs({x: 0, y: 0}),
               s.diff(F, y).subs({x: 0, y: 0})], (a, b))
estimate = Z.subs(jet).subs({x: s.Rational(2, 100), y: -s.Rational(1, 100)})
root = s.nsolve(s.log(z)+s.Rational(2, 100)*z-s.Rational(1, 100), z, 1, prec=40)
check(13, [jet[a], jet[b], estimate], [-1, -1, s.Rational(99, 100)])
check(13, bool(0 < abs(root-estimate) < s.Rational(5, 10000)), True,
      f" 数值核对 z={float(root):.9f}")

# 14: explicitly integrate, then use y as the parameter of both x and I.
X = y+s.log(y)
integral = s.integrate(1+t*t, (t, 1, y))
first = s.diff(integral, y)/s.diff(X, y)
second = s.diff(first, y)/s.diff(X, y)
check(14, [first.subs(y, 1), second.subs(y, 1)], [1, s.Rational(3, 4)])

# 15: expand the composed polynomial, solve for k, and check the dot product.
k = s.symbols("k", real=True)
f = x*x+x*y+y*y
g = f.subs({x: 1+2*t, y: 2+k*t}, simultaneous=True)
solution = s.solve(s.diff(g, t).subs(t, 0), k)[0]
vector_a = s.Matrix([s.diff(f, x).subs({x: 1, y: 2}),
                     s.diff(f, y).subs({x: 1, y: 2}), 0])
vector_b = s.Matrix([2, solution, 0])
check(15, [solution, vector_a.dot(vector_b),
           vector_a.norm() > 0, vector_b.norm() > 0],
      [-s.Rational(8, 5), 0, True, True])

# A missing question must not disappear silently from verify.py's summary.
chapter = Path(__file__).resolve().parent.parent
ids = set(re.findall(r"^\*\*(C21-\d+)\*\*", (chapter/"problems.md").read_text(), re.M))
if covered != ids:
    print(f"FAIL 覆盖题号不一致: missing={ids-covered}, extra={covered-ids}")
    failed += 1
sys.exit(bool(failed))
