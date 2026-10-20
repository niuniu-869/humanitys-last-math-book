import sympy as sp


def ok(label, condition):
    print(f"PASS {label}" if bool(condition) else f"FAIL {label}")

# L4-01
x, y, z = sp.symbols('x y z')
sol = sp.solve([
    x + y + z - 4,
    2*x - y + z - 1,
    x + 2*y - z - 2,
], [x, y, z], dict=True)[0]
ok("L4-01", sol == {x: sp.Rational(3, 7), y: sp.Rational(12, 7), z: sp.Rational(13, 7)})

# L4-02
M = sp.Matrix([[0, 0, 1, 4], [1, 0, 2, 3], [2, 0, 5, 10]])
rref, piv = M.rref()
ok("L4-02", rref == sp.Matrix([[1, 0, 0, -5], [0, 0, 1, 4], [0, 0, 0, 0]]) and piv == (0, 2))

# L4-03
A = sp.Matrix([[1, 2, -1, 1], [2, 4, -2, 2], [1, 1, 1, 0]])
b = sp.Matrix([1, 2, 0])
rref, piv = A.row_join(b).rref()
expected = sp.Matrix([[1, 0, 3, -1, -1], [0, 1, -2, 1, 1], [0, 0, 0, 0, 0]])
ok("L4-03", rref == expected and piv == (0, 1))

# L4-04: right multiplication implements c2 <- c2 - 2 c1; inverse restores it.
Q = sp.Matrix([[1, -2], [0, 1]])
Qi = sp.Matrix([[1, 2], [0, 1]])
A4 = sp.Matrix([[2, 5], [7, 11]])
B4 = A4 * Q
ok("L4-04", B4 == sp.Matrix([[2, 1], [7, -3]]) and B4 * Qi == A4)

# L4-05: check every option's truth value from the rref.
R = sp.Matrix([[1, 0, 2, -1, 3], [0, 1, -1, 2, 4], [0, 0, 0, 0, 0]])
rank_coeff = R[:, :4].rank()
option_truth = [
    rank_coeff == 4,
    rank_coeff < 4 and R[2, :].is_zero_matrix,
    R[2, :4].is_zero_matrix and R[2, 4] != 0,
    rank_coeff == 4,
]
ok("L4-05", option_truth == [False, True, False, False])

# L4-06: determinant and special-value rank.
t = sp.symbols('t')
At = sp.Matrix([[1, 1, 0], [0, t, 1], [1, 1, t]])
rank0 = At.subs(t, 0).rank()
option_truth = [
    (sp.factor(At.det()) == t**2 and rank0 == 1),
    (sp.factor(At.det()) == t**2 and rank0 == 2),
    rank0 == 3,
    rank0 == 3,
]
ok("L4-06", option_truth == [False, True, False, False])

# L4-07: mixed left/right multipliers on a concrete matrix.
A7 = sp.Matrix([[1,0,2],[2,1,0],[0,1,1]])
P7 = sp.eye(3); P7[1,0] = -2
R7 = sp.eye(3); R7[1,0] = 1  # c1 <- c1 + c2
S7 = sp.eye(3); S7.col_swap(1,2)
Q7 = R7*S7
B7 = sp.Matrix([[1,2,0],[1,-4,1],[1,1,1]])
ok("L4-07", P7*A7*Q7 == B7)

# L4-08 is a proof exercise.
print("MANUAL L4-08")

# L4-09: column swap changes the represented system and its solution.
orig = sp.Matrix([[1, 1, 2], [1, -1, 0]])
changed = orig[:, [2, 1, 0]]
sol_orig = sp.linsolve((orig[:, :2], orig[:, 2]))
sol_changed = sp.linsolve((changed[:, :2], changed[:, 2]))
ok("L4-09", sol_orig == sp.FiniteSet((sp.Integer(1), sp.Integer(1))) and sol_changed == sp.FiniteSet((sp.Integer(1), sp.Integer(-1))))

# L4-10: parameter in two rows; compare coefficient and augmented pivot counts.
a, b, t = sp.symbols('a b t')
A10 = sp.Matrix([[1,1,1,1],[1,2,3,4],[2,3,4,a],[0,1,1,1]])
aug10 = A10.row_join(sp.Matrix([1,4,5,b]))
sol_generic = sp.Matrix([1-b, 2*b-3, 3-b, 0])
unique_ok = all(sp.simplify(v) == 0 for v in A10*sol_generic-sp.Matrix([1,4,5,b]))
rank_cases = (A10.subs(a,6).rank(), aug10.subs({a:6,b:0}).rank(), A10.subs(a,5).rank(), aug10.subs({a:5,b:0}).rank())
fam = sp.Matrix([1-b, 2*b+t-3, 3-b-2*t, t])
family_ok = all(sp.simplify(v) == 0 for v in A10.subs(a,5)*fam-sp.Matrix([1,4,5,b]))
ok("L4-10", unique_ok and rank_cases == (4,4,3,3) and family_ok)

# L4-11: nullspace gives all coefficient relations.
V = sp.Matrix([[1, 0, 2, 1], [2, 1, 1, 0], [0, 1, 1, 2]])
ns = V.nullspace()
ok("L4-11", len(ns) == 1 and ns[0] == sp.Matrix([1, -1, -1, 1]))

# L4-12: solve and check nonnegativity.
w1, w2, w3 = sp.symbols('w1 w2 w3')
sol12 = sp.solve([
    w1+w2+w3-1,
    2*w1+w2+3*w3-sp.Rational(9, 5),
    w1+2*w2+w3-sp.Rational(6, 5),
], [w1, w2, w3], dict=True)[0]
ok("L4-12", sol12 == {w1: sp.Rational(4, 5), w2: sp.Rational(1, 5), w3: 0} and all(v >= 0 for v in sol12.values()))

# L4-13: dependent columns; one target compatible and one incompatible.
C13 = sp.Matrix([[1, 0, 1], [0, 1, 1], [1, 1, 2]])
sol_b = next(iter(sp.linsolve((C13, sp.Matrix([2, 1, 3])))))
sol_c = sp.linsolve((C13, sp.Matrix([2, 1, 4])))
ok("L4-13", sol_b[0] + sol_b[2] == 2 and sol_b[1] + sol_b[2] == 1 and sol_c == sp.EmptySet)

# L4-14: parameterized fourth column and all representations.
C14 = sp.Matrix([[1,0,1,0],[0,1,1,1],[1,1,2,t]])
b14 = sp.Matrix([2,1,3])
R14 = C14.row_join(b14)
R14[2,:] = R14[2,:] - R14[0,:] - R14[1,:]
ok("L4-14", R14[2,3] == t-1 and R14[2,4] == 0 and C14.subs(t,2).rank() == 3 and C14.subs(t,1).rank() == 2)

# L4-15: independent P, Q construction and product.
A15 = sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]])
P1 = sp.eye(3); P1[1, :] = P1[1, :] - 2*P1[0, :]
P2 = sp.eye(3); P2.row_swap(0, 2)
P15 = P2*P1
Q15 = sp.eye(3); Q15[:, 1] = Q15[:, 1] + Q15[:, 0]
B15 = sp.Matrix([[1, 1, 1], [-2, -5, 1], [1, 3, 0]])
ok("L4-15", P15*A15*Q15 == B15)
