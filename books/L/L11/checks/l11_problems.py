import sympy as sp
lam=sp.symbols('lam')
def check(i,c):
    print(f"PASS {i}" if c else f"FAIL {i}")
    if not c: raise AssertionError(i)
# 01
A=sp.Matrix([[2,0,1],[0,3,0],[1,0,2]])
check('L11-01', A*sp.Matrix([1,0,1])==3*sp.Matrix([1,0,1]) and A*sp.Matrix([0,1,0])==3*sp.Matrix([0,1,0]) and A*sp.Matrix([1,1,0]) not in [2*sp.Matrix([1,1,0]),3*sp.Matrix([1,1,0])])
# 02
A=sp.Matrix([[1,2],[2,1]])
check('L11-02',(lam*sp.eye(2)-A).det().factor()==(lam-3)*(lam+1))
# 03
avec,b=sp.symbols('a b')
check('L11-03', sp.solve([sp.Eq(avec+2,7),sp.Eq(2*avec-b,12)],[avec,b],dict=True)==[{avec:5,b:-2}])
# 04
vals=[1-3,1-3,2-3]
f=lambda x:x*x-3*x+4
check('L11-04', sp.prod(vals)==-4 and sp.prod([f(1),f(1),f(2)])==8)
# 05
A=sp.Matrix([[2,1],[0,3]]); v=sp.Matrix([1,0]); check('L11-05',A.inv()*v==sp.Rational(1,2)*v and A.T*v!=2*v)
# 06
avec=sp.symbols('a'); A=sp.Matrix([[2,1,1],[0,2,0],[avec,0,3]])
A0=A.subs(avec,0); check('L11-06', A0*sp.Matrix([1,0,1])==3*sp.Matrix([1,0,1]) and sp.factor((lam*sp.eye(3)-A0).det())==(lam-3)*(lam-2)**2 and (2*sp.eye(3)-A0).rank()==2)
# 07
x,y=sp.symbols('x y'); sols=sp.solve([sp.Eq(x+y,5),sp.Eq(2*x*y,12)],[x,y],dict=True); check('L11-07', set(tuple(sorted((d[x],d[y]))) for d in sols)=={(2,3)} and 3*3*5==45)
# 08
A=sp.diag(2,1); B=sp.diag(-1,3); check('L11-08',(A+B).eigenvals()=={1:1,4:1})
# 09 manual
print('MANUAL L11-09')
# 10
avec=sp.symbols('a'); P=sp.Matrix([[1,0,0],[0,1,0],[0,0,1]])
A=sp.Matrix([[1,1,0],[-1,3,0],[avec-2,2-avec,avec]])
check('L11-10',sp.simplify(sp.factor((lam*sp.eye(3)-A).det())-(lam-2)**2*(lam-avec))==0 and (2*sp.eye(3)-A.subs(avec,3)).rank()==2 and (2*sp.eye(3)-A.subs(avec,2)).rank()==1)
# 11
c,d=sp.symbols('c d'); check('L11-11', [sp.expand(sp.Rational(8,l)+c*sp.Integer(l)+d) for l in [1,2,4]]==[8+c+d,4+2*c+d,2+4*c+d])
# 12
a,b=sp.symbols('a b'); A=sp.Matrix([[1,1,0],[0,2,1],[0,a,b]])
cp=sp.factor((lam*sp.eye(3)-A).det()); check('L11-12', sp.simplify(cp-(lam-1)*((lam-2)*(lam-b)-a))==0 and (sp.eye(3)-A.subs({a:-1,b:0})).rank()==2)
# 13
u=sp.Matrix([1,2,2]); P=u*u.T/(u.T*u)[0]; check('L11-13',P*P==P and P.eigenvals()=={0:2,1:1} and (P+2*sp.eye(3)).det()==12)
# 14
Q=sp.diag(-1,1,1); check('L11-14',Q.T*Q==sp.eye(3) and Q.det()==-1 and sp.trace(Q)==1 and (Q+2*sp.eye(3)).det()==9)
# 15
x=sp.symbols('x'); m=sp.solve(sp.Eq(sp.symbols('m')+2*(3-sp.symbols('m')),4),sp.symbols('m'))[0]; check('L11-15',sp.solve(x**2-3*x+2,x)==[1,2] and m==2 and 1**2*2==2)
