"""独立核对 lesson.md 中例 1--12 的数值与结论。"""
import sympy as sp


def ok(k, cond):
    if not bool(cond):
        print(f"FAIL 例{k}")
        raise AssertionError(k)
    print(f"PASS 例{k}")

# 例1：两个右端的秩分别为 2/2 和 2/3。
A = sp.Matrix([[1, 1, 2], [2, 1, 3], [1, 0, 1]])
b = sp.Matrix([1, 3, 2])
bp = sp.Matrix([1, 3, 1])
ok(1, A.rank() == 2 and A.row_join(b).rank() == 2 and A.row_join(bp).rank() == 3)

# 例2：四个判断分别为错、错、对、对；用反例及秩条件核对。
A1 = sp.Matrix([[1], [1]])
A2 = sp.ones(2, 2)
A4 = sp.eye(2)
claim1_false = A1.row_join(sp.Matrix([1, 2])).rank() > A1.rank()
claim2_false = A2.row_join(sp.Matrix([1, 2])).rank() > A2.rank()
claim3_true = sp.Matrix([[1, 0], [0, 0]]).nullspace() != []
claim4_true = A4.rank() == A4.rows
ok(2, claim1_false and claim2_false and claim3_true and claim4_true)

# 例3：行最简形、两个基础解和通解。
A = sp.Matrix([[2, 1, -1, 1], [4, 2, 1, -1], [2, 1, 2, -2]])
xi1 = sp.Matrix([-1, 2, 0, 0])
xi2 = sp.Matrix([0, 0, 1, 1])
ok(3, A.rank() == 2 and A * xi1 == sp.zeros(3, 1) and A * xi2 == sp.zeros(3, 1)
   and sp.Matrix.hstack(xi1, xi2).rank() == 2)

# 例4：三个组合的系数矩阵分别可逆、奇异、个数不足。
P1 = sp.Matrix([[1, 0, 1], [1, 1, 0], [0, 1, 1]])
P2 = sp.Matrix([[1, 0, -1], [-1, 1, 0], [0, -1, 1]])
ok(4, P1.det() == 2 and P2.det() == 0 and (P2 * sp.ones(3, 1) == sp.zeros(3, 1)))

# 例5：秩为2，增广秩为2，通解的三个代表向量。
A = sp.Matrix([[1, 2, -1, 1], [2, 4, -1, 3], [1, 2, 1, 3]])
b = sp.Matrix([2, 5, 4])
eta = sp.Matrix([3, 0, 1, 0])
xi1 = sp.Matrix([-2, 1, 0, 0])
xi2 = sp.Matrix([-2, 0, -1, 1])
ok(5, A.rank() == 2 and A.row_join(b).rank() == 2 and A * eta == b
   and A * xi1 == sp.zeros(3, 1) and A * xi2 == sp.zeros(3, 1))

# 例6：系数和为0的组合是齐次解，且非零，零化度为1。
eta1 = sp.Matrix([2, 3, 4, 5])
sum23 = sp.Matrix([1, 2, 3, 4])
xi = 2 * eta1 - sum23
ok(6, xi == sp.Matrix([3, 4, 5, 6]) and xi != sp.zeros(4, 1) and 4 - 3 == 1)

# 例7：回归矩阵秩2，特解和零空间方向正确。
X = sp.Matrix([[2, 1, 3], [1, 3, 4], [3, 2, 5]])
y = sp.Matrix([5, 5, 8])
w = sp.Matrix([2, 1, 0])
h = sp.Matrix([1, 1, -1])
ok(7, X.rank() == 2 and X * w == y and X * h == sp.zeros(3, 1)
   and sp.Matrix.hstack(w, h).rank() == 2)

# 例8：行列式特殊值及两种特殊情形。
l = sp.symbols("l")
A = sp.Matrix([[l, 1, 1], [1, l, 1], [1, 1, l]])
b = sp.Matrix([1, l, l**2])
ok(8, sp.factor(A.det()) == (l + 2) * (l - 1) ** 2
   and A.subs(l, 1).rank() == A.row_join(b).subs(l, 1).rank() == 1
   and A.subs(l, -2).rank() == 2 and A.row_join(b).subs(l, -2).rank() == 3)

# 例9：消元后的两个主元均为 a-1，a=1 时再按 b 分相容性。
a, bb = sp.symbols("a bb")
A = sp.Matrix([[1, 1, 1, 1], [0, 1, 2, 2], [0, -1, a - 3, -2], [3, 2, 1, a]])
b = sp.Matrix([0, 1, bb, -1])
ok(9, sp.factor(A.det()) == (a - 1) ** 2
   and A.subs(a, 1).rank() == 2
   and A.row_join(b).subs({a: 1, bb: -1}).rank() == 2
   and A.row_join(b).subs({a: 1, bb: 0}).rank() == 3)

# 例10：AB=O 且 B 非零迫使 lambda=1，并使 A 的秩为2。
l = sp.symbols("l")
A = sp.Matrix([[1, 2, -2], [2, -1, l], [3, 1, -1]])
ok(10, sp.simplify(sp.factor(A.det()) - 5 * (l - 1)) == 0
   and A.subs(l, 1).rank() == 2 and 3 - A.subs(l, 1).rank() == 1)

# 例11：一个非零代数余子式加 det=0 给出秩 n-1，伴随矩阵列为非零齐次解。
A = sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 2, 1]])
cof11 = A.minor_submatrix(0, 0).det()
adj = A.adjugate()
col = adj[:, 0]
ok(11, A.det() == 0 and cof11 != 0 and A.rank() == 2
   and A * col == sp.zeros(3, 1) and col != sp.zeros(3, 1))

# 例12：上下拼接后秩为3，公共零空间是一维。
A = sp.Matrix([[1, 1, 0, 0], [0, 1, 0, -1]])
B = sp.Matrix([[1, -1, 1, 0], [0, 1, -1, 1]])
v = sp.Matrix([-1, 1, 2, 1])
ok(12, A.col_join(B).rank() == 3 and A * v == sp.zeros(2, 1)
   and B * v == sp.zeros(2, 1) and (A.col_join(B)).nullspace() == [v])


# v2 正文新增的数（老朋友④⑤、第 5 节的具体例）
def okt(tag, cond):
    print(("PASS " if bool(cond) else "FAIL ") + tag)

P4 = sp.Rational(1, 2) * sp.ones(2, 2)
okt("正文④", all(P4 * sp.Matrix(v) == sp.Matrix([1, 1]) for v in ([2, 0], [0, 2], [3, -1]))
    and P4 * sp.Matrix([-1, 1]) == sp.zeros(2, 1) and P4.rank() == 1
    and P4.row_join(sp.Matrix([1, 0])).rank() == 2)
A5 = sp.Matrix([[1, 2, 1], [2, 4, 3], [3, 6, 4]])
okt("正文⑤基础解系", A5.rref()[0] == sp.Matrix([[1, 2, 0], [0, 0, 1], [0, 0, 0]])
    and A5.nullspace() == [sp.Matrix([-2, 1, 0])])
okt("正文⑤解集", A5 * sp.Matrix([0, 0, 1]) == sp.Matrix([1, 3, 4])
    and A5 * sp.Matrix([-2, 1, 1]) == sp.Matrix([1, 3, 4]))
okt("正文⑤伴随", A5.adjugate() == sp.Matrix([[-2, -2, 2], [1, 1, -1], [0, 0, 0]])
    and A5.adjugate().rank() == 1 and A5 * A5.adjugate() == sp.zeros(3, 3))
A = sp.ones(2, 2); B = sp.Matrix([[1, 2], [-1, -2]])
okt("正文AB=O", A * B == sp.zeros(2, 2) and A.rank() + B.rank() == 2)
A = sp.Matrix([[1, 2], [2, 4]])
okt("正文ATA", A.T * A == sp.Matrix([[5, 10], [10, 20]]) and (A.T * A).rank() == A.rank() == 1)
A = sp.Matrix([1, sp.I])
okt("正文复数反例", A.rank() == 1 and sp.simplify((A.T * A)[0]) == 0)
K = sp.Matrix([[1, 0, 1], [1, 1, 0], [0, 1, 1]])
okt("例4的K", K.det() == 2)
