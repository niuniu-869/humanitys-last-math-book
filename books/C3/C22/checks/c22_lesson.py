import sympy as sp


def ok(label, condition):
    print(f"{'PASS' if bool(condition) else 'FAIL'} {label}")


def main():
    x, y, z, a, b = sp.symbols("x y z a b", real=True)

    # 例1 and its follow-up.
    t = sp.symbols("t", positive=True)
    f1 = sp.sqrt((3*t/5)**2 + (4*t/5)**2)
    s = sp.symbols("s", real=True)
    right_q = sp.limit(sp.Abs(s) / s, s, 0, dir="+")
    left_q = sp.limit(sp.Abs(s) / s, s, 0, dir="-")
    ok("例1", sp.simplify(f1 / t) == 1 and right_q == 1 and left_q == -1)
    reverse = sp.sqrt((-3*t/5)**2+(-4*t/5)**2)
    ok("例1-反向", sp.limit(reverse/t, t, 0, dir="+") == 1)
    ok("例1小题", sp.simplify((sp.Abs(3*t/5) + sp.Abs(4*t/5)) / t) == sp.Rational(7, 5))

    # 例2 and its follow-up.
    f2 = (1 + t*a)**2 * (2 + t*b)
    coeff = sp.expand(f2).coeff(t, 1)
    ok("例2", coeff == 4*a + b)
    ok("例2-定义极限", sp.limit((f2-2)/t, t, 0, dir="+") == 4*a+b)

    # Check the counterexamples directly along lines and the curved path.
    rational = x*x*y/(x*x+y*y)
    quotient = rational.subs({x: t*a, y: t*b})/t
    ok("反例-方向公式", sp.simplify(quotient-a*a*b/(a*a+b*b)) == 0
       and sp.simplify(quotient.subs({a: 1/sp.sqrt(2), b: 1/sp.sqrt(2)})) == sp.sqrt(2)/4)
    for name, function in [("偏导存在但不连续", x*y/(x*x+y*y)),
                           ("方向导数存在但不连续", x*x*y/(x**4+y*y)),
                           ("连续但不可微", rational)]:
        ok(f"反例-{name}-偏导", function.subs(y, 0) == 0 and function.subs(x, 0) == 0)
    xy = x*y/(x*x+y*y)
    ok("反例-连续不保证偏导", sp.limit(sp.Abs(s)/s, s, 0, dir="+")
       != sp.limit(sp.Abs(s)/s, s, 0, dir="-") and sp.limit(sp.Abs(s), s, 0) == 0)
    ok("反例-偏导不保证方向导数", sp.limit(xy.subs({x: t/sp.sqrt(2), y: t/sp.sqrt(2)})/t,
       t, 0, dir="+") == sp.oo)
    bn = sp.symbols("bn", real=True, nonzero=True)
    discontinuous = x*x*y/(x**4+y*y)
    ok("反例-各方向存在", sp.limit(discontinuous.subs({x: t*a, y: t*bn})/t,
       t, 0, dir="+") == a*a/bn and discontinuous.subs(y, 0) == 0)
    ok("反例-曲线路径", sp.limit(discontinuous.subs(y, x*x), x, 0) == sp.Rational(1, 2))
    # The continuous bound follows from x^2 <= x^2+y^2.
    ok("反例-连续性上界", sp.expand(x*x+y*y-x*x).is_nonnegative
       and sp.limit(sp.Abs(y), y, 0) == 0)

    # 例3 and its follow-up.
    grad3 = sp.Matrix([sp.exp(y), x*sp.exp(y)]).subs({x: 1, y: 0})
    ok("例3", grad3.dot(sp.Matrix([2, -1]) / sp.sqrt(5)) == 1 / sp.sqrt(5))
    grad3b = sp.Matrix([2*x + 3*y, 3*x]).subs({x: 1, y: 1})
    ok("例3小题", grad3b.dot(sp.Matrix([3, 4]) / 5) == sp.Rational(27, 5))

    # 例4.
    grad4 = sp.Matrix([y**2, 2*x*y, 3*z**2]).subs({x: 1, y: -1, z: 2})
    ok("例4", grad4.dot(sp.Matrix([2, -2, 1]) / 3) == 6)

    # 例5 and its follow-up.
    grad5 = sp.Matrix([2*x, 2*y]).subs({x: 1, y: 2})
    ok("例5", grad5.norm() == 2*sp.sqrt(5) and grad5.dot(sp.Matrix([-2, 1]) / sp.sqrt(5)) == 0)
    grad5b = sp.Matrix([2*x + y, x + 4*y]).subs({x: 1, y: -1})
    ok("例5小题", -grad5b / grad5b.norm() == sp.Matrix([-1, 3]) / sp.sqrt(10))

    # 例6.
    p, q = sp.symbols("p q")
    sol6 = sp.solve([sp.Eq((p + q)/sp.sqrt(2), 2*sp.sqrt(2)), sp.Eq((p-q)/sp.sqrt(2), 0)], [p, q])
    ok("例6", sol6 == {p: 2, q: 2} and sol6[p]*sp.Rational(3, 5) + sol6[q]*sp.Rational(4, 5) == sp.Rational(14, 5))

    # 例7.
    grad7 = sp.Matrix([y*z, x*z, x*y]).subs({x: 1, y: 2, z: 3})
    ok("例7", grad7 == sp.Matrix([6, 3, 2]) and grad7.norm() == 7)

    # 例8 and its follow-up.
    grad8 = sp.Matrix([2*x, 8*y]).subs({x: 2, y: 1})
    tangent8 = sp.Matrix([1, 2]).dot(sp.Matrix([x-2, y-1]))
    ok("例8", grad8 == sp.Matrix([4, 8]) and sp.expand(tangent8 - (x + 2*y - 4)) == 0 and grad8.dot(sp.Matrix([1, -sp.Rational(1, 2)])) == 0)
    grad8b = sp.Matrix([2*x, -2*y]).subs({x: 2, y: 1})
    tangent8b = sp.Matrix([2, -1]).dot(sp.Matrix([x-2, y-1]))
    ok("例8小题", grad8b == sp.Matrix([4, -2]) and sp.expand(tangent8b - (2*x-y-3)) == 0 and grad8b.dot(sp.Matrix([1, 2])) == 0)
    for label, point, grad, tangent, normal in [
        ("例8", (2, 1), grad8, x+2*y-4, 2*x-y-3),
        ("例8小题", (2, 1), grad8b, 2*x-y-3, x+2*y-4),
    ]:
        for kind, line, is_tangent in [("切线", tangent, True), ("法线", normal, False)]:
            direction = sp.Matrix([sp.diff(line, y), -sp.diff(line, x)])
            relation = grad.dot(direction) if is_tangent else sp.det(sp.Matrix.hstack(grad, direction))
            ok(f"{label}-{kind}", line.subs(dict(zip((x, y), point))) == 0
               and direction.norm() != 0 and relation == 0)

    # 例9.
    grad9 = sp.Matrix([2*x, 2*y, 2*z]).subs({x: 1, y: 2, z: 2})
    ok("例9", grad9 == 2*sp.Matrix([1, 2, 2]) and 1**2 + 2**2 + 2**2 == 9)

    # 例10 and its follow-up.
    f10 = x**2 + 4*y**2
    g10 = sp.Matrix([sp.diff(f10, x), sp.diff(f10, y)]).subs({x: 4, y: 1})
    p10 = sp.Matrix([4, 1]) - sp.Rational(1, 10)*g10
    ok("例10", p10 == sp.Matrix([sp.Rational(16, 5), sp.Rational(1, 5)]) and f10.subs({x: p10[0], y: p10[1]}) == sp.Rational(52, 5))
    f10b = 3*x**2 + y**2
    g10b = sp.Matrix([sp.diff(f10b, x), sp.diff(f10b, y)]).subs({x: 1, y: 3})
    p10b = sp.Matrix([1, 3]) - sp.Rational(1, 10)*g10b
    ok("例10小题", p10b == sp.Matrix([sp.Rational(2, 5), sp.Rational(12, 5)]) and f10b.subs({x: p10b[0], y: p10b[1]}) == sp.Rational(156, 25))

    # 例11 convergence interval, sample values, and optimal rate.
    eta = sp.symbols("eta", real=True)
    interval = sp.solve_univariate_inequality(abs(1-2*eta) < 1, eta, relational=False).intersect(
        sp.solve_univariate_inequality(abs(1-8*eta) < 1, eta, relational=False))
    candidates = sp.solve((1-2*eta)**2-(1-8*eta)**2, eta)
    eta_opt, = [value for value in candidates if interval.contains(value)]
    def loss_after(k, e):
        return sp.expand((1-2*e)**(2*k) * 16 + 4*(1-8*e)**(2*k))
    vals = [float(loss_after(5, e)) for e in [sp.Rational(1, 100), sp.Rational(1, 10), sp.Rational(1, 5), sp.Rational(1, 4), sp.Rational(3, 10)]]
    ok("例11", interval == sp.Interval.open(0, sp.Rational(1, 4))
       and abs(vals[0] - 14.8) < 0.05
       and abs(vals[1] - 1.72) < 0.01
       and abs(vals[2] - 0.12) < 0.01
       and abs(vals[3] - 4.02) < 0.01
       and abs(vals[4] - 115.7) < 0.1
       and eta_opt == sp.Rational(1, 5)
       and abs(1-2*eta_opt) == abs(1-8*eta_opt))
    left = sp.Interval.open(0, eta_opt)
    right = sp.Interval.open(eta_opt, sp.Rational(1, 4))
    dominance = (1-2*eta)**2-(1-8*eta)**2
    ok("例11-最优分段", left.is_subset(sp.solve_univariate_inequality(dominance > 0, eta, relational=False))
       and right.is_subset(sp.solve_univariate_inequality(dominance < 0, eta, relational=False))
       and sp.diff(1-2*eta, eta) < 0 and sp.diff(8*eta-1, eta) > 0)
    k = sp.symbols("k", integer=True, nonnegative=True)
    boundary_loss = loss_after(k, sp.Rational(1, 4))
    ok("例11-端点", sp.simplify(boundary_loss - (4+16*sp.Rational(1, 4)**k)) == 0
       and sp.limit(boundary_loss, k, sp.oo) == 4
       and sp.limit((-1)**(2*k), k, sp.oo) == 1
       and sp.limit((-1)**(2*k+1), k, sp.oo) == -1)
    squared_distance = 16*(1-2*eta_opt)**(2*k)+(1-8*eta_opt)**(2*k)
    ok("例11-距离与损失比", sp.simplify(squared_distance.subs(k, k+1)/squared_distance) == sp.Rational(9, 25)
       and sp.sqrt(sp.Rational(9, 25)) == sp.Rational(3, 5)
       and sp.simplify(loss_after(k+1, eta_opt)/loss_after(k, eta_opt)) == sp.Rational(9, 25))


if __name__ == "__main__":
    main()
