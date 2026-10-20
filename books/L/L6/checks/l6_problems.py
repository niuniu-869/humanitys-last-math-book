import sympy as sp

def ok(q, cond): print(f"PASS {q}" if bool(cond) else f"FAIL {q}")
A01=sp.Matrix([[2,-1],[3,4]]); ok('L6-01', A01.det()==11 and 7*abs(A01.det())==77)
A02=sp.Matrix([[1,0,2],[-1,3,1],[2,4,0]]); ok('L6-02', A02.det()==-24)
c1,c3=sp.Matrix([1,0,0]),sp.Matrix([0,1,0]); ok('L6-03', sp.Matrix.hstack(c1+c3,c1,c3).det()==0)
A04=sp.Matrix([[0,1,0,0],[2,3,1,0],[0,1,4,1],[0,0,2,5]]); ok('L6-04', A04.det()==-36)
ok('L6-05', sp.Rational(2,-3)==-sp.Rational(2,3) and sp.Rational(1,2*-3)==-sp.Rational(1,6))
a,b,c,p,d,q,e=sp.symbols('a b c p d q e'); M=sp.Matrix([[a,b,c],[p,d,0],[q,0,e]]); ok('L6-06', sp.factor(M.det()- (a*d*e-b*p*e-c*d*q))==0)
t=sp.symbols('t'); A07=sp.Matrix([[1,1,0],[2,t,1],[3,4,t]]); roots=sp.solve(A07.det(),t); ok('L6-07', set(roots)=={1-sp.sqrt(2),1+sp.sqrt(2)} and all(A07.subs(t,r).rank()==2 for r in roots))
ok('L6-08', (-2)**3==-8 and sp.Rational(-1,-2)==sp.Rational(1,2))
x=sp.symbols('x'); F=sp.Matrix([[2*x,1,x,0],[1,x,2,1],[0,1,1,x],[1,0,1,2]]).det(); ok('L6-09', sp.Poly(F,x).degree()==3 and sp.Poly(F,x).LC()==-1 and F.subs(x,0)==-1)
N=sp.Matrix([[1,0,2,0],[2,1,0,1],[0,0,3,4],[t,0,1,2]]); ok('L6-10', sp.expand(N.det())==8*t+2 and sp.solve(N.det(),t)==[-sp.Rational(1,4)])
la=sp.symbols('la'); a,b,c=sp.symbols('a b c'); M=sp.Matrix([[la,a,b],[-a,la,c],[-b,-c,la]]); ok('L6-11', sp.factor(M.det()-la*(la**2+a**2+b**2+c**2))==0)
ok('L6-12', sp.Matrix([[1,2],[2,4]]).det()==0)
rec=True
for n in range(1,7):
 D=sp.zeros(n)
 for i in range(n):
  D[i,i]=2
  if i+1<n: D[i,i+1]=D[i+1,i]=1
 rec=rec and D.det()==n+1
ok('L6-13',rec)
t=sp.symbols('t'); V=sp.Matrix([[1,1,1],[0,1,t],[0,1,t**2]]); ok('L6-14', sp.factor(V.det()-t*(t-1))==0 and V.subs(t,2).LUsolve(sp.Matrix([1,3,7]))==sp.Matrix([0,-1,2]))
a15=sp.symbols('a15'); A15=sp.Matrix([[i+(a15 if i==j else 0) for j in range(1,5)] for i in range(1,5)]); det15=sp.factor(A15.det()); roots15=set(sp.solve(sp.Eq(det15,0),a15)); ok('L6-15', det15==(a15+10)*a15**3 and roots15=={0,-10})
A16=sp.Matrix([[1,2],[2,1]]); ok('L6-16', A16.det()==-3 and sp.Rational(21,2)/A16.det()==-sp.Rational(7,2))
A17=sp.Matrix([[2,1],[1,1]]); tt=sp.symbols('tt'); B17=sp.Matrix([[1,tt],[0,2]]); X=A17.inv()*B17; ok('L6-17', A17.det()!=0 and X==sp.Matrix([[1,tt-2],[-1,4-tt]]) and sp.factor(X.det())==2)
t,s=sp.symbols('t s'); x18=(2-s)/(2*t-2); y18=(t*s-2)/(2*t-2); ok('L6-18', sp.simplify(t*x18+y18-1)==0 and sp.simplify(2*x18+2*y18-s)==0 and sp.Matrix([[1,1],[2,2]]).rank()==1 and sp.Matrix([[1,1,1],[2,2,2]]).rank()==1 and sp.Matrix([[1,1,1],[2,2,3]]).rank()==2)
