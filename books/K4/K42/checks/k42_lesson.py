"""Independent exact calculations for all ten lesson examples and numeric exercises."""
from collections import defaultdict
import sympy as s


def check(label, condition):
    if not bool(condition):
        raise AssertionError(label)
    print(f"PASS {label}")


R = s.Rational
x, y, a, b, lam = s.symbols("x y a b lam", real=True)
remaining = 150 - 8 - 18
large = remaining - 10 * 4
check("例1", remaining == 124 and large == 84 and large / 7 == 12
      and round(float(R(60, large)),2) == 0.71 and R(4) / R(60, large) == R(28, 5))
large3 = remaining - 12 * 4
check("例1-练习", large3 == 76 and round(float(R(52, large3)),2) == 0.68
      and round(float(R(4) / R(52, large3)),1) == 5.8)

A = s.Matrix([[1, 0], [0, 0]])
B = s.Matrix([[0, 0], [1, 0]])
C = s.Matrix([[1, 1], [0, 1]])
D = s.Matrix([[1, 0], [1, 1]])
check("例2", A*A == A and B*B == s.zeros(2) and A*B == s.zeros(2) and B*A == B
      and (A+B)**2 != A*A+2*A*B+B*B and (2*s.eye(2)).det() != 2
      and (C*D).inv() == s.Matrix([[1, -1], [-1, 2]])
      and C.inv()*D.inv() == s.Matrix([[2, -1], [-1, 1]]))
U = s.Matrix(2, 2, s.symbols("u:4"))
V = s.Matrix(2, 2, s.symbols("v:4"))
check("例2-C", (U*V).T == V.T*U.T)
N = s.Matrix([[0, 1], [0, 0]])
check("例2-练习", (A+B)*(A-B) != A*A-B*B and (2*s.eye(2)).det() != 2
      and C.T.inv() == C.inv().T and N*N == s.zeros(2) and N != s.zeros(2))

p = s.symbols("p", real=True)
for n in range(1, 9):
    odd = sum(s.binomial(n, k)*p**k*(1-p)**(n-k) for k in range(1, n+1, 2))
    check(f"例3-n={n}", s.expand(odd - (1-(1-2*p)**n)/2) == 0)
options = [R(1, 2), (1-(1-2*p)**3)/2, 3*p*(1-p)**2, (1+(1-2*p)**3)/2]
check("例3", [v.subs(p, 0) for v in options] == [R(1,2), 0, 0, 1]
      and [v.subs(p, 1) for v in options] == [R(1,2), 1, 0, 0])
E2 = s.diag(1, 2)
E3 = 2*s.eye(3)
check("例3-练习", E2.adjugate().det() == 2 and E3.adjugate().det() == 64
      and E3.adjugate() == 4*s.eye(3))

# Distinct dimensions make all four candidate shapes distinguishable.
X = s.Matrix(3, 2, s.symbols("X:6"))
W = s.Matrix(2, 1, s.symbols("W:2"))
Y = s.Matrix(3, 1, s.symbols("Y:3"))
residual = X*W-Y
loss = sum(z*z for z in residual)
actual = W.applyfunc(lambda z: s.diff(loss, z))
check("例4", s.simplify(actual - 2*X.T*residual) == s.zeros(2, 1))
check("例4-形状", residual.cols != X.T.rows and (residual.T*X).shape != W.shape
      and X.cols != residual.rows)
H = s.Matrix([[2, 1], [1, 3]])
vec = s.Matrix([x, y])
grad = s.Matrix([s.diff((vec.T*H*vec)[0], z) for z in vec])
check("例4-练习", grad == 2*H*vec and grad != H*vec and grad.shape != (2*vec.T*H).shape)

H = s.Matrix([[2, 1], [1, 2]])
vec = s.ones(2, 1)
check("例5", H.eigenvals() == {1: 1, 3: 1} and H*vec == 3*vec
      and (vec.T*H*vec)[0] == 6 and vec.dot(vec) == 2)
print("MANUAL 例5-证明 正定定义与实对称谱分解的一般性推理，数值已核对")

sol = s.solve([y-2*lam*x, x-2*lam*y, x*x+y*y-2], (x, y, lam))
points = {(xx, yy) for xx, yy, _ in sol}
values = {xx*yy for xx, yy in points}
check("例6", points == {(1,1), (-1,-1), (1,-1), (-1,1)} and values == {-1, 1})
sol = s.solve([1-2*lam*x, 1-2*lam*y, x*x+y*y-2], (x, y, lam))
check("例6-练习", {(xx, yy, xx+yy) for xx, yy, _ in sol} == {(1,1,2),(-1,-1,-2)})

A = s.Matrix([[1,1,1], [1,a,1], [1,1,a]])
rhs = s.Matrix([1,1,b])
claimed = s.Matrix([(a-b)/(a-1), 0, (b-1)/(a-1)])
check("例7", s.factor(A.det()) == (a-1)**2 and s.simplify(A*claimed-rhs) == s.zeros(3,1))
u, v = s.symbols("u v")
check("例7-特殊值", A.subs(a,1).rank() == 1
      and A.subs(a,1)*s.Matrix([1-u-v,u,v]) == s.ones(3,1)
      and A.subs(a,1).row_join(rhs).extract([0,2], [0,3]).det() == b-1)
F = s.Matrix([[1,1], [1,lam]])
check("例7-练习", F.det() == lam-1 and F*s.Matrix([0,1]) == s.Matrix([1,lam])
      and F.subs(lam,1)*s.Matrix([1-u,u]) == s.ones(2,1))

term = s.Float(1, 80)
for _ in range(12):
    next_term = s.sqrt(2+term)
    assert 0 < term < next_term < 2
    term = next_term
increment = s.expand(2+x-x*x)
roots = s.solve(x*x-x-2, x)
check("例8", s.expand(increment-(2-x)*(1+x)) == 0 and roots == [-1, 2]
      and [r for r in roots if r >= 0 and r == s.sqrt(2+r)] == [2])
check("例8-练习", s.solve(s.Eq(x, x/2+1/x), x) == [-s.sqrt(2), s.sqrt(2)])
print("MANUAL 例8-证明 归纳有界及单调有界定理，有限项检验不代替收敛证明")

losses = [(4,"方法"),(4,"计算"),(2,"过程"),(6,"过程"),(4,"计算"),(3,"过程"),(7,"概念"),(4,"时间")]
totals = defaultdict(int)
for value, cause in losses:
    totals[cause] += value
check("例9", dict(totals) == {"过程":11,"计算":8,"概念":7,"方法":4,"时间":4}
      and sum(totals.values()) == 34)

expr = (x+s.sin(x))/(x-s.sin(x))
derivative_ratio = (1+s.cos(x))/(1-s.cos(x))
k = s.symbols("k", integer=True, positive=True)
check("例10", s.limit(expr, x, s.oo) == 1
      and s.simplify(derivative_ratio.subs(x, (2*k+1)*s.pi)) == 0
      and s.simplify(derivative_ratio.subs(x, 2*k*s.pi+s.pi/2)) == 1)
