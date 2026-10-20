"""Independently derive exercise results; only the proof is MANUAL."""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as s

R = s.Rational
ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*(M16-\d+)\*\*\n(.*?)(?=\n\*\*M16-|\Z)", ANSWERS, re.S))
failures = 0


def equal(actual, expected):
    if isinstance(actual, s.MatrixBase):
        assert actual.shape == expected.shape
        for a, b in zip(actual, expected):
            equal(a, b)
        return
    delta = s.simplify(s.expand_log(actual - expected, force=True))
    assert delta == 0, (actual, expected, delta)


def normal_mean(poly, *variables):
    """Exact independent standard normal moments of a polynomial."""
    result = s.expand(poly)
    for variable in variables:
        terms = s.Poly(result, variable).terms()
        result = sum(
            coefficient * (0 if degree[0] % 2 else
                           1 if degree[0] == 0 else s.factorial2(degree[0] - 1))
            for degree, coefficient in terms
        )
    return s.expand(result)


def kl(q, p):
    return sum(a * s.log(a / b) for a, b in zip(q, p))


def choices(pid, actual, expected):
    for letter, got, want in zip("ABCD", actual, expected):
        assert bool(got) == want, (pid, letter, got, want)
        print(f"PASS {pid}({letter})")
    selected = "ABCD"[expected.index(True)]
    assert f"选 {selected}" in BLOCKS[pid]


def p01():
    pi = s.symbols("pi", positive=True)
    joint = s.Matrix([R(3, 4) * pi, R(1, 4) * (1 - pi)])
    root, = s.solve(joint[0] / sum(joint) - R(3, 5), pi)
    equal(root, R(1, 3))
    equal(sum(joint).subs(pi, root), R(5, 12))


def p02():
    values = [R(1, 4), s.Integer(4)]
    log_mean = s.log(sum(values) / 2)
    mean_log = s.expand_log(sum(s.log(x) for x in values) / 2)
    second = sum(x**2 for x in values) / 2
    equal(mean_log, 0)
    equal(log_mean, s.log(R(17, 8)))
    equal(second, R(257, 32))
    choices("M16-02", [log_mean < mean_log, s.Eq(log_mean, mean_log),
                       s.And(log_mean > mean_log, s.Eq(mean_log, 0)),
                       s.Eq(mean_log, s.log(second))], [False, False, True, False])


def p03():
    prior = [R(1, 2)] * 2
    likelihood = [R(1, 4), R(3, 4)]
    joint = [a * b for a, b in zip(prior, likelihood)]
    marginal = sum(joint)
    posterior = [a / marginal for a in joint]
    elbo = sum(q * s.log(a / q) for q, a in zip(prior, joint))
    gap = s.log(marginal) - elbo
    equal(elbo, s.log(s.sqrt(3) / 4))
    equal(gap, s.log(2 / s.sqrt(3)))
    equal(gap, kl(prior, posterior))
    claims = [s.log(R(1, 2)) - elbo, kl(posterior, prior) - gap,
              s.log(2 / s.sqrt(3)) - gap, -s.log(2 / s.sqrt(3)) - gap]
    choices("M16-03", [abs(float(v)) < 1e-12 for v in claims],
            [False, False, True, False])


def p04():
    e = s.symbols("e", real=True)
    contributions = []
    for mu, variance in [(0, 1), (1, R(1, 4))]:
        z = mu + s.sqrt(variance) * e
        log_ratio = -s.log(variance) / 2 - e**2 / 2 + z**2 / 2
        contributions.append(normal_mean(log_ratio, e))
    equal(contributions[0], 0)
    equal(sum(contributions), R(1, 8) + s.log(2))


def p05():
    theta, e = s.symbols("theta e", positive=True)
    probabilities = [1 - theta, theta]
    expectation = sum(q * z for z, q in enumerate(probabilities))
    exact = s.diff(expectation, theta)
    score = sum(q * z * s.diff(s.log(q), theta) for z, q in enumerate(probabilities))
    # Compare probabilities on an interval that contains neither 0 nor 1.
    mu, variance = R(1, 4), R(3, 16)
    interval_probability = (s.erf((R(2, 3) - mu) / s.sqrt(2 * variance))
                            - s.erf((R(1, 3) - mu) / s.sqrt(2 * variance))) / 2
    sd_derivative = s.diff(s.sqrt(theta * (1 - theta)), theta).subs(theta, R(1, 4))
    equal(sd_derivative, 1 / s.sqrt(3))
    choices("M16-05", [s.Eq(exact, 0), abs(float(interval_probability)) < 1e-12,
                       s.Eq(s.simplify(score), 1), s.Eq(exact, sd_derivative)],
            [False, False, True, False])


def p06():
    t = s.symbols("t", positive=True)
    joint = [R(1, 16), R(1, 4), R(3, 16)]
    q = [t, t, 1 - 2 * t]
    f = sum(b * s.log(a / b) for a, b in zip(joint, q))
    first = 2 * s.log(2 * (1 - 2 * t) / (3 * t))
    equal(s.diff(f, t), first)
    root, = s.solve(2 * (1 - 2 * t) - 3 * t, t)
    equal(root, R(2, 7))
    equal(s.diff(f, t, 2), -2 / t - 4 / (1 - 2 * t))
    equal(f.subs(t, root), s.log(R(7, 16)))
    equal(s.log(sum(joint)) - f.subs(t, root), s.log(R(8, 7)))
    posterior = [a / sum(joint) for a in joint]
    assert posterior[0] != posterior[1]
    equal(s.Matrix(posterior), s.Matrix([R(1, 8), R(1, 2), R(3, 8)]))


def p07():
    m = s.symbols("m", real=True)
    x = s.Matrix([-1, 0, 3])
    r = s.Matrix([R(3, 4), R(1, 2), R(1, 4)])
    objective = -sum(a * (v + m)**2 + (1 - a) * (v - m)**2
                     for v, a in zip(x, r)) / 2
    equal(objective, -R(3, 2) * m**2 + 2 * m - 5)
    root, = s.solve(s.diff(objective, m), m)
    equal(root, R(2, 3))
    equal(s.diff(objective, m, 2), -3)
    means = [sum(a * v for a, v in zip(r, x)) / sum(r),
             sum((1 - a) * v for a, v in zip(r, x)) / sum(1 - a for a in r)]
    equal(s.Matrix(means), s.Matrix([0, R(4, 3)]))
    assert sum(means) != 0


def p08():
    u, v, a, b, e, h = s.symbols("u v a b e h", real=True)
    f = (u + a * e + v + b * h)**2
    params = [u, v, a, b]
    gradient = s.Matrix([s.diff(f, p) for p in params])
    point = {u: 1, v: -1, a: 1, b: 2}
    averaged = (gradient.subs({e: 1, h: -1}) + gradient.subs({e: -1, h: 1})) / 2
    equal(averaged.subs(point), s.Matrix([0, 0, -2, 2]))
    exact_f = normal_mean(f, e, h)
    equal(exact_f, (u + v)**2 + a**2 + b**2)
    exact = s.Matrix([s.diff(exact_f, p) for p in params]).subs(point)
    equal(exact, s.Matrix([0, 0, 2, 4]))
    assert averaged.subs(point) != exact


def p09():
    t = s.symbols("t", real=True)
    p = [R(1, 2), t, R(1, 2) - t]
    d = [R(3, 4), R(1, 4), R(1, 2)]
    g = [a * (1 - b) / b for a, b in zip(p, d)]
    root, = s.solve(sum(g) - 1, t)
    equal(root, R(1, 6))
    p, g = [[v.subs(t, root) for v in vector] for vector in (p, g)]
    equal(s.Matrix(g), s.Matrix([R(1, 6), R(1, 2), R(1, 3)]))
    mix = [(a + b) / 2 for a, b in zip(p, g)]
    js = (kl(p, mix) + kl(g, mix)) / 2
    value = sum(a * s.log(c) + b * s.log(1 - c) for a, b, c in zip(p, g, d))
    equal(js, s.log(3) / 2 - R(2, 3) * s.log(2))
    equal(value, s.log(3) - R(10, 3) * s.log(2))
    equal(value, 2 * js - s.log(4))


def p10():
    mu, sigma = s.symbols("mu sigma", positive=True)
    e = s.symbols("e", real=True)
    z = mu + sigma * e
    loss = (1 - z)**2 / 2 + (mu**2 + sigma**2 - 1 - s.log(sigma**2)) / 2
    point = {mu: R(1, 2), sigma: 1}
    equal(loss.subs(point).subs(e, 0), R(1, 4))
    sampled = s.Matrix([s.diff(loss, p) for p in [mu, sigma]]).subs(point).subs(e, 0)
    equal(sampled, s.zeros(2, 1))
    expected_loss = normal_mean(loss, e)
    expected = s.Matrix([s.diff(expected_loss, p) for p in [mu, sigma]]).subs(point)
    equal(expected, s.Matrix([0, 1]))
    assert expected != sampled


def p12():
    mu, v = s.symbols("mu v", positive=True)
    e, z = s.symbols("e z", real=True)
    loss = normal_mean((2 - mu - s.sqrt(v) * e)**2, e) + (mu**2 + v - 1 - s.log(v)) / 2
    solution, = s.solve([s.diff(loss, mu), s.diff(loss, v)], [mu, v], dict=True)
    equal(solution[mu], R(4, 3))
    equal(solution[v], R(1, 3))
    equal(loss.subs(solution), R(4, 3) + s.log(3) / 2)
    equal(s.diff(loss, mu, 2), 3)
    equal(s.diff(loss, v, 2), 1 / (2 * v**2))
    exponent = -z**2 / 2 - (2 - z)**2
    center, = s.solve(s.diff(exponent, z), z)
    variance = -1 / s.diff(exponent, z, 2)
    equal(center, solution[mu])
    equal(variance, solution[v])
    equal(exponent, -R(3, 2) * (z - R(4, 3))**2 - R(4, 3))
    # Independent normalization of the joint also checks the tight-bound claim.
    joint = s.exp(exponent) / (s.sqrt(2 * s.pi) * s.sqrt(s.pi))
    marginal = s.integrate(joint, (z, -s.oo, s.oo))
    equal(-s.log(marginal), loss.subs(solution) + s.log(s.pi) / 2)


def p11():
    old_joint = [R(9, 20), R(1, 20)]
    new_joint = [R(1, 5), R(1, 5)]
    q = [R(1, 2), R(1, 2)]
    old_marginal, new_marginal = sum(old_joint), sum(new_joint)
    old_elbo = sum(a * s.log(b / a) for a, b in zip(q, old_joint))
    new_elbo = sum(a * s.log(b / a) for a, b in zip(q, new_joint))
    equal(old_marginal, R(1, 2))
    equal(new_marginal, R(2, 5))
    equal(old_elbo, s.log(R(3, 10)))
    equal(new_elbo, s.log(R(2, 5)))
    old_post = [a / old_marginal for a in old_joint]
    new_post = [a / new_marginal for a in new_joint]
    equal(s.Matrix(old_post), s.Matrix([R(9, 10), R(1, 10)]))
    equal(s.Matrix(new_post), s.Matrix([R(1, 2), R(1, 2)]))
    equal(kl(q, old_post), s.log(R(5, 3)))
    equal(kl(q, new_post), 0)
    assert new_elbo > old_elbo and new_marginal < old_marginal


def p13():
    u = s.symbols("u", real=True)
    d = 1 / (1 + s.exp(-u))
    h = -3 * s.log(d) - s.log(1 - d)
    equal(s.diff(h, u), 4 * d - 3)
    equal(s.diff(h, u, 2), 4 * d * (1 - d))
    root, = s.solve(s.diff(h, u), u)
    equal(root, s.log(3))
    equal(h.subs(u, root), 4 * s.log(4) - 3 * s.log(3))
    equal(s.diff(h, u, 2).subs(u, root), R(3, 4))
    equal(d.subs(u, root), R(3, 3 + 1))


def p14():
    theta = s.symbols("theta", positive=True)
    q = [1 - theta, theta]
    f = [s.Integer(1), s.Integer(4)]
    estimates = [a * s.diff(s.log(b), theta) for a, b in zip(f, q)]
    at = {theta: R(1, 3)}
    equal(s.Matrix(estimates).subs(at), s.Matrix([-R(3, 2), 12]))
    equal(s.Matrix(q).subs(at), s.Matrix([R(2, 3), R(1, 3)]))
    mean = sum(a * b for a, b in zip(estimates, q))
    variance = sum(a**2 * b for a, b in zip(estimates, q)) - mean**2
    direct = s.diff(sum(a * b for a, b in zip(f, q)), theta)
    equal(mean, 3)
    equal(mean, direct)
    equal(variance.subs(at), R(81, 2))


def p15():
    x, y, eta = s.symbols("x y eta", real=True)
    old = s.Matrix([x, y])
    simultaneous = s.Matrix([x - eta * y, y + eta * x])
    sequential = s.Matrix([simultaneous[0], y + eta * simultaneous[0]])
    a = simultaneous.jacobian(old).subs(eta, R(1, 2))
    b = sequential.jacobian(old).subs(eta, R(1, 2))
    equal(a, s.Matrix([[1, -R(1, 2)], [R(1, 2), 1]]))
    equal(b, s.Matrix([[1, -R(1, 2)], [R(1, 2), R(3, 4)]]))
    equal(a.det(), R(5, 4))
    equal(b.det(), 1)
    start = s.Matrix([1, 0])
    aa, bb = a**2 * start, b**2 * start
    equal(aa, s.Matrix([R(3, 4), 1]))
    equal(bb, s.Matrix([R(3, 4), R(7, 8)]))
    equal(aa.dot(aa), R(25, 16))
    equal(bb.dot(bb), R(85, 64))
    equal(simultaneous.dot(simultaneous), (1 + eta**2) * old.dot(old))
    assert s.expand(sequential.dot(sequential) - (1 + eta**2) * old.dot(old)) != 0
    np.testing.assert_allclose(np.linalg.norm(np.array(aa, dtype=float))**2, 25 / 16)


# These anchors bind the independently calculated expectations to the printed
# answer, so deleting or changing a principal result also fails verification.
anchors = {
    1: [r"\pi=1/3", "5/12"], 2: ["选 C", "17/8", "257/32"],
    3: ["选 C", r"\log(2/\sqrt3)"], 4: [r"1/8+\log2"],
    5: ["选 C", "精确导数为 $1$"], 6: ["t=2/7", "7/16", "8/7"],
    7: ["m=2/3", "(0,4/3)"], 8: ["(-2,2)", "(2,4)"],
    9: ["t=1/6", "(1/6,1/2,1/3)", r"\frac{10}{3}\log2"],
    10: ["L=1/4", "(0,1)"], 11: ["旧边缘为 $1/2$", "ELBO 上升", "不会下降"],
    12: [r"\mu=4/3", r"\sigma^2=1/3", r"4/3+\frac12\log3"],
    13: [r"s=\log3", r"4\log4-3\log3", "3/4"],
    14: ["81/2", "估计无偏"], 15: ["25/16", "85/64", r"\det B=1"],
}


def main():
    global failures
    ids = re.findall(r"^\*\*(M16-\d+)\*\*", PROBLEMS, re.M)
    expected_ids = [f"M16-{i:02}" for i in range(1, 16)]
    assert ids == expected_ids and set(BLOCKS) == set(ids)
    for i, pid in enumerate(ids, 1):
        try:
            body = BLOCKS[pid].split("\n### ", 1)[0].strip()
            assert body.startswith("**答案：**")
            assert body.splitlines()[-1].startswith("区分点：")
            for token in anchors[i]:
                assert token in body, (pid, "answer changed", token)
            tier = re.search(rf"\*\*{pid}\*\*〔([ABC])", PROBLEMS)[1]
            assert len(body) <= {"A": 400, "B": 900, "C": 1400}[tier], (pid, len(body))
            if i == 11:
                p11()
                assert "（证明）" in PROBLEMS.split(f"**{pid}**", 1)[1].split("**M16-12**", 1)[0]
                print(f"PASS {pid} 数值部分；一般证明须人工审阅")
            else:
                globals()[f"p{i:02}"]()
                print(f"PASS {pid}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {pid} {type(exc).__name__}: {exc}")
    return int(failures != 0)


if __name__ == "__main__":
    sys.exit(main())
