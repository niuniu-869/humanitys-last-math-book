import sympy as s

def ok(k, cond):
    if not bool(cond):
        print(f"FAIL 例{k}")
        raise AssertionError(k)
    print(f"PASS 例{k}")

# 例1
A=s.Matrix([[4,1],[2,3]]); P=s.Matrix([[1,1],[0,1]])
B=P.inv()*A*P
ok(1, B==s.Matrix([[2,0],[2,5]]) and B*s.Matrix([0,1])==5*s.Matrix([0,1]))

# 例2 and the C subexample
A=s.Matrix([[2,0,1],[0,1,0],[1,0,2]])
Bb=s.Matrix([[2,0,1],[1,1,0],[1,0,2]])
lam=s.symbols('lam')
pa=A.charpoly(lam).as_expr(); pb=Bb.charpoly(lam).as_expr()
C=s.Matrix([[3,0,0],[1,2,0],[1,0,2]])
ok(2, s.simplify(s.factor(pa)-(lam-1)**2*(lam-3))==0 and s.simplify(s.factor(pb)-pa)==0 and 3-(A-s.eye(3)).rank()==2 and 3-(Bb-s.eye(3)).rank()==1 and 3-(C-2*s.eye(3)).rank()==2)

# 例3
P=s.Matrix([[0,-1,1],[1,0,0],[0,1,1]])
Lam=s.diag(1,1,3)
ok(3, P.det()!=0 and A*P==P*Lam)

# 例4
T=s.symbols('a')
A4=s.Matrix([[T,0,0],[1,2,0],[0,1,3]])
ok(4, all(A4.subs(T,v).is_diagonalizable()==(v not in (2,3)) for v in (1,2,3,4)))

# 例5
x,y=s.symbols('x y')
A5=s.Matrix([[2,0,0],[0,3,2],[0,1,x]])
sol=s.solve([s.trace(A5)-(2+1+y), A5.det()-2*y],[x,y], dict=True)
ok(5, sol==[{x:2,y:4}] and s.factor(A5.subs(x,2).charpoly(lam).as_expr())==(lam-2)*(lam-1)*(lam-4))

# 例6
P=s.Matrix([[1,1],[1,2]]); Lam=s.diag(1,-2)
A6=P*Lam*P.inv()
ok(6, A6==s.Matrix([[4,-3],[6,-5]]) and A6*s.Matrix([1,2])==-2*s.Matrix([1,2]))

# 例7
A7=s.Matrix([[4,1],[2,3]])
formula=lambda k:s.Rational(1,3)*s.Matrix([[2*5**k+2**k,5**k-2**k],[2*5**k-2**(k+1),5**k+2**(k+1)]])
ok(7, all(A7**k==formula(k) for k in (1,2,5)))

# 例8
W=s.Matrix([[s.Rational(85,100),s.Rational(35,100)],[s.Rational(35,100),s.Rational(85,100)]])
h=s.Matrix([1,0])
h10=W**10*h; h20=W**20*h
ok(8, abs(float(h10[0])-3.0955) < .02 and abs(float(h10[1])-3.0945) < .02 and abs(float(h20[0])-19.17)<.05)

# 例9
A9=s.Matrix([[2,1,1],[4,2,2],[-2,-1,-1]])
ok(9, A9.rank()==1 and s.trace(A9)==3 and A9**4==3**3*A9)

# 例10
A10=s.Matrix([[3,1],[-1,1]])
ok(10, all(A10**k==2**(k-1)*s.Matrix([[k+2,k],[-k,2-k]]) for k in (1,2,5)))

# 例11
ok(11, A10.inv()==s.Rational(1,4)*s.Matrix([[1,-1],[1,3]]) and A10**4==32*A10-48*s.eye(2))

# 例12 Fibonacci
phi=(1+s.sqrt(5))/2; psi=(1-s.sqrt(5))/2
fib=lambda k:s.simplify((phi**k-psi**k)/s.sqrt(5))
ok(12, all(fib(k)==[0,1,1,2,3,5,8][k] for k in range(7)))

# 例13 double-root recurrence
seq=[1,4]
for _ in range(2,7): seq.append(4*seq[-1]-4*seq[-2])
ok(13, all(seq[k]==(k+1)*2**k for k in range(7)))

# 例14 stationary and three iterations
M=s.Matrix([[s.Rational(7,10),s.Rational(3,10),s.Rational(3,10)],[s.Rational(1,10),s.Rational(6,10),s.Rational(1,10)],[s.Rational(2,10),s.Rational(1,10),s.Rational(6,10)]])
pi=s.Matrix([s.Rational(1,2),s.Rational(1,5),s.Rational(3,10)])
x=s.Matrix([1,0,0])
ok(14, M*pi==pi and [M**k*x for k in (1,2,3)] == [s.Matrix([s.Rational(7,10),s.Rational(1,10),s.Rational(1,5)]), s.Matrix([s.Rational(29,50),s.Rational(3,20),s.Rational(27,100)]), s.Matrix([s.Rational(133,250),s.Rational(7,40),s.Rational(293,1000)])])
