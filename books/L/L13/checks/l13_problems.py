import sympy as sp

def ok(tag, cond):
    print(f"{'PASS' if bool(cond) else 'FAIL'} {tag}")

def mat_equal(a,b): return all(sp.simplify(x)==0 for x in (a-b))

# 01
M=sp.Matrix([[0,-2],[2,0]])
ok('L13-01', sp.factor(M.charpoly().as_expr())==sp.Symbol('lambda')**2+4 and all(sp.re(z)==0 for z in M.eigenvals()))
# 02
N=sp.Matrix([[1,1,0],[1,-1,2]])
ns=N.nullspace(); ok('L13-02', len(ns)==1 and ns[0][1]/ns[0][0]==-1 and ns[0][2]/ns[0][0]==-1)
# 03
A=sp.Matrix([[1,1],[0,2]]); E=sp.eye(2)
orthogonal_diagonalizable = A.T == A
real_spectrum_not_enough = A.eigenvals() == {1:1,2:1} and A.T != A
same_eigenspace_basis_not_orthogonal = sp.Matrix([1,0]).dot(sp.Matrix([1,1])) != 0
ok('L13-03', E.T==E and orthogonal_diagonalizable is False and real_spectrum_not_enough and same_eigenspace_basis_not_orthogonal)
# 04
t=sp.symbols('t'); At=sp.Matrix([[2,t],[t,2]]); Q=sp.Matrix([[1,1],[1,-1]])/sp.sqrt(2)
D=sp.simplify(Q.T*At*Q)
ok('L13-04', D==sp.diag(t+2,2-t) and (D.subs(t,3)==sp.diag(5,-1)))
# 05
A5=sp.Matrix([[3,1,1],[1,3,1],[1,1,3]]); q=sp.ones(3,1)/sp.sqrt(3); b=sp.Matrix([1,-1,0])
ok('L13-05', A5*q==5*q and A5*b==2*b)
# 06
R=sp.Matrix([[0,-1],[1,0]])
ok('L13-06', R.charpoly().as_expr()==sp.Symbol('lambda')**2+1)
# 07
x=sp.symbols('x'); Bt=sp.Matrix([[1,x],[0,2]]); e2=sp.Matrix([0,1])
ok('L13-07', Bt.subs(x,0)*e2==2*e2)
ok('L13-07-condition', Bt.subs(x,1)*e2!=2*e2)
# 08
AA=sp.diag(1,1,2); BB=sp.Matrix([[1,1,0],[0,1,0],[0,0,2]])
ok('L13-08', AA.charpoly().as_expr()==BB.charpoly().as_expr() and len((AA-sp.eye(3)).nullspace())==2 and len((BB-sp.eye(3)).nullspace())==1)
# 09
q1=sp.Matrix([1,-1,0])/sp.sqrt(2); q2=sp.Matrix([1,1,-2])/sp.sqrt(6); q3=sp.ones(3,1)/sp.sqrt(3); Q9=sp.Matrix.hstack(q1,q2,q3)
ok('L13-09', mat_equal(Q9.T*Q9,sp.eye(3)) and q1.dot(q2)==0 and q1.dot(q3)==0 and q2.dot(q3)==0)
# 10
q10=sp.Matrix([1,-1,1])/sp.sqrt(3); A10=2*sp.eye(3)+3*q10*q10.T; b10=sp.Matrix([1,2,0]);
res=(A10**2-3*A10+sp.eye(3))*b10
ok('L13-10', res==sp.Matrix([-5,2,-4]))
# 11
pts=[sp.Matrix([1,1]),sp.Matrix([3,3]),sp.Matrix([2,0])]; mu=sum(pts,sp.zeros(2,1))/3; C=sum(((x-mu)*(x-mu).T for x in pts),sp.zeros(2))/3
ok('L13-11', mu==sp.Matrix([2,sp.Rational(4,3)]) and C==sp.Matrix([[sp.Rational(2,3),sp.Rational(2,3)],[sp.Rational(2,3),sp.Rational(14,9)]]) and max(C.eigenvals())==sp.Rational(10,9)+2*sp.sqrt(13)/9)
# 12 manual
print('MANUAL L13-12')
# 13 manual + numeric
print('MANUAL L13-13')
A13=sp.diag(1,1,0)
ok('L13-13-num', (A13+sp.eye(3)).det()==4)
# 14
ok('L13-14', R.charpoly().as_expr()==sp.Symbol('lambda')**2+1 and R.eigenvals()=={sp.I:1,-sp.I:1} and R.T==-R and R.det()==1)
# 15
A15=sp.Matrix([[2,1],[1,2]]); ok('L13-15', A15**6*sp.Matrix([1,-1])==sp.Matrix([1,-1]) and A15**6*sp.Matrix([1,1])==729*sp.Matrix([1,1]))
# 16
q16=sp.Matrix([1,2])/sp.sqrt(5); P=q16*q16.T; ok('L13-16', mat_equal(P**2,P) and P*sp.Matrix([3,4])==sp.Matrix([11,22])/5)
# 17
q17=sp.ones(3,1)/sp.sqrt(3); A17=2*(sp.eye(3)-q17*q17.T); rhs=sp.Matrix([1,0,1]); aug=A17.row_join(rhs); ok('L13-17', mat_equal(A17,sp.Matrix([[4,-2,-2],[-2,4,-2],[-2,-2,4]])/3) and A17.rank()!=aug.rank())
# 18 manual
print('MANUAL L13-18')
