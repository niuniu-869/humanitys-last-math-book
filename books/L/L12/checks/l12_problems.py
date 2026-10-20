import sympy as s

E2 = s.eye(2)
def ok(label, cond):
    if not bool(cond):
        print(f"FAIL {label}")
        raise AssertionError(label)
    print(f"PASS {label}")

# L12-01: compute characteristic polynomials and compare similarity obstruction.
J = s.Matrix([[1, 1], [0, 1]])
E = s.eye(2)
ok("L12-01", E.charpoly().as_expr() == J.charpoly().as_expr() and E != J and E.is_diagonalizable() and not J.is_diagonalizable())

# L12-02
A = s.Matrix([[2, 1], [0, 3]])
P = s.Matrix([[1, 0], [1, 1]])
B = P.inv() * A * P
ok("L12-02", B == s.Matrix([[3, 1], [0, 2]]) and B * s.Matrix([1, -1]) == 2 * s.Matrix([1, -1]))

# L12-03
A = s.Matrix([[1,1,0],[0,2,0],[0,0,2]])
P = s.Matrix([[1,1,0],[0,1,0],[0,0,1]])
Lam = s.diag(1,2,2)
ok("L12-03", P.det()!=0 and A*P==P*Lam)
# L12-04
A = s.Matrix([[3, 1], [1, 3]])
x = 4**7 * s.Matrix([1, 1]) + 2**7 * s.Matrix([1, -1])
ok("L12-04", A**7 * s.Matrix([2, 0]) == x)

# L12-05
A = s.Matrix([[2,-1],[4,-2]])
ok("L12-05", A.rank()==1 and A.trace()==0 and A**2==s.zeros(2) and A**5==s.zeros(2))
# L12-06 is a proof item.
print("MANUAL L12-06")

# L12-07
a = s.symbols('a')
A = s.Matrix([[3,1,-1],[2-a,2,a-2],[3-a,1,a-1]])
char = s.factor(A.charpoly().as_expr())
generic = 3-(A.subs(a,5)-2*s.eye(3)).rank()
triple = 3-(A.subs(a,2)-2*s.eye(3)).rank()
ok("L12-07", s.simplify(char-(s.Symbol('lambda')-a)*(s.Symbol('lambda')-2)**2)==0 and generic==1 and triple==2)
# L12-08: only (A) is a valid general implication.
ok("L12-08", s.Matrix([[1, 0], [0, 2]]).is_diagonalizable() and
    not s.Matrix([[1, 1], [0, 1]]).is_diagonalizable())

# L12-09
A = s.Matrix([[0,1,0],[0,0,1],[6,-11,6]])
ok("L12-09", A.inv()==s.Matrix([[s.Rational(11,6),-1,s.Rational(1,6)],[1,0,0],[0,1,0]]) and A**5==150*s.eye(3)-239*A+90*A**2)
# L12-10
A = s.Matrix([[7,2],[-8,-1]])
N = A-3*s.eye(2)
ok("L12-10", N**2==s.zeros(2) and not A.is_diagonalizable() and A**4==3**4*s.eye(2)+4*3**3*N)
# L12-11
lam=s.symbols('lam')
ok("L12-11", s.expand((lam+1)*(lam-3))==lam**2-2*lam-3)
# L12-12
S=s.Matrix([[1,1,0],[0,1,1],[1,0,1]])
J=s.Matrix([[2,1,0],[0,2,0],[0,0,4]])
A=S*J*S.inv(); n=4
v=A**n*s.Matrix([1,0,0])
expected=s.Matrix([2**n+n*2**(n-2), 2**(n-1)-s.Rational(1,2)*4**n, 2**(n-1)+n*2**(n-2)-s.Rational(1,2)*4**n])
ok("L12-12", v==expected)
# L12-13
P = s.Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
B = s.Matrix([[2, 1, 0], [0, 2, 0], [0, 0, 3]])
A = P * B * P.inv()
e3 = s.Matrix([0, 0, 1])
expected = s.Matrix([-n*2**(n-1), 3**n - 2**n, 3**n])
ok("L12-13", A == s.Matrix([[2, 1, -1], [0, 2, 1], [0, 0, 3]]) and A**n*e3 == expected)

# L12-14
M = s.Matrix([[0, 1], [1, 0]])
pi = s.Matrix([s.Rational(1,2), s.Rational(1,2)])
ok("L12-14", M*pi == pi and M**6*s.Matrix([1, 0]) == s.Matrix([1, 0]) and M**7*s.Matrix([1, 0]) == s.Matrix([0, 1]))

# L12-15
vals = [-1, 2, 3]
ok("L12-15", s.prod(v**2 + 1 for v in vals) == 100 and sum(s.Rational(1, v) for v in vals) == -s.Rational(1,6))

# L12-16
C = s.Matrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
rhs = s.Matrix([2, 3, 4])
sol = C.LUsolve(rhs)
ok("L12-16", sol == s.Matrix([s.Rational(1,2), s.Rational(3,2), s.Rational(5,2)]) and C.det() != 0)

print("MANUAL L12-17")

# L12-18
R=s.Matrix([[s.Rational(1,2),s.Rational(1,2),0],[s.Rational(1,5),s.Rational(1,2),s.Rational(3,10)],[0,s.Rational(2,5),s.Rational(3,5)]])
pi=s.Matrix([[s.Rational(8,43),s.Rational(20,43),s.Rational(15,43)]])
ok("L12-18", pi*R==pi and (R-s.eye(3))*s.ones(3,1)==s.zeros(3,1))