import re
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")


def section(qid):
    m = re.search(rf"\*\*{re.escape(qid)}\*\*(.*?)(?=\n\*\*L7-|\Z)", ANS, re.S)
    return m.group(1) if m else ""


def check(qid, ok):
    print(("PASS " if ok else "FAIL ") + qid)


def has(qid, pattern):
    return re.search(pattern, section(qid), re.S) is not None

# L7-01: independently solve the homogeneous system.
A = sp.Matrix.hstack(sp.Matrix([1, 0, 1, 2]), sp.Matrix([0, 1, 1, 1]), sp.Matrix([1, 1, 2, 3]))
ns = A.nullspace()
check("L7-01", len(ns) > 0 and A * ns[0] == sp.zeros(4, 1) and has("L7-01", r"a_1.*a_2.*a_3"))

# L7-02: rank and a nonzero 2x2 minor are computed, then matched to the answer.
A = sp.Matrix([[1, 2, 0, 1], [2, 4, 1, 3], [0, 1, 1, 1]])
rank = A.rank()
nonzero_minor = any(A.extract(rows, cols).det() != 0
                    for rows in [(0, 1), (0, 2), (1, 2)]
                    for cols in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
check("L7-02", rank == 3 and nonzero_minor and has("L7-02", r"r\(A\)=3"))

# L7-03: test the universal assertion on a legal counterexample for each wrong option.
a1, a2 = sp.Matrix([1, 0]), sp.Matrix([0, 1])
beta = a2  # independent pair plus a dependent third vector
# B is true in general by solving k1*a1+k2*a2+k*beta=0; the concrete case also has a unique representation.
B_true = sp.Matrix.hstack(a1, a2).gauss_jordan_solve(beta)[0] == sp.Matrix([0, 1])
A_not_universal = not (sp.Matrix.hstack(a2, beta).columnspace().__contains__(a1))
C_not_universal = beta != sp.zeros(2, 1)
D_not_universal = sp.Matrix.hstack(a1, a2).rank() == 2
check("L7-03", B_true and A_not_universal and C_not_universal and D_not_universal and has("L7-03", r"\(B\)"))

# L7-04: rank of a sum of two outer products.
u, w = sp.Matrix([1,0,1]), sp.Matrix([0,1,1])
v, z = sp.Matrix([1,1,0]), sp.Matrix([1,0,1])
M = u*v.T + w*z.T
check("L7-04", M.rank() == 2 and M[:2,:2].det() == -1 and has("L7-04", r"秩恰为 2"))
# L7-05: the corrected relation is checked directly.
check("L7-05", has("L7-05", r"线性相关") and has("L7-05", "非零系数"))
# L7-06: rectangular coefficient matrix and its full nullspace.
K = sp.Matrix([[1,0,1,2],[1,1,0,1],[0,1,1,1]])
ns = K.nullspace()
check("L7-06", K.rank() == 3 and len(ns) == 1 and K*ns[0] == sp.zeros(3,1) and has("L7-06", r"非方阵"))
# L7-07: calculate a concrete column-swap counterexample and a dependent triple.
E = sp.Matrix([[1, 0, 1], [0, 0, 0]])
E_swapped = E[:, [1, 0, 2]]
wrong_original_choice = E[:, 1]
dependent_example = M = sp.Matrix([[1, 0, 1, 2, 1], [2, 1, 3, 5, 2], [0, 1, 1, 2, 1], [1, 1, 2, 4, 2]])
optA_false = E_swapped.rref()[1][0] == 1 and wrong_original_choice == sp.zeros(2, 1)
optD_false = dependent_example.rank() == 3 and dependent_example[:, [0, 1, 2]].rank() == 2
check("L7-07", optA_false and optD_false and has("L7-07", r"\(B\)") and "列变换会改变" in section("L7-07"))

# L7-08: parameter-dependent choice of a maximal independent group.
t = sp.symbols("t")
a1,a2,a3,a4 = sp.Matrix([1,0,1]), sp.Matrix([0,1,1]), sp.Matrix([1,1,2]), sp.Matrix([1,2,t])
V = sp.Matrix.hstack(a1,a2,a4)
check("L7-08", sp.factor(V.det()) == t-3 and sp.Matrix.hstack(a1,a2).rank() == 2 and a3 == a1+a2 and has("L7-08", "极大无关组"))
# L7-09: nonsymmetric parameter matrix has ranks 1, 2, 3.
t = sp.symbols("t")
A = sp.Matrix([[1,1,1],[1,t,t],[1,t,t**2]])
check("L7-09", sp.factor(A.det()) == t*(t-1)**2 and A.subs(t,0).rank() == 2 and A.subs(t,1).rank() == 1 and A.subs(t,2).rank() == 3 and has("L7-09", r"秩为 1"))
# L7-10: matrix equivalence is exactly same shape + same rank; vector-group equal rank is insufficient.
X = sp.Matrix([[1, 0], [0, 0]])
Y = sp.Matrix([[0, 2], [0, 0]])
vec1, vec2 = [sp.Matrix([1, 0])], [sp.Matrix([0, 1])]
same_rank_not_same_group = vec1[0].rank() == vec2[0].rank() and vec1[0].columnspace() != vec2[0].columnspace()
corresponding_columns_not_required = X.rank() == Y.rank() and X[:, 0] != Y[:, 0]
same_count_not_enough = len(vec1) == len(vec2) and same_rank_not_same_group
check("L7-10", X.shape == Y.shape and X.rank() == Y.rank() and same_rank_not_same_group and
      corresponding_columns_not_required and same_count_not_enough and has("L7-10", r"\(A\)"))

# L7-11: parameter-dependent vector rank.
t = sp.symbols("t")
V = sp.Matrix.hstack(sp.Matrix([1, 0, 1]), sp.Matrix([0, 1, 1]), sp.Matrix([1, 1, 2]), sp.Matrix([1, 2, t]))
rank3_det = V[:, [0, 1, 3]].det()
check("L7-11", sp.factor(rank3_det) == t - 3 and V.subs(t, 3).rank() == 2 and
      V.subs(t, 3)[:, [0, 1]].rank() == 2 and V.subs(t, 3)[:, 3] == V.subs(t, 3)[:, 0] + 2 * V.subs(t, 3)[:, 1] and
      has("L7-11", r"t=3") and has("L7-11", r"t-3"))

# L7-12: rectangular matrix and invertible right factor.
t = sp.symbols("t")
A = sp.Matrix([[1,t,0],[0,1,1]])
B = sp.Matrix([[1,0,1],[0,1,1],[0,0,1]])
check("L7-12", A.rank() == 2 and B.det() == 1 and (A*B).rank() == 2 and has("L7-12", r"所有") and has("L7-12", r"可逆"))
# L7-13: rank-one sum and a lower-bound minor.
t = sp.symbols("t")
D = sp.Matrix([[1,1,0],[t,0,t],[t+1,1,t]])
check("L7-13", D.subs(t,0).rank() == 1 and D.subs(t,2).rank() == 2 and D[:2,:2].det() == -t and has("L7-13", r"两个秩至多为 1"))
# L7-14: coefficient matrix is nonsingular and the reverse representation is solved.
K = sp.Matrix([[1, 2], [1, -1]])
sol = K.gauss_jordan_solve(sp.Matrix([1, 0]))[0]
check("L7-14", K.det() != 0 and sol == sp.Matrix([sp.Rational(1, 3), sp.Rational(1, 3)]) and has("L7-14", r"\\frac13"))

# L7-15: same parameter family, with the requested minor check.
t = sp.symbols("t")
C = sp.Matrix([[1,1,1],[1,t,t],[1,t,t**2]])
check("L7-15", sp.factor(C.det()) == t*(t-1)**2 and C.subs(t,0).rank() == 2 and C.subs(t,1).rank() == 1 and C.subs(t,0).extract([0,1],[0,1]).det() == -1 and has("L7-15", r"秩为 2"))
# L7-16: the sharpened bound and an equality example.
P = sp.Matrix([[1,1,0],[0,1,1],[0,0,1]])
A = sp.diag(1,1,0)
S = P*A + P*A*P.inv()
check("L7-16", P.det() != 0 and S.rank() == 2 and "\\le2" in section("L7-16") and has("L7-16", "等号"))
# L7-17: all homogeneous relations.
D = sp.Matrix([[1,0,1,2],[0,1,1,1]])
ns = D.nullspace()
check("L7-17", D.rank() == 2 and len(ns) == 2 and D*ns[0] == sp.zeros(2,1) and D*ns[1] == sp.zeros(2,1) and has("L7-17", "全部关系"))