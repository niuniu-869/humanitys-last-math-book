import sympy as sp

def ok(k, cond):
    print(f"PASS 例{k}" if bool(cond) else f"FAIL 例{k}")

# 例1
A1 = sp.Matrix([[1,2],[3,1]])
P = sp.Matrix([2,1]); Q = sp.Matrix([1,3])
ok(1, A1.det() == -5 and sp.det(sp.Matrix.hstack(P,Q)) / 2 == sp.Rational(5,2) and sp.det(sp.Matrix.hstack(A1*P,A1*Q))/2 == -sp.Rational(25,2))

# 例2
ok(2, sp.Matrix([[1,2,-1],[3,0,2],[-1,1,4]]).det() == -33)

# 例3
K3 = sp.Matrix([[1,1,0],[0,1,1],[1,0,1]])
K3m = sp.Matrix([[1,-1,0],[0,1,-1],[-1,0,1]])
ok(3, K3.det()*3 == 6 and K3m.det()*3 == 0)

# 例4
ok(4, sp.Matrix([[1,2,0,1],[2,4,1,3],[-1,0,2,1],[3,1,1,2]]).det() == 4)

# 例5
t = sp.symbols('t')
A5 = sp.Matrix([[1,2,-1],[2,t,-8],[3,7,t]])
ok(5, sp.factor(A5.det()) == (t-3)*(t+2) and set(sp.solve(A5.det(), t)) == {-2,3})

# 例6
ok(6, sp.factor(2**3 * 2 * (-sp.Rational(1,3))) == -sp.Rational(16,3) and (-3)**-1 * 2**2 * (-3) == 4)

# 例7
q7 = sp.symbols('q7')
ok(7, (-1)**2 == 1 and -1 < 0 and sp.solve(sp.Eq(q7, -q7), q7) == [0])

# 例8
x = sp.symbols('x')
A8 = sp.Matrix([[2*x,x,1,2],[1,x,1,-1],[3,2,x,1],[1,1,1,x]])
# sign of 4312 is negative; coefficients are computed from the determinant.
ok(8, (-1)**5 == -1 and sp.Poly(sp.expand(A8.det()), x).coeff_monomial(x**4) == 2 and sp.Poly(sp.expand(A8.det()), x).coeff_monomial(x**3) == -1)

# 例9
ok(9, sp.Matrix([[2,1,3,-1],[1,0,2,1],[3,-1,1,2],[0,0,1,4]]).det() == 20)

# 例10
D10 = sp.Matrix([[1,2,3,4],[2,-1,0,1],[3,1,2,-2],[1,1,1,1]])
D10b = sp.Matrix([[1,2,3,4],[2,-1,0,1],[3,1,2,-2],[2,-1,0,3]])
ok(10, D10.det() == 20 and D10b.det() == 10)

# 例11
x, a = sp.symbols('x a')
A11 = sp.Matrix([[x,a,a,a],[a,x,a,a],[a,a,x,a],[a,a,a,x]])
ok(11, sp.factor(A11.det()) == (x+3*a)*(x-a)**3)

# 例12
ok(12, sp.Matrix([[4,1,1,1],[1,1,0,0],[1,0,2,0],[1,0,0,3]]).det() == 13)

# 例13 and its variant
rec_ok = True
for nn in range(1,7):
    D = sp.zeros(nn)
    for i in range(nn):
        D[i,i] = 2
        if i+1 < nn:
            D[i,i+1] = D[i+1,i] = 1
    rec_ok = rec_ok and (D.det() == nn+1)
ok(13, rec_ok)

# 例14
ok(14, sp.Matrix([[1,1,1,1],[1,2,-1,3],[1,4,1,9],[1,8,-1,27]]).det() == 48)

# 例15
A15 = sp.Matrix([[1,2,0],[2,1,1],[1,0,1]])
Ast15 = sp.Matrix([[1,-2,2],[-1,1,-1],[-1,2,-3]])
ok(15, A15.det() == -1 and A15*Ast15 == A15.det()*sp.eye(3) and Ast15 == A15.det()*A15.inv())

# 例16
n16, d16 = 3, sp.Integer(2)
first16 = d16**(n16-1)
second16 = (sp.Rational(1,2)-d16)**n16 / d16
third16 = (d16+1)**n16 / d16
fourth16 = (first16 * d16**(-1) * 2**n16)  # |(A^*)^*| = |2A|
ok(16, first16 == 4 and second16 == -sp.Rational(27,16) and third16 == sp.Rational(27,2) and fourth16 == 16)

# 例17
C17 = sp.Matrix([[1,1,1],[2,-1,1],[1,2,-1]])
b17 = sp.Matrix([6,3,2])
ok(17, C17.det() == 7 and C17.inv()*b17 == sp.Matrix([1,2,3]))
