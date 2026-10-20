"""L.3 习题独立验算。"""
import sympy as sp

def ok(tag, condition):
    print(f"PASS {tag}" if bool(condition) else f"FAIL {tag}")

# L3-01
A = sp.Matrix([[1,-2,0],[2,1,3]]); x=sp.Matrix([2,-1,1])
ok("L3-01", A*x==sp.Matrix([4,6]) and sum((x[j]*A[:,j] for j in range(3)),sp.zeros(2,1))==A*x)
# L3-02
A2=sp.Matrix([[0,-1],[1,0]]); e1,e2=sp.eye(2)[:,0],sp.eye(2)[:,1]
ok("L3-02", A2*e1==sp.Matrix([0,1]) and A2*e2==sp.Matrix([-1,0]) and A2.det()!=0)
# L3-03
ok("L3-03", sp.Matrix([[1,-1],[2,1]])*sp.Matrix([2,3])==sp.Matrix([-1,7]))
# L3-04
A4=sp.Matrix([[1,0,2],[0,1,-1]]); P4=sp.Rational(1,2)*sp.Matrix([[1,1,0],[1,1,0],[0,0,0]])
ok("L3-04", A4*P4==sp.Matrix([[sp.Rational(1,2),sp.Rational(1,2),0],[sp.Rational(1,2),sp.Rational(1,2),0]]) and A4.shape==(2,3) and P4.shape==(3,3))
# L3-05
W=sp.Matrix([[1,-1],[2,0]]); b=sp.Matrix([1,-2]); y=W*sp.Matrix([2,3])+b
ok("L3-05", y==sp.Matrix([0,2]) and b!=sp.zeros(2,1))
# L3-06
A6=sp.diag(1,0); B6=sp.Matrix([[0,0],[1,0]]); C6=sp.Matrix([[0,1],[0,0]])
ok("L3-06", A6*B6==sp.zeros(2) and A6!=sp.zeros(2) and B6!=sp.zeros(2) and C6*A6==sp.zeros(2) and C6!=sp.zeros(2))
# L3-07
A7=sp.Matrix([[1,1],[0,0]]); B7=sp.Matrix([[0,0],[1,0]])
ok("L3-07", A7*B7!=B7*A7 and (A7+B7)**2==A7**2+A7*B7+B7*A7+B7**2 and (A7+B7)**2!=A7**2+2*A7*B7+B7**2 and (A7-B7)*(A7+B7)!=A7**2-B7**2 and (A7+B7)*(A7-B7)!=A7**2-B7**2)
# L3-08 formal coefficient recurrence

def mul_pair(u,v):
    p,q=u; r,s=v
    return (4*p*r+p*s+q*r, -3*p*r+q*s)
pair=(1,0)
for _ in range(4): pair=mul_pair(pair,(1,0))
ok("L3-08", pair==(121,-120))
# L3-09 direct instances for triangular structure plus diagonal
A9=sp.Matrix([[1,2,3],[0,4,5],[0,0,6]]); B9=sp.Matrix([[2,1,0],[0,3,4],[0,0,5]]); C9=A9*B9
ok("L3-09", C9[1,0]==0 and C9[2,0]==0 and C9[2,1]==0 and all(C9[i,i]==A9[i,i]*B9[i,i] for i in range(3)))
# L3-10
alpha=sp.Matrix([1,2,-1]); beta=sp.Matrix([2,0,1]); A10=alpha*beta.T
ok("L3-10", A10[:,1]==sp.zeros(3,1) and all(A10[:,j]==beta[j]*alpha for j in range(3)) and beta.dot(alpha)==1 and A10**4==A10)
# L3-11
R=sp.Matrix([[0,-1],[1,0]]); a,b,c,d=sp.symbols('a b c d'); X=sp.Matrix([[a,b],[c,d]])
ok("L3-11", R*X-X*R==sp.Matrix([[-b-c,a-d],[a-d,b+c]]) and X.subs({c:-b,d:a})==sp.Matrix([[a,b],[-b,a]]) and X.subs({b:0,c:0,d:a}).T==X.subs({b:0,c:0,d:a}))
# L3-12
R12=R; J12=sp.Matrix([[-1,2],[0,-1]])
for n in (1,2,4,5):
    Jn=sp.Matrix([[(-1)**n,2*n*(-1)**(n-1)],[0,(-1)**n]])
    ok(f"L3-12-n{n}", sp.diag(R12,J12)**n==sp.diag(R12**n,Jn))
ok("L3-12-M4", sp.diag(R12,J12)**4==sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,-8],[0,0,0,1]]))
# L3-13
P13=sp.Rational(1,10)*sp.Matrix([[1,3],[3,9]])
ok("L3-13", P13.T==P13 and P13**2==P13 and P13*sp.Matrix([2,1])==sp.Matrix([sp.Rational(1,2),sp.Rational(3,2)]) and P13*sp.Matrix([-3,1])==sp.zeros(2,1))
# L3-14
Q=sp.Matrix([[1,0,1],[0,1,1],[1,1,0]])
coeff=Q.inv()*sp.Matrix([2,3,4])
ok("L3-14", Q.det()==-2 and coeff==sp.Matrix([sp.Rational(3,2),sp.Rational(5,2),sp.Rational(1,2)]) and Q*coeff==sp.Matrix([2,3,4]))
# L3-15
P15=sp.Rational(1,5)*sp.Matrix([[4,-2],[-2,1]]); F15=2*P15-sp.eye(2)
ok("L3-15", F15**2==sp.eye(2) and F15*sp.Matrix([1,3])==sp.Matrix([sp.Rational(-9,5),sp.Rational(-13,5)]))
