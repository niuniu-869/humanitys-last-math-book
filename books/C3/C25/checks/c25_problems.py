"""用符号计算独立验算 C.25 题目。"""
import sympy as s

x, y, r, t = s.symbols("x y r t", real=True)


def ok(label, condition):
    print(f"{'PASS' if bool(condition) else 'FAIL'} {label}")


def main():
    # C25-01: 直接用极坐标算两个积分，再比较。
    I = s.integrate(2 * s.pi * r**3, (r, 0, 1))
    K = s.integrate(2 * s.pi * r**2, (r, 0, 1))
    ok("C25-01-A", not (I > K))
    ok("C25-01-B", I < K)
    ok("C25-01-C", not (I == K))
    ok("C25-01-D", s.simplify(K - I).is_positive)

    # C25-02
    f_center = 1**2 + 1 * (-2) + (-2)**2
    ok("C25-02", f_center == 3)

    # C25-03
    value = s.integrate(x, (x, 0, 1)) * s.integrate(s.sin(y), (y, 0, s.pi))
    ok("C25-03", value == 1)

    # C25-04
    inner = s.integrate(x + 2 * y, (y, x, 2 - x))
    ok("C25-04-内层", s.expand(inner - (4 - 2 * x - 2 * x**2)) == 0)
    value = s.integrate(inner, (x, 0, 1))
    ok("C25-04", s.simplify(value - s.Rational(7, 3)) == 0)

    # C25-05: 用 f=1 比较原区域和四个候选区域的面积。
    original = s.integrate(2 - x - x**2, (x, 0, 1))
    lower_part = s.integrate(s.sqrt(y), (y, 0, 1))
    upper_part = s.integrate(2 - y, (y, 1, 2))
    candidates = [
        lower_part,
        lower_part + upper_part,
        s.integrate(y**2, (y, 0, 1)) + upper_part,
        upper_part,
    ]
    for letter, area in zip("ABCD", candidates):
        ok(f"C25-05-{letter}", (area == original) == (letter == "B"))

    # sqrt(y)<=2-y 在 0<=y<=2 上等价于 y<=(2-y)^2。
    first_range = s.reduce_inequalities([y >= 0, y <= 2, y <= (2 - y)**2], y)
    ok("C25-05-分界", first_range.as_set() == s.Interval(0, 1))
    for f in (x, y, x * y):
        before = s.integrate(f, (y, x**2, 2 - x), (x, 0, 1))
        after = (s.integrate(f, (x, 0, s.sqrt(y)), (y, 0, 1))
                 + s.integrate(f, (x, 0, 2 - y), (y, 1, 2)))
        ok(f"C25-05-换序-{f}", s.simplify(before - after) == 0)

    # C25-06: 直接在题给平行四边形上积分，不预设奇函数积分为零。
    for letter, f in zip("ABCD", [x + y - 2, x, x * y, x**2]):
        value = s.integrate(f, (y, x - 1, x + 1), (x, 0, 2))
        ok(f"C25-06-{letter}", (value == 0) == (letter == "A"))
        if letter == "C":
            ok("C25-06-C-数值", value == s.Rational(16, 3))

    # C25-07: 由 y>=|x| 的两条射线和半径平方约束恢复区域。
    theta_lo, theta_hi = s.atan(1), s.pi - s.atan(1)
    correct = s.integrate(r**2, (r, s.sqrt(1), s.sqrt(9)), (t, theta_lo, theta_hi))
    bounds = [(0, 3, s.pi / 4, 3 * s.pi / 4),
              (1, 9, s.pi / 4, 3 * s.pi / 4),
              (1, 3, s.pi / 4, 3 * s.pi / 4),
              (1, 3, 0, s.pi)]
    for letter, (lo, hi, start, end) in zip("ABCD", bounds):
        candidate = s.integrate(r**2, (r, lo, hi), (t, start, end))
        ok(f"C25-07-{letter}", (s.simplify(candidate - correct) == 0) == (letter == "C"))

    # C25-08
    u, v = s.symbols("u v", real=True)
    inverse = s.solve([2 * x + y - u, x - y - v], [x, y])
    jac = s.Matrix([inverse[x], inverse[y]]).jacobian([u, v]).det()
    f = (2 * x + y) * (x - y)
    transformed = s.expand(f.subs(inverse))
    value = s.integrate(transformed * s.Abs(jac), (u, 0, 2), (v, 0, 1))
    direct = (s.integrate(f, (y, -2 * x, x), (x, 0, s.Rational(1, 3)))
              + s.integrate(f, (y, x - 1, x), (x, s.Rational(1, 3), s.Rational(2, 3)))
              + s.integrate(f, (y, x - 1, 2 - 2 * x), (x, s.Rational(2, 3), 1)))
    ok("C25-08-J", jac == -s.Rational(1, 3))
    ok("C25-08-被积函数", transformed == u * v)
    ok("C25-08-积分", value == direct == s.Rational(1, 3))

    # C25-09: q>0 覆盖 p>1 与 p<1 的全部参数，另验临界点。
    p = s.symbols("p", real=True)
    q = s.symbols("q", positive=True)
    R = s.symbols("R", positive=True)
    primitive = s.pi * (r**(2 - 2 * p) - 1) / (1 - p)
    ok("C25-09-原函数", s.simplify(s.diff(primitive, r) - 2 * s.pi * r**(1 - 2 * p)) == 0)
    finite = primitive.subs(r, R)
    ok("C25-09-p>1", s.limit(finite.subs(p, 1 + q), R, s.oo) == s.pi / q)
    ok("C25-09-p<1", s.limit(finite.subs(p, 1 - q), R, s.oo) == s.oo)
    critical = s.integrate(2 * s.pi / r, (r, 1, R))
    ok("C25-09-p=1", s.limit(critical, R, s.oo) == s.oo)
    value = s.integrate(2 * s.pi * r**-2, (r, 1, s.oo))
    ok("C25-09-p=3/2", value == 2 * s.pi)

    # C25-10
    phi_prime = s.integrate(x * s.exp(t * x), (x, 0, t)) + s.exp(t**2)
    ok("C25-10", s.simplify(phi_prime.subs(t, 1) - (s.E + 1)) == 0)
    explicit_phi = s.integrate(s.exp(t * x), (x, 0, t))
    ok("C25-10-直接求导", s.simplify(s.diff(explicit_phi, t).subs(t, 1) - (s.E + 1)) == 0)
    ok("C25-10-分部积分", s.integrate(x * s.exp(x), (x, 0, 1)) == 1)

    # C25-11 is a proof item.
    print("MANUAL C25-11")

    # C25-12
    first = s.integrate(r**3, (r, 1, 1 / s.cos(t)), (t, 0, s.pi / 4))
    second = s.integrate(r**3, (r, 1, 1 / s.sin(t)), (t, s.pi / 4, s.pi / 2))
    # 独立路径：正方形积分减去四分之一圆盘积分。
    square = s.integrate(x**2 + y**2, (x, 0, 1), (y, 0, 1))
    quarter_disk = s.integrate(r**3, (r, 0, 1), (t, 0, s.pi / 2))
    expected = s.Rational(2, 3) - s.pi / 8
    ok("C25-12-两段相等", s.simplify(first - second) == 0)
    ok("C25-12", s.simplify(first + second - expected) == 0)
    ok("C25-12-独立路径", s.simplify(first + second - (square - quarter_disk)) == 0)

    # C25-13: constrained extrema of x+y on the unit disk.
    lam = s.symbols("lam", real=True)
    sols = s.solve([1 - 2 * lam * x, 1 - 2 * lam * y, x**2 + y**2 - 1], [x, y, lam], dict=True)
    vals = sorted({s.simplify(sol[x] + sol[y]) for sol in sols})
    ok("C25-13", vals == [-s.sqrt(2), s.sqrt(2)])
    actual_I = s.integrate(s.integrate((3 + r * s.cos(t) + r * s.sin(t)) * r,
                                       (r, 0, 1)), (t, 0, 2 * s.pi))
    lower, upper = s.pi * (3 - s.sqrt(2)), s.pi * (3 + s.sqrt(2))
    ok("C25-13-下界", lower <= actual_I)
    ok("C25-13-上界", actual_I <= upper)

    # C25-14
    ok("C25-14", s.limit(s.sin(t) / t, t, 0) == 1)

    # C25-15
    volume = s.integrate(s.integrate((1 - r**2) * r, (r, 0, 1)), (t, 0, 2 * s.pi))
    ok("C25-15", volume == s.pi / 2)


if __name__ == "__main__":
    main()
