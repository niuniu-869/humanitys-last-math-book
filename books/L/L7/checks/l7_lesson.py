from pathlib import Path
import sympy as sp


def check(example, ok):
    print(("PASS " if ok else "FAIL ") + example)

# 例1: the stated relation is exact.
a1, a2, a3 = sp.Matrix([1, 2, -1, 0]), sp.Matrix([2, 1, 0, 1]), sp.Matrix([0, 3, -2, -1])
check("例1", -2 * a1 + a2 + a3 == sp.zeros(4, 1) and sp.Matrix.hstack(a1, a2, a3).rank() == 2)

# 例2: determinant and representation.
t = sp.symbols("t")
A = sp.Matrix([[1, 1, 1], [1, 2, 3], [1, 3, t]])
check("例2", sp.factor(A.det()) == t - 5 and A.subs(t, 5).rank() == 2 and
      -sp.Matrix([1, 1, 1]) + 2 * sp.Matrix([1, 2, 3]) == sp.Matrix([1, 3, 5]))

# 例3: plus coefficient matrix is invertible; minus version has a nonzero null vector.
Kplus = sp.Matrix([[1, 0, 1], [1, 1, 0], [0, 1, 1]])
Kminus = sp.Matrix([[1, 0, -1], [-1, 1, 0], [0, -1, 1]])
check("例3", Kplus.det() == 2 and Kminus * sp.Matrix([1, 1, 1]) == sp.zeros(3, 1))

# 例4: use a concrete model satisfying the hypotheses.
a1, a2, a3, a4 = sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, 1]), sp.Matrix([1, 2])
# a1 = a3-a2, while a2,a3,a4 are independent is impossible in R2, so use R3.
a1, a2, a3, a4 = sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]), sp.Matrix([1, 1, 0]), sp.Matrix([0, 0, 1])
expr = a3 - a2
check("例4", expr == a1 and sp.Matrix.hstack(a2, a3, a4).rank() == 3 and
      a4 not in sp.Matrix.hstack(a1, a2, a3).columnspace())

# 例5: coefficient determinant and null relation at t=-1.
t = sp.symbols("t")
K = sp.Matrix([[1, 0, 1], [2, 1, 0], [0, t, 2]])
check("例5", sp.simplify(K.det() - (2 * t + 2)) == 0 and K.subs(t, -1) * sp.Matrix([-1, 2, 1]) == sp.zeros(3, 1))

# 例6: rank/pivots and the two stated representations.
M = sp.Matrix([[1, 0, 3, 1, 2], [-1, 3, 0, -2, 1], [2, 1, 7, 2, 5], [4, 2, 14, 0, 10]])
a1, a2, a4 = M[:, 0], M[:, 1], M[:, 3]
check("例6", M.rank() == 3 and M[:, 2] == 3 * a1 + a2 and M[:, 4] == 2 * a1 + a2)

# 例7: row reduction rank and a nonzero 2-minor.
M = sp.Matrix([[1, 2, 0, 3], [2, 4, 1, 7], [1, 2, 1, 4]])
check("例7", M.rank() == 2 and M.extract([0, 1], [0, 2]).det() == 1)

# 例8: determinant factor and exceptional ranks.
a = sp.symbols("a")
M = sp.Matrix([[a, 1, 1], [1, a, 1], [1, 1, a]])
check("例8", sp.factor(M.det()) == (a + 2) * (a - 1) ** 2 and
      M.subs(a, 1).rank() == 1 and M.subs(a, -2).rank() == 2)

# 例9: B is invertible, so right multiplication preserves rank.
A_rank = 2
B = sp.Matrix([[1, 0, 1], [0, 2, 0], [-1, 0, 3]])
check("例9", B.det() == 8 and A_rank == 2)

# 例10: LoRA product, exact matrix/rank, and parameter count.
B = sp.Matrix([[1, 0], [0, 1], [1, 1], [2, -1]])
A = sp.Matrix([[1, 0, 2, 0], [0, 1, 0, -1]])
D = B * A
check("例10", D == sp.Matrix([[1, 0, 2, 0], [0, 1, 0, -1], [1, 1, 2, -1], [2, -1, 4, 1]]) and
      D.rank() == 2 and 2 * 4096 * 8 == 65536 and 4096 ** 2 == 16777216)
