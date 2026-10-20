"""Recompute every determinate answer from the problem data.

Expected expressions below transcribe answers.md. Actual expressions come from
definitions, differentiation, solving equations, and limits, not those answers.
Only the general proof P14-11 is marked MANUAL.
"""
import sys

import numpy as np
import sympy as s

R = s.Rational
failures = 0
z = s.symbols("z1:4", real=True)
logsum = s.log(sum(s.exp(v) for v in z))


def same(actual, expected):
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            same(a, b) for a, b in zip(actual, expected)
        )
    if isinstance(expected, (bool, np.bool_)):
        return bool(actual) == bool(expected)
    if isinstance(expected, str):
        return actual == expected
    if actual == expected:
        return True
    difference = actual - expected
    if s.simplify(difference) == 0:
        return True
    # All logarithm arguments are positive on the stated finite domains.
    return s.simplify(s.logcombine(difference, force=True)) == 0


def report(pid, actual, expected):
    global failures
    ok = same(actual, expected)
    print(f"{'PASS' if ok else 'FAIL'} {pid}")
    if not ok:
        failures += 1
        print(f"  actual={actual}; expected={expected}")


def ce(p, q, bits=True):
    terms = []
    for pi, qi in zip(p, q):
        if pi == 0:
            continue
        if qi == 0:
            return s.oo
        terms.append(-pi * s.log(qi))
    return s.simplify(sum(terms) / (s.log(2) if bits else 1))


def entropy(p, bits=True):
    return ce(p, p, bits)


def kl(p, q, bits=True):
    cross_entropy = ce(p, q, bits)
    if cross_entropy == s.oo:
        return s.oo
    return s.simplify(cross_entropy - entropy(p, bits))


def softmax(scores, temperature=1):
    weights = [s.exp(v / temperature) for v in scores]
    return [s.simplify(w / sum(weights)) for w in weights]


def grad_at(loss, scores):
    return [
        s.simplify(s.diff(loss, zi).subs(dict(zip(z, scores))))
        for zi in z
    ]


def choices(pid, truth_values, correct):
    for letter, truth in zip("ABCD", truth_values):
        report(f"{pid} ({letter})", truth, letter == correct)
    report(pid, [i for i, v in zip("ABCD", truth_values) if v], [correct])


def run():
    p = [R(3, 4), R(1, 4), 0]
    info = -s.log(p[1], 2)
    h = entropy(p)
    report("P14-01", [info, h, info * s.log(2), entropy(p, False)],
           [2, 2 - R(3, 4) * s.log(3, 2), 2 * s.log(2),
            2 * s.log(2) - R(3, 4) * s.log(3)])

    p, q = [1, 0], [R(1, 4), R(3, 4)]
    choices("P14-02", [
        same(ce(p, q), ce(q, p)),
        same(kl(p, q), 0),
        same([ce(p, q), kl(p, q)], [2, 2]),
        same(ce(p, q), entropy(q)),
    ], "C")
    report("P14-02 反向交叉熵", ce(q, p), s.oo)

    q = softmax([s.log(9), s.Integer(0)], 2)
    options = [[R(9, 10), R(1, 10)], [R(81, 82), R(1, 82)],
               [3, 1], [R(3, 4), R(1, 4)]]
    choices("P14-03", [same(q, option) for option in options], "D")

    q2 = s.exp(-s.log(5))
    q3 = s.solve(2 * s.Symbol("v") + q2 + s.Symbol("v") - 1,
                  s.Symbol("v"))[0]
    q = [2 * q3, q2, q3]
    gradient = grad_at(logsum - z[1], [s.log(v) for v in q])
    report("P14-04", [q, gradient],
           [[R(8, 15), R(1, 5), R(4, 15)],
            [R(8, 15), -R(4, 5), R(4, 15)]])

    p, q, r = [R(3, 4), R(1, 4)], [R(1, 2)] * 2, [R(1, 4), R(3, 4)]
    dpr, dpq, dqr = kl(p, r), kl(p, q), kl(q, r)
    gap = s.simplify(dpr - dpq - dqr)
    report("P14-05", [dpr, dpq, dqr, gap, bool(gap > 0)],
           [s.log(3, 2) / 2, R(3, 4) * s.log(3, 2) - 1,
            1 - s.log(3, 2) / 2, s.log(3, 2) / 4, True])

    t = s.symbols("t", real=True)
    qt = [t, (1 - t) / 2, (1 - t) / 2]
    p = [0, R(1, 2), R(1, 2)]
    forward = kl(p, qt)
    x = s.symbols("x", positive=True)
    increasing = s.simplify(s.diff(forward, t).subs(t, x / (1 + x))).is_positive
    report("P14-06", [
        forward, kl(qt, p),
        kl(p, [0, R(1, 2), R(1, 2)]),
        kl([0, R(1, 2), R(1, 2)], p),
        kl(p, [1, 0, 0]), kl([1, 0, 0], p),
        s.limit(forward, t, 1, dir="-"), increasing,
    ], [-s.log(1 - t, 2), s.oo, 0, 0, s.oo, s.oo, s.oo, True])

    avg_loss = ((logsum - z[0]) + (logsum - z[1])) / 2
    scores = [s.log(2), 0, 0]
    loss_value = s.simplify(avg_loss.subs(dict(zip(z, scores))))
    gradient = grad_at(avg_loss, scores)
    sum_gradient = grad_at(2 * avg_loss, scores)
    choices("P14-07", [
        same(loss_value, s.log(R(8, 3))),
        same(gradient, [-R(1, 2), -R(3, 4), R(1, 4)]),
        same(gradient, [0, -R(1, 4), R(1, 4)]),
        same(sum_gradient, [0, -R(1, 4), R(1, 4)]),
    ], "C")
    report("P14-07 损失与总梯度", [loss_value, sum_gradient],
           [R(3, 2) * s.log(2), [0, -R(1, 2), R(1, 2)]])

    a, temp, u = s.symbols("a T u", positive=True)
    q = softmax([a, a, s.Integer(0)], temp)
    ratio_u = s.solve(1 / (2 * u + 1) - R(1, 5), u)
    relation = s.solve(a / temp - s.log(ratio_u[0]), a)
    report("P14-08", [
        relation, [v.subs(a, relation[0]).simplify() for v in q],
        [s.limit(v, temp, 0, dir="+") for v in q],
        [s.limit(v, temp, s.oo) for v in q],
    ], [[temp * s.log(2)], [R(2, 5), R(2, 5), R(1, 5)],
        [R(1, 2), R(1, 2), 0], [R(1, 3)] * 3])
    # Keeping q3=1/5 fixes T once a is fixed; part (2) releases it.
    fixed_temperature = s.solve(a / temp - s.log(ratio_u[0]), temp)
    report("P14-08 两问条件区分", [
        fixed_temperature, s.simplify(s.diff(q[2], temp)).is_positive,
    ], [[a / s.log(2)], True])

    ht = entropy([t, t, 1 - 2 * t])
    dh = s.simplify(s.diff(ht, t))
    # The exact derivative and its minimum on (0, 1/4] establish monotonicity.
    ddh = s.simplify(s.diff(dh, t))
    report("P14-09", [
        dh, ddh, dh.subs(t, R(1, 4)).simplify(),
        ht.subs(t, R(1, 4)).simplify(), s.limit(ht, t, 0, dir="+"),
        s.solve(1 - 2 * t - t, t),
    ], [2 * s.log((1 - 2 * t) / t, 2),
        -2 / (t * (1 - 2 * t) * s.log(2)), 2, R(3, 2), 0, [R(1, 3)]])

    theta = s.symbols("theta", positive=True)
    counts = [4, 2, 2]
    phat = [R(c, sum(counts)) for c in counts]
    model = [theta, theta, 1 - 2 * theta]
    likelihood = s.prod(v ** c for v, c in zip(model, counts))
    f = ce(phat, model, False)
    df = s.factor(s.diff(f, theta))
    optimum = s.solve(df, theta)
    fitted = [v.subs(theta, optimum[0]) for v in model]
    report("P14-10", [
        likelihood, f, df, optimum, fitted,
        f.subs(theta, optimum[0]), entropy(phat, False), kl(phat, fitted, False),
    ], [
        theta ** 6 * (1 - 2 * theta) ** 2,
        -R(3, 4) * s.log(theta) - s.log(1 - 2 * theta) / 4,
        (8 * theta - 3) / (4 * theta * (1 - 2 * theta)),
        [R(3, 8)], [R(3, 8), R(3, 8), R(1, 4)],
        R(11, 4) * s.log(2) - R(3, 4) * s.log(3),
        R(3, 2) * s.log(2),
        R(5, 4) * s.log(2) - R(3, 4) * s.log(3),
    ])

    print("MANUAL P14-11 证明：逐项对数不等式、归一化与等号条件")

    p = [R(1, 2), R(1, 3), R(1, 6)]
    q = softmax([t, s.Integer(0), -t])
    f = ce(p, q, False)
    derivative_u = s.factor(s.diff(f, t).subs(t, s.log(u)))
    roots = s.solve(s.together(derivative_u).as_numer_denom()[0], u)
    ustar = (1 + s.sqrt(33)) / 4
    # u is positive, so solve discards the negative quadratic root.
    qstar = [s.simplify(v.subs(t, s.log(roots[0]))) for v in q]
    report("P14-12", [
        f, derivative_u, roots, qstar,
        f.subs(t, s.log(roots[0])),
        s.simplify(q[1] ** 2 - q[0] * q[2]),
        p[1] ** 2 - p[0] * p[2],
        bool(s.N(kl(p, qstar, False), 30) > 0),
    ], [
        s.log(s.exp(t) + 1 + s.exp(-t)) - t / 3,
        (2 * u ** 2 - u - 4) / (3 * (u ** 2 + u + 1)),
        [ustar], [ustar ** 2 / (ustar ** 2 + ustar + 1),
                  ustar / (ustar ** 2 + ustar + 1),
                  1 / (ustar ** 2 + ustar + 1)],
        s.log(ustar + 1 + 1 / ustar) - s.log(ustar) / 3,
        0, R(1, 36), True,
    ])

    joint = s.Matrix([[R(3, 8), R(1, 8)], [R(1, 8), R(3, 8)]])
    px = [sum(joint.row(i)) for i in range(2)]
    py = [sum(joint.col(i)) for i in range(2)]
    independent = all(joint[i, j] == px[i] * py[j]
                      for i in range(2) for j in range(2))
    conditional = joint[1, 1] / px[1]
    icond = -s.log(conditional, 2)
    report("P14-13", [
        px, py, independent, entropy(list(joint)),
        entropy(px) + entropy(py), conditional, icond,
        -s.log(py[1], 2) - icond,
    ], [[R(1, 2)] * 2, [R(1, 2)] * 2, False,
        3 - R(3, 4) * s.log(3, 2), 2,
        R(3, 4), 2 - s.log(3, 2), s.log(3, 2) - 1])

    data = [1, 1, 2, 4]
    likelihood = s.prod(theta * (1 - theta) ** (k - 1) for k in data)
    f = -s.expand_log(s.log(likelihood), force=True) / len(data)
    df = s.factor(s.diff(f, theta))
    optimum = s.solve(df, theta)
    support = sorted(set(data))
    phat = [R(data.count(k), len(data)) for k in support]
    fitted = [optimum[0] * (1 - optimum[0]) ** (k - 1) for k in support]
    report("P14-14", [
        R(sum(data), len(data)), f, df, optimum, support, phat,
        entropy(phat, False), ce(phat, fitted, False),
        kl(phat, fitted, False), optimum[0] * (1 - optimum[0]) ** (3 - 1),
    ], [2, -s.log(theta) - s.log(1 - theta),
        (2 * theta - 1) / (theta * (1 - theta)),
        [R(1, 2)], [1, 2, 4], [R(1, 2), R(1, 4), R(1, 4)],
        R(3, 2) * s.log(2), 2 * s.log(2), s.log(2) / 2, R(1, 8)])

    models = [[R(3, 4), R(3, 4), R(1, 64)], [R(1, 4)] * 3]
    result = []
    for probabilities in models:
        likelihood = s.prod(probabilities)
        avg = -sum(s.log(v) for v in probabilities) / len(probabilities)
        result.append([sum(probabilities) / len(probabilities), likelihood,
                       avg, s.exp(avg)])
    report("P14-15", result, [
        [R(97, 192), R(9, 1024), (10 * s.log(2) - 2 * s.log(3)) / 3,
         (R(1024, 9)) ** R(1, 3)],
        [R(1, 4), R(1, 64), s.log(4), 4],
    ])
    report("P14-15 排序", [
        result[0][0] > result[1][0], result[0][1] < result[1][1],
        bool(s.N(result[0][2] - result[1][2]) > 0),
        bool(s.N(result[0][3] - result[1][3]) > 0),
    ], [True] * 4)


if __name__ == "__main__":
    run()
    sys.exit(bool(failures))
