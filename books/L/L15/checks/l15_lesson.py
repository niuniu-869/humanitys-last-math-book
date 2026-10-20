import sympy as sp

def report(k, cond):
    print(("PASS " if cond else "FAIL ") + f"例{k}")

# 例1
A = sp.Matrix([[0,-3],[2,0]])
U = sp.diag(-1,1)
S = sp.diag(3,2)
V = sp.Matrix([[0,1],[1,0]])
report(1, U*S*V.T == A)

# 例2
A = sp.Matrix([[3,0],[4,5]])
v1 = sp.Matrix([1,1])/sp.sqrt(2)
v2 = sp.Matrix([-1,1])/sp.sqrt(2)
u1 = sp.Matrix([1,3])/sp.sqrt(10)
u2 = sp.Matrix([-3,1])/sp.sqrt(10)
report(2, A.T*A == sp.Matrix([[25,20],[20,25]])
       and A*v1 == 3*sp.sqrt(5)*u1
       and A*v2 == sp.sqrt(5)*u2)

# 例3
A = sp.Matrix([[1,1],[0,1],[1,0]])
u1 = sp.Matrix([2,1,1])/sp.sqrt(6)
u2 = sp.Matrix([0,1,-1])/sp.sqrt(2)
u3 = sp.Matrix([-1,1,1])/sp.sqrt(3)
V = sp.Matrix([[1,-1],[1,1]])/sp.sqrt(2)
S = sp.Matrix([[sp.sqrt(3),0],[0,1],[0,0]])
U = sp.Matrix.hstack(u1,u2,u3)
report(3, U*S*V.T == A and U.T*U == sp.eye(3))

# 例4
a = sp.Matrix([1,2])
b = sp.Matrix([1,1,1])
A = a*b.T
v2 = sp.Matrix([1,-1,0])/sp.sqrt(2)
v3 = sp.Matrix([1,1,-2])/sp.sqrt(6)
report(4, A == sp.Matrix([[1,1,1],[2,2,2]])
       and a.dot(sp.Matrix([2,-1])) == 0
       and b.dot(sp.Matrix([1,-1,0])) == 0
       and b.dot(sp.Matrix([1,1,-2])) == 0
       and v2.dot(v3) == 0 and v2.norm() == 1 and v3.norm() == 1)

# 例5
Ap = sp.Matrix([[1,2],[1,2],[1,2]])/15
xplus = Ap*sp.Matrix([1,1])
report(5, Ap == sp.Matrix([[sp.Rational(1,15),sp.Rational(2,15)],
                           [sp.Rational(1,15),sp.Rational(2,15)],
                           [sp.Rational(1,15),sp.Rational(2,15)]])
       and xplus == sp.Matrix([sp.Rational(1,5)]*3))

# 例6
A = sp.Matrix([[3,0],[4,5]])
A1 = sp.Matrix([[sp.Rational(3,2),sp.Rational(3,2)],
                [sp.Rational(9,2),sp.Rational(9,2)]])
E = A-A1
report(6, max((A.T*A).eigenvals().keys()) == 45
       and sp.sqrt(sum(A[i,j]**2 for i in range(2) for j in range(2))) == sp.sqrt(50)
       and sp.sqrt(sum(E[i,j]**2 for i in range(2) for j in range(2))) == sp.sqrt(5)
       and max((E.T*E).eigenvals().keys()) == 5
       and sp.Rational(45,50) == sp.Rational(9,10))

# 例7
X = sp.Matrix([[2,1],[1,2],[-1,-2],[-2,-1]])
report(7, X.T*X == sp.Matrix([[10,8],[8,10]])
       and X*sp.Matrix([1,1])/sp.sqrt(2) == sp.Matrix([3,3,-3,-3])/sp.sqrt(2)
       and sp.Rational(18,1) / sp.trace(X.T*X) == sp.Rational(9,10))


# 讲义正文与随堂题里的数（v2 新增）
def rep2(k, cond):
    print(("PASS " if cond else "FAIL ") + k)
Sh = sp.Matrix([[1,1],[0,1]])
ev = sorted((Sh.T*Sh).eigenvals().keys(), key=lambda e: float(e))
rep2("剪切奇异值", sp.simplify(sp.sqrt(ev[1]) - (sp.sqrt(5)+1)/2) == 0 and sp.simplify(sp.sqrt(ev[0]) - (sp.sqrt(5)-1)/2) == 0)
rep2("第4节引例", sp.Matrix([[1,1],[1,1]]).pinv()*sp.Matrix([1,3]) == sp.Matrix([1,1]))
B = sp.Matrix([[1,2],[2,4]])
rep2("例5随堂题", B.pinv() == B/25 and B.pinv()*sp.Matrix([3,1]) == sp.Matrix([sp.Rational(1,5), sp.Rational(2,5)]))
rep2("例1随堂题", sp.Matrix([[1,-1],[1,1]])/sp.sqrt(2)*sp.diag(2*sp.sqrt(2), sp.sqrt(2)) == sp.Matrix([[2,-1],[2,1]]))
rep2("例4随堂题", sorted((sp.Matrix([[3,4],[-3,-4]]).T*sp.Matrix([[3,4],[-3,-4]])).eigenvals().keys()) == [0, 50])
rep2("存储与LoRA计数", 50*(1000+1000+1) == 100050 and 4096**2 == 16777216 and 2*4096*8 == 65536 and 16777216 // 65536 == 256)
Ae = sp.Matrix([[1,1],[0,1],[1,0]])
rep2("例6随堂题", sorted((Ae.T*Ae).eigenvals().keys()) == [1, 3] and sum(x**2 for x in Ae) == 4)
A1 = sp.Matrix([[0,-3],[2,0]])
rep2("配错符号的反例", A1*A1.T == sp.diag(9,4) and sp.eye(2)*sp.diag(3,2)*sp.Matrix([[0,1],[1,0]]).T == sp.Matrix([[0,3],[2,0]]))
