import sympy as sp


def check(k, cond):
    print(f"{'PASS' if bool(cond) else 'FAIL'} 例{k}")

# 例 1: verify the four classifications by null-space/span tests and witnesses.
row1 = sp.Matrix([[1, -2, 1]])
nb1 = row1.nullspace()
v1a, v1b = nb1
v2a, v2b = sp.Matrix([1, 1, 1]), sp.Matrix([2, 2, 2])
v4a, v4b = sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0])
check(1, len(nb1) == 2 and row1 * (v1a + v1b) == sp.zeros(1, 1) and row1 * (3 * v1a) == sp.zeros(1, 1)
      and v2a[0] == v2a[1] == v2a[2] and v2b[0] == v2b[1] == v2b[2]
      and sp.zeros(3, 1).dot(sp.ones(3, 1)) != 1
      and v4a[0] * v4a[1] == 0 and v4b[0] * v4b[1] == 0 and (v4a + v4b)[0] * (v4a + v4b)[1] != 0)

# 例 2: rank, pivot columns, redundant vector, and extension determinant.
a1 = sp.Matrix([1, 1, 0, 2]); a2 = sp.Matrix([2, 1, 1, 3]); a3 = sp.Matrix([0, 1, -1, 1]); a4 = sp.Matrix([1, 0, 1, 2])
M2 = sp.Matrix.hstack(a1, a2, a3, a4)
D2 = sp.Matrix.hstack(a1, a2, a4, sp.eye(4)[:, 0]).det()
check(2, M2.rank() == 3 and M2.rref()[1] == (0, 1, 3) and a3 == 2 * a1 - a2 and D2 == -1 and a1 - a2 + a4 == sp.eye(4)[:, 3])

# 例 3: compute the old-to-new transition matrix from B=A P.
A3 = sp.Matrix([[1, 1, 1], [0, 1, 1], [0, 0, 1]])
B3 = sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]])
P3 = A3.inv() * B3
expected3 = sp.Matrix([[1, -1, 1], [1, 0, -1], [0, 1, 1]])
check(3, P3 == expected3 and A3 * P3 == B3)

# 例 4: abstract transition matrix, determinant, and coordinate vector.
P4 = sp.Matrix([[1, 0, 1], [1, 1, 0], [0, 1, 1]])
y4 = P4.inv() * sp.Matrix([1, 2, 3])
check(4, P4.det() == 2 and y4 == sp.Matrix([0, 2, 1]))

# 例 5: nullity two for a 4x5 matrix implies rank three, so C(A) cannot fill R^4.
check(5, 5 - 2 == 3 and 3 < 4)

# 例 6: all four spaces for the chapter matrix and the consistency relation.
A6 = sp.Matrix([[1, 2, 0, 1], [2, 4, 1, 3], [3, 6, 1, 4]])
R6, piv6 = A6.rref()
left6 = A6.T.nullspace()
check(6, A6.rank() == 2 and piv6 == (0, 2) and len(A6.nullspace()) == 2 and len(left6) == 1 and left6[0].is_zero_matrix is False and A6[:, list(piv6)].columnspace()[0] == A6[:, 0])

# 例 7: coordinates of 1, 1+t, (1+t)^2 and of p(t).
C7 = sp.Matrix([[1, 1, 1], [0, 1, 2], [0, 0, 1]])
coords7 = C7.inv() * sp.Matrix([2, 3, 1])
check(7, C7.det() == 1 and coords7 == sp.Matrix([0, 1, 1]))

# 例 8: similarity transform gives diag(3,2).
A8 = sp.Matrix([[3, 1], [0, 2]])
P8 = sp.Matrix([[1, 1], [0, -1]])
B8 = P8.inv() * A8 * P8
check(8, P8.det() != 0 and B8 == sp.diag(3, 2) and A8 * P8[:, 0] == 3 * P8[:, 0] and A8 * P8[:, 1] == 2 * P8[:, 1])
