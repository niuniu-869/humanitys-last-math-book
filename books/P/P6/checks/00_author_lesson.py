"""P.6 讲义例题数值的独立验算（作者）。"""
from fractions import Fraction as Fr
import itertools
import sympy as sp
import numpy as np
from scipy.stats import norm

def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)

# ---------- 老朋友⑤ ----------
T = {(0,1): Fr(20,100), (0,2): Fr(15,100), (0,3): Fr(5,100),
     (1,1): Fr(10,100), (1,2): Fr(25,100), (1,3): Fr(25,100)}
ok("⑤总和", sum(T.values()) == 1)
ok("⑤例1 P(Y>=2)", sum(p for (x,y),p in T.items() if y>=2) == Fr(7,10))
ok("⑤例1 P(X=1,Y>=2)", sum(p for (x,y),p in T.items() if x==1 and y>=2) == Fr(1,2))
ok("⑤例1 P(X<Y)", sum(p for (x,y),p in T.items() if x<y) == Fr(9,10))
pX = {x: sum(p for (a,b),p in T.items() if a==x) for x in (0,1)}
pY = {y: sum(p for (a,b),p in T.items() if b==y) for y in (1,2,3)}
ok("⑤边缘", pX == {0: Fr(2,5), 1: Fr(3,5)} and pY == {1: Fr(3,10), 2: Fr(2,5), 3: Fr(3,10)})
ok("⑤条件 X=1", [T[(1,y)]/pX[1] for y in (1,2,3)] == [Fr(1,6), Fr(5,12), Fr(5,12)])
ok("⑤条件 X=0", [T[(0,y)]/pX[0] for y in (1,2,3)] == [Fr(1,2), Fr(3,8), Fr(1,8)])
ok("⑤不独立", T[(0,1)] != pX[0]*pY[1] and pX[0]*pY[1] == Fr(12,100))
# 同边缘的独立联合表
Ti = {(x,y): pX[x]*pY[y] for x in (0,1) for y in (1,2,3)}
ok("同边缘独立表", Ti[(0,1)] == Fr(12,100) and Ti[(0,2)] == Fr(16,100) and Ti[(0,3)] == Fr(12,100) and Ti[(1,1)] == Fr(18,100) and Ti[(1,2)] == Fr(24,100) and Ti[(1,3)] == Fr(18,100))

# ---------- 两颗骰子 (M, U) ----------
cnt = {}
for a, b in itertools.product(range(1,7), repeat=2):
    k = (max(a,b), min(a,b)); cnt[k] = cnt.get(k, 0) + 1
ok("(M,U) 联合", all(cnt.get((m,u),0) == (2 if u<m else 1) for m in range(1,7) for u in range(1,m+1)))
ok("P(M-U>=3)", Fr(sum(c for (m,u),c in cnt.items() if m-u>=3), 36) == Fr(1,3))
ok("M 边缘", all(Fr(sum(c for (m,u),c in cnt.items() if m==mm),36) == Fr(2*mm-1,36) for mm in range(1,7)))
ok("给定 M=4 的 U", [Fr(cnt[(4,u)], 7) for u in range(1,5)] == [Fr(2,7),Fr(2,7),Fr(2,7),Fr(1,7)])

x, y, z = sp.symbols('x y z', real=True)
xp, yp = sp.symbols('x y', positive=True)
# ---------- f = c(x+y) ----------
c = sp.symbols('c', positive=True)
cc = sp.solve(sp.integrate(sp.integrate(c*(x+y), (y,0,1)), (x,0,1)) - 1, c)[0]
ok("f=c(x+y) c=1", cc == 1)
ok("P(X+Y<=1)=1/3", sp.integrate(sp.integrate(x+y, (y,0,1-x)), (x,0,1)) == sp.Rational(1,3))
ok("f_X=x+1/2", sp.integrate(x+y, (y,0,1)) == x + sp.Rational(1,2))
ok("条件 P(Y>1/2|X=1/4)=2/3", sp.integrate((1+4*y)/3, (y,sp.Rational(1,2),1)) == sp.Rational(2,3))
ok("f(y|1/4)=(1+4y)/3", sp.simplify((sp.Rational(1,4)+y)/(sp.Rational(1,4)+sp.Rational(1,2)) - (1+4*y)/3) == 0)
ok("P(Y>1/2)=5/8", sp.integrate(y+sp.Rational(1,2), (y,sp.Rational(1,2),1)) == sp.Rational(5,8))
ok("条件密度积分为1", sp.simplify(sp.integrate((x+y)/(x+sp.Rational(1,2)), (y,0,1))) == 1)
ok("P(Y>2)=0.0787", abs(1-norm.cdf(2/np.sqrt(2)) - 0.0787) < 1e-4)
ok("通勤", abs(1-norm.cdf(2) - 0.0228) < 1e-4 and 16+9 == 25 and 25+15 == 40)
zz2 = sp.symbols('z2', positive=True)
ok("U+U 卷积 0<z<=1", sp.integrate(1,(x,0,zz2)) == zz2)
ok("U+U 卷积 1<z<2", sp.integrate(1,(x,zz2-1,1)) == 2-zz2)
rngu = np.random.default_rng(5); Zs = rngu.random(200000)+rngu.random(200000)
ok("U+U 模拟 P(Z<=1/2)", abs((Zs<=0.5).mean()-0.125) < 0.003)
A_, B_ = sp.symbols('A B', positive=True)
ok("F(x,y)=x*y*(x+y)/2", sp.simplify(sp.integrate(sp.integrate(x+y, (y,0,B_)), (x,0,A_)) - A_*B_*(A_+B_)/2) == 0)
ok("f=x+y 不独立", sp.simplify((x+y) - (x+sp.Rational(1,2))*(y+sp.Rational(1,2))) != 0)
# ---------- 6 e^{-2x-3y} ----------
f6 = 6*sp.exp(-2*xp-3*yp)
ok("6e^{-2x-3y} 总量", sp.integrate(sp.integrate(f6, (xp,0,sp.oo)), (yp,0,sp.oo)) == 1)
ok("P(X<Y)=2/5", sp.integrate(sp.integrate(f6, (yp,xp,sp.oo)), (xp,0,sp.oo)) == sp.Rational(2,5))
a_, b_ = sp.symbols('a b', positive=True)
Fxy = sp.integrate(sp.integrate(f6.subs({xp:sp.Symbol('s',positive=True), yp:sp.Symbol('t',positive=True)}), (sp.Symbol('s',positive=True),0,a_)), (sp.Symbol('t',positive=True),0,b_))
ok("F(x,y) 乘积", sp.simplify(Fxy - (1-sp.exp(-2*a_))*(1-sp.exp(-3*b_))) == 0)
# 矩形概率 P(0<X<=1, 0<Y<=1)
F = lambda a,b: (1-np.exp(-2*a))*(1-np.exp(-3*b)) if a>0 and b>0 else 0
ok("矩形公式", abs(F(1,1)-F(0,1)-F(1,0)+F(0,0) - (1-np.exp(-2))*(1-np.exp(-3))) < 1e-12)
# ---------- 三角形上均匀 0<y<x<1 ----------
ok("三角形 P(X+Y>1)=1/2", sp.integrate(sp.integrate(2, (y, 1-x, x)), (x, sp.Rational(1,2), 1)) == sp.Rational(1,2))
ok("三角形 f_X=2x", sp.integrate(2, (y,0,x)) == 2*x)
ok("三角形 f_Y=2(1-y)", sp.integrate(2, (x,y,1)) == 2*(1-y))
# ---------- 棍子：X~U(0,1), Y|X~U(0,x) ----------
fY = sp.integrate(1/xp, (xp, yp, 1))
ok("棍子 f_Y=-ln y", sp.simplify(fY + sp.log(yp)) == 0)
ok("棍子 P(Y>1/2)", sp.simplify(sp.integrate(-sp.log(yp), (yp, sp.Rational(1,2), 1)) - (sp.Rational(1,2) - sp.log(2)/2)) == 0)
ok("棍子 数值", abs(0.5 - np.log(2)/2 - 0.15343) < 1e-4)
# ---------- 独立性 ----------
ok("4xy 总量", sp.integrate(sp.integrate(4*x*y, (x,0,1)), (y,0,1)) == 1)
ok("8xy 三角形总量", sp.integrate(sp.integrate(8*x*y, (x,0,y)), (y,0,1)) == 1)
fx8 = sp.integrate(8*x*y, (y,x,1)); fy8 = sp.integrate(8*x*y, (x,0,y))
ok("8xy 边缘", sp.simplify(fx8 - 4*x*(1-x**2)) == 0 and sp.simplify(fy8 - 4*y**3) == 0)
ok("8xy 不独立", sp.simplify(8*sp.Rational(1,2)*sp.Rational(1,4) - fx8.subs(x,sp.Rational(1,2))*fy8.subs(y,sp.Rational(1,4))) != 0)
# 用两个矩形事件直接核对三角形支撑导致的不独立，避免在支撑外代入密度公式。
ok("8xy 支撑外的点", Fr(0) != Fr(49,4096) and Fr(49,4096) > 0)
# 两骰子点数和与第一颗不独立
pairs = [(a,b) for a in range(1,7) for b in range(1,7)]
P_joint = Fr(sum(1 for a,b in pairs if a==1 and a+b==12), 36)
ok("S 与 X1 不独立", P_joint == 0 and Fr(1,6)*Fr(1,36) > 0)
ok("X1,X2 独立", all(Fr(1,36) == Fr(1,6)*Fr(1,6) for _ in pairs))
# ---------- 二维正态 ⑦ ----------
S = sp.Matrix([[2,1],[1,2]])
ok("⑦ |Σ|=3", S.det() == 3)
ok("⑦ Σ^{-1}", S.inv() == sp.Rational(1,3)*sp.Matrix([[2,-1],[-1,2]]))
rho = sp.Rational(1,2)
dens_const = 1/(2*sp.pi*sp.sqrt(2)*sp.sqrt(2)*sp.sqrt(1-rho**2))
ok("⑦ 常数 1/(2π√3)", sp.simplify(dens_const - 1/(2*sp.pi*sp.sqrt(3))) == 0)
q_general = 1/(2*(1-rho**2))*(x**2/2 - 2*rho*x*y/2 + y**2/2)
ok("⑦ 指数 (x²-xy+y²)/3", sp.simplify(q_general - (x**2 - x*y + y**2)/3) == 0)
ok("⑦ 配方", sp.simplify((x**2 - x*y + y**2)/3 - ((y - x/2)**2/(2*sp.Rational(3,2)) + x**2/(2*2))) == 0)
ok("⑦ 条件 N(x/2,3/2)", rho*sp.sqrt(2)/sp.sqrt(2) == sp.Rational(1,2) and 2*(1-rho**2) == sp.Rational(3,2))
ok("⑦ P(Y>2|X=2)", abs(1-norm.cdf(1/np.sqrt(1.5)) - 0.2071) < 1e-3)
print("   P(Y>2|X=2) = %.4f" % (1-norm.cdf(1/np.sqrt(1.5))))
ok("⑦ P(Y>1|X=2)=0.5", abs(1-norm.cdf(0)-0.5) < 1e-12)
# 标准二维正态：配方恒等式
r = sp.symbols('r', real=True)
ok("配方恒等式", sp.simplify((x**2 - 2*r*x*y + y**2) - ((y - r*x)**2 + (1-r**2)*x**2)) == 0)
# 采样构造
L = np.array([[np.sqrt(2),0],[1/np.sqrt(2),np.sqrt(1.5)]])
ok("构造 LL^T=Σ", np.allclose(L@L.T, [[2,1],[1,2]]))
e = np.array([1.0,-1.0]); xy = L@e
print("   (ε1,ε2)=(1,-1) -> (%.4f, %.4f)" % tuple(xy))
ok("构造数值", abs(xy[0]-1.4142) < 1e-3 and abs(xy[1]+0.5176) < 1e-3)
rng = np.random.default_rng(2026)
E = rng.standard_normal((100000,2)); XY = E@L.T
Cv = np.cov(XY.T)
print("   样本协方差", Cv.round(3).tolist(), " Var(X+Y)=%.3f Var(X-Y)=%.3f" % ((XY[:,0]+XY[:,1]).var(), (XY[:,0]-XY[:,1]).var()))
sel = XY[np.abs(XY[:,0]-2) < 0.1]
print("   X在[1.9,2.1]的样本数 %d, Y 均值 %.3f, 方差 %.3f" % (len(sel), sel[:,1].mean(), sel[:,1].var()))
print("   P(Y>2 | X≈2) 频率 %.4f" % (sel[:,1] > 2).mean())
ok("模拟-协方差", abs(Cv[0,1]-1) < 0.03 and abs(Cv[0,0]-2) < 0.04)
ok("模拟-条件均值", abs(sel[:,1].mean()-1) < 0.05 and abs(sel[:,1].var()-1.5) < 0.1)
ok("模拟-Var(X+Y)", abs((XY[:,0]+XY[:,1]).var()-6) < 0.1 and abs((XY[:,0]-XY[:,1]).var()-2) < 0.05)
# X+Y ~ N(0,6) 用 f(x,z-x) 积分
zz = sp.symbols('zz', real=True)
fxy = 1/(2*sp.pi*sp.sqrt(3))*sp.exp(-(x**2 - x*y + y**2)/3)
fz = sp.integrate(fxy.subs(y, zz-x), (x,-sp.oo,sp.oo))
ok("⑦ X+Y~N(0,6)", sp.simplify(fz - sp.exp(-zz**2/12)/sp.sqrt(12*sp.pi)) == 0)
# 特征值
ok("⑦ 特征值 3,1", sorted(S.eigenvals().keys()) == [1,3])

# ---------- §7 和 ----------
# 骰子和卷积
pd = {k: Fr(1,6) for k in range(1,7)}
pS = {s: sum(pd[i]*pd.get(s-i,0) for i in pd) for s in range(2,13)}
ok("骰子和卷积", all(pS[s] == Fr(6-abs(s-7),36) for s in pS))
ok("S=7 六项", sum(1 for i in range(1,7) if 1 <= 7-i <= 6) == 6)
# U+U
conv = lambda zv: sp.integrate(1, (x, sp.Max(0, zv-1), sp.Min(1, zv)))
ok("U+U 三角", sp.integrate(1,(x,0,sp.Rational(1,2))) == sp.Rational(1,2) and sp.integrate(1,(x,sp.Rational(1,2),1)) == sp.Rational(1,2))
ok("U+U 总量", sp.integrate(z, (z,0,1)) + sp.integrate(2-z, (z,1,2)) == 1)
ok("U+U P(Z<=1/2)=1/8", sp.integrate(z,(z,0,sp.Rational(1,2))) == sp.Rational(1,8))
# Poisson 可加
from scipy.stats import poisson
ok("泊松和 P(N>=5)", abs((1-poisson.cdf(4,3)) - 0.1847) < 1e-3)
pc = [sum(poisson.pmf(i,1.5)*poisson.pmf(k-i,1.5) for i in range(k+1)) for k in range(6)]
ok("泊松卷积=P(3)", all(abs(pc[k]-poisson.pmf(k,3)) < 1e-12 for k in range(6)))
print("   P(N=0)=%.4f P(N<=2)=%.4f P(N>=5)=%.4f" % (poisson.pmf(0,3), poisson.cdf(2,3), 1-poisson.cdf(4,3)))
# 二项可加
from scipy.stats import binom
ok("二项和", all(abs(sum(binom.pmf(i,3,0.7)*binom.pmf(k-i,4,0.7) for i in range(k+1)) - binom.pmf(k,7,0.7)) < 1e-12 for k in range(8)))
# 正态可加: 配方
s1, s2 = sp.symbols('s1 s2', positive=True)
ok("正态配方", sp.simplify(x**2/s1**2 + (zz-x)**2/s2**2 - ((s1**2+s2**2)/(s1**2*s2**2)*(x - s1**2*zz/(s1**2+s2**2))**2 + zz**2/(s1**2+s2**2))) == 0)
# 身高: X~N(170,36), Y~N(160... ) 设两人身高之和
ok("N(170,36)+N(160,64)", 170+160 == 330 and 36+64 == 100)
print("   P(|X+Y-330|<=10)= %.4f" % (norm.cdf(1)-norm.cdf(-1)))
# 比值 X/Y, E(1)
zp = sp.symbols('z', positive=True)
Fz = sp.integrate(sp.exp(-yp)*(1-sp.exp(-zp*yp)), (yp,0,sp.oo))
ok("比值F", sp.simplify(Fz - zp/(1+zp)) == 0 and sp.simplify(sp.diff(zp/(1+zp), zp) - 1/(1+zp)**2) == 0)
# Erlang
lam = 3
fE = sp.integrate(lam*sp.exp(-lam*xp)*lam*sp.exp(-lam*(zp-xp)), (xp,0,zp))
ok("两指数之和", sp.simplify(fE - lam**2*zp*sp.exp(-lam*zp)) == 0)
ok("P(Z>1)=4e^{-3}", abs(float(sp.integrate(lam**2*zp*sp.exp(-lam*zp), (zp,1,sp.oo))) - 4*np.exp(-3)) < 1e-9)
print("   4e^{-3}=%.4f" % (4*np.exp(-3)))
# 离散 X1,X2 ~ E(3) 平均 20 分钟 -> 两间隔和的平均 40 分钟
# ---------- §8 ----------
ok("骰子最大值", all(Fr(m*m,36)-Fr((m-1)**2,36) == Fr(2*m-1,36) for m in range(1,7)))
ok("骰子最小值", all(Fr((7-u)**2-(6-u)**2,36) == Fr(13-2*u,36) for u in range(1,7)))
ok("U(0,1) n=3 最大值密度", sp.integrate(3*z**2,(z,0,1)) == 1)
ok("min n=3 密度", sp.integrate(3*(1-z)**2,(z,0,1)) == 1)
# 元件
ok("串联 P(min>0.5)", abs(np.exp(-1.5)-0.22313) < 1e-5)
ok("并联 P(max<=1)", abs((1-np.exp(-1))**3 - 0.25257) < 1e-4)
print("   (1-e^-1)^3 = %.4f ; e^-1.5 = %.4f" % ((1-np.exp(-1))**3, np.exp(-1.5)))
ok("max 密度", sp.simplify(sp.diff((1-sp.exp(-zp))**3, zp) - 3*sp.exp(-zp)*(1-sp.exp(-zp))**2) == 0)
l1,l2 = sp.symbols('l1 l2', positive=True)
ok("min E(l1)E(l2)", sp.simplify(1-(1-(1-sp.exp(-l1*zp)))*(1-(1-sp.exp(-l2*zp))) - (1-sp.exp(-(l1+l2)*zp))) == 0)
# 模拟：串联并联
rng = np.random.default_rng(7)
L3 = rng.exponential(1.0, (100000,3))
print("   模拟 P(min>0.5)=%.4f P(max<=1)=%.4f" % ((L3.min(1)>0.5).mean(), (L3.max(1)<=1).mean()))
ok("模拟-串联", abs((L3.min(1)>0.5).mean()-np.exp(-1.5)) < 0.005)
ok("模拟-并联", abs((L3.max(1)<=1).mean()-(1-np.exp(-1))**3) < 0.005)
# 最小值 vs 最大值 混合 例: X,Y indep, P(max<=m)
# X~E(2),Y~E(3) 的 P(X<Y) 与 min 无关: 2/5
ok("P(X<Y)=λ1/(λ1+λ2)", sp.integrate(2*sp.exp(-2*xp)*sp.exp(-3*xp),(xp,0,sp.oo)) == sp.Rational(2,5))
