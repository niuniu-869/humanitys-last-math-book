#!/usr/bin/env python3
import re
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = (ROOT / 'problems.md').read_text(encoding='utf-8')
ANSWERS = (ROOT / 'answers.md').read_text(encoding='utf-8')


def check(pid, ok):
    print(f"{'PASS' if ok else 'FAIL'} {pid}")


def answer_block(pid):
    m = re.search(rf'^\*\*{pid}\*\*(.*?)(?=^\*\*[A-Z]+\d+-\d+\*\*|\Z)', ANSWERS, re.M | re.S)
    return m.group(1) if m else ''


def has_text(pid, *snippets):
    text = re.sub(r'\s+', '', answer_block(pid))
    return all(re.sub(r'\s+', '', s) in text for s in snippets)


x, a = sp.symbols('x a', real=True)

problem_ids = re.findall(r'^\*\*(C6-\d+)\*\*', PROBLEMS, re.M)
answer_ids = re.findall(r'^\*\*(C6-\d+)\*\*', ANSWERS, re.M)
table_ids = re.findall(r'^\| (C6-\d+) \|', PROBLEMS, re.M)
check('题号对应', problem_ids == answer_ids == table_ids
      and len(set(problem_ids)) == 15)

# C6-01
f = x**4 + a*x**2
sol = sp.solve(sp.Eq(sp.diff(f, x).subs(x, 1), 0), a)[0]
delta1 = sp.factor(f.subs(a, sol) - f.subs({a: sol, x: 1}))
ok = sol == -2 and delta1 == (x - 1)**2*(x + 1)**2
check('C6-01', ok and has_text('C6-01', 'a=-2'))

# C6-02, calculate every option's truth value.
f2 = x**2 - 4*x
fp2 = sp.diff(f2, x)
right2 = sp.limit((f2 - f2.subs(x, 0))/x, x, 0, dir='+')
left2 = sp.limit((f2 - f2.subs(x, 3))/(x-3), x, 3, dir='-')
options2 = [
    right2 == 0,
    fp2.subs(x, 2) == 0 and (fp2.subs(x, sp.Rational(19, 10)) > 0),
    fp2.subs(x, 2) == 0 and fp2.subs(x, sp.Rational(19, 10)) < 0 and fp2.subs(x, sp.Rational(21, 10)) > 0,
    sp.Interval.open(0, 3).contains(3) and left2 == 0,
]
# The derivative changes from negative to positive at the stationary point.
check('C6-02', options2 == [False, False, True, False]
      and right2 == -4 and left2 == 2 and has_text('C6-02', '(C)'))

# C6-03
p = (x + 2)*(x - 1)*(x - 4)
roots = sorted([sp.N(r) for r in sp.solve(sp.diff(p, x), x)])
ok = len(roots) == 2 and -2 < roots[0] < 1 and 1 < roots[1] < 4
check('C6-03', ok and has_text('C6-03', '(-2,1)', '(1,4)'))

# C6-04, calculate every choice alternative.
xi4 = sp.solve(sp.Eq(1/x, sp.Rational(2, 1)/(sp.E**2 - 1)), x)[0]
choices4 = [
    sp.simplify(xi4 - (sp.E**2 - 1)/2) == 0 and 1 < xi4 < sp.E**2,
    sp.simplify(sp.Rational(2, 1)/(sp.E**2 - 1) - xi4) == 0,
    sp.simplify((sp.E**2 - 1) - xi4) == 0,
    sp.simplify(sp.E**2/2 - xi4) == 0,
]
check('C6-04', choices4 == [True, False, False, False] and has_text('C6-04', '(A)'))

# C6-05, calculate all four choices.
domain5 = sp.calculus.util.continuous_domain(1/x, x, sp.S.Reals)
slope5 = (sp.Abs(2)-sp.Abs(-1))/3
derivatives5 = [sp.diff(-x, x), sp.diff(x, x)]
roots5c = sp.solveset(sp.diff(x**2, x), x, domain=sp.Interval.open(-1, 1))
roots5d = sp.solveset(sp.diff(x, x), x, domain=sp.Interval.open(0, 1))
choice5 = [
    sp.Interval(-1, 1) - domain5 == sp.S.EmptySet,
    any(d == slope5 for d in derivatives5),
    (-1)**2 == 1**2 and roots5c != sp.S.EmptySet,
    roots5d != sp.S.EmptySet,
]
check('C6-05', choice5 == [False, False, True, False] and has_text('C6-05', '(C)'))

# C6-06
w, eta = sp.symbols('w eta', real=True)
loss = (w-3)**2
g6 = sp.diff(loss, w).subs(w, 1)
update6 = 1-eta*g6
change6 = sp.factor(loss.subs(w, update6)-loss.subs(w, 1))
range6 = sp.solve_univariate_inequality(change6 < 0, eta, relational=False)
M6 = sp.diff(loss, w, 2)
sufficient6 = sp.Interval.open(0, 1/M6)
check('C6-06', g6 == -4 and update6 == 1+4*eta
      and range6 == sp.Interval.open(0, 1)
      and sufficient6 == sp.Interval.open(0, sp.Rational(1, 2))
      and loss.subs(w, update6.subs(eta, sp.Rational(3, 4))) == 1
      and has_text('C6-06', 'L(w)=(w-3)^2', '0<\\eta<1', '0<\\eta<1/2'))

# C6-07
H7 = sp.log(1+x)/x
check('C6-07-导数与端点',
      sp.simplify(sp.diff(H7, x)-(x/(1+x)-sp.log(1+x))/x**2) == 0
      and H7.subs(x, 1) == sp.log(2)
      and sp.limit(H7, x, 0, dir='+') == 1
      and has_text('C6-07', '[\\ln2,1)'))
print('MANUAL C6-07')

# C6-08
f8 = sp.Function('f')(x)
g8 = 1+x**2
check('C6-08-条件与求导', sp.diff(g8, x).subs(x, 0) == 0
      and g8.subs(x, 1)-g8.subs(x, -1) == 0
      and sp.minimum(g8, x, sp.Interval(-1, 1)) == 1
      and sp.simplify(sp.diff(f8/g8, x)*g8**2
                      - (g8*sp.diff(f8, x)-2*x*f8)) == 0)
print('MANUAL C6-08')

# C6-09
f9, g9 = sp.Function('f')(x), sp.Function('g')(x)
quotient_derivative = sp.diff(f9/g9, x)
check('C6-09-求导恒等式', sp.simplify(quotient_derivative - (sp.diff(f9, x)*g9 - f9*sp.diff(g9, x))/g9**2) == 0)
print('MANUAL C6-09')

# C6-10
print('MANUAL C6-10')

# C6-11: the interval nesting is the deterministic conclusion.
print('MANUAL C6-11')

# C6-12
pa, pb, pc = sp.symbols('pa pb pc')
poly12 = pa*x**2+pb*x+pc
coeffs12 = sp.solve([poly12.subs(x, 0), poly12.subs(x, 1),
                    poly12.subs(x, sp.Rational(1, 2))-1], [pa, pb, pc])
poly12 = poly12.subs(coeffs12)
F12 = sp.Function('f')(x)-poly12
check('C6-12-比较函数', sp.expand(poly12-4*x*(1-x)) == 0
      and sp.diff(poly12, x, 2) == -8
      and sp.simplify(sp.diff(F12, x, 2)-sp.diff(sp.Function('f')(x), x, 2)) == 8
      and has_text('C6-12', "f''(\\eta)=-8"))
print('MANUAL C6-12')

# C6-13
h = x**3 - 3*x + 1
roots13 = [r for r in sp.nroots(h) if abs(sp.im(r)) < 1e-12 and 0 <= float(sp.re(r)) <= 2]
check('C6-13', len(roots13) == 2
      and sum(0 < float(sp.re(r)) < 1 for r in roots13) == 1
      and sum(1 < float(sp.re(r)) < 2 for r in roots13) == 1
      and [h.subs(x, i) for i in range(3)] == [1, -1, 3])

# C6-14
linear14 = sp.Rational(2) + sp.Rational(1, 4)*sp.Rational(1, 10)
actual14 = sp.sqrt(sp.Rational(41, 10))
error14 = linear14 - actual14
check('C6-14', linear14 == sp.Rational(81, 40) and 0 < error14 < sp.Rational(1, 40)
      and has_text('C6-14', '2.025'))

# C6-15
F15 = x*sp.log(x)
check('C6-15', sp.diff(F15, x) == sp.log(x) + 1 and has_text('C6-15', '\\ln\\xi+1'))
