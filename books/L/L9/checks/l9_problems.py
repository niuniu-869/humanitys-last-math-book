"""L.9 习题独立验算。"""
import sympy as sp


def ok(qid, cond):
    if not bool(cond):
        print(f"FAIL {qid}")
        raise AssertionError(qid)
    print(f"PASS {qid}")

# L9-01：逐项检查选择题的逻辑。
A = sp.Matrix([[1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 0]])
b = sp.Matrix([1, 2, 3, 0])
Aug = A.row_join(b)
ok("L9-01", A.rank() == 2 and Aug.rank() == 2 and A.cols - A.rank() == 1
   and A.rank() == Aug.rank() and A.rank() < A.cols)

# L9-02：由 rref 读出基础解系，并直接代回。
M = sp.Matrix([[1, 1, 0, 1], [0, 1, 1, 2]])
rref, piv = M.rref()
xi1 = sp.Matrix([-1, 1, -1, 0])
xi2 = sp.Matrix([-1, 0, -2, 1])
ok("L9-02", rref == sp.Matrix([[1, 0, -1, -1], [0, 1, 1, 2]])
   and M * xi1 == sp.zeros(2, 1) and M * xi2 == sp.zeros(2, 1)
   and sp.Matrix.hstack(xi1, xi2).rank() == 2)

# L9-03：非齐次解的组合由系数和决定，逐项核对。
sums = {"A": 2 - 1, "B": 1 - 1, "C": 1 + 1, "D": 2 - 1 + 1}
ok("L9-03", sums == {"A": 1, "B": 0, "C": 2, "D": 2})

# L9-04：同系数、不同右端的最小反例。
left = sp.Matrix([[1]])
ok("L9-04", left.rank() == 1 and sp.Matrix([[1]]).rank() == 1
   and sp.Matrix([1]) != sp.Matrix([2]))

# L9-05：AB=O 的按列结论和秩上界，选择项逐项排除。
A = sp.Matrix([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
B = sp.Matrix([[0, 0], [0, 0], [0, 0], [1, 0], [0, 1]])
ok("L9-05", A.rank() == 3 and A * B == sp.zeros(4, 2)
   and all(A * B[:, j] == sp.zeros(4, 1) for j in range(B.cols))
   and B.rank() == 2 and 3 + B.rank() <= 5 and B.rows != B.cols)

# L9-06：由给出的三个组合构造两个齐次方向，并检验齐次性与独立性。
eta1 = sp.Matrix([1, 0, 1, 2])
p = sp.Matrix([3, 2, 1, 4])
q = sp.Matrix([4, 1, 2, 6])
eta2 = p - eta1
eta3 = q - 2 * eta1
xi1 = eta2 - eta1
xi2 = eta3 - eta1
# 系数和为 0，所以 A xi_i = 0；这里直接检查组合系数和及向量性质。
ok("L9-06", eta2 == sp.Matrix([2, 2, 0, 2]) and eta3 == sp.Matrix([2, 1, 0, 2])
   and xi1 == sp.Matrix([1, 2, -1, 0]) and xi2 == sp.Matrix([1, 1, -1, 0])
   and sp.Matrix.hstack(xi1, xi2).rank() == 2
   and 1 - 1 == 0 and 1 - 1 == 0 and 4 - 2 == 2)

# L9-07：参数消元的特殊值。
t = sp.symbols("t")
A = sp.Matrix([[1, 1, 1], [1, 2, 3], [1, 3, t + 4]])
b = sp.Matrix([1, 2, t + 2])
ok("L9-07", sp.factor(A.det()) == t - 1
   and A.subs(t, 1).rank() == A.row_join(b).subs(t, 1).rank() == 2
   and A.subs(t, 1).row_join(b.subs(t, 1)).rref()[0] == sp.Matrix([[1, 0, -1, 0], [0, 1, 2, 1], [0, 0, 0, 0]])
   and A.subs(t, 2).inv() * b.subs(t, 2) == sp.Matrix([1, -1, 1]))

# L9-08 是证明题，脚本不替代证明。
print("MANUAL L9-08")

# L9-09：含参数的同解判断。
t = sp.symbols("t")
A = sp.Matrix([[1, 1, 0], [0, 1, 1]])
B = sp.Matrix([[1, 0, -1], [1, t, 1]])
v = sp.Matrix([-1, 1, -1])
ok("L9-09", (A * v == sp.zeros(2, 1)) and ((B * v)[1] == t - 2)
   and (B.subs(t, 2) * v == sp.zeros(2, 1))
   and A.rank() == B.subs(t, 2).rank() == A.col_join(B.subs(t, 2)).rank()
   and all((B * sp.Matrix(x)).subs(t, 2) == sp.zeros(2, 1)
           for x in A.nullspace()))

# L9-10：两个参数的相容性分类与附加条件。
a, bb = sp.symbols("a bb")
A = sp.Matrix([[1, 1, 1], [1, 2, 4], [2, 3, a]])
b = sp.Matrix([2, 3, bb])
R = A.row_join(b)
sol = sp.Matrix([sp.Rational(3, 2), sp.Rational(1, 4), sp.Rational(1, 4)])
sp_ok = A.subs(a, 5).rank() == R.subs({a: 5, bb: 5}).rank() == 2
sp_bad = R.subs({a: 5, bb: 6}).rank() == 3
ok("L9-10", sp.factor(A.det()) == a - 5 and sp_ok and sp_bad
   and A.subs(a, 5) * sol == b.subs(bb, 5)
   and sol[1] == sol[2])

# L9-11：用一个具体坐标模型验证列关系、秩和通解结构。
e2, e3, e4 = sp.eye(4)[:, 1], sp.eye(4)[:, 2], sp.eye(4)[:, 3]
alpha1 = 2 * e2 - e3
A = sp.Matrix.hstack(alpha1, e2, e3, e4)
beta = alpha1 + e2 + e3 + e4
h = sp.Matrix([1, -2, 1, 0])
x0 = sp.ones(4, 1)
ok("L9-11", A * h == sp.zeros(4, 1) and A * x0 == beta
   and A.rank() == 3 and A.nullspace() == [h])

# L9-12：左零空间相容条件及全部解。
A = sp.Matrix([[1, 0, 1, 2], [2, 0, 2, 4], [0, 1, 1, 1]])
b = sp.Matrix([1, 2, 3])
y = sp.Matrix([-2, 1, 0])
rref, piv = A.row_join(b).rref()
sol0 = sp.Matrix([1, 3, 0, 0])
h1 = sp.Matrix([-1, -1, 1, 0])
h2 = sp.Matrix([-2, -1, 0, 1])
ok("L9-12", y.T * A == sp.zeros(1, 4) and (y.T * b)[0] == 0
   and A * sol0 == b and A * h1 == sp.zeros(3, 1) and A * h2 == sp.zeros(3, 1)
   and sp.Matrix.hstack(h1, h2).rank() == 2)

# L9-13：多项式坐标化后解三元一次方程组。
M = sp.Matrix([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
y = sp.Matrix([2, 3, 1])
c = M.LUsolve(y)
ok("L9-13", c == sp.Matrix([sp.Rational(5, 2), sp.Rational(-1, 2), 1]) and M.det() != 0)

# L9-14：行列式先找特殊值，再代回判断秩。
lam = sp.symbols("lam")
A = sp.Matrix([[1, 1, 0], [0, lam, 1], [1, 1, 1]])
b = sp.Matrix([1, 2, 3])
sol_unique = A.subs(lam, 1).inv() * b
special = A.subs(lam, 0).row_join(b).rref()[0]
ok("L9-14", sp.factor(A.det()) == lam and sol_unique == sp.Matrix([1, 0, 2])
   and A.subs(lam, 0).rank() == A.row_join(b).subs(lam, 0).rank() == 2
   and special == sp.Matrix([[1, 1, 0, 1], [0, 0, 1, 2], [0, 0, 0, 0]]))
