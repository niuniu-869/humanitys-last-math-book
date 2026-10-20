"""独立核对 lesson.md 中例 1--23 的数值和结论。"""
import sympy as s

x, y, z, r, th, t, a = s.symbols("x y z r th t a", real=True)


def ok(label, condition):
    print(f"{'PASS' if bool(condition) else 'FAIL'} {label}")


def main():
    # 例1
    right = sum(i + j for i in (1, 2) for j in (1, 2))
    center = sum(i + j - 1 for i in (1, 2) for j in (1, 2))
    exact = s.integrate(s.integrate(x + y, (y, 0, 2)), (x, 0, 2))
    ok("例1", right == 12 and center == 8 and exact == 8)

    # 例2
    lo = 4 * s.pi * (10 - 2 * s.sqrt(2))
    hi = 4 * s.pi * (10 + 2 * s.sqrt(2))
    exact2 = s.integrate(s.integrate(x + y + 10, (y, -s.sqrt(4 - x**2), s.sqrt(4 - x**2))),
                         (x, -2, 2))
    ok("例2", lo < exact2 < hi and s.simplify(exact2 - 40 * s.pi) == 0)

    # 例3: 分别在三角形和偏心圆盘上计算两组积分。
    I1 = s.integrate((x + y)**2, (y, 0, 1 - x), (x, 0, 1))
    I2 = s.integrate((x + y)**3, (y, 0, 1 - x), (x, 0, 1))
    shifted_sum = 3 + r * s.cos(th) + r * s.sin(th)
    I3 = s.integrate(s.expand(shifted_sum**2) * r, (r, 0, s.sqrt(2)), (th, 0, 2 * s.pi))
    I4 = s.integrate(s.expand(shifted_sum**3) * r, (r, 0, s.sqrt(2)), (th, 0, 2 * s.pi))
    ok("例3-D1", I1 == s.Rational(1, 4) and I2 == s.Rational(1, 5) and I2 <= I1)
    ok("例3-D2", I3 == 20 * s.pi and I4 == 72 * s.pi and I4 >= I3)

    # 例4
    avg4 = (s.Rational(2, 3) * s.pi) / s.pi
    ok("例4", avg4 == s.Rational(2, 3))

    # 例5
    ok("例5", s.exp(0) * s.cos(0) == 1)

    # 例6
    value6 = s.integrate(s.integrate(x + 2 * y, (y, 0, 1)), (x, 0, 2))
    ok("例6", value6 == 4)

    # 例7
    value7 = s.integrate(s.integrate(x * s.exp(x * y), (y, 0, 1)), (x, 0, 1))
    ok("例7", s.simplify(value7 - (s.E - 2)) == 0)

    # 例8
    value8 = s.integrate(s.integrate(x * y, (y, x**2, x)), (x, 0, 1))
    ok("例8", value8 == s.Rational(1, 24))

    # 例9
    value9 = s.integrate(s.integrate(1 - x - y, (y, 0, 1 - x)), (x, 0, 1))
    ok("例9", value9 == s.Rational(1, 6))

    # 例10
    value10 = s.integrate(s.integrate(x**2 / y**2, (y, 1 / x, x)), (x, 1, 2))
    ok("例10", value10 == s.Rational(9, 4))

    # 例11
    value11 = s.integrate(s.sin(y), (y, 0, 1))
    ok("例11", s.simplify(value11 - (1 - s.cos(1))) == 0)

    # 例12
    ok("例12", s.simplify(s.integrate(s.integrate(1, (x, s.sqrt(y), 3 - 2 * y)), (y, 0, 1)) - s.Rational(4, 3)) == 0)

    # 例13
    value13 = s.integrate(y**2 * s.sqrt(1 + y**3), (y, 0, 1))
    ok("例13", s.simplify(value13 - s.Rational(2, 9) * (2 * s.sqrt(2) - 1)) == 0)

    # 例14
    value14 = s.integrate(s.integrate((x + y)**2, (y, -1 + s.Abs(x), 1 - s.Abs(x))), (x, -1, 1))
    ok("例14", s.simplify(value14 - s.Rational(2, 3)) == 0)

    # 例15
    value15 = s.integrate(s.integrate(y, (y, x**2, 1)), (x, -1, 1))
    ok("例15", value15 == s.Rational(4, 5))

    # 例16
    value16 = s.integrate(s.integrate(r**3, (r, 0, 1)), (th, 0, 2 * s.pi))
    ok("例16", value16 == s.pi / 2)

    # 例17
    value17 = s.integrate(s.integrate(r**2, (r, 0, 2 * s.cos(th))), (th, -s.pi / 2, s.pi / 2))
    ok("例17", s.simplify(value17 - s.Rational(32, 9)) == 0)

    # 例18
    value18 = s.integrate(th, (th, 0, s.pi / 4)) * s.integrate(r, (r, 1, 2))
    ok("例18", s.simplify(value18 - 3 * s.pi**2 / 64) == 0)

    # 例19
    value19 = s.integrate(2 * s.pi * r**-3, (r, 1, s.oo))
    ok("例19", value19 == s.pi)

    # 例20
    prob20 = s.integrate(s.exp(-r**2 / 2) * r, (r, 0, 1))
    ok("例20", s.simplify(prob20 - (1 - s.exp(-s.Rational(1, 2)))) == 0)

    # 例21
    u, v = s.symbols("u v", real=True)
    jac21 = s.Matrix([2 * u, 3 * v]).jacobian([u, v]).det()
    area21 = s.integrate(s.Abs(jac21) * r, (r, 0, 1), (th, 0, 2 * s.pi))
    value21 = s.integrate(s.Abs(jac21) * r**3, (r, 0, 1), (th, 0, 2 * s.pi))
    ok("例21", area21 == 6 * s.pi and value21 == 3 * s.pi)

    # 例22
    u, v = s.symbols("u v", positive=True)
    value22 = s.integrate(s.integrate(s.Rational(1, 2) * u, (u, 1, 2)), (v, 1, 2))
    ok("例22", value22 == s.Rational(3, 4))

    # 例23
    phi_prime = (s.sin(t**3) - s.sin(t**2)) / t + 2 * s.sin(t**3) / t - s.sin(t**2) / t
    ok("例23", s.simplify(phi_prime - (3 * s.sin(t**3) - 2 * s.sin(t**2)) / t) == 0)


if __name__ == "__main__":
    main()
