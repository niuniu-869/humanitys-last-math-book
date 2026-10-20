"""Recompute the exercises and every choice with SymPy.

Expected expressions are transcribed from answers.md; actual expressions are
obtained from the stated curves and integrands. Choice keys are read from the
answer text so that a changed key cannot silently pass.
"""

from pathlib import Path
import re
import sys

import sympy as sp
import mpmath as mp


x, y, t, r, v = sp.symbols("x y t r v", real=True)
ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
failed = 0


def equal(actual, expected):
    return sp.simplify(actual - expected) == 0


def report(pid, ok, detail=""):
    global failed
    ok = bool(ok)
    failed += int(not ok)
    print(f"{'PASS' if ok else 'FAIL'} {pid}" + (f" {detail}" if detail else ""))


def line_integral(p, q, xt, yt, lo, hi):
    integrand = p.subs({x: xt, y: yt}, simultaneous=True) * sp.diff(xt, t)
    integrand += q.subs({x: xt, y: yt}, simultaneous=True) * sp.diff(yt, t)
    return sp.integrate(sp.simplify(integrand), (t, lo, hi))


def choices(pid, truth):
    match = re.search(rf"\*\*{pid}\*\*\s*\*\*答案：\*\*\s*\(([A-D])\)", ANSWERS)
    if not match:
        report(pid, False, "answer key missing")
        return
    key = match[1]
    for letter, result in zip("ABCD", truth):
        report(pid, bool(result) == (letter == key), f"({letter}) truth={bool(result)}")
    selected = [letter for letter, result in zip("ABCD", truth) if result]
    report(pid, selected == [key], f"computed choice={','.join(selected)}")


def problem01():
    xt, yt = 1 - t, 2 - 2 * t
    speed = sp.sqrt(sp.diff(xt, t) ** 2 + sp.diff(yt, t) ** 2)
    first = sp.integrate(speed, (t, 0, 1))
    second = line_integral(sp.Integer(1), sp.Integer(2), xt, yt, 0, 1)
    options = [(-sp.sqrt(5), -5), (sp.sqrt(5), -5), (sp.sqrt(5), 5), (1, -5)]
    choices("C27-01", [equal(first, a) and equal(second, b) for a, b in options])


def problem02():
    xt, yt = sp.cos(t), sp.sin(t)
    speed = sp.sqrt(sp.trigsimp(sp.diff(xt, t) ** 2 + sp.diff(yt, t) ** 2))
    first = sp.integrate(xt * speed, (t, 0, 2 * sp.pi))
    second = line_integral(sp.Integer(0), x, xt, yt, 0, 2 * sp.pi)
    options = [(0, 0), (0, -sp.pi), (4, sp.pi), (0, sp.pi)]
    choices("C27-02", [equal(first, a) and equal(second, b) for a, b in options])
    report("C27-02", equal(sp.integrate(sp.Abs(xt) * speed, (t, 0, 2 * sp.pi)), 4),
           "absolute-value distractor")


def problem03():
    lam = sp.symbols("lambda", real=True)
    p, q = 2 * x * y + 1, lam * x ** 2 + 2 * y
    condition = sp.solve(sp.Poly(sp.diff(q, x) - sp.diff(p, y), x).coeffs(), lam)
    first = (line_integral(p, q, t, sp.Integer(0), 0, 1)
             + line_integral(p, q, sp.Integer(1), t, 0, 1))
    second = (line_integral(p, q, sp.Integer(0), t, 0, 1)
              + line_integral(p, q, t, sp.Integer(1), 0, 1))
    q = q.subs(lam, 1)
    partial = sp.integrate(p, x)
    h = sp.integrate(q - sp.diff(partial, y), y)
    potential = partial + h
    endpoints = potential.subs({x: 1, y: 1}) - potential.subs({x: 0, y: 0})
    report("C27-03", all([
        condition == {lam: 1}, equal(first, lam + 2), equal(second, 3),
        equal(first - second, lam - 1),
        equal(h, y ** 2), equal(potential, x ** 2 * y + x + y ** 2),
        equal(sp.diff(potential, x), p), equal(sp.diff(potential, y), q),
        equal(endpoints, 3), equal(first.subs(lam, 1), endpoints),
    ]), f"condition={condition}; I1={first}; I2={second}; u={potential}")


def problem04():
    p, q = -3 * x ** 2, 2 * y
    partial = sp.integrate(p, x)
    potential = partial + sp.integrate(q - sp.diff(partial, y), y)
    constant = potential.subs({x: 0, y: 1})
    roots = sp.solve(potential - constant, y)
    selected = [root for root in roots if equal(root.subs(x, 0), 1)]
    valid = len(selected) == 1
    if valid:
        sol = selected[0]
        valid = equal(sol, sp.sqrt(x ** 3 + 1))
        valid = valid and equal(p + q.subs(y, sol) * sp.diff(sol, x), 0)
        interval = sp.solve_univariate_inequality(x ** 3 + 1 > 0, x, relational=False)
        valid = valid and interval == sp.Interval.open(-1, sp.oo)
        valid = valid and sp.limit(sp.diff(sol, x), x, -1, dir="+") == sp.oo
    slope = sp.symbols("slope", real=True)
    endpoint_residual = (p + q * slope).subs({x: -1, y: 0})
    report("C27-04", valid and equal(potential, y ** 2 - x ** 3)
           and equal(constant, 1) and equal(endpoint_residual, -3),
           f"u={potential}; branch={selected}; endpoint residual={endpoint_residual}")


def problem05():
    p, q = -y, x
    outer = line_integral(p, q, 2 * sp.cos(t), 2 * sp.sin(t), 0, 2 * sp.pi)
    inner = line_integral(p, q, sp.cos(t), -sp.sin(t), 0, 2 * sp.pi)
    curl = sp.diff(q, x) - sp.diff(p, y)
    area_integral = sp.integrate(curl * r, (r, 1, 2), (t, 0, 2 * sp.pi))
    report("C27-05", equal(outer, 8 * sp.pi) and equal(inner, -2 * sp.pi)
           and equal(outer + inner, 6 * sp.pi) and equal(area_integral, outer + inner),
           f"outer={outer}; inner={inner}; total={area_integral}")


def problem06():
    p = -y / ((x + 1) ** 2 + y ** 2) + 2 * y / ((x - 1) ** 2 + y ** 2)
    q = (x + 1) / ((x + 1) ** 2 + y ** 2) - 2 * (x - 1) / ((x - 1) ** 2 + y ** 2)
    curl = sp.simplify(sp.diff(q, x) - sp.diff(p, y))
    half = sp.Rational(1, 2)
    rectangle = [(-2, -1), (2, -1), (2, 1), (-2, 1)]
    diamond = [(1 + half, 0), (1, -half), (1 - half, 0), (1, half)]

    def polygon(vertices):
        value, area = mp.mpf(0), sp.Integer(0)
        regular = True
        for start, end in zip(vertices, vertices[1:] + vertices[:1]):
            xt = start[0] + t * (end[0] - start[0])
            yt = start[1] + t * (end[1] - start[1])
            integrand = (p.subs({x: xt, y: yt}, simultaneous=True) * sp.diff(xt, t)
                         + q.subs({x: xt, y: yt}, simultaneous=True) * sp.diff(yt, t))
            value += mp.quad(sp.lambdify(t, integrand, "mpmath"), [0, 0.5, 1])
            area += start[0] * end[1] - end[0] * start[1]
            for a in (-1, 1):
                zeros = sp.solveset((xt - a) ** 2 + yt ** 2, t, domain=sp.Interval(0, 1))
                regular = regular and zeros == sp.EmptySet
        return value, area / 2, regular

    mp.mp.dps = 40
    first, area1, exists1 = polygon(rectangle)
    second, area2, exists2 = polygon(diamond)
    close = lambda a, b: abs(a - b) < mp.mpf("1e-25")
    # Radius 1/4 disks are disjoint and strictly inside the stated polygons.
    radius = sp.Rational(1, 4)
    holes_valid = radius < 1 and 2 * radius < 2 and sp.sqrt(2) * radius < half
    truth = [
        equal(curl, 0) and close(first, 0) and close(second, 0),
        close(first, -2 * mp.pi) and close(second, -4 * mp.pi),
        close(first, -2 * mp.pi) and close(second, 4 * mp.pi) and holes_valid,
        not exists1 and not exists2,
    ]
    choices("C27-06", truth)
    report("C27-06", equal(curl, 0) and exists1 and exists2 and area1 > 0 and area2 < 0
           and truth[2], f"polygon quadrature I1={first}; I2={second}; signed areas={area1},{area2}")


def problem07():
    print("MANUAL C27-07 general triangle proof: check three edges and both integration orders")
    p, q = x * y + y ** 2 + 1, x ** 2 + x * y + 2
    edges = [line_integral(p, q, t, sp.Integer(0), 0, 1),
             line_integral(p, q, 1 - t, t, 0, 1),
             line_integral(p, q, sp.Integer(0), 1 - t, 0, 1)]
    double = (sp.integrate(sp.diff(q, x), (x, 0, 1 - y), (y, 0, 1))
              - sp.integrate(sp.diff(p, y), (y, 0, 1 - x), (x, 0, 1)))
    report("C27-07", equal(sum(edges), double) and equal(double, 0)
           and all(equal(a, b) for a, b in zip(edges, [1, 1, -2])),
           f"polynomial spot check only; edges={edges}; double={double}")


def problem08():
    p, q = sp.Integer(1), x ** 2 * y ** 2 + 2
    direct = line_integral(p, q, sp.cos(t), sp.sin(t), 0, sp.pi / 2)
    vertical = line_integral(p, q, sp.Integer(0), t, 1, 0)
    horizontal = line_integral(p, q, t, sp.Integer(0), 0, 1)
    closing = vertical + horizontal
    curl = sp.diff(q, x) - sp.diff(p, y)
    double = sp.integrate(curl, (y, 0, sp.sqrt(1 - x ** 2)), (x, 0, 1))
    swapped = sp.integrate(curl, (x, 0, sp.sqrt(1 - y ** 2)), (y, 0, 1))
    signed_area = line_integral(-y, x, sp.cos(t), sp.sin(t), 0, sp.pi / 2) / 2
    report("C27-08", all([
        equal(direct, sp.Rational(17, 15)), equal(vertical, -2), equal(horizontal, 1),
        equal(double, sp.Rational(2, 15)), equal(swapped, double),
        equal(direct + closing, double), equal(signed_area, sp.pi / 4),
    ]), f"direct={direct}; closing={closing}; double={double}; signed area={signed_area}")


if __name__ == "__main__":
    for number, check in [(1, problem01), (2, problem02), (3, problem03),
                          (4, problem04), (5, problem05), (6, problem06),
                          (7, problem07), (8, problem08)]:
        try:
            check()
        except Exception as exc:
            report(f"C27-{number:02d}", False, f"{type(exc).__name__}: {exc}")
    sys.exit(1 if failed else 0)
