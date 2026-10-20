"""Independently recompute all 15 numbered examples and nearby exercises.

Abstract first/second derivatives are tested with independent polynomial-jet
coefficients. Example 14 checks the symbolic elimination under its proof's
explicit G_z != 0 condition; the statement's omission is recorded in notes.
"""

import sys

import sympy as s

x, y, z, t, u, v, w = s.symbols("x y z t u v w", real=True)
c0, c1, c2, c11, c12, c22 = s.symbols("c0 c1 c2 c11 c12 c22")
P = c0+c1*u+c2*v+c11*u*u/2+c12*u*v+c22*v*v/2
failed = 0


def eq(actual, expected):
    if isinstance(actual, (tuple, list, s.MatrixBase)):
        return len(actual) == len(expected) and all(eq(a, b) for a, b in zip(actual, expected))
    return s.simplify(s.trigsimp(actual-expected)).is_zero is True


def check(number, actual, expected, extra=""):
    global failed
    ok = eq(actual, expected)
    print(f"{'PASS' if ok else 'FAIL'} 例{number}{extra}")
    if not ok:
        failed += 1
        print(f"  computed: {actual}; lesson: {expected}")


def compose(expr, U, V):
    return expr.subs({u: U, v: V}, simultaneous=True)


# Direct substitution followed by ordinary differentiation.
surface = x*x+y*y
start = {x: s.Rational(1, 2), y: s.Rational(1, 4)}
end = {x: s.Rational(3, 5), y: s.Rational(9, 25)}
increment = surface.subs(end)-surface.subs(start)
linear = sum(s.diff(surface, q).subs(start)*(end[q]-start[q]) for q in (x, y))
check("1 前路径图", [end[x]-start[x], end[y]-start[y], increment, linear],
      [s.Rational(1, 10), s.Rational(11, 100),
       s.Rational(1771, 10000), s.Rational(155, 1000)])
Z = s.sin(t)**2*s.cos(t)
check(1, [s.diff(Z, t), s.diff(Z, t).subs(t, s.pi/4)],
      [2*s.sin(t)*s.cos(t)**2-s.sin(t)**3, s.sqrt(2)/4])
check(1, s.diff(t*t*s.exp(2*t), t), 2*t*(t+1)*s.exp(2*t), " 后随堂题")
check(2, s.diff(t*t**2*t**3, t), 6*t**5)
L = (u*v-10)**2
path = compose(L, w, 2*w)
point = {u: 3, v: 6}
check(3, [L.subs(point), s.diff(L, u).subs(point), s.diff(L, v).subs(point),
          s.diff(path, w).subs(w, 3), 3-s.Rational(1, 100)*s.diff(path, w).subs(w, 3)],
      [64, 96, 48, 192, s.Rational(108, 100)])

Z = (x/y)**2*s.log(3*x-2*y)
dx, dy = [s.diff(Z, q).subs({x: 2, y: 1}) for q in (x, y)]
check(4, [dx, dy], [4*s.log(4)+3, -8*s.log(4)-2])
check(4, [round(float(dx), 3), round(float(dy), 3)], [8.545, -13.090], " 小数")
Z = s.exp(x*y)*s.sin(x+y)
check(4, [s.diff(Z, x), s.diff(Z, y)],
      [s.exp(x*y)*(y*s.sin(x+y)+s.cos(x+y)),
       s.exp(x*y)*(x*s.sin(x+y)+s.cos(x+y))], " 后随堂题")

# P has a fully arbitrary second jet, including independent mixed terms.
U, V = x*x-y*y, s.exp(x*y)
Z = compose(P, U, V)
p1, p2 = [compose(s.diff(P, q), U, V) for q in (u, v)]
check(5, [s.diff(Z, x), s.diff(Z, y)],
      [2*x*p1+y*s.exp(x*y)*p2, -2*y*p1+x*s.exp(x*y)*p2])
Z = compose(P, x*y, x/y)
p1, p2 = [compose(s.diff(P, q), x*y, x/y) for q in (u, v)]
check(5, [s.diff(Z, x), s.diff(Z, y)],
      [y*p1+p2/y, x*p1-x*p2/y**2], " 后随堂题")
Z = compose(P, x, x*y)
check(6, s.diff(Z, x), compose(s.diff(P, u)+y*s.diff(P, v), x, x*y))
check(6, s.diff(x**3*y, x), 3*x*x*y, " 具体核对")

Z = (x+y)**(x*y)
check(7, [s.diff(Z, q).subs({x: 1, y: 1}) for q in (x, y)],
      [1+2*s.log(2), 1+2*s.log(2)])
check(7, round(float(1+2*s.log(2)), 3), 2.386, " 小数")

Z = compose(P, x*y, x+y)
expected = compose(s.diff(P, u)+x*y*s.diff(P, u, 2)
                   +(x+y)*s.diff(P, u, v)+s.diff(P, v, 2), x*y, x+y)
check(8, s.diff(Z, x, y), expected)
check(8, s.diff(x*x*y*y*(x+y), x, y), 6*x*y*(x+y), " 具体核对")
Z = compose(P, x, x*y)
expected = compose(s.diff(P, u, 2)+2*y*s.diff(P, u, v)+y*y*s.diff(P, v, 2), x, x*y)
check(8, s.diff(Z, x, 2), expected, " 后随堂题")

q = s.symbols("q", real=True)
f = s.Function("f")
Z = f(x*x+y*y)
expected = (4*(s.diff(f(q), q)+q*s.diff(f(q), q, 2))).subs(q, x*x+y*y)
check(9, s.diff(Z, x, 2)+s.diff(Z, y, 2), expected)
Z = s.log(x*x+y*y)
check(9, s.diff(Z, x, 2)+s.diff(Z, y, 2), 0, " 对数（原点除外）")

F = x**3+y**3-3*x*y
point = {x: s.Rational(3, 2), y: s.Rational(3, 2)}
a = s.symbols("a")
# Substitute a tangent path into the defining equation and solve its linear term.
path = F.subs({x: point[x]+t, y: point[y]+a*t}, simultaneous=True)
slope = s.solve(s.diff(path, t).subs(t, 0), a)[0]
check(10, [F.subs(point), s.diff(F, x).subs(point), s.diff(F, y).subs(point), slope],
      [0, s.Rational(9, 4), s.Rational(9, 4), -1])
F = x*y+s.log(y)-1
check(10, (-s.diff(F, x)/s.diff(F, y)).subs({x: 1, y: 1}),
      -s.Rational(1, 2), " 后随堂题")

# The coefficients of x and x^2 independently recover y' and y''.
a, b = s.symbols("a b")
Y = 1+a*x+b*x*x
poly = s.series(s.exp(Y)+x*Y-s.E, x, 0, 3).removeO().expand()
jet = s.solve([poly.coeff(x, 1), poly.coeff(x, 2)], (a, b), dict=True)[0]
check(11, [jet[a], 2*jet[b]], [-1/s.E, 1/s.E**2])

F = s.sqrt(x*y)-6
point = {x: 4, y: 9}
Y = 36/x
check(12, [F.subs(point), s.diff(F, x).subs(point), s.diff(F, y).subs(point),
           s.diff(Y, x).subs(x, 4)],
      [0, s.Rational(3, 4), s.Rational(1, 3), -s.Rational(9, 4)])

# Explicit local branch verifies both general implicit-derivative formulas.
Z = 2-s.sqrt(4-x*x-y*y)
dx = x/(2-Z)
dxx = ((2-Z)**2+x*x)/(2-Z)**3
check(13, [s.diff(Z, x)-dx, s.diff(Z, x, 2)-dxx,
           s.diff(Z, x).subs({x: 0, y: 0}), s.diff(Z, x, 2).subs({x: 0, y: 0})],
      [0, 0, 0, s.Rational(1, 2)])
F = s.exp(z)-x*y*z
direct = -s.diff(F, x)/s.diff(F, z)
check(13, [direct, direct.subs(s.exp(z), x*y*z)],
      [y*z/(s.exp(z)-x*y), z/(x*(z-1))], " 后随堂题（分母非零）")

# Verify the general proof algebra with arbitrary outer first derivatives.
A, B = s.symbols("A B")
U, V = x+z/y, y+z/x
gx, gy, gz = [A*s.diff(U, q)+B*s.diff(V, q) for q in (x, y, z)]
zx, zy = -gx/gz, -gy/gz
check(14, [gz, x*zx+y*zy], [A/y+B/x, z-x*y], " 条件 xy != 0 且 G_z != 0")

# For the system, differentiate parametrized original equations and solve.
a, b = s.symbols("a b")
path = {x: 1+t, y: -2+a*t, z: 1+b*t}
equations = [x*x+y*y+z*z-6, x+y+z]
linear = [s.diff(e.subs(path, simultaneous=True), t).subs(t, 0) for e in equations]
jet = s.solve(linear, (a, b))
check(15, [jet[a], jet[b], s.Matrix([[-2, 1], [1, 1]]).det()], [0, -1, -3])
r = s.symbols("r", positive=True)
theta = s.symbols("theta", real=True)
matrix = s.Matrix([r*s.cos(theta), r*s.sin(theta)]).jacobian([r, theta])
result = s.simplify(matrix.inv()*s.Matrix([1, 0]))
check(15, [matrix.det(), result[0], result[1]],
      [r, s.cos(theta), -s.sin(theta)/r], " 后随堂题")

sys.exit(bool(failed))
