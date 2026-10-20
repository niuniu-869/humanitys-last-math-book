"""Independent exact checks for all 23 numbered examples in lesson.md."""

from pathlib import Path
import re
import sys

import sympy as s


V, R = s.Matrix, s.Rational
x, y, z, t, u, k = s.symbols("x y z t u k", real=True)
A, B, C, D = V([1, 0, 0]), V([0, 2, 0]), V([0, 0, 3]), V([1, 1, 1])
a, b = V([1, 2, 2]), V([3, 0, 4])
TESTS = []


def equal(actual, expected):
    if isinstance(actual, s.MatrixBase):
        assert actual.shape == expected.shape
        assert all(s.simplify(v) == 0 for v in actual-expected), (actual, expected)
    elif isinstance(actual, (list, tuple)):
        assert len(actual) == len(expected)
        for av, ev in zip(actual, expected):
            equal(av, ev)
    elif isinstance(actual, (bool, s.Set)) or isinstance(expected, bool):
        assert actual == expected, (actual, expected)
    else:
        assert s.simplify(actual-expected) == 0, (actual, expected)


def case(number):
    def register(fn):
        TESTS.append((number, fn))
        return fn
    return register


@case(1)
def ex01():
    edges2 = [(A-B).dot(A-B), (B-C).dot(B-C), (A-C).dot(A-C)]
    equal([s.sqrt(v) for v in edges2], [s.sqrt(5), s.sqrt(13), s.sqrt(10)])
    equal(any(sum(edges2)-v == v for v in edges2), False)


@case(2)
def ex02():
    p, m, n = V([0, 0, z]), V([1, 0, 2]), V([0, 1, -1])
    equal(s.solve((p-m).dot(p-m)-(p-n).dot(p-n), z), [R(1, 2)])


@case(3)
def ex03():
    p, q, r = V([1, -1, 2]), V([3, 1, 1]), V([7, 5, -1])
    equal(q-p, V([2, 2, -1]))
    equal(r-p, V([6, 6, -3]))
    equal(s.solve(list(r-p-t*(q-p)), t)[t], 3)


@case(4)
def ex04():
    equal(a.norm(), 3)
    unit = a/a.norm()
    equal(unit, V([R(1, 3), R(2, 3), R(2, 3)]))
    equal(unit.dot(unit), 1)


@case(5)
def ex05():
    equal([a.dot(b), a.norm(), b.norm()], [11, 3, 5])
    equal([a.dot(b)/(a.norm()*b.norm()), a.dot(b)/a.norm()], [R(11, 15), R(11, 3)])


@case(6)
def ex06():
    q, d1, d2 = V([2, 1, 0]), V([4, 3, 0]), V([20, 0, 20])
    equal([q.dot(d1), q.dot(d2)], [11, 40])
    equal([q.norm(), d1.norm(), d2.norm()], [s.sqrt(5), 5, 20*s.sqrt(2)])
    cosine1, cosine2 = q.dot(d1)/(q.norm()*d1.norm()), q.dot(d2)/(q.norm()*d2.norm())
    equal([cosine1, cosine2], [11/(5*s.sqrt(5)), 2/s.sqrt(10)])
    equal(cosine1 > cosine2, True)
    equal(abs(float(cosine1)-0.984) < 0.0005, True)
    equal(abs(float(cosine2)-0.632) < 0.0005, True)


@case(7)
def ex07():
    normal = (B-A).cross(C-A)
    equal(normal, V([6, 3, 2]))
    equal([normal.dot(B-A), normal.dot(C-A)], [0, 0])
    equal(normal.norm()/2, R(7, 2))


@case(8)
def ex08():
    p1, p2, p3, eye = V([0, 0, 0]), V([2, 0, 0]), V([0, 2, 0]), V([1, 1, 5])
    normal = (p2-p1).cross(p3-p1)
    equal(normal, V([0, 0, 4]))
    score = normal.dot(eye-p1)
    equal(score, 20)
    equal(score > 0, True)


@case(9)
def ex09():
    det = V.hstack(B-A, C-A, D-A).det()
    equal(det, 5)
    equal(det != 0, True)
    equal(s.Abs(det)/6, R(5, 6))


@case(10)
def ex10():
    # Fit plane coefficients with the printed normalization D=-6.
    nx, ny, nz = s.symbols("nx ny nz")
    n = V([nx, ny, nz])
    coeff = s.solve([n.dot(point)-6 for point in (A, B, C)], (nx, ny, nz))
    equal(n.subs(coeff), V([6, 3, 2]))
    equal([6/coeff[nx], 6/coeff[ny], 6/coeff[nz]], [1, 2, 3])


@case(11)
def ex11():
    n = V([6, 3, 2])
    foot = D-t*n
    param = s.solve(n.dot(foot)-6, t)[0]
    distance = (D-foot.subs(t, param)).norm()
    equal(distance, R(5, 7))
    equal((B-A).cross(C-A).norm()/2*distance/3, R(5, 6))


@case(12)
def ex12():
    w, bias = V([1, 2, 2]), -3
    p1, p2 = V([3, 0, 1]), V([0, 0, 0])
    scores = [w.dot(p)+bias for p in (p1, p2)]
    equal(w.dot(V([x, y, z]))+bias, x+2*y+2*z-3)
    equal(scores, [2, -3])
    equal([s.sign(score) for score in scores], [1, -1])
    equal([s.Abs(score)/w.norm() for score in scores], [R(2, 3), 1])


@case(13)
def ex13():
    f, g = x+y+z-1, 2*x-y+3*z-4
    direction = V([s.diff(f, v) for v in (x, y, z)]).cross(V([s.diff(g, v) for v in (x, y, z)]))
    equal(direction, V([4, -1, -3]))
    sol = s.solve([f, g, y], (x, y, z))
    equal(V([x, y, z]).subs(sol), V([-1, 0, 2]))
    parametrization = {x: -1+4*t, y: -t, z: 2-3*t}
    equal([s.expand(f.subs(parametrization)), s.expand(g.subs(parametrization))], [0, 0])
    # The symmetric equation has these same nonzero direction components.
    equal([(parametrization[x]+1)/4, -parametrization[y], (parametrization[z]-2)/(-3)], [t, t, t])


@case(14)
def ex14():
    p, n = V([1, 2, 3]), V([2, -1, 2])
    line = p+t*n
    root = s.solve(n.dot(line)+1, t)[0]
    equal(root, -R(7, 9))
    foot = line.subs(t, root)
    equal(foot, V([-R(5, 9), R(25, 9), R(13, 9)]))
    equal((foot-p).norm(), R(7, 3))


@case(15)
def ex15():
    line, n = V([1+t, 2, -1+t]), V([1, 1, 0])
    direction = line.diff(t)
    sine = s.Abs(direction.dot(n))/(direction.norm()*n.norm())
    equal(sine, R(1, 2))
    equal(s.asin(sine), s.pi/6)
    root = s.solve(n.dot(line)-5, t)[0]
    equal(root, 2)
    equal(line.subs(t, root), V([3, 2, 1]))


@case(16)
def ex16():
    p1, p2 = V([0, 1, 0]), V([2, 0, 1])
    d1, d2 = V([1, 2, 1]), V([2, 1, 0])
    equal(d1.cross(d2).dot(p2-p1), -7)
    equal(d1.cross(d2) != s.zeros(3, 1), True)
    equal(s.solve(list(p1+t*d1-p2-u*d2), (t, u)) == [], True)


@case(17)
def ex17():
    p, m, direction = V([3, 2, 1]), V([1, -1, 0]), V([2, -1, 2])
    equal((p-m).cross(direction), V([7, -2, -8]))
    equal((p-m).cross(direction).norm(), 3*s.sqrt(13))
    foot = m+t*direction
    squared = (p-foot).dot(p-foot)
    root = s.solve(s.diff(squared, t), t)[0]
    equal(root, R(1, 3))
    equal(foot.subs(t, root), V([R(5, 3), -R(4, 3), R(2, 3)]))
    equal(s.sqrt(squared.subs(t, root)), s.sqrt(13))
    equal(s.diff(squared, t, 2) > 0, True)


@case(18)
def ex18():
    f = x*x+y*y+z*z+4*y
    center = s.solve([s.diff(f, v) for v in (x, y, z)], (x, y, z))
    equal(V([x, y, z]).subs(center), V([0, -2, 0]))
    equal(s.sqrt(-f.subs(center)), 2)
    g = z-1+x*x
    equal(s.diff(g, y), 0)
    equal(s.solve(g, z), [1-x*x])
    equal(s.diff(s.solve(g, z)[0], x, 2), -2)


@case(19)
def ex19():
    f = x*x/4-z*z/9-1
    around_z = s.expand(f.subs(x, s.sqrt(x*x+y*y)))
    around_x = s.expand(f.subs(z, s.sqrt(y*y+z*z)))
    equal(around_z, (x*x+y*y)/4-z*z/9-1)
    equal(around_x, x*x/4-(y*y+z*z)/9-1)
    r2 = s.symbols("r2", real=True)
    section_z = s.solve(r2/4-k*k/9-1, r2)[0]
    section_x = s.solve(k*k/4-r2/9-1, r2)[0]
    equal(s.solve_univariate_inequality(section_z > 0, k, relational=False), s.S.Reals)
    equal(s.solve_univariate_inequality(section_x >= 0, k, relational=False),
          s.Union(s.Interval(-s.oo, -2), s.Interval(2, s.oo)))


@case(20)
def ex20():
    f = x*x-4*y*y+z*z+4
    section = f.subs(y, k)
    equal(section, x*x+z*z-(4*k*k-4))
    radius2 = -section.subs({x: 0, z: 0})
    equal(s.solve_univariate_inequality(radius2 < 0, k, relational=False), s.Interval.open(-1, 1))
    equal(s.solveset(radius2, k, domain=s.S.Reals), s.FiniteSet(-1, 1))
    equal(s.solve_univariate_inequality(radius2 > 0, k, relational=False),
          s.Union(s.Interval.open(-s.oo, -1), s.Interval.open(1, s.oo)))


@case(21)
def ex21():
    point = {x: s.cos(t), y: s.sin(t), z: 2-s.cos(t)-s.sin(t)}
    equal(s.trigsimp((x*x+y*y-1).subs(point)), 0)
    equal(s.expand((x+y+z-2).subs(point)), 0)
    equal(s.solve(x+y+z-2, z), [2-x-y])
    # Unit-circle coverage plus a unique height verifies the whole intersection.
    angle = s.atan2(y, x)
    equal(s.cos(angle).subs(x*x+y*y, 1), x)
    equal(s.sin(angle).subs(x*x+y*y, 1), y)


@case(22)
def ex22():
    sphere, plane = x*x+y*y+z*z-4, x+z-2
    eliminated = s.resultant(sphere, plane, z)
    equal(eliminated, 2*(x-1)**2+y*y-2)
    center = s.solve([s.diff(eliminated, v) for v in (x, y)], (x, y))
    equal(V([x, y]).subs(center), V([1, 0]))
    equal(s.solve(plane, z), [2-x])
    point = {x: 1+s.cos(t), y: s.sqrt(2)*s.sin(t), z: 1-s.cos(t)}
    equal(s.trigsimp(sphere.subs(point)), 0)
    equal(s.expand(plane.subs(point)), 0)
    # In the sloping plane the radius is sqrt(2), not the projected x radius 1.
    equal(s.trigsimp(sum((point[v]-c)**2 for v, c in zip((x, y, z), (1, 0, 1)))), 2)


@case(23)
def ex23():
    q = s.symbols("q", real=True)  # q = x^2+y^2
    lower, upper = s.sqrt(q), s.sqrt(2-q)
    real_domain = s.Interval(0, 2)
    roots = s.solveset(lower-upper, q, domain=real_domain)
    equal(roots, s.FiniteSet(1))
    equal(lower.subs(q, 1), 1)
    domain = s.solve_univariate_inequality(lower <= upper, q, relational=False)
    equal(domain.intersect(real_domain), s.Interval(0, 1))
    equal([lower.subs(q, 0), upper.subs(q, 0)], [0, s.sqrt(2)])


# 随堂题与迁入第 7 节的跨章题：每项都从题面重新计算。
@case(24)
def ex24():
    equal(s.sqrt(3**2+(-4)**2+12**2), 13)


@case(25)
def ex25():
    m, n = s.symbols("m n")
    sol = s.solve([m+6, n-2], (m, n), dict=True)[0]
    equal([sol[m], sol[n]], [-6, 2])


@case(26)
def ex26():
    equal([6*s.Rational(1, 2), -6*s.Rational(1, 2)], [3, -3])
    equal(s.solve(s.Symbol("cg")**2 - s.Rational(1, 2), s.Symbol("cg")),
          [-s.sqrt(2)/2, s.sqrt(2)/2])


@case(27)
def ex27():
    p, q = V([1, 2, 1]), V([3, -1, 2])
    equal(p.dot(q), 3-2+2)


@case(28)
def ex28():
    p, q = V([1, 2, -1]), V([2, 0, 1])
    equal(p.cross(q), V([2, -3, -4]))
    equal(p.cross(q).norm(), s.sqrt(29))


@case(29)
def ex29():
    equal(s.Abs(V([[1, 0, 0], [1, 2, 0], [1, 2, 3]]).det())/6, 1)


@case(30)
def ex30():
    point, normal = V([1, 2, 3]), V([2, -1, 2])
    equal(s.Abs(normal.dot(point)+1)/normal.norm(), s.Rational(7, 3))


@case(31)
def ex31():
    equal(V([3, 1, 4])-V([1, 0, -2]), V([2, 1, 6]))


@case(32)
def ex32():
    equal(s.solve(y**2+z**2-9, z), [-s.sqrt(9-y**2), s.sqrt(9-y**2)])
    equal(5**2+3**2, 34)


@case(33)
def ex33():
    equal((x*x+y*y-9).subs({x: 5, y: 3}), 25+9-9)


@case(34)
def ex34():
    equal((x*x/4+y*y-1).subs({x: s.Symbol("X"), y: s.Symbol("Y")}),
          s.Symbol("X")**2/4+s.Symbol("Y")**2-1)


@case(35)
def ex35():
    tt = s.symbols("tt", real=True)
    point = {x: s.Rational(3, 1)/s.sqrt(2)*s.cos(tt),
             y: 3*s.sin(tt), z: s.Rational(3, 1)/s.sqrt(2)*s.cos(tt)}
    equal(s.trigsimp((x*x+y*y+z*z-9).subs(point)), 0)


@case(36)
def ex36():
    point = V([s.sin(t), 1-s.cos(t), t])
    signed = V([1, 1, 1]).dot(point)/s.sqrt(3)
    quotient = s.Abs(signed)/s.Abs(t)
    equal(s.limit(quotient, t, 0, dir="+"), 2/s.sqrt(3))
    equal(s.limit(quotient, t, 0, dir="-"), 2/s.sqrt(3))


@case(37)
def ex37():
    equal(V([2, 0, 0]).cross(V([0, 3, 0])).dot(V([0, 0, 4])), 24)
    equal(V([-1, 2, 0]).cross(V([-1, 0, 3])), V([6, 3, 2]))
    equal(V([-1, 2, 0]).dot(V([6, 3, 2])), 0)
    equal(V([-1, 0, 3]).dot(V([6, 3, 2])), 0)
    equal(a.cross(b), V([8, 2, -6]))
    equal(V([3, 4, 0]).cross(V([1, 0, 0])).norm(), 4)


@case(38)
def ex38():
    P, Q, Rr = V([1, 1, 0]), V([0, 1, 1]), V([1, 0, 1])
    n = (Q-P).cross(Rr-P)
    equal(n, V([1, 1, 1]))
    equal(n.dot(P), 2)
    equal(n.dot(Q), 2)
    equal(n.dot(Rr), 2)


@case(39)
def ex39():
    n1, n2 = V([1, 1, 0]), V([1, 0, 1])
    equal(s.Abs(n1.dot(n2))/(n1.norm()*n2.norm()), R(1, 2))
    equal(s.acos(R(1, 2)), s.pi/3)
    equal(V([1, 2, 3]).cross(V([2, 4, 6])), V([0, 0, 0]))


@case(40)
def ex40():
    equal(s.expand(x**2+y**2+(2-y)**2-4), s.expand(x**2+2*(y-1)**2-2))
    equal(s.expand((-x**2+y**2+z**2-1).subs(x, k)), s.expand(y**2+z**2-1-k**2))
    equal(s.expand(x**2+y**2+z**2-4).subs(z, 2-y), s.expand(x**2+2*(y-1)**2-2))
    equal(s.sqrt(9+16), 5)


def main():
    lesson = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")
    ids = [int(v) for v in re.findall(r"^\*\*例 (\d+)\*\*", lesson, re.M)]
    failures = 0
    if ids != [n for n, _ in TESTS[:23]]:
        print("FAIL 讲义例题覆盖不完整")
        failures += 1
    for number, fn in TESTS:
        try:
            fn()
            print(f"PASS 例{number}")
        except Exception as exc:
            print(f"FAIL 例{number} {type(exc).__name__}: {exc}")
            failures += 1
    return int(failures > 0)


if __name__ == "__main__":
    sys.exit(main())
