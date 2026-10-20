"""独立核对 lesson.md 中例 1--20 的数值与结论。"""
from __future__ import annotations

import sympy as sp


x, y, z, k, a, b, lam, t = sp.symbols("x y z k a b lam t", real=True)


def report(n: int, ok: bool) -> None:
    print(("PASS " if ok else "FAIL ") + f"例{n}")


def main() -> None:
    # 例 1
    f1 = x**3 + y**3 - 3 * x * y
    sol1 = sp.solve([sp.diff(f1, x), sp.diff(f1, y)], [x, y], dict=True)
    saddle1 = f1.subs({x: sp.Rational(1, 10), y: sp.Rational(1, 10)}) < 0
    saddle1 = saddle1 and f1.subs({x: sp.Rational(1, 10), y: -sp.Rational(1, 10)}) > 0
    report(1, sol1 == [{x: 0, y: 0}, {x: 1, y: 1}] and saddle1)

    # 例 2
    f2 = x * sp.exp(-(x**2 + y**2))
    eq2 = [(1 - 2 * x**2), -2 * x * y]
    sol2 = sp.solve(eq2, [x, y], dict=True)
    points2 = {(sp.simplify(sv[x]), sp.simplify(sv[y])) for sv in sol2}
    expected2 = {(sp.sqrt(2) / 2, 0), (-sp.sqrt(2) / 2, 0)}
    vals2 = {sp.simplify(f2.subs({x: px, y: py})) for px, py in expected2}
    report(2, points2 == expected2 and vals2 == {1 / sp.sqrt(2 * sp.E), -1 / sp.sqrt(2 * sp.E)})

    # 例 3
    f3 = sp.exp(x) * sp.cos(y)
    base3 = {x: 0, y: 0}
    coeff3 = [
        f3.subs(base3),
        sp.diff(f3, x).subs(base3),
        sp.diff(f3, y).subs(base3),
        sp.diff(f3, x, 2).subs(base3),
        sp.diff(f3, x, y).subs(base3),
        sp.diff(f3, y, 2).subs(base3),
    ]
    approx3 = 1 + sp.Rational(1, 5) + sp.Rational(1, 2) * (sp.Rational(1, 25) - sp.Rational(1, 100))
    report(3, coeff3 == [1, 1, 0, 1, 0, -1] and approx3 == sp.Rational(243, 200))

    # 例 4
    approx4 = 1 + sp.Rational(2, 100) + sp.Rational(2, 100) * sp.Rational(3, 100)
    true4 = sp.Rational(102, 100) ** sp.Rational(103, 100)
    report(4, approx4 == sp.Rational(5103, 5000) and abs(float(true4 - approx4)) < 1e-4)

    # 例 5
    f5 = f1
    A5 = sp.diff(f5, x, 2)
    B5 = sp.diff(f5, x, y)
    C5 = sp.diff(f5, y, 2)
    d11 = (A5 * C5 - B5**2).subs({x: 1, y: 1})
    d00 = (A5 * C5 - B5**2).subs({x: 0, y: 0})
    report(5, d11 == 27 and A5.subs({x: 1, y: 1}) > 0 and d00 == -9)

    # 例 6
    f6 = x**2 + k * x * y + y**2
    delta6 = sp.diff(f6, x, 2) * sp.diff(f6, y, 2) - sp.diff(f6, x, y) ** 2
    p6 = sp.solve_univariate_inequality(delta6 > 0, k)
    report(6, sp.simplify_logic(sp.Equivalent(p6, sp.And(k > -2, k < 2))) is sp.true and sp.simplify(f6.subs(k, 2) - (x + y) ** 2) == 0 and sp.simplify(f6.subs(k, -2) - (x - y) ** 2) == 0)

    # 例 7
    eta = sp.symbols("eta", real=True)
    converges = sp.And(abs(1 - eta) < 1, abs(1 - 10 * eta) < 1)
    report(7, sp.simplify(converges) == sp.And(eta > 0, eta < sp.Rational(1, 5)))

    # 例 8
    f8 = x * y * (1 - x - y)
    sol8 = sp.solve([sp.diff(f8, x), sp.diff(f8, y)], [x, y], dict=True)
    pts8 = {(sv[x], sv[y]) for sv in sol8}
    h8 = sp.hessian(f8, (x, y))
    p8 = (sp.Rational(1, 3), sp.Rational(1, 3)) in pts8
    p8 = p8 and sp.simplify((h8.det()).subs({x: sp.Rational(1, 3), y: sp.Rational(1, 3)})) == sp.Rational(1, 3)
    p8 = p8 and f8.subs({x: sp.Rational(1, 3), y: sp.Rational(1, 3)}) == sp.Rational(1, 27)
    report(8, pts8 == {(0, 0), (1, 0), (0, 1), (sp.Rational(1, 3), sp.Rational(1, 3))} and p8)

    # 例 9
    f9 = x**4 + y**4 - 2 * (x - y) ** 2
    points9 = [(0, 0), (sp.sqrt(2), -sp.sqrt(2)), (-sp.sqrt(2), sp.sqrt(2))]
    stationary9 = all(
        all(sp.diff(f9, v).subs({x: px, y: py}) == 0 for v in (x, y))
        for px, py in points9
    )
    values9 = [sp.simplify(f9.subs({x: px, y: py})) for px, py in points9]
    path_pos = f9.subs({x: t, y: t}) == 2 * t**4
    path_neg = sp.expand(f9.subs({x: t, y: -t})) == 2 * t**4 - 8 * t**2
    report(9, stationary9 and values9 == [0, -8, -8] and path_pos and path_neg)

    # 例 10
    f10 = x**2 - 2 * x * y + 2 * y
    vals10 = {
        (1, 1): f10.subs({x: 1, y: 1}),
        (0, 0): f10.subs({x: 0, y: 0}),
        (0, 2): f10.subs({x: 0, y: 2}),
        (3, 0): f10.subs({x: 3, y: 0}),
        (3, 2): f10.subs({x: 3, y: 2}),
        (2, 2): f10.subs({x: 2, y: 2}),
    }
    report(10, vals10[(3, 0)] == 9 and vals10[(0, 0)] == vals10[(2, 2)] == 0 and min(vals10.values()) == 0 and max(vals10.values()) == 9)

    # 例 11
    xs11, ys11 = [1, 2, 3, 4], [2, 3, 5, 6]
    eq11 = [
        sum((a * xx + b - yy) * xx for xx, yy in zip(xs11, ys11)),
        sum(a * xx + b - yy for xx, yy in zip(xs11, ys11)),
    ]
    sol11 = sp.solve(eq11, [a, b], dict=True)[0]
    s11 = sp.simplify(sum((sol11[a] * xx + sol11[b] - yy) ** 2 for xx, yy in zip(xs11, ys11)))
    report(11, sol11 == {a: sp.Rational(7, 5), b: sp.Rational(1, 2)} and s11 == sp.Rational(1, 5))

    # 例 12
    area = x * (10 - x)
    report(12, sp.solve(sp.diff(area, x), x) == [5] and area.subs(x, 5) == 25)

    # 例 13
    sol13 = sp.solve([2 * x - lam, 2 * y - lam, x + y - 2], [x, y, lam], dict=True)[0]
    report(13, sol13 == {x: 1, y: 1, lam: 2} and (x**2 + y**2).subs(sol13) == 2)

    # 例 14
    f14 = 2 * x**2 + 2 * x * y + 2 * y**2
    vals14 = [sp.simplify(f14.subs({x: 1 / sp.sqrt(2), y: 1 / sp.sqrt(2)})), sp.simplify(f14.subs({x: 1 / sp.sqrt(2), y: -1 / sp.sqrt(2)}))]
    report(14, vals14 == [3, 1])

    # 例 15
    f15 = x**2 * y
    pts15 = [(0, sp.sqrt(3)), (0, -sp.sqrt(3)), (sp.sqrt(2), 1), (-sp.sqrt(2), 1), (sp.sqrt(2), -1), (-sp.sqrt(2), -1)]
    vals15 = [sp.simplify(f15.subs({x: px, y: py})) for px, py in pts15]
    report(15, set(vals15) == {0, 2, -2} and max(vals15) == 2 and min(vals15) == -2)

    # 例 16
    f16 = (x - 1) ** 2 + y**2
    near = sp.simplify(f16.subs({x: sp.Rational(4, 3), y: sp.sqrt(5) / 3}))
    far = f16.subs({x: -2, y: 0})
    report(16, near == sp.Rational(2, 3) and far == 9 and sp.sqrt(near) == sp.sqrt(sp.Rational(2, 3)))

    # 例 17
    v17 = sp.Matrix([1, 2, 3])
    report(17, v17.dot(v17) == 14 and v17.dot(v17) == 14 and (-v17).dot(-v17) == 14)

    # 例 18
    zvals18 = [1 - sp.sqrt(2), 1 + sp.sqrt(2)]
    report(18, max(zvals18) == 1 + sp.sqrt(2) and min(zvals18) == 1 - sp.sqrt(2))

    # 例 19
    x19, y19 = sp.Rational(20), sp.Rational(5)
    report(19, 2 * x19 + 8 * y19 == 80 and sp.sqrt(x19 * y19) == 10 and sp.Rational(1, 8) == sp.diff(sp.sqrt(sp.Symbol("c") ** 2 / 64), sp.Symbol("c")).subs(sp.Symbol("c"), 80))

    # 例 20
    g20 = x * y + 2 * y * z + 2 * x * z
    sol20 = {x: 2, y: 2, z: 1}
    report(20, g20.subs(sol20) == 12 and (x * y * z).subs(sol20) == 4)


if __name__ == "__main__":
    main()
