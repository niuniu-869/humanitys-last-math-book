import sympy as sp


def check_line(line, parameter, point, direction):
    assert line.subs(parameter, 0) == point
    actual = line.diff(parameter)
    assert actual != sp.zeros(3, 1) and direction != sp.zeros(3, 1)
    assert actual.cross(direction) == sp.zeros(3, 1)


def main():
    t, x, y, z = sp.symbols("t x y z", real=True)
    s = sp.symbols("s", real=True)

    r1 = sp.Matrix([2*sp.cos(t), 2*sp.sin(t), t])
    p1 = r1.subs(t, sp.pi/2)
    tv1 = r1.diff(t).subs(t, sp.pi/2)
    assert p1 == sp.Matrix([0, 2, sp.pi/2]) and tv1 == sp.Matrix([-2, 0, 1])
    check_line(sp.Matrix([-2*s, 2, sp.pi/2+s]), s, p1, tv1)
    assert sp.expand(tv1.dot(sp.Matrix([x, y, z]) - p1)) == -2*x + z - sp.pi/2
    print("PASS 例1")

    r1b = sp.Matrix([t, t**2, t**3])
    assert r1b.subs(t, 1) == sp.Matrix([1, 1, 1])
    assert r1b.diff(t).subs(t, 1) == sp.Matrix([1, 2, 3])
    check_line(sp.Matrix([1+s, 1+2*s, 1+3*s]), s, r1b.subs(t, 1), r1b.diff(t).subs(t, 1))
    assert sp.expand(sp.Matrix([1, 2, 3]).dot(sp.Matrix([x, y, z]) - sp.Matrix([1, 1, 1]))) == x + 2*y + 3*z - 6
    print("PASS 例1后题")

    F2 = x**2 + 2*y**2 + 3*z**2 - 21
    p2 = {x: 1, y: -2, z: 2}
    g2 = sp.Matrix([sp.diff(F2, v).subs(p2) for v in (x, y, z)])
    assert F2.subs(p2) == 0 and g2 == sp.Matrix([2, -8, 12])
    check_line(sp.Matrix([1+s, -2-4*s, 2+6*s]), s, sp.Matrix([1, -2, 2]), g2)
    assert sp.expand(sp.Matrix([1, -4, 6]).dot(sp.Matrix([x, y, z]) - sp.Matrix([1, -2, 2]))) == x - 4*y + 6*z - 21
    print("PASS 例2")

    F2b = sp.exp(z) - z + x*y - 3
    p2b = {x: 2, y: 1, z: 0}
    g2b = sp.Matrix([sp.diff(F2b, v).subs(p2b) for v in (x, y, z)])
    assert F2b.subs(p2b) == 0 and g2b == sp.Matrix([1, 2, 0])
    check_line(sp.Matrix([2+s, 1+2*s, 0]), s, sp.Matrix([2, 1, 0]), g2b)
    assert sp.expand(sp.Matrix([1, 2, 0]).dot(sp.Matrix([x, y, z]) - sp.Matrix([2, 1, 0]))) == x + 2*y - 4
    print("PASS 例2后题")

    k = sp.symbols("k", real=True)
    eq = sp.Eq(k**2/4 + 2*k**2 + 3*k**2, 21)
    assert sp.solve(eq, k) == [-2, 2]
    assert [(k/2, k, k) for k in (2, -2)] == [(1, 2, 2), (-1, -2, -2)]
    for sign in (1, -1):
        point = sign*sp.Matrix([1, 2, 2])
        sub = dict(zip((x, y, z), point))
        assert F2.subs(sub) == 0
        normal = sp.Matrix([sp.diff(F2, v).subs(sub) for v in (x, y, z)])
        plane = sp.expand(normal.dot(sp.Matrix([x, y, z])-point)/(2*sign))
        assert plane == x+4*y+6*z-sign*21
    print("PASS 例3")

    F4 = x**2 + y**2 + z**2 - 6
    G4 = x + y + z
    p4 = {x: 1, y: -2, z: 1}
    n4 = sp.Matrix([sp.diff(F4, v).subs(p4) for v in (x, y, z)])
    m4 = sp.Matrix([sp.diff(G4, v) for v in (x, y, z)])
    assert n4.cross(m4) == sp.Matrix([-6, 0, 6])
    assert F4.subs(p4) == G4.subs(p4) == 0
    check_line(sp.Matrix([1+s, -2, 1-s]), s, sp.Matrix([1, -2, 1]), n4.cross(m4))
    assert sp.expand(sp.Matrix([1, 0, -1]).dot(sp.Matrix([x, y, z]) - sp.Matrix([1, -2, 1]))) == x - z
    print("PASS 例4")

    F4b = x**2 + y**2 - z
    G4b = x + 2*y + z - 5
    p4b = {x: 1, y: 1, z: 2}
    n4b = sp.Matrix([sp.diff(F4b, v).subs(p4b) for v in (x, y, z)])
    m4b = sp.Matrix([sp.diff(G4b, v).subs(p4b) for v in (x, y, z)])
    assert n4b.cross(m4b) == sp.Matrix([4, -3, 2])
    assert sp.expand(sp.Matrix([4, -3, 2]).dot(sp.Matrix([x, y, z]) - sp.Matrix([1, 1, 2]))) == 4*x - 3*y + 2*z - 5
    print("PASS 例4后题")


if __name__ == "__main__":
    main()
