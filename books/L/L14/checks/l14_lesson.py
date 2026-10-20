#!/usr/bin/env python3
"""独立核对 L.14 讲义例题中的数值和结论。"""
import sympy as sp
R=sp.Rational
def M(*xs):
    if len(xs) == 4:
        return sp.Matrix(2, 2, xs)
    if len(xs) == 9:
        return sp.Matrix(3, 3, xs)
    return sp.Matrix(xs)
def report(tag, ok): print(f"{'PASS' if ok else 'FAIL'} {tag}")

def inertia(A):
    ev=A.eigenvals()
    return sum(m for e,m in ev.items() if e>0), sum(m for e,m in ev.items() if e<0)

# 例1
A1=M(1,2,-1,2,3,1,-1,1,0)
report('例1', A1.det() == -8 and A1.rank()==3)
# 例2
A2=M(1,-2,0,-2,2,-2,0,-2,3)
cp=sp.expand(A2.charpoly().as_expr())
lam=next(iter(cp.free_symbols))
report('例2', cp == lam**3-6*lam**2+3*lam+10
       and set(A2.eigenvals()) == {-1,2,5}
       and all(A2*v == lam*v for lam,v in [(-1,M(2,2,1)),(2,M(-2,1,2)),(5,M(1,-2,2))]))
# 例3
A3=M(1,1,1,1,2,3,1,3,5); C3=M(1,-1,1,0,1,-2,0,0,1)
report('例3', C3.det()==1 and C3.T*A3*C3 == M(1,0,0,0,1,0,0,0,0))
# 例4
A41=M(0,1,1,0); A42=M(1,0,0,-1); A43=M(2,0,0,-3); A44=sp.eye(2)
report('例4', inertia(A41)==inertia(A42)==inertia(A43)==(1,1) and inertia(A44)==(2,0)
       and set(A41.eigenvals())==set(A42.eigenvals())=={1,-1})
# 例5 and 6
report('例5', all(lam**2-3*lam+2==0 for lam in [1,2]) and all(lam>0 for lam in [1,2]))
A6=sp.Matrix([[1,2],[0,1],[1,0]]); K=sp.eye(2)+A6.T*A6
report('例6', K==K.T and K.det()>0 and K[0,0]>0)
# 例7
T=sp.symbols('T'); A7=M(1,T,-1,T,1,2,-1,2,5)
D1=A7[0,0]; D2=A7[:2,:2].det(); D3=A7.det()
report('例7', D1==1 and sp.expand(D2-(1-T**2))==0 and sp.expand(D3-(-T*(5*T+4)))==0
       and all(bool(D2.subs(T,v)>0) == (-1 < v < 1) for v in [-2,-1,sp.Rational(-1,2),0,sp.Rational(1,2),1,2])
       and all(bool(D2.subs(T,v)>0 and D3.subs(T,v)>0) == (-R(4,5) < v < 0) for v in [-2,-R(4,5),-R(1,2),-R(1,10),0,1]))
# 例8
A8=M(-5,2,2,2,-6,0,2,0,-4)
report('例8', [A8[:k,:k].det() for k in [1,2,3]] == [-5,26,-80]
       and inertia(A8)==(0,3))
# 例9 (same eigen data as example 2)
report('例9', -4 == (-1)*4 and 20==5*4
       and M(R(4,3),R(4,3),R(2,3)).norm()==2
       and M(R(2,3),R(-4,3),R(4,3)).norm()==2)
# 例10
B10=sp.Matrix([[1,1],[1,-1],[1,0]]); b10=M(1,2,0)
report('例10', 2*B10.T*(B10*M(sp.symbols('x1'),sp.symbols('x2'))-b10) == 2*B10.T*B10*M(sp.symbols('x1'),sp.symbols('x2'))-2*B10.T*b10
       and 2*B10.T*B10 == M(6,0,0,4))
# 例11
x,y,z=sp.symbols('x y z'); f11=x**3+y**2+z**2+12*x*y+2*z
crit=[{x:0,y:0,z:-1},{x:24,y:-144,z:-1}]
H11=sp.hessian(f11,(x,y,z))
report('例11', H11==M(6*x,12,0,12,2,0,0,0,2)
       and f11.subs(crit[1])==-6913 and f11.subs(crit[0])==-1
       and H11.subs(crit[1]).det()>0 and H11.subs(crit[1])[0,0]>0)
# 例12
H12=M(R(11,2),R(9,2),R(9,2),R(11,2)); w0=M(2,0); eta=R(18,100)
w1=(sp.eye(2)-eta*H12)*w0; w2=(sp.eye(2)-eta*H12)*w1
report('例12', set(H12.eigenvals())=={1,10} and w1==M(R(1,50),-R(81,50))
       and w2==M(R(3281,2500),-R(81,2500)) and eta < R(2,10))
