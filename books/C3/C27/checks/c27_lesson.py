"""Independently check all 11 examples, plus the worked inline exercises.

After example 9 the check also confirms that the level curve x e^y + x^2 - y = 2
cannot serve as a differentiable solution with y(1)=0 (an early-draft erratum).
"""

import sys

import sympy as sp


x, y, t, v = sp.symbols("x y t v", real=True)
a, b, eps = sp.symbols("a b eps", positive=True)
failed = 0


def equal(actual, expected):
    return sp.simplify(actual - expected) == 0


def report(label, ok, detail=""):
    global failed
    ok = bool(ok)
    failed += int(not ok)
    print(f"{'PASS' if ok else 'FAIL'} {label}" + (f" {detail}" if detail else ""))


def check_values(label, pairs):
    report(label, all(equal(actual, expected) for actual, expected in pairs),
           "; ".join(str(actual) for actual, _ in pairs))


def pullback(p, q, xt, yt):
    value = p.subs({x: xt, y: yt}, simultaneous=True) * sp.diff(xt, t)
    value += q.subs({x: xt, y: yt}, simultaneous=True) * sp.diff(yt, t)
    return sp.simplify(value)


def potential(p, q):
    partial = sp.integrate(p, x)
    remainder = sp.simplify(q - sp.diff(partial, y))
    if x in remainder.free_symbols:
        raise ValueError("not an exact differential")
    return partial + sp.integrate(remainder, y)


def example01():
    # x is nonnegative on the stated arc, hence sqrt(y)=x.
    value = sp.integrate(x * sp.sqrt(1 + sp.diff(x ** 2, x) ** 2), (x, 0, 1))
    check_values("例1", [(value, (5 * sp.sqrt(5) - 1) / 12)])


def example02():
    xt, yt = a * sp.cos(t), a * sp.sin(t)
    speed = sp.sqrt(sp.trigsimp(sp.diff(xt, t) ** 2 + sp.diff(yt, t) ** 2))
    value = sp.integrate((xt ** 2 + yt) * speed, (t, 0, 2 * sp.pi))
    odd = sp.integrate(yt * speed, (t, 0, 2 * sp.pi))
    check_values("例2", [(value, sp.pi * a ** 3), (odd, 0)])


def example03():
    pairs = []
    for xt, yt, target in [(t, t, sp.Rational(2, 3)), (t, t ** 2, sp.Rational(3, 4))]:
        pairs.append((sp.integrate(pullback(x * y, x ** 2, xt, yt), (t, 0, 1)), target))
        pairs.append((sp.integrate(pullback(2 * x * y, x ** 2, xt, yt), (t, 0, 1)), 1))
    check_values("例3", pairs)


def example04():
    p, q = sp.exp(x) * sp.sin(y) - y, sp.exp(x) * sp.cos(y) - 1
    xt, yt = a * (1 + sp.cos(t)) / 2, a * sp.sin(t) / 2
    whole = pullback(p, q, xt, yt)
    # Integrate directly along the arc after extracting an exact derivative.
    h = sp.exp(xt) * sp.sin(yt) - yt
    remainder = sp.simplify(whole - sp.diff(h, t))
    result = h.subs(t, sp.pi) - h.subs(t, 0) + sp.integrate(remainder, (t, 0, sp.pi))
    closing = sp.integrate(p.subs({x: t, y: 0}), (t, 0, a))
    check_values("例4", [(result, sp.pi * a ** 2 / 8), (closing, 0),
                          (sp.diff(q, x) - sp.diff(p, y), 1)])


def example05():
    p, q = -y / (x ** 2 + y ** 2), x / (x ** 2 + y ** 2)
    circle = pullback(p, q, eps * sp.cos(t), eps * sp.sin(t))
    circle_cw = pullback(p, q, eps * sp.cos(t), -eps * sp.sin(t))
    # Curl=0 off the origin and cancellation on the punctured domain reduce
    # every enclosing positive simple curve to this arbitrary-radius circle.
    check_values("例5", [(sp.diff(q, x) - sp.diff(p, y), 0),
                         (sp.integrate(circle, (t, 0, 2 * sp.pi)), 2 * sp.pi),
                         (sp.integrate(circle_cw, (t, 0, 2 * sp.pi)), -2 * sp.pi)])


def example06():
    p = 2 * x * y ** 3 - y ** 2 * sp.cos(x)
    q = 1 - 2 * y * sp.sin(x) + 3 * x ** 2 * y ** 2
    u = potential(p, q)
    xt, yt = sp.pi * t ** 2 / 2, t
    along = u.subs({x: xt, y: yt}, simultaneous=True)
    chain_residual = pullback(p, q, xt, yt) - sp.diff(along, t)
    result = along.subs(t, 1) - along.subs(t, 0)
    check_values("例6", [(chain_residual, 0), (result, sp.pi ** 2 / 4),
                         (sp.diff(p, y) - sp.diff(q, x), 0)])


def example07():
    p, q = x ** 2 + 2 * x * y - y ** 2, x ** 2 - 2 * x * y - y ** 2
    u = potential(p, q)
    expected = x ** 3 / 3 + x ** 2 * y - x * y ** 2 - y ** 3 / 3
    check_values("例7", [(u, expected), (sp.diff(u, x), p), (sp.diff(u, y), q)])


def example08():
    f = x ** 2 + 3 * x * y
    xt, yt = t, 2 * t
    first = sp.integrate(sp.diff(f, x).subs({x: xt, y: yt}) * sp.diff(xt, t), (t, 0, 1))
    second = sp.integrate(sp.diff(f, y).subs({x: xt, y: yt}) * sp.diff(yt, t), (t, 0, 1))
    delta = f.subs({x: 1, y: 2}) - f.subs({x: 0, y: 0})
    check_values("例8", [(first, 4), (second, 3), (first + second, delta), (delta, 7)])


def example09():
    p, q = 3 * x ** 2 + 6 * x * y ** 2, 6 * x ** 2 * y + 4 * y ** 3
    u = potential(p, q)
    check_values("例9", [(u, x ** 3 + 3 * x ** 2 * y ** 2 + y ** 4),
                         (sp.diff(u, x), p), (sp.diff(u, y), q),
                         (sp.diff(p, y), sp.diff(q, x))])


def example10():
    xt, yt = a * sp.cos(t), a * sp.sin(t)
    speed = sp.sqrt(sp.trigsimp(sp.diff(xt, t) ** 2 + sp.diff(yt, t) ** 2))
    length = sp.integrate(speed, (t, 0, sp.pi))
    mx = sp.integrate(xt * speed, (t, 0, sp.pi))
    my = sp.integrate(yt * speed, (t, 0, sp.pi))
    check_values("例10", [(length, sp.pi * a), (mx / length, 0),
                          (my, 2 * a ** 2), (my / length, 2 * a / sp.pi)])


def example11():
    result = sp.integrate(pullback(x, y, 1 - t, 2 * t), (t, 0, 1))
    u = potential(x, y)
    delta = u.subs({x: 0, y: 2}) - u.subs({x: 1, y: 0})
    check_values("例11", [(result, sp.Rational(3, 2)), (delta, result),
                          (u, (x ** 2 + y ** 2) / 2)])


def supplements():
    xt, yt, zt = sp.cos(t), sp.sin(t), t
    speed = sp.sqrt(sp.trigsimp(sum(sp.diff(c, t) ** 2 for c in (xt, yt, zt))))
    helix = sp.integrate(sp.trigsimp(xt ** 2 + yt ** 2 + zt ** 2) * speed, (t, 0, 2 * sp.pi))
    check_values("随堂-螺旋线", [(helix, sp.sqrt(2) * (2 * sp.pi + 8 * sp.pi ** 3 / 3))])

    ellipse = sp.integrate(pullback(-y, x, a * sp.cos(t), b * sp.sin(t)) / 2, (t, 0, 2 * sp.pi))
    triangle = 0
    vertices = [(0, 0), (4, 0), (0, 3)]
    for start, end in zip(vertices, vertices[1:] + vertices[:1]):
        xt = start[0] + t * (end[0] - start[0])
        yt = start[1] + t * (end[1] - start[1])
        triangle += sp.integrate(pullback(-y, x, xt, yt) / 2, (t, 0, 1))
    check_values("正文-面积", [(ellipse, sp.pi * a * b), (triangle, 6)])

    p, q = -y / (x ** 2 + y ** 2), x / (x ** 2 + y ** 2)
    shifted = sp.trigsimp(pullback(p, q, 2 + sp.cos(t), sp.sin(t)))
    rational = sp.cancel(shifted.subs(sp.cos(t), (1 - v ** 2) / (1 + v ** 2)) * 2 / (1 + v ** 2))
    check_values("随堂-不围原点", [(sp.integrate(rational, (v, -sp.oo, sp.oo)), 0),
                                   (sp.diff(q, x) - sp.diff(p, y), 0)])

    p = 2 * x * sp.cos(y) + y ** 2 * sp.cos(x)
    q = 2 * y * sp.sin(x) - x ** 2 * sp.sin(y)
    u = potential(p, q)
    check_values("随堂-原函数", [(u, x ** 2 * sp.cos(y) + y ** 2 * sp.sin(x)),
                                 (sp.diff(u, x), p), (sp.diff(u, y), q)])

    p, q = sp.exp(y) + 2 * x, x * sp.exp(y) - 1
    u = potential(p, q)
    q0 = q.subs({x: 0, y: 1})
    check_values("例9后随堂-初值", [(u, x * sp.exp(y) + x ** 2 - y),
                                  (u.subs({x: 0, y: 1}), -1)])
    report("例9后随堂-Q非零", q0 != 0, f"Q(0,1)={q0}")


if __name__ == "__main__":
    examples = [example01, example02, example03, example04, example05, example06,
                example07, example08, example09, example10, example11]
    for index, check in enumerate(examples, 1):
        try:
            check()
        except Exception as exc:
            report(f"例{index}", False, f"{type(exc).__name__}: {exc}")
    try:
        supplements()
    except Exception as exc:
        report("随堂", False, f"{type(exc).__name__}: {exc}")
    sys.exit(1 if failed else 0)
