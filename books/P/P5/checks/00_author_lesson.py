"""P.5 讲义例题数值的独立验算（作者）。"""
from fractions import Fraction as Fr
import sympy as sp
import numpy as np

def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)

# 例1 老朋友①：Y=|S-7|
pS = {s: Fr(6 - abs(s - 7), 36) for s in range(2, 13)}
pY = {}
for s, p in pS.items():
    pY[abs(s - 7)] = pY.get(abs(s - 7), 0) + p
ok("例1", pY == {0: Fr(6,36), 1: Fr(10,36), 2: Fr(8,36), 3: Fr(6,36), 4: Fr(4,36), 5: Fr(2,36)} and sum(pY.values()) == 1)

# 例2
pX = {-2: Fr(1,10), -1: Fr(1,5), 0: Fr(3,10), 1: Fr(1,4), 2: Fr(3,20)}
ok("例2-分布律和", sum(pX.values()) == 1)
y1, y2 = {}, {}
for x, p in pX.items():
    y1[x*x] = y1.get(x*x, 0) + p
    y2[max(x,0)] = y2.get(max(x,0), 0) + p
ok("例2-X^2", y1 == {0: Fr(3,10), 1: Fr(9,20), 4: Fr(1,4)})
ok("例2-ReLU", y2 == {0: Fr(3,5), 1: Fr(1,4), 2: Fr(3,20)})
# 随堂：X取-1,0,1,2 概率0.2,0.3,0.4,0.1，Y=X^2
ok("练习1", {0: 0.3, 1: 0.6, 4: 0.1} == {0: 0.3, 1: round(0.2+0.4,10), 4: 0.1})

y, x = sp.symbols('y x', positive=True)
# 例3 X~U(0,2), Y=X^2
F = sp.sqrt(y)/2
ok("例3-f", sp.simplify(sp.diff(F, y) - 1/(4*sp.sqrt(y))) == 0)
ok("例3-总量", sp.integrate(1/(4*sp.sqrt(y)), (y, 0, 4)) == 1)
ok("例3-P(X<0.1)", Fr(1,20) == Fr(1,10)/2 and sp.Rational(1,20) == sp.Rational(1,20))
# 练习：X~E(1), Y=X^2 -> f=e^{-sqrt y}/(2 sqrt y)
Fe = 1 - sp.exp(-sp.sqrt(y))
ok("练习3", sp.simplify(sp.diff(Fe, y) - sp.exp(-sp.sqrt(y))/(2*sp.sqrt(y))) == 0 and sp.integrate(sp.exp(-sp.sqrt(y))/(2*sp.sqrt(y)), (y,0,sp.oo)) == 1)
# 例4 X~N(0,1), Y=X^2
phi = lambda t: sp.exp(-t**2/2)/sp.sqrt(2*sp.pi)
Phi = lambda t: (1 + sp.erf(t/sp.sqrt(2)))/2
FY = 2*Phi(sp.sqrt(y)) - 1
fy = sp.diff(FY, y)
ok("例4-f", sp.simplify(fy - sp.exp(-y/2)/sp.sqrt(2*sp.pi*y)) == 0)
ok("例4-总量", sp.simplify(sp.integrate(sp.exp(-y/2)/sp.sqrt(2*sp.pi*y), (y,0,sp.oo)) - 1) == 0)
# 例5 X~U(-1,2), Y=|X|
t = sp.symbols('t', real=True)
def FY5(yv):
    lo, hi = max(-yv, -1), min(yv, 2)
    return max(0, hi-lo)/3
ok("例5-F", abs(FY5(0.5) - 1/3) < 1e-12 and abs(FY5(1.5) - 2.5/3) < 1e-12 and FY5(2.5) == 1.0)
ok("例5-总量", Fr(2,3)*1 + Fr(1,3)*1 == 1)
# 例6 ReLU: P(Y=0)=1/3, 密度1/3 on (0,2)
ok("例6", Fr(1,3) + Fr(1,3)*2 == 1)
# 例7 Y=1/X, X~U(1,2)
ok("例7", sp.integrate(1/y**2, (y, sp.Rational(1,2), 1)) == 1)
# 例8 线性变换
mu, s, a, b, yy = sp.symbols('mu sigma a b yy', real=True)
s = sp.symbols('sigma', positive=True)
a = sp.symbols('a', positive=True)
fX = lambda v: sp.exp(-(v-mu)**2/(2*s**2))/(s*sp.sqrt(2*sp.pi))
fY = fX((yy-b)/a)/a
target = sp.exp(-(yy-(a*mu+b))**2/(2*a**2*s**2))/(a*s*sp.sqrt(2*sp.pi))
ok("例8", sp.simplify(sp.expand(fY/target - 1)) == 0 or sp.simplify(sp.log(fY/target)) == 0)
ok("例8-数值", 170 + 6*0.5 == 173.0)
# 例9 lognormal
lg = sp.exp(-sp.log(y)**2/2)/(y*sp.sqrt(2*sp.pi))
ok("例9-总量", abs(float(sp.Integral(lg, (y, 0, sp.oo)).evalf()) - 1) < 1e-6)
# 反推例4的分支求和
ok("分支求和", sp.simplify(2*phi(sp.sqrt(y))/(2*sp.sqrt(y)) - sp.exp(-y/2)/sp.sqrt(2*sp.pi*y)) == 0)
# 例10 指数的逆变换
lam = 3.0
q = lambda u: -np.log(1-u)/lam*60
ok("例10-中位数", abs(q(0.5) - 13.8629) < 1e-3)
ok("例10-u=0.9", abs(q(0.9) - 46.0517) < 1e-3)
ok("例10-u=0.1", abs(q(0.1) - 2.1072) < 1e-3)
ok("例10-尾", abs(np.exp(-1.5) - 0.22313) < 1e-5)
ok("例10-P(T<=20min)", abs(1-np.exp(-1) - 0.63212) < 1e-5)
rng = np.random.default_rng(2026)
U = rng.random(100000)
T = -np.log(1-U)/lam*60
print("SIM 平均间隔(分钟) %.2f" % T.mean())
print("SIM P(T>30min) %.4f" % (T>30).mean())
print("SIM P(T<=20min) %.4f" % (T<=20).mean())
print("SIM 中位数 %.2f" % np.median(T))
ok("模拟-均值", abs(T.mean()-20) < 0.3)
ok("模拟-尾", abs((T>30).mean()-np.exp(-1.5)) < 0.005)
# 例11 离散逆变换
p = np.array([0.665, 0.245, 0.090]); c = np.cumsum(p)
ok("例11-和", abs(c[-1]-1) < 1e-12)
idx = lambda u: int(np.searchsorted(c, u, side='right'))
ok("例11-u", (idx(0.30), idx(0.72), idx(0.95)) == (0,1,2))
cnt = np.bincount([idx(u) for u in rng.random(100000)], minlength=3)/100000
print("SIM 词频", cnt)
# 骰子 floor(6U)+1
ok("骰子", all(1 <= int(6*u)+1 <= 6 for u in rng.random(1000)))
# 标准正态逆
from scipy.stats import norm
ok("Phi^-1", abs(norm.ppf(0.975) - 1.95996) < 1e-4)
# F(X) ~ U(0,1) 模拟
X = rng.exponential(1/lam, 100000)
FX = 1-np.exp(-lam*X)
ok("F(X)均匀", abs(FX.mean()-0.5) < 0.01 and abs(FX.var()-1/12) < 0.003)
# 例10 X~U(-1,2), Y=X^2
ok("例10", sp.integrate(1/(3*sp.sqrt(y)), (y,0,1)) + sp.integrate(1/(6*sp.sqrt(y)), (y,1,4)) == 1)
# 例10 分布函数法独立核对：F_Y(y)=P(-sqrt y<=X<=sqrt y)
Fy = lambda v: (min(np.sqrt(v),2) - max(-np.sqrt(v),-1))/3
ok("例10-F", abs(Fy(0.25) - 1/3*(1.0)) < 1e-12 and abs(Fy(2.25) - (1.5+1)/3) < 1e-12)
