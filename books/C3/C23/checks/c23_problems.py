import sympy as sp


def same_line(a, b):
    a, b = sp.Matrix(a), sp.Matrix(b)
    return a != sp.zeros(3, 1) and b != sp.zeros(3, 1) and a.cross(b) == sp.zeros(3, 1)


def check_line(line, parameter, point, direction):
    assert line.subs(parameter, 0) == point
    assert same_line(line.diff(parameter), direction)


def main():
    t, s = sp.symbols("t s", real=True)
    x, y, z = sp.symbols("x y z")

    r = sp.Matrix([t**2, 2*t + 1, t**3 - t])
    p = sp.Matrix([1, 3, 0])
    tangent = r.diff(t).subs(t, 1)
    assert tangent == sp.Matrix([2, 2, 2]) and r.subs(t, 1) == p
    check_line(sp.Matrix([1+s, 3+s, s]), s, p, tangent)
    assert sp.expand(sp.Matrix([1, 1, 1]).dot(sp.Matrix([x, y, z]) - p)) == x + y + z - 4
    print("PASS C23-01")

    F2 = x**2 + 2*y**2 + z**2 - 2*x + 4*y - 6*z + 7
    p2 = sp.Matrix([2, -1, 1])
    grad2 = sp.Matrix([sp.diff(F2, v) for v in (x, y, z)]).subs(dict(zip((x, y, z), p2)))
    assert F2.subs(dict(zip((x, y, z), p2))) == 0
    assert grad2 == sp.Matrix([2, 0, -4])
    check_line(sp.Matrix([2+s, -1, 1-2*s]), s, p2, grad2)
    assert sp.expand((sp.Matrix([1, 0, -2]).dot(sp.Matrix([x, y, z]) - p2))) == x - 2*z
    print("PASS C23-02")

    a, b = sp.symbols("a b", real=True)
    f = x**2 + a*x*y + b*y**2
    fx, fy = sp.diff(f, x).subs({x: 1, y: 1}), sp.diff(f, y).subs({x: 1, y: 1})
    value = f.subs({x: 1, y: 1})
    assert sp.solve([fx-4, fy-2, value-3], (a, b)) == {a: 2, b: 0}
    options03 = [(2, 0), (0, 2), (1, 1), (2, 1)]
    data03 = [(value.subs({a: av, b: bv}), fx.subs({a: av, b: bv}),
               fy.subs({a: av, b: bv})) for av, bv in options03]
    assert data03 == [(3, 4, 2), (3, 2, 4), (3, 3, 3), (4, 4, 4)]
    assert [q == (3, 4, 2) for q in data03] == [True, False, False, False]
    assert sp.expand((value + fx*(x-1) + fy*(y-1)).subs({a: 2, b: 0})) == 4*x+2*y-3
    print("PASS C23-03")

    r4 = sp.Matrix([sp.cos(t), sp.sin(t), 2*t])
    p4 = r4.subs(t, 0)
    tv4 = r4.diff(t).subs(t, 0)
    check_line(sp.Matrix([1, s, 2*s]), s, p4, tv4)
    options04 = [tv4 == sp.Matrix([1, 0, 2]),
                 (p4 + s*tv4).tolist() == [[1], [s], [2*s]],
                 sp.expand(tv4.dot(sp.Matrix([x, y, z]) - p4)) == x - 1,
                 not same_line(tv4, tv4/sp.sqrt(tv4.dot(tv4)))]
    assert options04 == [False, True, False, False]
    print("PASS C23-04")

    F5 = x**2 + y**2 + z**2 - 9
    G5 = x + y + z - 3
    p5 = sp.Matrix([2, 2, -1])
    n1 = sp.Matrix([sp.diff(F5, v).subs({x: 2, y: 2, z: -1}) for v in (x, y, z)])
    n2 = sp.Matrix([sp.diff(G5, v) for v in (x, y, z)])
    cross = n1.cross(n2)
    assert F5.subs({x: 2, y: 2, z: -1}) == G5.subs({x: 2, y: 2, z: -1}) == 0
    assert same_line(cross, [1, -1, 0])
    assert sp.expand((cross/6).dot(sp.Matrix([x, y, z])-p5)) == x-y
    options05 = [same_line([5, 5, -1], cross), same_line([1, -1, 0], cross),
                 isinstance(n1.dot(n2), sp.MatrixBase),
                 sp.expand(x + y + z - 3) == sp.expand(cross.dot(sp.Matrix([x, y, z]) - p5))]
    assert cross == sp.Matrix([6, -6, 0]) and options05 == [False, True, False, False]
    print("PASS C23-05")

    F6 = (z-x-y)**3
    grad6 = sp.Matrix([sp.diff(F6, v).subs({x: 0, y: 0, z: 0}) for v in (x, y, z)])
    assert sp.solve(F6, z) == [x+y]
    reduced = z-x-y
    normal6 = sp.Matrix([sp.diff(reduced, v) for v in (x, y, z)])
    assert normal6 == sp.Matrix([-1, -1, 1])
    assert normal6.dot(sp.Matrix([1, 0, 1])) == normal6.dot(sp.Matrix([0, 1, 1])) == 0
    zero_equation = grad6.dot(sp.Matrix([x, y, z]))
    plane_exists = normal6 != sp.zeros(3, 1) and sp.Poly(reduced, x, y, z).total_degree() == 1
    options06 = [sp.Poly(zero_equation, x, y, z).total_degree() == 1,
                 not plane_exists,
                 grad6 == sp.zeros(3, 1) and plane_exists and F6.subs(z, x+y) == 0,
                 same_line([0, 0, 1], normal6)]
    assert options06 == [False, False, True, False]
    print("PASS C23-06")

    f7 = x**2+y**2
    plane7 = sp.expand(f7.subs({x: a, y: b}) +
                       sp.diff(f7, x).subs(x, a)*(x-a) +
                       sp.diff(f7, y).subs(y, b)*(y-b))
    assert plane7 == 2*a*x+2*b*y-a**2-b**2
    assert sp.expand(f7-plane7-((x-a)**2+(y-b)**2)) == 0
    assert plane7.subs({x: a, y: b}) == a**2+b**2
    print("MANUAL C23-07 证明：平方和非负，等号当且仅当 x=a、y=b；恒等式已符号核对")

    F8 = x**2 + y**2 + z**2 - 6
    G8 = x + 2*y + z - 5
    n8a = sp.Matrix([sp.diff(F8, v).subs({x: 1, y: 1, z: 2}) for v in (x, y, z)])
    n8b = sp.Matrix([sp.diff(G8, v) for v in (x, y, z)])
    tv8 = n8a.cross(n8b)
    gh = sp.Matrix([y, x, 1]).subs({x: 1, y: 1})
    rate = sp.simplify(gh.dot(tv8) / sp.sqrt(tv8.dot(tv8)))
    assert F8.subs({x: 1, y: 1, z: 2}) == 0 and G8.subs({x: 1, y: 1, z: 2}) == 0
    assert tv8 == sp.Matrix([-6, 2, 2]) and rate == -1/sp.sqrt(11)
    p8 = sp.Matrix([1, 1, 2])
    check_line(sp.Matrix([1-3*s, 1+s, 2+s]), s, p8, tv8)
    assert sp.expand((tv8/2).dot(sp.Matrix([x, y, z])-p8)) == -3*x+y+z
    unit8 = tv8/sp.sqrt(tv8.dot(tv8))
    assert unit8[1] > 0 and sp.simplify(unit8.dot(unit8)) == 1
    assert sp.simplify(gh.dot(-unit8)) == 1/sp.sqrt(11)
    # A unit-speed parameterization of the actual intersection circle checks the chain rule.
    center = sp.Rational(5, 6)*n8b
    radial = p8-center
    radius = sp.sqrt(radial.dot(radial))
    curve8 = center + radial*sp.cos(s/radius) + radius*unit8*sp.sin(s/radius)
    substitutions = dict(zip((x, y, z), curve8))
    assert sp.trigsimp(F8.subs(substitutions, simultaneous=True)) == 0
    assert sp.trigsimp(G8.subs(substitutions, simultaneous=True)) == 0
    assert curve8.subs(s, 0) == p8 and curve8.diff(s).subs(s, 0) == unit8
    assert sp.trigsimp(curve8.diff(s).dot(curve8.diff(s))) == 1
    assert sp.simplify(sp.diff(curve8[0]*curve8[1]+curve8[2], s).subs(s, 0)) == rate
    print("PASS C23-08")


if __name__ == "__main__":
    main()
