"""Recompute from problem data; expected values are transcribed from answers.md.

Exact answer fragments bind each comparison to the delivered answer. Choice
options are evaluated separately. Symbolic solving is used for complete sets;
sampling is never used to establish a universal claim or an extremum.
"""

from pathlib import Path
import re
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"^\*\*(C19-\d+)\*\*\n(.*?)(?=^\*\*C19-|\Z)",
    ANSWERS, re.M | re.S,
))
V = s.Matrix
R = s.Rational
x, y, z, t, u, lam = s.symbols("x y z t u lam", real=True)
TESTS = []


def equal(actual, expected):
    if isinstance(actual, s.MatrixBase):
        assert actual.shape == expected.shape
        assert all(s.simplify(v) == 0 for v in actual - expected), (actual, expected)
    elif isinstance(actual, (list, tuple)):
        assert len(actual) == len(expected), (actual, expected)
        for a, b in zip(actual, expected):
            equal(a, b)
    elif isinstance(actual, (bool, set, s.Set)) or isinstance(expected, bool):
        assert actual == expected, (actual, expected)
    else:
        assert s.simplify(actual - expected) == 0, (actual, expected)


def case(number, *fragments, manual=False):
    def register(fn):
        TESTS.append((f"C19-{number:02d}", fragments, manual, fn))
        return fn
    return register


def choices(pid, actual, expected):
    for letter, a, b in zip("ABCD", actual, expected):
        equal(bool(a), b)
        print(f"PASS {pid} 选项{letter}")


@case(1, r"M=(2,-1,1)", r"d(A,M)=\sqrt3")
def p01():
    a, b, m = V([1, -2, 0]), V([3, 0, 2]), V([x, y, z])
    sol = s.solve(m - a - (b - m), (x, y, z))
    point = m.subs(sol)
    equal(point, V([2, -1, 1]))
    equal((point - a).norm(), s.sqrt(3))


@case(2, "选 B", "(3,4,0)")
def p02():
    constraints = [x / 5 - R(3, 5), y / 5 - R(4, 5), x*x + y*y + z*z - 25]
    solutions = set(s.solve(constraints, (x, y, z)))
    equal(solutions, {(3, 4, 0)})
    choices("C19-02", [solutions == {(3, 4, 5), (3, 4, -5)},
                       solutions == {(3, 4, 0)},
                       solutions == {(R(3, 5), R(4, 5), 0)},
                       len(solutions) == 0], [False, True, False, False])


@case(3, "选 C", "(-1,2,1)", r"\sqrt6/2")
def p03():
    a, b = V([1, 0, 1]), V([1, 1, -1])
    dot, cross = a.dot(b), a.cross(b)
    equal(cross, V([-1, 2, 1]))
    equal(cross.norm() / 2, s.sqrt(6) / 2)
    choices("C19-03", [dot == 0 and (a.norm() == 0 or b.norm() == 0),
                       cross == s.zeros(3, 1),
                       dot == 0 and cross == V([-1, 2, 1]),
                       cross.norm() / 2 == s.sqrt(6)],
            [False, False, True, False])


@case(4, "u=-3", "夹角为钝角")
def p04():
    a, b = V([2, 0, 0]), V([u, 2, 0])
    roots = s.solve(a.dot(b) / a.norm() + 3, u)
    equal(roots, [-3])
    equal(a.dot(b.subs(u, roots[0])) < 0, True)


@case(5, "选 B", "整条直线在平面内")
def p05():
    point = V([1+t, -t, 2])
    normal, direction = V([1, 1, 0]), point.diff(t)
    residual = s.expand(point[0] + point[1] - 1)
    intersections = s.solveset(residual, t, domain=s.S.Reals)
    choices("C19-05", [intersections == s.EmptySet,
                       residual == 0,
                       direction.cross(normal) == s.zeros(3, 1),
                       intersections == s.FiniteSet(0)], [False, True, False, False])


@case(6, r"\sqrt7", r"\lambda=1/6", r"\boldsymbol{a}\cdot\boldsymbol{b}=3")
def p06():
    dot = s.solve(4 + 9 + 2*u - 19, u)[0]
    equal(dot, 3)
    # Construct actual vectors satisfying the given lengths, independently of
    # the written dot-product expansion used to solve the exercise.
    a, b = V([2, 0, 0]), V([dot/2, s.sqrt(9-dot**2/4), 0])
    equal([a.norm(), b.norm(), (a+b).norm()], [2, 3, s.sqrt(19)])
    equal((a-b).norm(), s.sqrt(7))
    roots = s.solve((a + lam*b).dot(a-b), lam)
    equal(roots, [R(1, 6)])
    equal((a + roots[0]*b).norm() > 0, True)


@case(7, "对角线垂直", "不是正方形", manual=True)
def p07():
    u = V(s.symbols("ux uy uz", real=True))
    v = V(s.symbols("vx vy vz", real=True))
    equal(s.expand((u+v).dot(v-u) - (v.dot(v)-u.dot(u))), 0)
    A, B, C, D = V([0, 0, 0]), V([2, 0, 0]), V([3, s.sqrt(3), 0]), V([1, s.sqrt(3), 0])
    ab, ad = B-A, D-A
    equal([ab.norm(), ad.norm(), ab.dot(ad)], [2, 2, 2])


@case(8, "t=1", "t=-1", "t=3", "|1-t|/6")
def p08():
    matrix = V([[1, 0, 1], [0, 1, 1], [1, t, 2]])
    det = matrix.det()
    equal(s.solveset(det, t, domain=s.S.Reals), s.FiniteSet(1))
    roots = s.solveset(s.Abs(det)/6 - R(1, 3), t, domain=s.S.Reals)
    equal(roots, s.FiniteSet(-1, 3))


@case(9, r"\pi:x-z+1=0", r"1/\sqrt2", "(-2,0,2)")
def p09():
    # Solve coefficients of a plane instead of using the answer's cross product.
    a, b, c, d = s.symbols("a b c d", real=True)
    point = V([1+t, -t, 2+t])
    coeff = s.Poly(a*point[0]+b*point[1]+c*point[2]+d, t)
    sol = s.solve(coeff.all_coeffs() + [a+b+c, a-1], (a, b, c, d))
    equal(V([a, b, c, d]).subs(sol), V([1, 0, -1, 1]))
    equal(s.Abs(sol[d])/s.sqrt(sol[a]**2 + sol[b]**2 + sol[c]**2), 1/s.sqrt(2))
    equal(V([1, -1, 1]).cross(V([1, 1, 1])), V([-2, 0, 2]))


@case(10, "x^2+y^2=(z-1)^2", r"z\ge1", "$z=0$ 没有截痕", "半径为 1")
def p10():
    radius = s.symbols("radius", nonnegative=True)
    theta = s.symbols("theta", real=True)
    rotated = {x: radius*s.cos(theta), y: radius*s.sin(theta), z: radius+1}
    equal(s.trigsimp((x*x+y*y-(z-1)**2).subs(rotated)), 0)
    equal(s.solveset(radius+1, radius, domain=s.Interval(0, s.oo)), s.EmptySet)
    equal(s.solveset(radius+1-2, radius, domain=s.Interval(0, s.oo)), s.FiniteSet(1))
    equal(s.solve(z-radius-1, radius), [z-1])
    equal(s.solve_univariate_inequality(z-1 >= 0, z, relational=False), s.Interval(1, s.oo))
    # Horizontal circle shrinks to the stated vertex at the lower endpoint.
    equal(V([rotated[x], rotated[y], rotated[z]]).subs(radius, 0), V([0, 0, 1]))


@case(11, r"\pi:-x+2y+z=0", r"1/\sqrt6", "P=(1/2,0,1/2)",
      "Q=(1/3,1/3,2/3)", "两直线异面")
def p11():
    p, q = V([t, 0, t]), V([1+u, 1+u, -u])
    v1, v2 = p.diff(t), q.diff(u)
    normal = v1.cross(v2)
    equal(normal, V([-1, 2, 1]))
    equal(normal.dot(q-p), 1)
    equal(s.solve(list(q-p), (t, u)), [])
    equal(normal.dot(p), 0)
    distance2 = s.expand((q-p).dot(q-p))
    solution = s.solve([s.diff(distance2, t), s.diff(distance2, u)], (t, u))
    equal([solution[t], solution[u]], [R(1, 2), -R(2, 3)])
    equal(p.subs(solution), V([R(1, 2), 0, R(1, 2)]))
    equal(q.subs(solution), V([R(1, 3), R(1, 3), R(2, 3)]))
    equal(s.sqrt(distance2.subs(solution)), 1/s.sqrt(6))
    # A sum of positive multiples of squares proves global minimality.
    equal(distance2, 2*(t-R(1, 2))**2 + 3*(u+R(2, 3))**2 + R(1, 6))


@case(12, r"x=2\cos t", r"y=4\sin^2t", r"z=2\sin t", r"0\le t<2\pi",
      r"-2\le x\le2", "其余投影点各对应两个点")
def p12():
    param = {x: 2*s.cos(t), y: 4*s.sin(t)**2, z: 2*s.sin(t)}
    f, g = x*x+z*z-4, y-z*z
    equal(s.trigsimp(f.subs(param)), 0)
    equal(s.trigsimp(g.subs(param)), 0)
    # Elimination plus real-root classification gives the exact projected set.
    resultant = s.factor(s.resultant(f, g, z))
    equal(resultant, (x*x+y-4)**2)
    heights2 = s.solve(f, z*z)[0]
    equal(heights2, 4-x*x)
    domain = s.solve_univariate_inequality(heights2 >= 0, x, relational=False)
    equal(domain, s.Interval(-2, 2))
    equal(s.solveset(heights2, x, domain=s.S.Reals), s.FiniteSet(-2, 2))
    equal(s.solve_univariate_inequality(heights2 > 0, x, relational=False), s.Interval.open(-2, 2))
    equal(s.discriminant(z*z-heights2, z), 4*heights2)
    # The polar angle reconstructs any (x,z) on this circle; y is then unique.
    angle = s.atan2(z, x)
    equal(s.simplify(2*s.cos(angle)).subs(x*x+z*z, 4), x)
    equal(s.simplify(2*s.sin(angle)).subs(x*x+z*z, 4), z)


@case(13, "球心 $(t,0,0)$", r"\sqrt{2t}", "$t=0$ 时是原点", "$t<0$ 时是空集",
      "最小 $x$ 为 $-1/2$", "t=1/2", "(-1/2,0,0)")
def p13():
    f = x*x+y*y+z*z-2*t*x+t*t-2*t
    center = s.solve([s.diff(f, v) for v in (x, y, z)], (x, y, z))
    equal(V([x, y, z]).subs(center), V([t, 0, 0]))
    radius2 = -f.subs(center)
    equal(radius2, 2*t)
    equal(s.solve_univariate_inequality(radius2 > 0, t, relational=False), s.Interval.open(0, s.oo))
    equal(s.solveset(radius2, t, domain=s.S.Reals), s.FiniteSet(0))
    equal(s.solve_univariate_inequality(radius2 < 0, t, relational=False), s.Interval.open(-s.oo, 0))
    left = center[x]-s.sqrt(radius2)
    roots = s.solveset(s.diff(left, t), t, domain=s.Interval.open(0, 2))
    equal(roots, s.FiniteSet(R(1, 2)))
    equal([left.subs(t, v) for v in (0, R(1, 2), 2)], [0, -R(1, 2), 0])
    equal(f.subs({x: -R(1, 2), y: 0, z: 0, t: R(1, 2)}), 0)


@case(14, r"(x-1)^2+y^2\le1", r"面积为 $\pi$")
def p14():
    lower, upper = x*x+y*y, 2*x
    equal(upper-lower, 1-(x-1)**2-y*y)
    edge_y = sorted(s.solve(upper-lower, y), key=lambda expr: expr.subs(x, 1))
    equal(edge_y, [-s.sqrt(x*(2-x)), s.sqrt(x*(2-x))])
    equal(s.solve_univariate_inequality(x*(2-x) >= 0, x, relational=False), s.Interval(0, 2))
    # Integrate in translated Cartesian coordinates, independently of the
    # trigonometric substitution used in the printed solution.
    width = (edge_y[1]-edge_y[0]).subs(x, u+1)
    equal(s.integrate(s.simplify(width), (u, -1, 1)), s.pi)


@case(15, "最小距离为 1", "t=0,1", r"\sqrt{66}/8", "t=1/2")
def p15():
    p, q = V([t, t*t, 0]), V([u, u, 1])
    distance2 = (p-q).dot(p-q)
    foot_u = s.solve(s.diff(distance2, u), u)[0]
    minimum_on_line = s.factor(distance2.subs(u, foot_u))
    equal(s.diff(distance2, u, 2), 4)
    equal(minimum_on_line, 1+(t-t*t)**2/2)
    roots = s.solveset(s.diff(minimum_on_line, t), t, domain=s.Interval.open(0, 1))
    equal(roots, s.FiniteSet(R(1, 2)))
    candidates = {v: s.sqrt(minimum_on_line.subs(t, v)) for v in (0, R(1, 2), 1)}
    equal(min(candidates.values()), 1)
    equal(max(candidates.values()), s.sqrt(66)/8)
    equal({v for v, value in candidates.items() if value == 1}, {0, 1})
    equal({v for v, value in candidates.items() if value == s.sqrt(66)/8}, {R(1, 2)})


def main():
    failures = 0
    ids = re.findall(r"^\*\*(C19-\d+)\*\*", PROBLEMS, re.M)
    if ids != [item[0] for item in TESTS] or set(ids) != set(BLOCKS):
        print("FAIL C19 覆盖题号不一致")
        failures += 1
    for pid, fragments, manual, fn in TESTS:
        try:
            block = BLOCKS[pid].split("\n### ")[0].strip()
            assert block.startswith("**答案：**"), "缺答案行"
            assert block.splitlines()[-1].startswith("区分点："), "区分点须在末行"
            tier = re.search(rf"\*\*{pid}\*\*〔([ABC])", PROBLEMS)[1]
            assert len(block) <= {"A": 400, "B": 900, "C": 1400}[tier], len(block)
            for fragment in fragments:
                assert fragment in block, f"答案与核对值不同: {fragment}"
            fn()
            print(f"{'MANUAL' if manual else 'PASS'} {pid}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {pid} {type(exc).__name__}: {exc}")
    return int(failures > 0)


if __name__ == "__main__":
    sys.exit(main())
