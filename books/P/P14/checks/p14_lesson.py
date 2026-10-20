"""Check all 15 examples, using the explicit recorded erratum for example 14."""
from collections import Counter
from pathlib import Path
import sys

import numpy as np
import sympy as s

failures = 0


def ce(p, q, bits=True):
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    support = p > 0
    if np.any(q[support] == 0):
        return np.inf
    log = np.log2 if bits else np.log
    return float(-np.dot(p[support], log(q[support])))


def entropy(p, bits=True):
    return ce(p, p, bits)


def kl(p, q, bits=True):
    return ce(p, q, bits) - entropy(p, bits)


def softmax(z, temp=1):
    z = np.asarray(z, dtype=float)
    weights = np.exp((z - z.max()) / temp)
    return weights / weights.sum()


def near(actual, expected, digits):
    return bool(np.allclose(actual, expected, rtol=0,
                            atol=0.50001 * 10 ** (-digits)))


def report(number, checks):
    global failures
    ok = all(checks)
    print(f"{'PASS' if ok else 'FAIL'} 例{number}")
    if not ok:
        failures += 1
        print(f"  failed subchecks: {[i + 1 for i, value in enumerate(checks) if not value]}")


def run():
    dice = Counter(i + j for i in range(1, 7) for j in range(1, 7))
    info7 = -np.log2(dice[7] / 36)
    info2 = -np.log2(dice[2] / 36)
    tail = sum(count for total, count in dice.items() if total >= 10) / 36
    report(1, [near([info7, info2], [2.585, 5.170], 3),
               near(info2, 2 * info7, 12), near(tail, 1 / 6, 12)])

    pjoint = dice[7] / 36 * 0.7
    report(2, [near(pjoint, 7 / 60, 12), near(-np.log2(pjoint), 3.100, 3),
               near(-np.log2(0.7), 0.515, 3),
               near(-np.log2(pjoint), info7 - np.log2(0.7), 12)])

    p = np.array([1 / 2, 1 / 4, 1 / 8, 1 / 8])
    codes = ["0", "10", "110", "111"]
    lengths = np.array([len(code) for code in codes])
    prefix_free = all(not b.startswith(a) for i, a in enumerate(codes)
                      for j, b in enumerate(codes) if i != j)
    report(3, [near(-np.log2(p), [1, 2, 3, 3], 12),
               near(entropy(p), 7 / 4, 12),
               near(p @ lengths, 7 / 4, 12), prefix_free,
               near(2 - p @ lengths, 1 / 4, 12)])

    sum_probs = [dice[k] / 36 for k in range(2, 13)]
    joint_probs = [1 / 36] * 36
    report(4, [near(entropy(sum_probs), 3.274, 3),
               near(entropy([1 / 11] * 11), 3.459, 3),
               near(entropy(joint_probs), 5.170, 3),
               entropy(sum_probs) < entropy([1 / 11] * 11),
               entropy(sum_probs) < entropy(joint_probs)])

    k = s.symbols("k", integer=True, positive=True)
    prob = s.Rational(7, 10) * s.Rational(3, 10) ** (k - 1)
    # Sum the original entropy series exactly rather than reusing the answer formula.
    h_geom = -s.summation(prob * (s.log(s.Rational(7, 10))
                         + (k - 1) * s.log(s.Rational(3, 10))), (k, 1, s.oo)) / s.log(2)
    report(5, [near(float(h_geom), 1.259, 3),
               near(float(s.summation(k * prob, (k, 1, s.oo))), 1 / .7, 12),
               near(-.3 / .7 * np.log2(.3), .744, 3)])

    uniform = np.array([1 / 4] * 4)
    wrong = p[::-1]
    rng = np.random.default_rng(2026)
    sample = rng.choice(4, size=100000, p=p)
    sim = [(-np.log2(q)[sample]).mean() for q in [p, uniform, wrong]]
    report(6, [
        near([ce(p, uniform), ce(p, wrong), ce(uniform, p)], [2, 2.625, 2.25], 12),
        near([kl(p, uniform), kl(p, wrong)], [.25, .875], 12),
        near(sim, [1.745, 2.000, 2.628], 3),
    ])

    p7, q7 = [.9, .1], [.5, .5]
    report(7, [near(ce(p7, q7), 1, 12),
               near(entropy(p7), .469, 3), near(kl(p7, q7), .531, 3),
               near(kl(q7, p7), .737, 3)])

    p8, q8 = [.5, .5, 0], [1 / 3] * 3
    report(8, [near(kl(p8, q8), np.log2(1.5), 12),
               near(kl(p8, q8), .585, 3), np.isposinf(kl(q8, p8))])

    ref, new, reward = [.5, .3, .2], [.7, .2, .1], np.array([1, 0, 0])
    old_reward, new_reward = np.dot(ref, reward), np.dot(new, reward)
    divergence = kl(new, ref, False)
    threshold = (new_reward - old_reward) / divergence
    report(9, [near(divergence, .0851, 4),
               near([old_reward, new_reward, kl(ref, ref, False)], [.5, .7, 0], 12),
               near(threshold, 2.35, 2),
               near(new_reward - divergence, .615, 3),
               near(new_reward - 10 * divergence, -.15, 2),
               new_reward - divergence > old_reward,
               new_reward - 10 * divergence < old_reward])

    scores = [2, 1, 0]
    q10 = softmax(scores)
    report(10, [
        near(np.exp(scores), [7.389, 2.718, 1], 3),
        near(np.exp(scores).sum(), 11.107, 3),
        near(q10, [.6652, .2447, .0900], 4),
        near(q10.sum(), 1, 12), np.all(q10 > 0),
        near(softmax([1000, 999, 998]), q10, 12),
    ])

    c = s.symbols("c", real=True)
    logits = [s.log(2) + c, c, c]
    weights = [s.exp(v) for v in logits]
    recovered = [s.simplify(v / sum(weights)) for v in weights]
    report(11, [recovered == [s.Rational(1, 2), s.Rational(1, 4), s.Rational(1, 4)],
                s.simplify(logits[0] - logits[1] - s.log(2)) == 0,
                s.simplify(logits[1] - logits[2]) == 0])

    losses = np.log(np.exp(scores).sum()) - np.asarray(scores)
    report(12, [near(losses, [.4076, 1.4076, 2.4076], 4),
                near(losses, -np.log(q10), 12),
                losses[0] < losses[1] < losses[2]])

    zs = s.symbols("z0:3", real=True)
    loss = -zs[1] + s.log(sum(s.exp(v) for v in zs))
    gradient = np.array([float(s.diff(loss, v).subs(dict(zip(zs, scores)))) for v in zs])
    updated = np.asarray(scores) - gradient
    updated_probs = softmax(updated)
    updated_loss = -np.log(updated_probs[1])
    report(13, [
        near(gradient, [.6652, -.7553, .0900], 4), near(gradient.sum(), 0, 12),
        near(updated, [1.3348, 1.7553, -.0900], 4),
        near(updated_probs, [.3619, .5511, .0871], 4),
        near(updated_loss, .5959, 4),
        updated_probs[1] > q10[1], updated_loss < losses[1],
    ])

    theta = s.symbols("theta", positive=True)
    likelihood = theta ** 7 * (1 - theta) ** 3
    avg_loss = -s.log(likelihood) / 10
    optimum = s.solve(s.diff(avg_loss, theta), theta)
    phat = [.7, .3]
    table = [[ce(phat, [v, 1 - v], False), kl(phat, [v, 1 - v], False)]
             for v in [.5, .6, .7, .8]]
    lesson = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")
    erratum_recorded = "| 0.8 | 0.6390 | 0.0282 |" in lesson  # 早期稿四舍五入写成 0.0281，已改正
    print(f"NOTE 例14 theta=0.8: computed KL={table[-1][1]:.10f}; lesson 0.0282")
    report("14", [optimum == [s.Rational(7, 10)],
                near(table, [[.6931, .0823], [.6325, .0216],
                             [.6109, 0], [.6390, .0282]], 4),
                near(entropy(phat, False), .6109, 4), erratum_recorded])

    probabilities = np.array([.5, .25, .1])
    avg = -np.log(probabilities).mean()
    perplexity = np.exp(avg)
    report(15, [near(avg, 1.461, 3), near(perplexity, 4.31, 2),
                near(perplexity, np.prod(probabilities) ** (-1 / 3), 12)])

    # Also check the numerical temperature table between examples 11 and 12.
    distributions = [softmax(scores, temp) for temp in [.5, 1, 2]]
    values = [entropy(p, False) for p in distributions]
    report("10（温度表）", [
        near(distributions, [[.8668, .1173, .0159], [.6652, .2447, .0900],
                             [.5065, .3072, .1863]], 4),
        near(values, [.441, .832, 1.020], 3),
        values[0] < values[1] < values[2] < np.log(3),
    ])


if __name__ == "__main__":
    run()
    sys.exit(bool(failures))
