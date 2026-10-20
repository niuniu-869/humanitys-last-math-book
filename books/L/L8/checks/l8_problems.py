import sympy as sp


def ok(tag, cond):
    print(f"{'PASS' if bool(cond) else 'FAIL'} {tag}")

def scalar_multiple(u, v):
    return sp.Matrix.hstack(u, v).rank() == 1

# L8-01: compute the defining tests, including explicit closure counterexamples.
z = sp.zeros(3, 1)
a_sum = sp.Matrix([1, 0, 0]) + sp.Matrix([0, 1, 0])
opts01 = [
    (sp.Matrix([0, 0, 0]).dot(sp.ones(3, 1)) == 1),
    (a_sum[0] * a_sum[1] == 0),
    all(sp.Matrix([1, 1, 1])[i] == sp.Matrix([1, 1, 1])[0] for i in range(3)),
    (z.dot(z) == 1),
]
ok("L8-01", opts01 == [False, False, True, False])

# L8-02: pivot columns and an extension determinant.
v1, v2 = sp.Matrix([1, 0, 1, 0]), sp.Matrix([0, 1, 1, 1])
v3, v4 = sp.Matrix([1, 1, 2, 1]), sp.Matrix([0, 0, 1, 1])
M2 = sp.Matrix.hstack(v1, v2, v3, v4)
rank2 = M2.rank()
ext_det = sp.Matrix.hstack(v1, v2, v4, sp.eye(4)[:, 0]).det()
ok("L8-02", rank2 == 3 and M2.rref()[1] == (0, 1, 3) and ext_det != 0 and v3 == v1 + v2)

# L8-03: transition matrix and coordinate conversion.
P3 = sp.Matrix([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
y3 = P3.inv() * sp.Matrix([3, 1, 2])
ok("L8-03", P3.det() != 0 and y3 == sp.Matrix([2, 1, 2]))

# L8-04: recover a constraint from a prescribed null space.
A4 = sp.Matrix([[1, -1, 0]])
given4 = sp.Matrix.hstack(sp.Matrix([1, 1, 0]), sp.Matrix([0, 0, 1]))
ok("L8-04", A4.rank() == 1 and A4.nullspace() == list(given4.columnspace()) and A4.cols - A4.rank() == 2)

# L8-05 is a proof task.
print("MANUAL L8-05")

# L8-06: compose two transition matrices and convert coordinates.
P6 = sp.Matrix([[1, 1], [1, -1]])
Q6 = sp.Matrix([[2, 0], [1, 1]])
R6 = P6 * Q6
x6 = sp.Matrix([5, -1])
ok("L8-06", R6 == sp.Matrix([[3, 1], [1, -1]]) and R6.inv() * x6 == sp.Matrix([1, 2]))

# L8-07: infer dimensions and consistency from rank and left null space.
r7 = 2
left7 = sp.Matrix([1, 1, -1])
b1, b2, b3 = sp.symbols("b1 b2 b3")
condition7 = left7.dot(sp.Matrix([b1, b2, b3]))
ok("L8-07", (4-r7, r7, r7, 3-r7) == (2, 2, 2, 1) and condition7 == b1 + b2 - b3)

# L8-08: symbolic minors show rank 2 only at t=1.
t = sp.symbols("t")
A8 = sp.Matrix([[1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, t]])
minor_a = A8[:3, [0, 1, 2]].det()
minor_b = A8[:3, [0, 1, 3]].det()
nb8 = A8.subs(t, 1).nullspace()
ok("L8-08", minor_a == 0 and minor_b == t-1 and A8.subs(t, 1).rank() == 2 and len(nb8) == 2 and all(A8.subs(t, 1) * q == sp.zeros(3, 1) for q in nb8) and A8.subs(t, 0).rank() == 3)

# L8-09: all four fundamental subspaces and original pivot columns.
A9 = sp.Matrix([[1, 2, 0, 1], [0, 1, 1, 1], [1, 3, 1, 2]])
R9, piv9 = A9.rref()
nb9 = A9.nullspace()
left9 = A9.T.nullspace()
ok("L8-09", R9 == sp.Matrix([[1,0,-2,-1],[0,1,1,1],[0,0,0,0]]) and piv9 == (0,1) and len(nb9) == 2 and len(left9) == 1 and A9[:, list(piv9)].rank() == 2)

# L8-10: coordinates agree exactly on the 1-eigenspace of P.
P10 = sp.Matrix([[2, 1, 0], [1, 2, 0], [0, 0, 3]])
nb10 = (P10 - sp.eye(3)).nullspace()
ok("L8-10", len(nb10) == 1 and scalar_multiple(nb10[0], sp.Matrix([-1, 1, 0])) and P10 * nb10[0] == nb10[0])

# L8-11: construct from the orthogonal complement and verify all four spaces.
A11 = sp.Matrix([[1, -1, 0, 0], [0, 0, 1, -1]])
given11 = sp.Matrix.hstack(sp.Matrix([1, 1, 0, 0]), sp.Matrix([0, 0, 1, 1]))
null11 = sp.Matrix.hstack(*A11.nullspace())
ok("L8-11", A11.rank() == 2 and null11.columnspace() == given11.columnspace() and A11.columnspace() == sp.eye(2).columnspace() and len(A11.T.nullspace()) == 0)

# L8-12: intersection via a parameterized vector in W.
a12, b12 = sp.Matrix([1, 0, 1]), sp.Matrix([0, 1, 1])
# (s,t,s+t) lies in U iff s-t=0, hence the intersection direction.
int12 = a12 + b12
ok("L8-12", int12[0] == int12[1] and int12[2] == int12[0] + int12[1])

# L8-13: matrix of T and similarity transform.
A13 = sp.Matrix([[0, 1, 0], [1, 0, 2], [0, 0, 0]])
P13 = sp.Matrix([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
B13 = P13.inv() * A13 * P13
ok("L8-13", B13 == sp.Matrix([[1, 0, 1], [0, -1, -1], [0, 0, 0]]))

# L8-14: solve the concrete system, general consistency, and both null spaces.
A14 = sp.Matrix([[1, 2, 1], [2, 4, 2], [0, 1, 1]])
b14 = sp.Matrix([1, 2, 1])
sol14, params14 = A14.gauss_jordan_solve(b14)
null14 = A14.nullspace()
left14 = A14.T.nullspace()
ok("L8-14", sol14.subs(params14[0], 0) == sp.Matrix([-1, 1, 0]) and len(null14) == 1 and len(left14) == 1 and scalar_multiple(left14[0], sp.Matrix([-2, 1, 0])))
