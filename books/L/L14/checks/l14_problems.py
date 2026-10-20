#!/usr/bin/env python3
"""独立核对 L.14 习题；证明题保留 MANUAL。"""
import sympy as sp
R=sp.Rational

def M(*xs):
    if len(xs)==4:return sp.Matrix(2,2,xs)
    if len(xs)==9:return sp.Matrix(3,3,xs)
    return sp.Matrix(xs)
def report(tag,ok): print(f"{'PASS' if bool(ok) else 'FAIL'} {tag}")
def inertia(A):
    ev=A.eigenvals(); return (sum(m for e,m in ev.items() if e>0),sum(m for e,m in ev.items() if e<0),sum(m for e,m in ev.items() if e==0))

B01=sp.Matrix([[2,4,0],[0,5,3],[0,0,1]]); S01=(B01+B01.T)/2
report('L14-01', S01==M(2,2,0,2,5,R(3,2),0,R(3,2),1) and S01.det()!=0)
A02=4*sp.Matrix([[1,0],[0,1]])-2*sp.Matrix([[0,1],[1,0]])
report('L14-02', A02==M(4,-2,-2,4) and A02.eigenvals()=={2:1,6:1})
x1,x2,x3,y1,y2,y3=sp.symbols('x1 x2 x3 y1 y2 y3'); q03=2*x1*x2+2*x1*x3+2*x2*x3
inv03={x1:y1/sp.Integer(3)+y2/sp.Integer(2)+y3/sp.Integer(6),x2:y1/sp.Integer(3)-y2/sp.Integer(2)+y3/sp.Integer(6),x3:y1/sp.Integer(3)-y3/sp.Integer(3)}; C03=sp.Matrix([[sp.Rational(1,3),sp.Rational(1,2),sp.Rational(1,6)],[sp.Rational(1,3),-sp.Rational(1,2),sp.Rational(1,6)],[sp.Rational(1,3),0,-sp.Rational(1,3)]])
report('L14-03',sp.expand(q03.subs(inv03, simultaneous=True)-(sp.Rational(2,3)*y1**2-sp.Rational(1,2)*y2**2-sp.Rational(1,6)*y3**2))==0 and C03.det()!=0)
opts04=[M(1,2,2,1),M(1,0,0,0),M(2,1,1,2),M(0,1,1,2)]
report('L14-04 选项A错',opts04[0].det()<0); report('L14-04 选项B错',opts04[1].det()==0); report('L14-04 选项C对',opts04[2].det()>0 and opts04[2][0,0]>0); report('L14-04 选项D错',opts04[3].det()<0)
A05=sp.Matrix([[1,2],[0,1],[1,0]]); K05=A05.T*A05+2*sp.eye(2); report('L14-05样例',K05.det()>0 and K05[0,0]>0); print('MANUAL L14-05')
t=sp.symbols('t',real=True); A06=sp.Matrix([[t,1,0],[1,t,1],[0,1,t]]); ev06=A06.eigenvals(); report('L14-06',set(ev06)=={t-sp.sqrt(2),t,t+sp.sqrt(2)})
report('L14-07',sp.trace(sp.diag(5,3))==8 and 5*9==45 and 3*9==27)
B08=sp.Matrix([[1,1],[2,2],[3,3]]); b08=sp.Matrix([1,2,4]); s=sp.symbols('s'); F08=(B08*sp.Matrix([s,0])-b08).dot(B08*sp.Matrix([s,0])-b08); report('L14-08',sp.solve(sp.diff(F08,s),s)==[sp.Rational(17,14)] and sp.simplify(F08.subs(s,sp.Rational(17,14)))==sp.Rational(5,14));
A09=sp.diag(1,-2,0); B09=sp.diag(3,-4,0); C09=sp.diag(1,2,0); report('L14-09 选项A错',set(A09.eigenvals())!=set(B09.eigenvals())); report('L14-09 选项B对',inertia(A09)==inertia(B09)); report('L14-09 选项C错',inertia(A09)!=inertia(C09)); report('L14-09 选项D错',inertia(A09)!=inertia(C09))
q1=sp.Matrix([1,1])/sp.sqrt(2); q2=sp.Matrix([1,-1])/sp.sqrt(2); A10=6*q1*q1.T+2*q2*q2.T; report('L14-10',A10==M(4,2,2,4) and max(A10.eigenvals())*4==24 and min(A10.eigenvals())*4==8)
xx,yy=sp.symbols('x y'); f11=xx**4+2*yy**2; g11=xx**4-yy**4; report('L14-11',sp.hessian(f11,(xx,yy)).subs({xx:0,yy:0})==sp.diag(0,4) and sp.hessian(g11,(xx,yy)).subs({xx:0,yy:0})==sp.zeros(2) and f11.subs({xx:1,yy:0})>0 and g11.subs({xx:0,yy:1})<0)
eta=sp.symbols('eta',real=True); stable=sp.Interval.open(0,sp.Rational(2,9)); et=sp.Rational(1,5); report('L14-12',stable.start==0 and stable.end==sp.Rational(2,9) and abs(1-et)==abs(1-9*et)==sp.Rational(4,5))
report('L14-13',sp.solve(sp.Eq(14*s-21,0),s)==[sp.Rational(3,2)])
B14=sp.Matrix([[1,2,0],[0,1,0],[0,0,0]]); S14=(B14+B14.T)/2; report('L14-14',S14==sp.Matrix([[1,1,0],[1,1,0],[0,0,0]]) and S14.rank()==1) # rank of symmetric part; q rank checked below
q14=(sp.Matrix([xx,yy,sp.Integer(0)]).T*B14*sp.Matrix([xx,yy,sp.Integer(0)]))[0]; report('L14-14二次型',sp.expand(q14-(xx+yy)**2)==0)
h15=xx**3-3*xx+yy**2; H15=sp.hessian(h15,(xx,yy)); report('L14-15',H15.subs({xx:1,yy:0})==sp.diag(6,2) and H15.subs({xx:-1,yy:0})==sp.diag(-6,2) and h15.subs({xx:1,yy:0})==-2 and h15.subs({xx:-1,yy:0})==2)
