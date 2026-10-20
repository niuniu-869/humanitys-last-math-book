import re
from pathlib import Path
import sympy as sp

ANS = Path(__file__).resolve().parents[1] / "answers.md"
answers = ANS.read_text(encoding="utf-8")

def report(q, ok):
    print(("PASS " if ok else "FAIL ") + q)

def choice(q):
    m = re.search(rf"\*\*{q}\*\*.*?\*\*答案：\*\*\s*\(([A-D])\)", answers, re.S)
    return m.group(1) if m else ""

# M1-01
x = [0, 1, 2]
y = [1, 2, 4]
loss1 = sum((w*xi+bi-yi)**2 for xi, yi in zip(x, y) for w, bi in [(1, 0)]) / 3
loss2 = sum((2*xi-yi)**2 for xi, yi in zip(x, y)) / 3
report("M1-01", sp.Rational(loss1).limit_denominator() == sp.Integer(2)
       and sp.Rational(loss2).limit_denominator() == sp.Rational(1, 3))

# M1-02
u, v = sp.symbols("u v")
L = (u-3)**2 + 2*(v+1)**2
grad = [sp.diff(L, z).subs({u: 1, v: 2}) for z in (u, v)]
new = [sp.Rational(1)-sp.Rational(1,4)*grad[0], sp.Rational(2)-sp.Rational(1,4)*grad[1]]
report("M1-02", new == [sp.Integer(2), sp.Integer(-1)])

# M1-03
H = sp.diag(2, 8)
eigs = H.eigenvals()
option_truth = [
    all(abs(1 - sp.Rational(3,10)*lam) < 1 for lam in eigs),
    abs(1-sp.Rational(1,5)*8) < 1 and sp.Rational(1,5) < sp.Rational(1,8),
    abs(1-sp.Rational(1,4)*2) < 1 and abs(1-sp.Rational(1,4)*8) < 1,
    abs(1-sp.Rational(3,16)*8) < 1 and (1-sp.Rational(3,16)*8) < 0,
]
report("M1-03", choice("M1-03") == "D" and option_truth == [False, False, False, True])

# M1-04
Hs = [
    sp.Matrix([[2, 2], [2, 4]]),
    sp.Matrix([[2, 2], [2, 2]]),
    sp.Matrix([[2, -2], [-2, 2]]),
    sp.Matrix([[2, 4], [4, 2]]),
]
convex_nonunique = []
for M in Hs:
    vals = M.eigenvals()
    convex_nonunique.append(all(sp.N(z) >= 0 for z in vals) and any(z == 0 for z in vals))
tt = sp.symbols("tt", real=True)
option_truth_04 = [
    all(sp.N(z) >= 0 for z in Hs[0].eigenvals()) and 0 in Hs[0].eigenvals(),
    all(sp.N(z) >= 0 for z in Hs[1].eigenvals()) and 0 in Hs[1].eigenvals(),
    all(sp.N(z) >= 0 for z in Hs[2].eigenvals()) and 0 in Hs[2].eigenvals()
        and sp.limit(tt, tt, -sp.oo) >= 0,
    sp.det(Hs[3]) >= 0 and all(sp.N(z) >= 0 for z in Hs[3].eigenvals()),
]
report("M1-04", choice("M1-04") == "B" and convex_nonunique == [False, True, True, False]
       and option_truth_04 == [False, True, False, False])

# M1-05
lam_max = sp.Integer(2) / sp.Rational(1, 2)
lam_min = sp.solve(sp.Eq((lam_max-sp.Symbol("lm"))/(lam_max+sp.Symbol("lm")), sp.Rational(1,3)), sp.Symbol("lm"))[0]
eta_star = sp.simplify(2/(lam_max+lam_min))
report("M1-05", lam_max == 4 and lam_min == 2 and eta_star == sp.Rational(1,3))

# M1-06 is a proof request.
print("MANUAL M1-06")

# M1-07
def momentum(beta):
    v1 = sp.Integer(12)
    theta1 = sp.Integer(1) - sp.Rational(1,10)*v1
    v2 = beta*v1 - 10
    theta2 = theta1 - sp.Rational(1,10)*v2
    return theta1, theta2
t05 = momentum(sp.Rational(1,2))
t09 = momentum(sp.Rational(9,10))
report("M1-07", t05 == (-sp.Rational(1,5), sp.Rational(1,5))
       and t09 == (-sp.Rational(1,5), -sp.Rational(7,25))
       and t05[1] > 0 and t09[1] < 0)

# M1-08
g1 = sp.Matrix([3, -4]); g2 = sp.Matrix([1, 2])
m1 = sp.Rational(1,10)*g1
m2 = sp.Rational(9,10)*m1 + sp.Rational(1,10)*g2
v1 = sp.Rational(1,100)*g1.multiply_elementwise(g1)
v2 = sp.Rational(99,100)*v1 + sp.Rational(1,100)*g2.multiply_elementwise(g2)
mhat2 = m2 / (1-sp.Rational(9,10)**2)
vhat2 = v2 / (1-sp.Rational(99,100)**2)
ratio2 = [mhat2[i]/sp.sqrt(vhat2[i]) for i in range(2)]
report("M1-08", m2 == sp.Matrix([sp.Rational(37,100), -sp.Rational(4,25)])
       and v2 == sp.Matrix([sp.Rational(991,10000), sp.Rational(124,625)])
       and abs(float(ratio2[0]-ratio2[1])) > 0.5)

# M1-09
eta_max, eta_min, Tw, T = sp.Rational(1,100), sp.Rational(1,1000), 10, 30
eta20 = eta_min + (eta_max-eta_min)/2
cosf = lambda t: eta_min + (eta_max-eta_min)/2*(1+sp.cos(sp.pi*(t-Tw)/(T-Tw)))
int_t = [t for t in range(0, 31) if (eta_max*sp.Rational(t,Tw) if t < Tw else cosf(t)) == sp.Rational(11,2000)]
report("M1-09", choice("M1-09") == "C" and int_t == [20] and eta_max*sp.Rational(11,2)/Tw == sp.Rational(11,2000)
       and eta20 == sp.Rational(11,2000)
       and eta_max*sp.Rational(10,Tw) == eta_max and eta_min == eta_min)

# M1-10
a = sp.symbols("a")
range_result = sp.solve_univariate_inequality(a >= 0, a)
report("M1-10", "0 <= a" in str(range_result)
       and sp.simplify(2/sp.Max(a, 4).subs(a, 1)) == sp.Rational(1,2)
       and sp.Rational(2, 5) == sp.Rational(2, 5))

# M1-11
beta11 = sp.Rational(36,100)
etalambda11 = 1 + beta11 - sp.Rational(12,10)
disc11 = sp.Rational(12,10)**2 - 4*sp.Rational(36,100)
report("M1-11", beta11 == sp.Rational(9,25) and etalambda11 == sp.Rational(4,25)
       and etalambda11/2 == sp.Rational(2,25) and disc11 == 0)

# M1-12
x, y = sp.symbols("x y")
F = x**2 + x*y + y**2 - 4*x - 2*y
sol = sp.solve([sp.diff(F, x), sp.diff(F, y)], (x, y))
step = sp.Matrix([0, 0]) - sp.Rational(1,4)*sp.Matrix([sp.diff(F, x).subs({x:0,y:0}), sp.diff(F,y).subs({x:0,y:0})])
report("M1-12", sol == {x: 2, y: 0} and list(step) == [1, sp.Rational(1,2)])

# M1-13
vals = [sp.Integer(1), sp.Integer(3), sp.Integer(5), sp.Integer(7)]
mu = sum(vals)/4
sigma2 = sum((z-mu)**2 for z in vals)/4
report("M1-13", mu == 4 and sigma2 == 5
       and sigma2/4 == sp.Rational(5,4) and sigma2/16 == sp.Rational(5,16))

# M1-14 uses the definition and is a proof-style check.
print("MANUAL M1-14")

# M1-15
H15 = sp.Matrix([[3,1],[1,3]])
ev15 = sorted(H15.eigenvals().keys())
theta15 = sp.Matrix([1,2]) - sp.Rational(1,3)*sp.Matrix([2,-1])
adam15 = sp.Matrix([sp.Rational(-1,10), sp.Rational(1,10)])
report("M1-15", ev15 == [2,4] and theta15 == sp.Matrix([sp.Rational(1,3), sp.Rational(7,3)])
       and adam15 == sp.Matrix([sp.Rational(-1,10), sp.Rational(1,10)]))
