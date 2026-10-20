import sympy as sp


def ok(tag, cond):
    print(f"{'PASS' if bool(cond) else 'FAIL'} {tag}")

# 例1：反对称三阶矩阵
M1 = sp.Matrix([[0,1,2],[-1,0,3],[-2,-3,0]])
lam = sp.symbols('lambda')
char1 = sp.factor(M1.charpoly(lam).as_expr())
roots1 = M1.eigenvals()
ok('例1', M1.T == -M1 and sp.expand(char1) == lam**3 + 14*lam and roots1.get(0,0) == 1)

# 例2：由两个特征向量的正交补补出第三个方向
v1 = sp.Matrix([1,1,0]); v2 = sp.Matrix([1,-1,1]); v3 = sp.Matrix([1,-1,-2])
ok('例2', v1.dot(v2)==0 and v3.dot(v1)==0 and v3.dot(v2)==0 and v3 != sp.zeros(3,1))

# 例3：A、B、C 中只有 A 与 C 相似
A3 = sp.Matrix([[1,1,0],[1,1,0],[0,0,2]])
B3 = sp.Matrix([[2,1,0],[0,2,0],[0,0,0]])
C3 = sp.diag(2,2,0)
ok('例3', A3.T==A3 and C3.T==C3 and A3.eigenvals()==C3.eigenvals() and len((B3-2*sp.eye(3)).nullspace())==1 and A3.eigenvals()==B3.eigenvals())

# 例4：对称矩阵的正交对角化
A4 = sp.Matrix([[0,1,1],[1,0,1],[1,1,0]])
q1 = sp.Matrix([1,1,1])/sp.sqrt(3)
q2 = sp.Matrix([1,-1,0])/sp.sqrt(2)
q3 = sp.Matrix([1,1,-2])/sp.sqrt(6)
Q4 = sp.Matrix.hstack(q1,q2,q3)
ok('例4', Q4.T*Q4 == sp.eye(3) and Q4.T*A4*Q4 == sp.diag(2,-1,-1) and A4*q1==2*q1 and A4*q3==-q3)

# 例5：谱分解反求 A
vv = [sp.Matrix([1,1,0]), sp.Matrix([1,-1,1]), sp.Matrix([1,-1,-2])]
ll = [2,3,6]
A5 = sum((l*(v*v.T)/(v.dot(v)) for l,v in zip(ll,vv)), sp.zeros(3))
expected5 = sp.Matrix([[3,-1,-1],[-1,3,1],[-1,1,5]])
ok('例5', A5 == expected5 and all(A5*v == l*v for l,v in zip(ll,vv)))

# 例6：两个特征值的简式
q6 = sp.Matrix([1,-1,1])/sp.sqrt(3)
A6 = sp.eye(3) + 3*q6*q6.T
expected6 = sp.Matrix([[2,-1,1],[-1,2,-1],[1,-1,2]])
ok('例6', A6 == expected6 and A6*q6 == 4*q6 and A6*sp.Matrix([1,1,0]) == sp.Matrix([1,1,0]))

# 例7：协方差矩阵与第一主方向
pts = [sp.Matrix([2,2]), sp.Matrix([-2,-2]), sp.Matrix([1,-1]), sp.Matrix([-1,1])]
C7 = sum((x*x.T for x in pts), sp.zeros(2))/4
q7 = sp.Matrix([1,1])/sp.sqrt(2)
q7b = sp.Matrix([1,-1])/sp.sqrt(2)
ok('例7', C7 == sp.Matrix([[sp.Rational(5,2),sp.Rational(3,2)],[sp.Rational(3,2),sp.Rational(5,2)]]) and C7.eigenvals() == {4:1,1:1} and C7*q7 == 4*q7 and C7*q7b == q7b)
