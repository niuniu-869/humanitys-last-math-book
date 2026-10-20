"""Recompute the current lesson examples; every mismatch is a failure."""
from collections import Counter
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
EXAMPLES = dict(re.findall(r"(?s)\*\*例 (\d+)\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON))
failures = 0
W = np.array([[.5, -.5], [.25, .5]])
OUT = np.array([[1., 0.], [0., 1.], [-1., -1.]])
X = np.eye(2)
TARGETS = [1, 2]


def close(actual, expected, atol=1e-10):
    np.testing.assert_allclose(actual, expected, atol=atol, rtol=0)


def rounded(actual, printed, places):
    close(actual, printed, .5 * 10**(-places) + 1e-12)


def softmax(x):
    e = np.exp(np.asarray(x) - np.max(x))
    return e / e.sum()


def forward(Wp=W, U=np.eye(2), b=np.zeros(2), xs=X):
    hs, pre, logits, probabilities, losses = [np.zeros(2)], [], [], [], []
    for x, target in zip(xs, TARGETS):
        a = Wp @ hs[-1] + U @ x + b
        h = np.tanh(a)
        o = OUT @ h
        p = softmax(o)
        pre.append(a)
        hs.append(h)
        logits.append(o)
        probabilities.append(p)
        losses.append(-np.log(p[target]))
    return np.array(hs), np.array(pre), np.array(logits), np.array(probabilities), np.array(losses)


def objective(Wp, U, b):
    return forward(Wp, U, b)[-1].mean()


def finite_difference(which):
    params = [W.copy(), np.eye(2), np.zeros(2)]
    result = np.zeros_like(params[which])
    epsilon = 1e-5
    for index in np.ndindex(result.shape):
        plus, minus = [p.copy() for p in params], [p.copy() for p in params]
        plus[which][index] += epsilon
        minus[which][index] -= epsilon
        result[index] = (objective(*plus) - objective(*minus)) / (2 * epsilon)
    return result


def e01():
    p = np.array([softmax([2, 1, 0])[0], .5, .25, .8])
    terms = -np.log(p)
    rounded(p[0], .6652409558, 10)
    rounded(p.prod(), .0665241, 7)
    rounded(terms, [.4076, .6931, 1.3863, .2231], 4)
    rounded(terms.sum(), 2.7101911, 7)
    rounded(terms.mean(), .6775478, 7)
    rounded(terms.mean(), .6775, 4)
    rounded(-np.log([.5, .5, .25]).mean(), .9242, 4)


def e02():
    pa, pb = np.array([softmax([2, 1, 0])[0], .5, .25, .8]), np.array([.4, .4, .2, .5])
    la, lb = -np.log(pa).mean(), -np.log(pb).mean()
    rounded(np.exp(la), 1.97, 2)
    rounded(-np.log(pb), [.9163, .9163, 1.6094, .6931], 4)
    rounded(lb, 1.0338, 4)
    rounded(np.exp(lb), 2.81, 2)
    assert np.exp(la) < np.exp(lb)
    pair = np.array([.5, .125])
    close(np.exp(-np.log(pair).mean()), 4)
    close((1 / pair).mean(), 5)


def e03():
    transitions = Counter({("s", "a"): 2, ("s", "c"): 1, ("a", "b"): 2,
                           ("a", "end"): 1, ("b", "c"): 1, ("b", "d"): 1,
                           ("b", "a"): 1, ("c", "end"): 1, ("c", "b"): 1,
                           ("d", "end"): 1})
    totals = Counter()
    for (a, b), count in transitions.items():
        totals[a] += count
    def probability(a, b):
        return sp.Rational(transitions[a, b], totals[a])
    expected = [sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(1, 3), sp.Rational(1, 2)]
    sequence = ("s", "a", "b", "c", "end")
    calculated = [probability(a, b) for a, b in zip(sequence, sequence[1:])]
    assert calculated == expected
    assert sp.prod(calculated) == sp.Rational(2, 27)
    rounded(float(sp.prod(calculated)), .0741, 4)
    sequence = ("s", "d", "b", "c", "end")
    zero = sp.prod(probability(a, b) for a, b in zip(sequence, sequence[1:]))
    assert zero == 0
    assert sp.limit(sp.Symbol("p", positive=True)**(-sp.Rational(1, 4)),
                    sp.Symbol("p", positive=True), 0, dir="+") == sp.oo
    counts = sp.Matrix([1, 0, 1])
    smoothed = counts + sp.ones(3, 1)
    assert smoothed / sum(smoothed) == sp.Matrix([sp.Rational(2, 5), sp.Rational(1, 5), sp.Rational(2, 5)])
    assert "2/5" in EXAMPLES["3"] and "1/5" in EXAMPLES["3"]


def e04():
    hs, pre, logits, probabilities, losses = forward()
    rounded(hs[1:], [[.7616, 0], [.3634, .8307]], 4)
    rounded(pre, [[1, 0], [.3808, 1.1904]], 4)
    rounded(logits, [[.7616, 0, -.7616], [.3634, .8307, -1.1941]], 4)
    rounded(probabilities, [[.5935, .2771, .1294], [.3563, .5686, .0751]], 4)
    rounded(losses, [1.2833, 2.5894], 4)
    rounded(losses.mean(), 1.9364, 4)
    rounded(np.exp(losses.mean()), 6.9, 1)
    assert np.exp(losses.mean()) > 3
    other_hs, other_pre, *_ = forward(xs=np.array([[1, 1], [1, 0]]))
    rounded(other_hs[1:], [[.7616, .7616], [.7616, .5162]], 4)
    rounded(other_pre[1], [1, .5712], 4)


def e05():
    hs, _, _, probabilities, _ = forward()
    gout = (probabilities - np.eye(3)[TARGETS]) / 2
    rounded(gout, [[.2967, -.3614, .0647], [.1782, .2843, -.4625]], 4)
    delta = np.zeros((3, 2))
    gh = np.zeros((2, 2))
    for t in (1, 0):
        gh[t] = OUT.T @ gout[t] + W.T @ delta[t+1]
        delta[t] = (1 - hs[t+1]**2) * gh[t]
    rounded(gh, [[.5679, -.5884], [.6406, .7468]], 4)
    rounded(1 - hs[2]**2, [.8679, .3099], 4)
    # This intermediate line explicitly uses the already rounded gout.
    # Each subtraction propagates at most two half-units of rounding error.
    rounded(OUT.T @ np.array([.2967, -.3614, .0647]), [.2320, -.4261], 4)
    close(OUT.T @ gout[0], [.2320, -.4261], 1e-4)
    rounded(W.T @ delta[1], [.3359, -.1623], 4)
    rounded(delta[:2], [[.2385, -.5884], [.5560, .2314]], 4)
    grad_w = sum(np.outer(delta[t], hs[t]) for t in range(2))
    grad_u = sum(np.outer(delta[t], X[t]) for t in range(2))
    grad_b = delta[:2].sum(axis=0)
    printed_u = np.array([[.2385, .5560], [-.5884, .2314]])
    rounded(grad_u, printed_u, 4)
    rounded(grad_w, [[.4235, 0], [.1763, 0]], 4)
    rounded(grad_b, [.7945, -.3570], 4)
    for which, analytic in enumerate([grad_w, grad_u, grad_b]):
        close(analytic, finite_difference(which), 1e-6)
    printed_error = np.max(np.abs(finite_difference(1) - printed_u))
    assert printed_error > 1e-6
    assert printed_error < 1e-4
    assert "未经舍入的解析梯度" in EXAMPLES["5"]
    assert r"10^{-4}" in EXAMPLES["5"]


def e06():
    symbolic_w = sp.Matrix([[sp.Rational(1, 2), -sp.Rational(1, 2)],
                            [sp.Rational(1, 4), sp.Rational(1, 2)]])
    assert sorted(symbolic_w.singular_values()) == [sp.Rational(1, 2), sp.Rational(3, 4)]
    assert symbolic_w.det() == sp.Rational(3, 8)
    rounded(np.linalg.norm(W, 2)**20, .0032, 4)
    gradient = np.array([30., 40.])
    norm = np.linalg.norm(gradient)
    close(norm, 50)
    clipped = gradient * min(1, 5 / norm)
    close(clipped, [3, 4])
    close(np.linalg.norm(clipped), 5)
    threshold = np.log(.01) / np.log(.95)
    rounded(threshold, 89.8, 1)
    minimum_steps = int(np.floor(threshold)) + 1
    assert minimum_steps == 90
    assert .95**minimum_steps < .01 <= .95**(minimum_steps - 1)
    lam = sp.symbols("lambda")
    gram = symbolic_w.T * symbolic_w
    assert gram == sp.Matrix([[sp.Rational(5, 16), -sp.Rational(1, 8)],
                              [-sp.Rational(1, 8), sp.Rational(1, 2)]])
    assert sp.expand(gram.charpoly(lam).as_expr()) == lam**2 - sp.Rational(13, 16)*lam + sp.Rational(9, 64)
    for base, values, places in [(.9, [.349, .122, .0052], [3, 3, 4]),
                                (1.1, [2.59, 6.73, 117], [2, 2, 0])]:
        for steps, value, digits in zip([10, 20, 50], values, places):
            rounded(base**steps, value, digits)
    rounded(.99**50, .61, 2)
    k = sp.symbols("k", integer=True, nonnegative=True)
    initial = sp.symbols("initial")
    for a, b, start, expected in [(sp.Rational(1, 3), 1, 2, sp.Rational(3, 2) + sp.Rational(1, 2)*3**(-k)),
                                 (sp.Rational(1, 2), 1, 0, 2-2**(1-k))]:
        r = sp.Function("r")
        solution = sp.rsolve(r(k+1)-a*r(k)-b, r(k), {r(0): initial})
        assert sp.simplify(solution.subs(initial, start)-expected) == 0
        assert sp.simplify(sp.diff(solution, initial)-a**k) == 0


def e07():
    h, x, old_c = .5, 1., 1.
    parameters = np.array([[1, 1, 1], [1, 1, -1], [1, 0, 1], [1, -1, 0]])
    pre = parameters @ np.array([h, x, 1])
    close(pre, [2.5, .5, 1.5, -.5])
    f, i, o = 1 / (1 + np.exp(-pre[:3]))
    candidate = np.tanh(pre[3])
    rounded([f, i, o, candidate], [.9241, .6225, .8176, -.4621], 4)
    rounded(i * candidate, -.2876, 4)
    c = f * old_c + i * candidate
    new_h = o * np.tanh(c)
    rounded([c, np.tanh(c), new_h], [.6365, .5625, .4599], 4)
    rounded(.9241**20, .206, 3)
    rounded(f**20, .206, 3)
    rounded(.99**20, .818, 3)
    previous, candidate = sp.symbols("previous candidate")
    preserved = 1 * previous + 0 * candidate
    assert sp.simplify(preserved - previous) == 0
    assert sp.diff(preserved, previous) == 1
    c = sp.Rational(3, 4)*2 + sp.Rational(1, 4)*(-sp.Rational(1, 2))
    assert c == sp.Rational(11, 8)
    result = sp.tanh(c)/2
    rounded(float(result), .4399, 4)
    assert float(result) < .5 < float(c)
    assert "0.4399" in EXAMPLES["7"]


def e08():
    h, z, candidate = sp.Rational(1, 2), sp.Rational(1, 5), sp.Rational(4, 5)
    assert (1-z)*h + z*candidate == sp.Rational(14, 25)
    result = (1-z)*h + z*candidate
    assert abs(result-h) < abs(result-candidate)
    dh = dx = 256
    per_group = dh*dh + dh*dx + dh
    assert per_group == 131328
    assert 3 * per_group == 393984
    assert 4 * per_group == 525312
    previous, proposal, gate = sp.symbols("previous proposal gate")
    update = (1-gate)*previous + gate*proposal
    assert sp.simplify(update.subs(gate, 0) - previous) == 0
    assert sp.diff(update, previous).subs(gate, 0) == 1


def e09():
    p = np.array([.7, .5, .9])
    terms = -np.log(p)
    close(p.prod(), .315)
    rounded(terms, [.3567, .6931, .1054], 4)
    rounded(terms.sum(), 1.1552, 4)
    rounded(terms.mean(), .3851, 4)
    rounded(np.exp(terms.mean()), 1.47, 2)
    close(np.exp(terms.mean()), p.prod()**(-1/len(p)))
    # Check the missing prerequisite against the example data and method 2.
    other_targets = np.array([.4, .4, .2, .5])
    assert len(p) != len(other_targets)
    assert "同一份测试文本" in LESSON
    assert "不能拿来比较模型优劣" in EXAMPLES["9"]
    assert "也可以直接和例 2" not in EXAMPLES["9"]


def e10():
    H = np.array([[1., 0.], [0., 1.], [1., 1.]])
    s = np.array([1., 0.])
    Ws = Wh = np.eye(2)
    v = np.array([1., 1.])
    scores = np.array([v @ np.tanh(Ws @ s + Wh @ h) for h in H])
    rounded(scores, [.9640, 1.5232, 1.7256], 4)
    exponents = np.exp(scores)
    rounded(exponents, [2.622, 4.587, 5.616], 3)
    rounded(exponents.sum(), 12.825, 3)
    weights = softmax(scores)
    context = weights @ H
    rounded(weights, [.2045, .3576, .4379], 4)
    rounded(context, [.6424, .7955], 4)
    assert weights.argmax() == scores.argmax() == 2
    close(weights.sum(), 1)
    assert np.all(weights > 0)
    close(softmax([0, 0, 0]) @ H, [2/3, 2/3])


def run(number, calculation, anchors):
    global failures
    try:
        for anchor in anchors:
            assert anchor in EXAMPLES[str(number)], f"Lesson transcription drift: {anchor}"
        calculation()
        print(f"PASS 例{number}")
    except Exception as exc:
        failures += 1
        print(f"FAIL 例{number} {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    run(1, e01, [r"\dfrac{e^2}{e^2+e+1}", "0.6652409558", "0.0665241", "2.7101911", "0.6775478", "0.6775", "0.9242"])
    run(2, e02, ["1.97", "1.0338", "2.81", "算术平均是 5"])
    run(3, e03, [r"\frac{2}{27}", "0.0741", "困惑度成了无穷大"])
    run(4, e04, ["0.7616", "0.3634", "0.8307", "0.0751", "1.9364", "6.9", "0.5162"])
    run(5, e05, ["0.2385", "-0.5884", "0.5560", "0.2314", "0.4235", "0.1763", "10^{-6}"])
    run(6, e06, ["0.75", "0.5", "0.0032", "$(3,4)$", "90 步"])
    run(7, e07, ["0.6365", "0.4599", "0.206", "0.818"])
    run(8, e08, ["0.56", "131328", "393984", "525312"])
    run(9, e09, ["0.315", "1.1552", "0.3851", "1.47"])
    run(10, e10, ["0.2045", "0.3576", "0.4379", "0.6424", "0.7955"])
    sys.exit(bool(failures))
