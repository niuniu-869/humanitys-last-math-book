import sympy as sp

failures = 0

def check(name, cond):
    global failures
    if cond:
        print(f"PASS {name}")
    else:
        print(f"FAIL {name}")
        failures += 1

def manual(name):
    print(f"MANUAL {name}")

# L5-01
A = sp.Matrix([[3, 2], [1, 1]])
check("L5-01", A.det() != 0 and A.inv() == sp.Matrix([[1, -2], [-1, 3]]) and A.inv() * sp.Matrix([7, 3]) == sp.Matrix([1, 2]))

# L5-02: independently test all four options on concrete matrices
A = sp.Matrix([[1, 1], [0, 1]])
B = sp.Matrix([[1, 0], [2, 1]])
k = sp.Integer(2)
option_truth = [
    (A * B).inv() == A.inv() * B.inv(),
    (A + B).inv() == A.inv() + B.inv(),
    A.T.inv() == A.inv().T,
    (k * A).inv() == k * A.inv(),
]
check("L5-02", option_truth == [False, False, True, False])

# L5-03
M = sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 3, 1]])
x = sp.Matrix([2, -1, 1])
check("L5-03", M.det() == 0 and M.rank() == 2 and M * x == sp.zeros(3, 1) and x != sp.zeros(3, 1))

# L5-04
R = sp.Matrix([[1, 2], [0, 1]])
B = sp.Matrix([[2, 5], [1, 3]])
X = B * R.inv()
check("L5-04", R.det() != 0 and X == sp.Matrix([[2, 1], [1, 1]]) and X * R == B)

# L5-05: test every option
A1 = sp.Matrix([[1, 0]])
B1 = sp.Matrix([[1], [0]])
A2 = sp.Matrix([[1, 1], [0, 1]])
B2 = A2.inv()
A3 = sp.Matrix([[1, 0], [0, 0]])
A4 = A3
b4 = sp.zeros(2, 1)
option_truth = [
    (A1 * B1 == sp.eye(1) and B1 * A1 == sp.eye(2)),
    (A2 * B2 == sp.eye(2) and B2 == A2.inv()),
    (A3 != sp.zeros(2) and A3.det() != 0),
    (A4 * sp.zeros(2, 1) == b4 and A4.det() != 0),
]
check("L5-05", option_truth == [False, True, False, False])

# L5-06 proof skeleton is required rather than a numerical instance
manual("L5-06")

# L5-07
E1 = sp.Matrix([[0, 1], [1, 0]])
E2 = sp.Matrix([[1, 0], [2, 1]])
E3 = sp.Matrix([[1, 3], [0, 1]])
P = E3 * E2 * E1
claim = E1.inv() * E2.inv() * E3.inv()
check("L5-07", claim == sp.Matrix([[-2, 7], [1, -3]]) and P * claim == sp.eye(2))

# L5-08
A = sp.Matrix([[2, 1], [0, 3]])
X = A.inv() * (2 * A - sp.eye(2))
check("L5-08", X == sp.Matrix([[sp.Rational(3, 2), sp.Rational(1, 6)], [0, sp.Rational(5, 3)]]) and A * X + sp.eye(2) == 2 * A)

# L5-09: test all options through rank and compatibility
A = sp.Matrix([[1, 2], [2, 4]])
B = sp.Matrix([[1, 0], [2, 1]])
option_truth = [
    A.det() != 0,
    A.det() == 0 and A.row_join(B).rank() == A.rank(),
    A.det() == 0 and B.row(1) != 2 * B.row(0) and A.row_join(B).rank() > A.rank(),
    A.det() == 0 and A.row_join(B).rank() == A.rank(),
]
check("L5-09", option_truth == [False, False, True, False])

# L5-10: block diagonal inverse criterion and singular instance
A1 = sp.Matrix([[1, 2], [0, 1]])
A2 = sp.Matrix([[1, 1], [1, 1]])
M = sp.diag(A1, A2)
check("L5-10", A1.det() != 0 and A2.det() == 0 and M.det() == 0)

# L5-11
A = sp.Matrix([[2, 1], [0, 3]])
X = (A - sp.eye(2)).inv() * (3 * A)
check("L5-11", (A - sp.eye(2)).det() != 0 and X == sp.Matrix([[6, -sp.Rational(3, 2)], [0, sp.Rational(9, 2)]]) and A * X * A.inv() == X * A.inv() + 3 * sp.eye(2))

# L5-12
c = sp.Rational(1, 3)
C = sp.Matrix([[0, c, 0], [0, 0, sp.Rational(1, 4)], [0, 0, 0]])
d = sp.Matrix([3, 4, 5])
x = sp.Matrix([sp.Rational(19, 4), sp.Rational(21, 4), 5])
check("L5-12", (sp.eye(3) - C) * x == d and C**3 == sp.zeros(3) and c >= 0)

# L5-13
C = sp.Matrix([[1, 2], [2, 4]])
D = sp.Matrix([[3, 6], [1, 2]])
X = sp.Matrix([[3 - 2 * sp.Symbol('s'), sp.Symbol('s')], [1 - 2 * sp.Symbol('t'), sp.Symbol('t')]])
compatible = X * C == D
D_bad = sp.Matrix([[3, 6], [1, 3]])
check("L5-13", compatible and D_bad.row(1) != 2 * D_bad.row(0))

# Mixed practice
# L5-14
X = sp.Matrix([[2, 1], [1, 2]])
check("L5-14", X * sp.Matrix([1, 0]) == sp.Matrix([2, 1]) and X * sp.Matrix([1, 1]) == sp.Matrix([3, 3]) and X * sp.Matrix([2, -1]) == sp.Matrix([3, 0]))

# L5-15
E1 = sp.Matrix([[1, 0], [2, 1]])
E2 = sp.Matrix([[1, -1], [0, 1]])
P = E2 * E1
claim = sp.Matrix([[1, 1], [-2, -1]])
check("L5-15", P * claim == sp.eye(2) and claim == E1.inv() * E2.inv())

# L5-16
A = sp.Matrix([[1, 2], [2, 4]])
check("L5-16", A * sp.Matrix([3 - 2 * sp.Symbol('t'), sp.Symbol('t')]) == sp.Matrix([3, 6]) and sp.linsolve((A, sp.Matrix([3, 5]))) == sp.EmptySet)

# L5-17
A = sp.Matrix([[1, 2], [2, 4]])
B = sp.eye(2)
C = sp.Matrix([[3, 0], [-1, 1]])
check("L5-17", B != C and A * B == A * C)

raise SystemExit(1 if failures else 0)
