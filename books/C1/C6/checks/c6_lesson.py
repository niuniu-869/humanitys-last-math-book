#!/usr/bin/env python3
import sympy as sp


def check(name, ok):
    print(f"{'PASS' if ok else 'FAIL'} {name}")


x, a, b, c = sp.symbols('x a b c', real=True)

# 例 1
f1 = x**3 + a*x**2 + b*x
sol1 = sp.solve([sp.diff(f1, x).subs(x, 1), sp.diff(f1, x).subs(x, 3)], [a, b], dict=True)[0]
check('例1', sol1 == {a: -6, b: 9})

# 例 2
f2p = sp.diff(x**3 - 3*x + c, x)
check('例2', sp.solve(f2p, x) == [-1, 1] and all(v <= 0 or v >= 1 for v in sp.solve(f2p, x)))

# 例 3
f3p = sp.diff((x - 1)*(x - 2)*(x - 3), x)
roots3 = sorted([sp.N(r) for r in sp.solve(f3p, x)])
check('例3', len(roots3) == 2 and 1 < roots3[0] < 2 and 2 < roots3[1] < 3)

# 例 4
xi4 = sp.solve(sp.Eq(1/(2*sp.sqrt(x)), sp.Rational(1, 3)), x)[0]
check('例4', xi4 == sp.Rational(9, 4) and 1 < xi4 < 4)

# 例 5
speed5 = sp.Rational(20, 1) / sp.Rational(11, 60)
check('例5', speed5 == sp.Rational(1200, 11) and speed5 > 100)

# 例 6
h6 = sp.asin(x) + sp.acos(x)
check('例6', sp.simplify(sp.diff(h6, x)) == 0 and h6.subs(x, 0) == sp.pi/2)

# 例 7
check('例7', sp.Rational(1, 11) < sp.log(sp.Rational(11, 10)) < sp.Rational(1, 10))

# 例 8
L = lambda z: sp.log(1 + sp.exp(-z))
actual8 = sp.N(L(sp.Rational(1, 2)) - L(0), 12)
bound8 = sp.Rational(-3, 16)
Lp = sp.diff(L(x), x)
Lpp = sp.diff(L(x), x, 2)
u = sp.symbols('u', positive=True)
upper_gap = sp.Rational(1, 4) - u/(1+u)**2
check('例8-导数与全域上界',
      sp.simplify(Lp + 1/(1+sp.exp(x))) == 0
      and sp.simplify(Lpp - sp.exp(x)/(1+sp.exp(x))**2) == 0
      and sp.simplify(upper_gap - (u-1)**2/(4*(1+u)**2)) == 0
      and ((u-1)**2).is_nonnegative and (4*(1+u)**2).is_positive)
update8 = -Lp.subs(x, 0)
computed_bound8 = -1*(1-sp.Rational(1, 4))*Lp.subs(x, 0)**2
check('例8-更新与损失', update8 == sp.Rational(1, 2)
      and computed_bound8 == bound8 and actual8 < 0 and actual8 < sp.N(bound8, 12))

# 例 9
check('例9', sp.simplify((sp.cos(sp.pi/4) / (-sp.sin(sp.pi/4))) + 1) == 0)

# 例 10
F10 = sp.Function('F')(x)
check('例10-求导恒等式', sp.simplify(sp.diff(F10, x) / sp.diff(sp.log(x), x) - x*sp.diff(F10, x)) == 0)

# 例 11
f11 = sp.Function('f')(x)
check('例11-求导恒等式', sp.expand(sp.diff(x*f11, x) - (x*sp.diff(f11, x) + f11)) == 0)

# 例 12
f12, g12 = sp.Function('f')(x), sp.Function('g')(x)
check('例12-求导恒等式', sp.simplify(sp.diff(sp.exp(g12)*f12, x) - sp.exp(g12)*(sp.diff(f12, x) + sp.diff(g12, x)*f12)) == 0)

# 例 13
k13 = sp.symbols('k13')
phi = f11 - k13*sp.log(x)
phi2 = f11 - f11.subs(x, 1) - k13*(sp.log(x) - sp.log(1))
check('例13-辅助函数恒等式', sp.simplify(phi - phi2 - (f11.subs(x, 1) - k13*sp.log(1))) == 0)

# 例 14
c14 = sp.symbols('c14', positive=True)
check('例14-倒数和', sp.simplify(c14/sp.Rational(1, 2) + (1-c14)/sp.Rational(1, 2)) == 2)

# Algebraic checks above do not certify general existence proofs.
for number in (2, 6, 7, 8, 10, 11, 12, 13, 14):
    print(f'MANUAL 例{number} proof')

# Nine in-class exercises, including the author's new exponential exercise.
q1 = x**3-3*x+c
check('随堂1-极值候选与差式', sp.solve(sp.diff(q1, x), x) == [-1, 1]
      and sp.factor(q1-q1.subs(x, 1)) == (x-1)**2*(x+2)
      and sp.factor(q1-q1.subs(x, -1)) == (x+1)**2*(x-2))
check('随堂2-指数导数无零点',
      sp.solveset(sp.diff(sp.exp(x)+c, x), x, domain=sp.Interval.open(0, 1)) == sp.S.EmptySet)
print('MANUAL 随堂2 proof')
q3 = x*(x-1)*(x-2)*(x-3)
q3_roots = sp.solve(sp.diff(q3, x), x)
check('随堂3-三个根区间', len(q3_roots) == 3
      and all(sum(bool(i < r < i+1) for r in q3_roots) == 1 for i in range(3)))
q4_roots = sp.solveset(sp.diff(x**3, x)-4, x, domain=sp.Interval.open(0, 2))
check('随堂4-中值点筛根', q4_roots == sp.FiniteSet(2/sp.sqrt(3)))
xp = sp.symbols('xp', positive=True)
q5 = sp.atan(xp)+sp.atan(1/xp)
check('随堂5-反正切求导与常数', sp.simplify(sp.diff(q5, xp)) == 0
      and q5.subs(xp, 1) == sp.pi/2)
print('MANUAL 随堂5 proof')
cos_range = sp.calculus.util.function_range(sp.diff(sp.sin(x), x), x, sp.S.Reals)
check('随堂6-正弦导数界', cos_range == sp.Interval(-1, 1))
print('MANUAL 随堂6 proof')
q7_ratio = sp.diff(x**3, x)/sp.diff(x**2, x)
q7_roots = sp.solveset(q7_ratio-sp.Rational(7, 3), x, domain=sp.Interval.open(1, 2))
check('随堂7-柯西中值点', q7_roots == sp.FiniteSet(sp.Rational(14, 9))
      and sp.simplify(q7_ratio.subs(x, sp.Rational(14, 9))-sp.Rational(7, 3)) == 0)
check('随堂8-商函数求导',
      sp.simplify(sp.diff(f11/x, x)-(x*sp.diff(f11, x)-f11)/x**2) == 0)
print('MANUAL 随堂8 proof')
check('随堂9-指数因子求导',
      sp.simplify(sp.diff(sp.exp(2*x)*f11, x)-sp.exp(2*x)*(sp.diff(f11, x)+2*f11)) == 0)
print('MANUAL 随堂9 proof')
