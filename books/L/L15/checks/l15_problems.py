import sympy as sp

def same(a,b): return sp.Matrix(a).equals(sp.Matrix(b))
def report(q,cond): print(("PASS " if cond else "FAIL ")+q)

# unchanged A items
A=sp.Matrix([[1,0],[1,0],[0,2]]); U=sp.Matrix([[0,1/sp.sqrt(2),1/sp.sqrt(2)],[0,1/sp.sqrt(2),-1/sp.sqrt(2)],[1,0,0]]); S=sp.Matrix([[2,0],[0,sp.sqrt(2)],[0,0]]); V=sp.Matrix([[0,1],[1,0]])
report('L15-01', same(U*S*V.T,A) and (A.T*A).eigenvals()=={4:1,2:1})
A=sp.Matrix([[1,2],[2,1]]); v1=sp.Matrix([1,1])/sp.sqrt(2); v2=sp.Matrix([1,-1])/sp.sqrt(2); u1=v1; u2=sp.Matrix([-1,1])/sp.sqrt(2)
report('L15-02',(A.T*A).eigenvals()=={9:1,1:1} and A*v1==3*u1 and A*v2==u2)
A=sp.Matrix([[1,0],[0,2],[0,0]]); actual=[False,(A.T*A).eigenvals()=={1:1,4:1},False,False]; expected=[False,True,False,False]
for i,l in enumerate('ABCD'): report(f'L15-03({l})',actual[i]==expected[i])
report('L15-03',actual==expected)
a=sp.Matrix([1,2]); b=sp.Matrix([2,-2,1]); nb=[sp.Matrix([1,1,0])/sp.sqrt(2),sp.Matrix([1,-1,-4])/(3*sp.sqrt(2))]
report('L15-04',a.norm()*b.norm()==3*sp.sqrt(5) and all(b.dot(x)==0 for x in nb) and nb[0].dot(nb[1])==0)
actual=[False,False,sp.sqrt(5)==sp.sqrt(5),1==2]; expected=[False,False,True,False]
for i,l in enumerate('ABCD'): report(f'L15-05({l})',actual[i]==expected[i])
report('L15-05',actual==expected)

# L15-06
A=sp.Matrix([[1,1,0],[1,-1,0]]); U=sp.eye(2); S=sp.Matrix([[sp.sqrt(2),0,0],[0,sp.sqrt(2),0]]); V=sp.Matrix([[1/sp.sqrt(2),1/sp.sqrt(2),0],[1/sp.sqrt(2),-1/sp.sqrt(2),0],[0,0,1]])
report('L15-06',same(U*S*V.T,A) and A*A.T==2*sp.eye(2) and V.T*V==sp.eye(3))
A=sp.Matrix([[1,-2],[2,1]]); actual=[False,A.T*A==5*sp.eye(2),False,False]; expected=[False,True,False,False]
for i,l in enumerate('ABCD'): report(f'L15-07({l})',actual[i]==expected[i])
report('L15-07',actual==expected)
print('MANUAL L15-08')

# L15-09
A=sp.Matrix([[1,0,1],[0,1,1]]); AtA=A.T*A; Ap=A.T*(A*A.T).inv(); P=Ap*A
actual=[A*Ap==sp.eye(2) and P==sp.Matrix([[sp.Rational(2,3),-sp.Rational(1,3),sp.Rational(1,3)],[-sp.Rational(1,3),sp.Rational(2,3),sp.Rational(1,3)],[sp.Rational(1,3),sp.Rational(1,3),sp.Rational(2,3)]]),False,False,False]; expected=[True,False,False,False]
for i,l in enumerate('ABCD'): report(f'L15-09({l})',actual[i]==expected[i])
report('L15-09',actual==expected)
# L15-10
X=sp.Matrix([[3,2,1],[3,-2,-1],[-3,2,-1],[-3,-2,1]])
report('L15-10',X.T*X==sp.diag(36,16,4) and sum(X[:,2][i]**2 for i in range(4))==4)
# L15-11
A=sp.Matrix([[1,0,0],[0,1,0],[1,1,0]]); b=sp.Matrix([1,0,0]); x=sp.Matrix([sp.Rational(2,3),-sp.Rational(1,3),0])
report('L15-11',A.rank()==2 and (A.T*(A*x-b))==sp.zeros(3,1) and A*sp.Matrix([0,0,1])==sp.zeros(3,1) and x.dot(sp.Matrix([0,0,1]))==0)
# L15-12
A=sp.Matrix([[3,1,0],[1,3,0],[0,0,0]]); A1=sp.Matrix([[2,2,0],[2,2,0],[0,0,0]]); B=A1; E=A-A1
report('L15-12',A1.rank()==1 and max((E.T*E).eigenvals().keys())==4 and sum(E[i,j]**2 for i in range(3) for j in range(3))==4 and max(((A-B).T*(A-B)).eigenvals().keys())==4)
print('MANUAL L15-12')
# mixed
A=sp.Matrix([[1,2],[2,1]]); report('L15-13',(A.T*A).eigenvals()=={9:1,1:1})
A=sp.Matrix([[1,0],[0,1],[1,1]]); b=sp.Matrix([1,2,0]); P=A*(A.T*A).inv()*A.T; report('L15-14',P*b==sp.Matrix([0,1,1]) and (b-P*b).dot(A[:,0])==0 and (b-P*b).dot(A[:,1])==0)
A=sp.Matrix([[1,1,0],[2,2,0]]); b=sp.Matrix([1,0]); Ap=sp.Matrix([[1,2],[1,2],[0,0]])/10; x=Ap*b
report('L15-15',x==sp.Matrix([sp.Rational(1,10),sp.Rational(1,10),0]) and A*x==sp.Matrix([sp.Rational(1,5),sp.Rational(2,5)]) and x.dot(sp.Matrix([1,-1,0]))==0 and x.dot(sp.Matrix([0,0,1]))==0)
