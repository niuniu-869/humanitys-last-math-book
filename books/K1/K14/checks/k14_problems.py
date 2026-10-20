"""Recompute from problem data, then compare with the stated answer values.

Expected values below are answer assertions, never substitutes for calculations.
Text anchors also detect drift between these assertions and answers.md.
Only the general proof is marked MANUAL; finite claims use exhaustive checks.
"""

from itertools import combinations, product
from pathlib import Path
import re
import sys

import numpy as np
import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = {
    m.group(1): m.group(2)
    for m in re.finditer(
        r"^\*\*(K14-\d+)\*\*\n(.*?)(?=^\*\*K14-\d+\*\*|\Z)",
        ANSWERS,
        re.M | re.S,
    )
}
R = s.Rational
failures = []


def same(actual, expected):
    if isinstance(actual, s.Expr) and isinstance(expected, (s.Expr, int)):
        assert s.simplify(actual - expected) == 0, (actual, expected)
    else:
        assert actual == expected, (actual, expected)


def anchors(pid, *fragments):
    for fragment in fragments:
        assert fragment in BLOCKS[pid], (pid, "answer text drift", fragment)


def run(pid, calculation):
    try:
        calculation()
    except Exception as exc:
        failures.append(pid)
        print(f"FAIL {pid}: {exc}")
    else:
        print(f"PASS {pid}")


def check_choices(pid, truth, winner):
    actual_winners = [chr(65 + i) for i, value in enumerate(truth) if value]
    same(actual_winners, [winner])
    anchors(pid, f"**答案：** ({winner})")
    for i, value in enumerate(truth):
        label = chr(65 + i)
        same(bool(value), label == winner)
        print(f"PASS {pid}({label})")


def posterior(prior, likelihood_h, likelihood_not_h):
    # Direct joint-probability normalization, independent of odds calculations.
    h_mass = prior * likelihood_h
    other_mass = (1 - prior) * likelihood_not_h
    return s.cancel(h_mass / (h_mass + other_mass))


def p01():
    n = s.symbols("n", integer=True, positive=True)
    f = n + 1
    g = n + 1 + (n - 1) * (n - 2) * (n - 3)
    values = [(f.subs(n, i), g.subs(n, i)) for i in range(1, 5)]
    same(values, [(2, 2), (3, 3), (4, 4), (5, 11)])
    same(s.solve(g - f, n), [1, 2, 3])
    # The proposed induction step already fails from k=3 to k+1=4.
    same(bool(s.Implies(s.Eq(f.subs(n, 3), g.subs(n, 3)),
                        s.Eq(f.subs(n, 4), g.subs(n, 4)))), False)
    anchors("K14-01", "$2,3,4$", "$f(4)=5$", "$g(4)=11$", "不能推出全称结论")


def p02():
    prior, lr = R(1, 5), s.Integer(3)
    # Choose likelihoods with the stated ratio; their common scale cancels.
    q = posterior(prior, R(3, 5), R(1, 5))
    options = [R(3, 5), R(3, 4), R(3, 7), R(1, 13)]
    check_choices("K14-02", [q == option for option in options], "C")
    same(prior * lr, options[0])
    same(prior / (1 - prior) * lr, options[1])
    reversed_odds = prior / (1 - prior) / lr
    same(reversed_odds / (1 + reversed_odds), options[3])
    anchors("K14-02", r"\frac37")


def p03():
    rows = np.array([[1, 1, 0, 1], [1, 1, 1, 1],
                     [0, 1, 0, 0], [0, 0, 1, 0]])
    positive, negative = rows[rows[:, 3] == 1], rows[rows[:, 3] == 0]
    common = np.all(positive[:, :3] == 1, axis=0)
    candidates = common & np.all(negative[:, :3] == 0, axis=0)
    names = np.array(["A", "B", "C"])
    same(names[common].tolist(), ["A", "B"])
    same(names[candidates].tolist(), ["A"])
    pairs = [(i + 1, j + 1) for i, j in combinations(range(4), 2)
             if rows[i, 3] != rows[j, 3]
             and np.flatnonzero(rows[i, :3] != rows[j, :3]).tolist() == [0]]
    same(pairs, [(1, 3)])
    # Two models fit: Y=A, or hidden Z=A on these rows and Y=Z.
    hidden_z = rows[:, 0].copy()
    assert np.array_equal(rows[:, 3], hidden_z)
    # Holding Z=0, the second model has no Y change when A changes.
    same([int(hidden_z[2]) for _a in (0, 1)], [0, 0])
    anchors("K14-03", "正面共有 $A,B$", "符合要求的是 $A$", "①与③")


def p04():
    rates = [R(3, 4), R(1, 2), R(2, 3)]
    # Enumerate first failure and all-success paths; verify the full partition.
    paths = []
    surviving = s.Integer(1)
    for rate in rates:
        paths.append(surviving * (1 - rate))
        surviving *= rate
    same(sum(paths) + surviving, 1)
    options = [R(23, 12), R(3, 4), R(1, 4), R(23, 36)]
    check_choices("K14-04", [surviving == option for option in options], "C")
    same(sum(rates), options[0])
    same(rates[0], options[1])
    same(sum(rates) / len(rates), options[3])
    anchors("K14-04", r"=\frac14")


def p05():
    yes = [70, 75]
    no = [60, 80]
    differences = [100 * (R(a, 100) - R(b, 100)) for a, b in zip(yes, no)]
    overall = 100 * (R(sum(yes), 200) - R(sum(no), 200))
    same(differences, [10, -5])
    same(overall, R(5, 2))
    same(all(d > 0 for d in differences), False)
    # A balanced random split of four distinguishable objects need not balance
    # an unrelated binary attribute. All six assignments have positive chance.
    attribute = [1, 1, 0, 0]
    balanced = [sum(attribute[i] for i in pair) == 1
                for pair in combinations(range(4), 2)]
    same(R(sum(balanced), len(balanced)), R(2, 3))
    assert not all(balanced)
    # With no treatment effect, the observed counts still have positive
    # probability under independent Bernoulli outcomes with chance 1/2.
    probability_under_no_effect = s.prod(s.binomial(100, k) / s.Integer(2)**100
                                       for k in yes + no)
    assert probability_under_no_effect > 0
    anchors("K14-05", "$10$ 个百分点", "$-5$ 个百分点", "$2.5$ 个百分点",
            "(2) 不成立", "不能保证完全相同")


def p06():
    raw = np.array(list(product((0, 1), repeat=2)))
    selected = raw[raw.sum(axis=1) == 1]

    def probability_y1(data, x):
        subset = data[data[:, 0] == x]
        return R(int(subset[:, 1].sum()), len(subset))

    before = [probability_y1(raw, x) for x in (0, 1)]
    after = [probability_y1(selected, x) for x in (0, 1)]
    joint = R(int(np.all(raw == (1, 1), axis=1).sum()), len(raw))
    # In the given independent generating model, changing one chosen coordinate
    # leaves the other unchanged. This is a countermodel to causal entailment.
    def generate(seeds, forced_x=None, forced_y=None):
        x = seeds[0] if forced_x is None else forced_x
        y = seeds[1] if forced_y is None else forced_y
        return x, y

    y_changes_when_x_set = [generate(seeds, forced_x=1)[1]
                            - generate(seeds, forced_x=0)[1] for seeds in raw]
    x_changes_when_y_set = [generate(seeds, forced_y=1)[0]
                            - generate(seeds, forced_y=0)[0] for seeds in raw]
    truth = [any(v != 0 for v in y_changes_when_x_set),
             any(v != 0 for v in x_changes_when_y_set),
             joint == 0,
             before == [R(1, 2), R(1, 2)] and after == [1, 0]]
    check_choices("K14-06", truth, "D")
    same(joint, R(1, 4))
    anchors("K14-06", r"\frac12", "$1$ 和 $0$", r"\frac14")


def p07():
    p = s.symbols("p", real=True)
    q = posterior(p, R(3, 4), R(1, 4))
    feasible = s.solve_univariate_inequality(q >= R(2, 3), p, relational=False)
    feasible = feasible.intersect(s.Interval.open(0, R(1, 2)))
    same(feasible, s.Interval.Ropen(R(2, 5), R(1, 2)))
    same(q.subs(p, R(2, 5)), R(2, 3))
    anchors("K14-07", r"\frac25\le p<\frac12", "左端能取到")


def p08():
    prior, a, b = R(1, 3), R(1, 2), R(1, 4)
    # Enumerate the joint outcomes of duplicate records: only 11 and 00 exist.
    h = {(1, 1): a, (0, 0): 1 - a}
    nh = {(1, 1): b, (0, 0): 1 - b}
    actual = posterior(prior, h[(1, 1)], nh[(1, 1)])
    mistaken = posterior(prior, a * a, b * b)
    same((actual, mistaken), (R(1, 2), R(2, 3)))
    same((a, a * a, b, b * b), (R(1, 2), R(1, 4), R(1, 4), R(1, 16)))
    assert a != a * a and b != b * b
    anchors("K14-08", r"真实后验为 $\frac12$", r"错误算法给出 $\frac23$",
            r"\frac1{16}", "两种条件下都不独立")


def p09():
    a, b = s.symbols("a b")
    models = [a, b, a * b]

    def predictions(cases):
        return [tuple(m.subs({a: av, b: bv}) for av, bv in cases) for m in models]

    same(predictions([(0, 0), (1, 1)]), [(0, 1)] * 3)
    cases = [(0, 1), (1, 0)]
    minimum = next(size for size in range(3)
                   if any(len(set(predictions(subset))) == len(models)
                          for subset in combinations(cases, size)))
    signatures = predictions(cases)
    same(minimum, 2)
    same(signatures, [(0, 1), (1, 0), (0, 0)])
    same([i + 1 for i, signature in enumerate(signatures) if signature == (1, 0)], [2])
    same([i + 1 for i, signature in enumerate(signatures) if signature == (1, 1)], [])
    anchors("K14-09", "一个也不能排除", "最少需要两个新场合", "选中 $H_2$",
            "$(1,1)$ 与三个规则都不相容", "| $H_1:Y=A$ | $(0,1)$ |",
            "| $H_2:Y=B$ | $(1,0)$ |", "| $H_3:Y=AB$ | $(0,0)$ |")


def p10():
    t = s.symbols("t", real=True)
    px, py = R(1, 3), R(2, 3)
    raw = {(x, y): (px if x else 1 - px) * (py if y else 1 - py)
           for x, y in product((0, 1), repeat=2)}
    kept = {(x, y): mass * (t if x == y else R(1, 2))
            for (x, y), mass in raw.items()}
    same(sum(raw.values()), 1)
    same(list(raw.values()), [R(2, 9), R(4, 9), R(1, 9), R(2, 9)])
    same(list(kept.values()), [2 * t / 9, R(2, 9), R(1, 18), 2 * t / 9])
    rates = [s.cancel(kept[x, 1] / (kept[x, 0] + kept[x, 1])) for x in (0, 1)]
    same(rates[0], 1 / (1 + t))
    same(rates[1], 4 * t / (1 + 4 * t))
    gap = s.factor(rates[1] - rates[0])
    domain = s.Interval(0, 1)
    for relation, expected in [(gap > 0, s.Interval.Lopen(R(1, 2), 1)),
                               (gap < 0, s.Interval.Ropen(0, R(1, 2)))]:
        actual = s.solve_univariate_inequality(relation, t, relational=False)
        same(actual.intersect(domain), expected)
    same(s.solveset(gap, t, domain=domain), s.FiniteSet(R(1, 2)))
    # Endpoint conditioning events have positive mass, including when t=0.
    for endpoint in (0, R(1, 2), 1):
        for x in (0, 1):
            assert (kept[x, 0] + kept[x, 1]).subs(t, endpoint) > 0
    same([raw[x, 1] / (raw[x, 0] + raw[x, 1]) for x in (0, 1)], [py, py])
    # An explicit independent generation model: changing X leaves the Y seed.
    seeds = list(product(range(3), repeat=2))
    for forced_x in (0, 1):
        generated = [(forced_x, int(y_seed < 2)) for _x_seed, y_seed in seeds]
        same(R(sum(y for _x, y in generated), len(generated)), py)
    anchors("K14-10", r"\frac1{1+t}", r"\frac{4t}{1+4t}",
            r"\frac12<t\le1", r"t=\frac12", r"0\le t<\frac12", "关联来自筛选")


def p11_counterexample():
    rows = [(R(1, 4),) * 4, (R(1, 4), 0, 0, R(3, 4))]
    marginal = []
    for row in rows:
        same(sum(row), 1)
        assert all(value >= 0 for value in row)
        marginal.append((row[0] + row[1], row[0] + row[2]))
    (eh, fh), (en, fn) = marginal
    same(rows[0][0], eh * fh)
    assert rows[1][0] != en * fn
    assert en > 0 and fn > 0 and rows[1][0] > 0
    same((eh / en, fh / fn, rows[0][0] / rows[1][0]), (2, 2, 1))
    assert rows[0][0] / rows[1][0] != (eh / en) * (fh / fn)
    anchors("K14-11", "联合似然比为 $1$", "单条似然比的乘积为 $4$",
            r"\frac14\ne\frac1{16}", r"1\ne2\times2=4")


def p12():
    rows = list(product((True, False), repeat=2))
    h = s.Matrix([[R(2, 5), R(3, 10), R(1, 10), R(1, 5)]])
    nh = s.Matrix([[R(1, 10), R(1, 10), R(3, 10), R(1, 2)]])
    same(sum(h), 1)
    same(sum(nh), 1)
    e_mask = s.Matrix([int(e) for e, _f in rows])
    f_mask = s.Matrix([int(f) for _e, f in rows])
    g_mask = s.Matrix([int(bool(s.Implies(e, f))) for e, f in rows])
    union_mask = s.Matrix([int((not e) or f) for e, f in rows])
    same(g_mask, union_mask)
    joint_mask = s.Matrix([int(e and f) for e, f in rows])
    eh, en = (h * e_mask)[0], (nh * e_mask)[0]
    fh, fn = (h * f_mask)[0], (nh * f_mask)[0]
    same((eh / en, fh / fn), (R(7, 2), R(5, 4)))
    assert eh / en > 1 and fh / fn > 1
    gh, gn = (h * g_mask)[0], (nh * g_mask)[0]
    same((gh, gn), (R(7, 10), R(9, 10)))
    qg = posterior(R(1, 4), gh, gn)
    same(qg, R(7, 34))
    assert qg < R(1, 4)
    jh, jn = (h * joint_mask)[0], (nh * joint_mask)[0]
    same(posterior(R(1, 4), jh, jn), R(4, 7))
    same(posterior(R(1, 4), eh * fh, en * fn), R(35, 59))
    same((eh * fh, en * fn), (R(7, 20), R(2, 25)))
    assert jh != eh * fh and jn != en * fn
    anchors("K14-12", r"LR_E=\frac72", r"LR_F=\frac54", r"G=\neg E\cup F",
            r"P(H\mid G)=\frac7{34}", r"正确后验为 $\frac47$",
            r"\frac{35}{59}", r"\frac7{20}", r"\frac2{25}")


if __name__ == "__main__":
    expected_ids = {f"K14-{i:02d}" for i in range(1, 13)}
    if set(BLOCKS) != expected_ids:
        print("FAIL K14-coverage: answer identifiers differ")
        sys.exit(1)
    for number, check in [(1, p01), (2, p02), (3, p03), (4, p04), (5, p05),
                          (6, p06), (7, p07), (8, p08), (9, p09), (10, p10)]:
        run(f"K14-{number:02d}", check)
    print("MANUAL K14-11: proof of likelihood-ratio multiplication under both conditional independence assumptions")
    run("K14-11-counterexample", p11_counterexample)
    run("K14-12", p12)
    sys.exit(bool(failures))
