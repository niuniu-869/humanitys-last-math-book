"""P.7 习题的独立验算。"""
from fractions import Fraction as F
from math import comb
import sympy as sp
from scipy.integrate import quad
from scipy.stats import norm


def chk(name, ok):
    print(("PASS " if ok else "FAIL ") + name)


# P7-01
vals = [-2, 0, 3]
probs = [F(1, 4), F(1, 2), F(1, 4)]
chk("P7-01", sum(F(x) * p for x, p in zip(vals, probs)) == F(1, 4))

# P7-02
x = sp.symbols("x")
f = 6 * x * (1 - x)
chk("P7-02", sp.integrate(x * f, (x, 0, 1)) == sp.Rational(1, 2))

# P7-03: enumerate all admissible target counts via the distribution.
den = comb(8, 3)
solutions = []
for d in range(9):
    ex = sum(k * F(comb(d, k) * comb(8-d, 3-k), den)
             for k in range(max(0, 3-(8-d)), min(3, d)+1))
    if ex == F(15, 8):
        solutions.append(d)
chk("P7-03", solutions == [5])

# P7-04
n, p = sp.symbols("n p")
sol = sp.solve([n*p-6, n*p*(1-p)-sp.Rational(21, 5)], (n, p))
chk("P7-04", sol == [(20, sp.Rational(3, 10))])

# P7-05: a countermodel for each claimed extra condition, while B follows by linearity.
EX, EY = 2, -1
rvals = [-1, 1]
mean = lambda vals: sum(F(v, len(vals)) for v in vals)
xs_counter = [2 + r for r in rvals]
ys_counter = [-1 + r for r in rvals]
EXY_counter = mean([a * b for a, b in zip(xs_counter, ys_counter)])
EX2_counter = mean([a * a for a in xs_counter])
var_x = mean([a * a for a in xs_counter]) - mean(xs_counter) ** 2
var_y = mean([b * b for b in ys_counter]) - mean(ys_counter) ** 2
var_sum_counter = mean([(a + b) ** 2 for a, b in zip(xs_counter, ys_counter)]) - mean([a + b for a, b in zip(xs_counter, ys_counter)]) ** 2
chk("P7-05 B", EX + 2 * EY == 0)
chk("P7-05 A", EXY_counter != EX * EY)
chk("P7-05 C", var_sum_counter != var_x + var_y)
chk("P7-05 D", EX2_counter != EX * EX)

# P7-06
theta = sp.symbols("theta", real=True)
joint = {(0, 0): theta, (0, 1): sp.Rational(1, 2)-theta,
         (1, 0): sp.Rational(1, 2)-theta, (1, 1): theta}
ed = sum((i-j)*q for (i, j), q in joint.items())
vd = sp.expand(sum((i-j)**2*q for (i, j), q in joint.items())-ed**2)
chk("P7-06 parameter", sp.solve(vd-sp.Rational(1, 5), theta) == [sp.Rational(2, 5)])
for label, value in zip("ABCD", [sp.Rational(1, 10), sp.Rational(1, 4), sp.Rational(2, 5), sp.Rational(1, 2)]):
    chk("P7-06 " + label, (vd.subs(theta, value) == sp.Rational(1, 5)) == (label == "C"))

# P7-07
cov = (11 - 5 - 2) / 2
chk("P7-07", cov == 2 and 5 + 2 - 2 * cov == 3)

# P7-08 is a proof question.
print("MANUAL P7-08")

# P7-09
a, b = sp.symbols("a b", real=True)
mse = 9-6*b+4*b**2+(3-a-b)**2
astar = sp.solve(sp.diff(mse, a), a)[0]
reduced = sp.expand(mse.subs(a, astar))
u = sp.symbols("u", nonnegative=True)
chk("P7-09 boundary minimum", sp.expand(reduced.subs(b, 1+u)-7) == 4*u**2+2*u
    and astar.subs(b, 1) == 2)
chk("P7-09 unconstrained excluded", sp.solve(sp.diff(reduced, b), b) == [sp.Rational(3, 4)])

# P7-10
p00, p01, p10, p11 = sp.symbols("p00 p01 p10 p11")
tables = sp.solve([p00+p01+p10+p11-1, p10+p11-sp.Rational(1, 2),
                   p01+p11-sp.Rational(3, 10), p11-sp.Rational(3, 20)],
                  (p00, p01, p10, p11), dict=True)
joint = dict(zip([(0, 0), (0, 1), (1, 0), (1, 1)],
                 [tables[0][v] for v in (p00, p01, p10, p11)]))
px = {i: sum(q for (k, j), q in joint.items() if k == i) for i in (0, 1)}
py = {j: sum(q for (i, k), q in joint.items() if k == j) for j in (0, 1)}
ex = sum(i*q for i, q in px.items())
ey = sum(j*q for j, q in py.items())
vx = sum(i*i*q for i, q in px.items())-ex**2
vy = sum(j*j*q for j, q in py.items())-ey**2
cov = sum(i*j*q for (i, j), q in joint.items())-ex*ey
independent = all(q == px[i]*py[j] for (i, j), q in joint.items())
chk("P7-10 A", vx == sp.Rational(1, 4) and vy == sp.Rational(21, 100) and vx > 0 and vy > 0)
chk("P7-10 B", independent and cov == 0)
chk("P7-10 C", not (cov == 0 and not independent))
chk("P7-10 D", len(tables) == 1 and all(q >= 0 for q in joint.values()))

# P7-11
y = sp.symbols("y")
fxy = 1 + (2 * x - 1) * (2 * y - 1)
fx = sp.integrate(fxy, (y, 0, 1))
ey_cond = sp.simplify(sp.integrate(y * fxy, (y, 0, 1)) / fx)
EX = sp.integrate(x * fx, (x, 0, 1))
EY = sp.integrate(y * sp.integrate(fxy, (x, 0, 1)), (y, 0, 1))
EXY = sp.integrate(sp.integrate(x * y * fxy, (y, 0, 1)), (x, 0, 1))
cov = sp.simplify(EXY - EX * EY)
varx = sp.integrate(x**2 * fx, (x, 0, 1)) - EX**2
vary = sp.integrate(y**2 * sp.integrate(fxy, (x, 0, 1)), (y, 0, 1)) - EY**2
rho = sp.simplify(cov / sp.sqrt(varx * vary))
chk("P7-11", (ey_cond, EX, EY, cov, rho) == ((x + 1) / 3, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 36), sp.Rational(1, 3)))

# P7-12
t = sp.symbols("t", real=True)
moment = lambda g: sp.integrate(2*g, (y, 0, x), (x, 0, 1))
ex, ey = moment(x), moment(y)
vx, vy, cxy = moment(x*x)-ex**2, moment(y*y)-ey**2, moment(x*y)-ex*ey
chk("P7-12 moments", (moment(1), ex, ey, vx, vy, cxy) ==
    (1, sp.Rational(2, 3), sp.Rational(1, 3), sp.Rational(1, 18), sp.Rational(1, 18), sp.Rational(1, 36)))
v = sp.expand(moment((y-t*x)**2)-moment(y-t*x)**2)
tv = sp.solve(sp.diff(v, t), t)[0]
chk("P7-12 minimum", (tv, sp.simplify(v.subs(t, tv)), sp.diff(v, t, 2)) ==
    (sp.Rational(1, 2), sp.Rational(1, 24), sp.Rational(1, 9)))

# P7-13
Sigma = sp.Matrix([[4, 2], [2, 9]])
A = sp.Matrix([[1, t], [1, -1]])
new_cov = A * Sigma * A.T
new_mu = A * sp.Matrix([1, -1])
ts = sp.solve(new_cov[0, 1], t)
chk("P7-13 independence", ts == [sp.Rational(2, 7)] and A.det().subs(t, ts[0]) != 0)
new_cov, new_mu = new_cov.subs(t, ts[0]), new_mu.subs(t, ts[0])
chk("P7-13 distribution", new_mu == sp.Matrix([sp.Rational(5, 7), 2]) and new_cov == sp.diag(sp.Rational(288, 49), 9))
threshold = sp.Rational(5, 7)+12*sp.sqrt(2)/7
zu = sp.simplify((threshold-new_mu[0])/sp.sqrt(new_cov[0, 0]))
zv = (2-new_mu[1])/sp.sqrt(new_cov[1, 1])
prob = norm.sf(float(zu))*norm.cdf(float(zv))
integrated = quad(lambda v: norm.pdf(v, float(new_mu[1]), 3), -float('inf'), 2)[0] * quad(
    lambda u: norm.pdf(u, float(new_mu[0]), float(sp.sqrt(new_cov[0, 0]))), float(threshold), float('inf'))[0]
chk("P7-13 probability", zu == 1 and zv == 0 and abs(prob-0.07932762696572854) < 1e-12 and abs(prob-integrated) < 1e-10)

# P7-14
zmean = sp.integrate(2 * x * sp.log(x), (x, 0, 1))
z2 = sp.integrate(2 * x * sp.log(x) ** 2, (x, 0, 1))
chk("P7-14", (zmean, sp.simplify(z2 - zmean**2)) == (-sp.Rational(1, 2), sp.Rational(1, 4)))

# P7-15
rho = sp.symbols("rho", real=True)
solutions = sp.solve(2/sp.sqrt(2+2*rho)-2, rho)
rr = solutions[0]
chk("P7-15 inverse", solutions == [-sp.Rational(1, 2)] and
    abs(norm.sf(2/float(sp.sqrt(2+2*rr)))-norm.sf(2)) < 1e-12)
zdiff = sp.simplify(sp.sqrt(3)/sp.sqrt(2-2*rr))
prob = quad(lambda z: norm.pdf(z, 0, float(sp.sqrt(2-2*rr))), float(sp.sqrt(3)), float('inf'))[0]
chk("P7-15 probability", zdiff == 1 and abs(prob-norm.sf(float(zdiff))) < 1e-10 and abs(prob-0.15865525393145707) < 1e-10)

# P7-16
S = sp.Matrix([[1, t], [t, 1]])
eigenvalues = list(S.eigenvals())
allowed = sp.reduce_inequalities([ev >= 0 for ev in eigenvalues], t)
chk("P7-16 range", allowed.as_set() == sp.Interval(-1, 1))
construction = sp.Matrix([[1, 0], [t, sp.sqrt(1-t*t)]])
chk("P7-16 construction", sp.simplify(construction*construction.T-S) == sp.zeros(2))
for endpoint, direction in [(1, sp.Matrix([1, -1])), (-1, sp.Matrix([1, 1]))]:
    chk("P7-16 endpoint " + str(endpoint), (direction.T*S.subs(t, endpoint)*direction)[0] == 0
        and construction.subs(t, endpoint)[1, 0] == endpoint
        and construction.subs(t, endpoint)[1, 1] == 0)
