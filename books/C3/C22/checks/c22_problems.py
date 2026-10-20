import sympy as sp


def ok(pid, condition, detail=""):
    tag = f"PASS {pid}" if bool(condition) else f"FAIL {pid}"
    print(tag + (f" {detail}" if detail else ""))


def check_lines(pid, x, y, point, gradient, tangent, normal):
    for name, line, is_tangent in [("切线", tangent, True), ("法线", normal, False)]:
        coefficients = sp.Matrix([sp.diff(line, x), sp.diff(line, y)])
        direction = sp.Matrix([coefficients[1], -coefficients[0]])
        relation = gradient.dot(direction) if is_tangent else sp.det(sp.Matrix.hstack(gradient, direction))
        ok(f"{pid}-{name}", line.subs(dict(zip((x, y), point))) == 0
           and coefficients.norm() != 0 and relation == 0)


def main():
    x, y, a, eta = sp.symbols("x y a eta", real=True)

    # C22-01
    f = x**2 * y + y**3
    grad = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: 1})
    u = sp.Matrix([-2, 3]) / sp.sqrt(13)
    ok("C22-01", sp.simplify(grad.dot(u) - 8 / sp.sqrt(13)) == 0)

    # C22-02, check each option independently.
    g = sp.Matrix([-3, 4])
    opts = {
        "A": sp.simplify(g.norm() - 5) == 0 and g.dot(g / 5) == 5,
        "B": g.dot(sp.Matrix([3, -4]) / 5) == 5,
        "C": g.dot(sp.Matrix([4, 3]) / 5) == 0 and g.dot(sp.Matrix([-4, -3]) / 5) != 0,
        "D": g.dot(sp.Matrix([3, -4]) / 5) == 5,
    }
    ok("C22-02-A", opts["A"])
    ok("C22-02-B", not opts["B"])
    ok("C22-02-C", not opts["C"])
    ok("C22-02-D", not opts["D"])

    # C22-03
    f = x**2 + 2*x*y + 3*y**2
    gg = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: 1})
    ok("C22-03-等高线", f.subs({x: 1, y: 1}) == 6 and gg == sp.Matrix([4, 8]))
    check_lines("C22-03", x, y, (1, 1), gg, x + 2*y - 3, 2*x - y - 1)

    # C22-04
    f = x**2 + 4*y**2
    p0 = sp.Matrix([1, 1])
    grad0 = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: 1})
    candidates = [sp.Matrix(v)/5 for v in [(4, 1), (4, 4), (6, 9), (5, 1)]]
    for letter, candidate in zip("ABCD", candidates):
        rates = [(p0[i] - candidate[i])/grad0[i] for i in range(2)]
        possible = rates[0] == rates[1] and rates[0] > 0
        ok(f"C22-04-{letter}", bool(possible) == (letter == "A"))
        if letter == "A":
            ok("C22-04-学习率", rates[0] == sp.Rational(1, 10))

    # C22-05
    f = x**2 + a*x*y + y**2
    gg = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: 1})
    sol = sp.solve(sp.Eq(gg.dot(sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5)])), 4), a)[0]
    ok("C22-05", sol == sp.Rational(6, 7))

    # C22-06
    t = sp.symbols("t", positive=True)
    b, s = sp.symbols("b s", real=True)
    f = sp.Abs(x + y)
    quotient = f.subs({x: t*a, y: t*b})/t
    general = sp.limit(quotient, t, 0, dir="+")
    partials = [(sp.limit(f.subs({x: s if axis == 0 else 0, y: s if axis == 1 else 0})/s, s, 0, dir="+"),
                 sp.limit(f.subs({x: s if axis == 0 else 0, y: s if axis == 1 else 0})/s, s, 0, dir="-"))
                for axis in (0, 1)]
    forward = general.subs({a: 1, b: 0})
    reverse = general.subs({a: -1, b: 0})
    ok("C22-06-A", all(right != left for right, left in partials))
    ok("C22-06-B", sp.simplify(general-sp.Abs(a+b)) == 0)
    ok("C22-06-C", forward == 1 and forward != 0)
    ok("C22-06-D", reverse == 1 and forward != -reverse)

    # C22-07
    p, q = sp.symbols("p q")
    sol = sp.solve([p*p + q*q - 25, 3*p + 4*q], [p, q])
    values = {sp.Matrix(v).dot(sp.Matrix([4, 3])/5) for v in sol}
    ok("C22-07", set(sol) == {(-4, 3), (4, -3)}
       and values == {-sp.Rational(7, 5), sp.Rational(7, 5)})

    # C22-08
    aval = sp.solve(sp.Eq(4 + 2*a + 2, 0), a)[0]
    f = x**2 + aval*y**2 + 2*x*y
    gg = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: 1})
    ok("C22-08", aval == -3 and f.subs({x: 1, y: 1}) == 0 and gg == sp.Matrix([4, -4]) and gg.norm() == 4 * sp.sqrt(2))
    check_lines("C22-08", x, y, (1, 1), gg, x-y, x+y-2)

    # C22-09
    f = 3*x**2 + 2*x*y + y**2
    p1 = sp.Matrix([1 - 8*eta, 1 - 4*eta])
    f1 = sp.expand(f.subs({x: p1[0], y: p1[1]}))
    eta_star = sp.solve(sp.diff(f1, eta), eta)[0]
    roots = sp.solve(sp.Eq(f1, f.subs({x: 1, y: 1})), eta)
    ok("C22-09", f1 == 272*eta**2 - 80*eta + 6 and eta_star == sp.Rational(5, 34) and sp.Rational(5, 17) in roots)
    decrease = sp.solve_univariate_inequality(f1 < 6, eta, relational=False)
    ok("C22-09-严格区间", decrease == sp.Interval.open(0, sp.Rational(5, 17))
       and f1.subs(eta, 0) == 6 and f1.subs(eta, sp.Rational(5, 17)) == 6
       and f1.subs(eta, eta_star) == sp.Rational(2, 17))

    # C22-10 is the requested proof item.
    print("MANUAL C22-10")
    saddle = x*x-y*y
    saddle_grad = sp.Matrix([sp.diff(saddle, x), sp.diff(saddle, y)])
    ok("C22-10-反例", saddle_grad.subs({x: 0, y: 0}) == sp.zeros(2, 1)
       and saddle.subs({x: 0, y: t}) == -t*t and -t*t < 0)

    # C22-11
    z, c = sp.symbols("z c", real=True)
    f = x*x + 2*y*y + z*z
    gg = sp.Matrix([sp.diff(f, v) for v in (x, y, z)]).subs({x: 1, y: 1, z: 1})
    normal = sp.Matrix([1, -1, 0])
    allowed = gg - gg.dot(normal)/normal.dot(normal)*normal
    u = allowed/allowed.norm()
    ok("C22-11-受限", allowed.norm() == sp.sqrt(22)
       and u == sp.Matrix([3, 3, 2])/sp.sqrt(22)
       and u.dot(u) == 1 and u.dot(normal) == 0 and gg.dot(u) == sp.sqrt(22))
    direction = sp.Matrix([a, a, c])
    ok("C22-11-上界", sp.expand((gg-allowed).dot(direction)) == 0
       and sp.expand(allowed.dot(allowed)*direction.dot(direction)-allowed.dot(direction)**2)
       == sp.expand(2*(2*a-3*c)**2))
    ok("C22-11-不受限", gg.norm() == 2*sp.sqrt(6)
       and gg/gg.norm() == sp.Matrix([1, 2, 1])/sp.sqrt(6)
       and gg.norm() > allowed.norm() and gg.dot(normal) != 0)

    # C22-12
    r = sp.Matrix([sp.Symbol("t"), sp.Symbol("t")**2])
    tt = sp.Symbol("t")
    f = x**2 + x*y + y**2
    comp = sp.expand(f.subs({x: tt, y: tt**2}))
    grad = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: 1})
    ok("C22-12", sp.diff(comp, tt).subs(tt, 1) == 9 and grad.dot(sp.Matrix([1, 2]) / sp.sqrt(5)) == 9 / sp.sqrt(5))

    # C22-13
    f = x**2 + x*y + 2*y**2
    f0 = f.subs({x: 1, y: -1})
    f1 = f.subs({x: sp.Rational(101, 100), y: sp.Rational(-102, 100)})
    grad = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: -1})
    linear = grad.dot(sp.Matrix([sp.Rational(1, 100), sp.Rational(-2, 100)]))
    ok("C22-13", linear == sp.Rational(7, 100) and f1 - f0 == sp.Rational(707, 10000) and f1 - f0 - linear == sp.Rational(7, 10000))

    # C22-14
    f = x**2 + x*y + y**2
    grad = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: 1})
    slope = -sp.diff(f, x).subs({x: 1, y: 1}) / sp.diff(f, y).subs({x: 1, y: 1})
    h = x*y+y*y
    hgrad = sp.Matrix([sp.diff(h, x), sp.diff(h, y)]).subs({x: 1, y: 1})
    tangent = sp.Matrix([1, slope])
    ok("C22-14", f.subs({x: 1, y: 1}) == 3 and slope == -1
       and grad.dot(tangent) == 0 and hgrad.dot(tangent) == -2
       and sp.simplify(hgrad.dot(tangent/tangent.norm())) == -sp.sqrt(2))


if __name__ == "__main__":
    main()
