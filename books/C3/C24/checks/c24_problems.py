"""独立核对 C.24 习题的确定性答案。"""
from __future__ import annotations

import re
from pathlib import Path

import sympy as sp


x, y, z, k, a, b, lam = sp.symbols("x y z k a b lam", real=True)
ANSWERS = (Path(__file__).resolve().parents[1] / "answers.md").read_text(encoding="utf-8")


def chosen(pid):
    """从 answers.md 读出该题选择的选项字母。"""
    m = re.search(rf"\*\*{pid}\*\*\s*\n\*\*答案：\*\*\s*\(([A-D])\)", ANSWERS)
    return m.group(1) if m else None


def close(u, v, tol=sp.Rational(1, 10**4)):
    return abs(float(sp.N(u - v))) < float(tol)


def report(pid: str, ok: bool) -> None:
    print(("PASS " if ok else "FAIL ") + pid)


def main() -> None:
    # C24-01
    f = 2 * x**2 - 2 * x * y + y**2 - 6 * x + 2 * y
    sol = sp.solve([sp.diff(f, x), sp.diff(f, y)], [x, y], dict=True)
    p = sol == [{x: 2, y: 1}]
    H = sp.hessian(f, (x, y))
    p = p and sp.simplify(H.det().subs({x: 2, y: 1})) > 0 and H[0, 0].subs({x: 2, y: 1}) > 0
    p = p and f.subs({x: 2, y: 1}) == -5
    report("C24-01", p)

    # C24-02：保留正确答案，再按三种错法复算干扰项。
    F = sp.sqrt(x + y)
    base = {x: 1, y: 1}
    h = k2 = sp.Rational(3, 100)
    fx = sp.diff(F, x).subs(base)
    fy = sp.diff(F, y).subs(base)
    fxx = sp.diff(F, x, 2).subs(base)
    fxy = sp.diff(F, x, y).subs(base)
    fyy = sp.diff(F, y, 2).subs(base)
    first = fx * h + fy * k2
    quad = sp.Rational(1, 2) * (fxx * h**2 + 2 * fxy * h * k2 + fyy * k2**2)
    approx = F.subs(base) + first + quad
    expected = sp.sqrt(2) + sp.Rational(3, 100) / sp.sqrt(2) - sp.Rational(9, 10000) / (4 * sp.sqrt(2))
    options = {
        "A": F.subs(base) + first,          # 只用一阶项
        "B": F.subs(base) + first - quad,   # 二阶项符号写反
        "C": approx,                        # 正确
        "D": F.subs(base) + first + 2 * quad,  # 二阶项漏乘 1/2
    }
    rounded = {key: round(float(sp.N(val)), 5) for key, val in options.items()}
    p = sp.simplify(approx - expected) == 0 and close(approx, sp.sqrt(sp.Rational(206, 100)))
    p = p and rounded == {"A": 1.43543, "B": 1.43559, "C": 1.43527, "D": 1.43511}
    ch2 = chosen("C24-02")
    p = p and ch2 == "C" and rounded[ch2] == 1.43527
    report("C24-02", p)

    # C24-03, independently evaluate all four statements.
    q = 2 * x**2 - 4 * x * y + 3 * y**2
    grad0 = [sp.diff(q, v).subs({x: 0, y: 0}) for v in (x, y)]
    A, B, C = [sp.diff(q, v1, v2).subs({x: 0, y: 0}) for v1, v2 in ((x, x), (x, y), (y, y))]
    delta = A * C - B**2
    options = [
        grad0 != [0, 0],
        delta > 0 and A < 0,
        grad0 == [0, 0] and delta > 0 and A > 0,
        B == 0,
    ]
    p = options == [False, False, True, False]
    report("C24-03", p)

    # C24-04
    xs, ys = [0, 1, 2], [1, 2, 4]
    aa, bb = sp.symbols("aa bb")
    eqs = [
        sum((aa * xx + bb - yy) * xx for xx, yy in zip(xs, ys)),
        sum(aa * xx + bb - yy for xx, yy in zip(xs, ys)),
    ]
    ls = sp.solve(eqs, [aa, bb], dict=True)[0]
    S = sp.simplify(sum((ls[aa] * xx + ls[bb] - yy) ** 2 for xx, yy in zip(xs, ys)))
    report("C24-04", ls == {aa: sp.Rational(3, 2), bb: sp.Rational(5, 6)} and S == sp.Rational(1, 6))

    # C24-05
    ft = x**3 - 3 * k * x + y**2
    p = sp.diff(ft, x) == 3 * (x**2 - k) and sp.diff(ft, y) == 2 * y
    p = p and sp.simplify(sp.diff(ft, x, 2).subs(x, sp.sqrt(k))) == 6 * sp.sqrt(k)
    p = p and sp.simplify(sp.diff(ft, x, 2).subs(x, -sp.sqrt(k))) == -6 * sp.sqrt(k)
    p = p and sp.simplify(ft.subs({k: 0, y: 0})) == x**3
    report("C24-05", p)

    # C24-06: compare all edges and the only stationary point.
    f6 = x**2 + y**2 - 4 * x - 2 * y
    stationary = sp.solve([sp.diff(f6, x), sp.diff(f6, y)], [x, y], dict=True)
    # 逐边列出端点和一元驻点，再比较有限个候选值。
    candidates = [(0, 0), (3, 0), (0, 3), (1, 0), (2, 0), (0, 1), (2, 1)]
    vals = [f6.subs({x: xx, y: yy}) for xx, yy in candidates]
    p = stationary == [{x: 2, y: 1}] and min(vals) == -5 and max(vals) == 3
    p = p and f6.subs({x: 2, y: 1}) == -5 and f6.subs({x: 0, y: 3}) == 3
    report("C24-06", p)

    # C24-07
    eq7 = sp.solve([3 * x**2 - 2 * lam * x, -2 * lam * y, x**2 + y**2 - 1], [x, y, lam], dict=True)
    pts7 = {(s[x], s[y]) for s in eq7}
    vals7 = {pt: (x**3).subs({x: pt[0]}) for pt in pts7}
    p = pts7 == {(-1, 0), (1, 0), (0, -1), (0, 1)} and max(vals7.values()) == 1 and min(vals7.values()) == -1
    report("C24-07", p)

    # C24-08
    ca, cb, cc = sp.symbols("ca cb cc")
    data8 = [(0, 0, 1), (1, 0, 2), (0, 1, 3), (1, 1, 5)]
    S8_expr = sum((ca * xx + cb * yy + cc - zz) ** 2 for xx, yy, zz in data8)
    eqs8 = [sp.diff(S8_expr, v) for v in (ca, cb, cc)]
    ls8 = sp.solve(eqs8, [ca, cb, cc], dict=True)[0]
    S8 = sp.simplify(S8_expr.subs(ls8))
    H8 = sp.hessian(S8_expr, (ca, cb, cc))
    p = ls8 == {ca: sp.Rational(3, 2), cb: sp.Rational(5, 2), cc: sp.Rational(3, 4)} and S8 == sp.Rational(1, 4)
    p = p and [H8[:i, :i].det() for i in (1, 2, 3)] == [4, 12, 32]

    # 干扰项按各自的错法解出，再复算误差平方和。
    ls8_no_c = sp.solve([eqs8[0].subs(cc, 0), eqs8[1].subs(cc, 0)], [ca, cb], dict=True)[0]
    S8_no_c = sp.simplify(S8_expr.subs({**ls8_no_c, cc: 0}))
    swap_ab = {ca: cb, cb: ca}
    ls8_swap = sp.solve(
        [eqs8[0].subs(swap_ab, simultaneous=True), eqs8[1].subs(swap_ab, simultaneous=True), eqs8[2]],
        [ca, cb, cc], dict=True
    )[0]
    S8_swap = sp.simplify(S8_expr.subs(ls8_swap))
    eq_c_wrong = sp.expand((eqs8[0] - 2 * cc) / 2)  # 第一个方程中 c 的系数 2 误写成 1
    ls8_c_wrong = sp.solve([eq_c_wrong, eqs8[1], eqs8[2]], [ca, cb, cc], dict=True)[0]
    S8_c_wrong = sp.simplify(S8_expr.subs(ls8_c_wrong))

    p = p and ls8_no_c == {ca: 2, cb: 3} and S8_no_c == 1
    p = p and ls8_swap == {ca: sp.Rational(5, 2), cb: sp.Rational(3, 2), cc: sp.Rational(3, 4)} and S8_swap == sp.Rational(9, 4)
    p = p and ls8_c_wrong == {ca: 2, cb: sp.Rational(5, 2), cc: sp.Rational(1, 2)} and S8_c_wrong == sp.Rational(1, 2)
    ch8 = chosen("C24-08")
    p = p and ch8 == "A" and ls8 == {ca: sp.Rational(3, 2), cb: sp.Rational(5, 2), cc: sp.Rational(3, 4)} and S8 == sp.Rational(1, 4)
    report("C24-08", p)

    # C24-09
    g9 = (y - x**2) ** 2
    grad_g0 = sp.Matrix([sp.diff(g9, x).subs({x: 0, y: 0}), sp.diff(g9, y).subs({x: 0, y: 0})])
    p = grad_g0 == sp.zeros(2, 1) and sp.diff(y, y) == 1 and 0 <= 1
    report("C24-09", p)

    # The proof is checked by hand, as required.
    print("MANUAL C24-10")

    # C24-11: interior multiplier solution and boundary comparison.
    sol11 = sp.solve([y * z - lam, x * z - 2 * lam, x * y - 3 * lam, x + 2 * y + 3 * z - 6], [x, y, z, lam], dict=True)
    interior = any(sv[x] == 2 and sv[y] == 1 and sv[z] == sp.Rational(2, 3) for sv in sol11)
    p = interior and sp.simplify((x * y * z).subs({x: 2, y: 1, z: sp.Rational(2, 3)})) == sp.Rational(4, 3)
    boundary = [sv for sv in sol11 if sv[x] == 0 or sv[y] == 0 or sv[z] == 0]
    p = p and len(boundary) == 3 and all(sp.simplify((x * y * z).subs(sv)) == 0 for sv in boundary)
    report("C24-11", p)

    # C24-12
    t = sp.symbols("t")
    series12 = sp.series(sp.exp(t + 2 * t**2), t, 0, 3).removeO().expand()
    p = series12 == 1 + t + sp.Rational(5, 2) * t**2
    report("C24-12", p)

    # C24-13
    yx = (1 - x) / (1 + x)
    G = x**2 + yx**2
    p = yx.subs(x, 0) == 1 and sp.diff(yx, x).subs(x, 0) == -2 and sp.diff(yx, x, 2).subs(x, 0) == 4
    p = p and sp.series(G, x, 0, 3).removeO().expand() == 1 - 4 * x + 9 * x**2
    report("C24-13", p)

    # C24-14
    grad = sp.Matrix([3, -4])
    p1 = sp.simplify(2 * grad / sp.sqrt(grad.dot(grad)))
    p2 = -p1
    p = grad.dot(p1) == 10 and grad.dot(p2) == -10 and p1 == sp.Matrix([sp.Rational(6, 5), -sp.Rational(8, 5)])
    report("C24-14", p)


if __name__ == "__main__":
    main()
