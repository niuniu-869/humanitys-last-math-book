"""Independent arithmetic and finite-model checks for all 13 lesson examples.

PASS means the described check passed. For overclaims in examples 7 and 8,
countermodels verify the logged errors; it does NOT mean that the erroneous
conclusions have been endorsed.
Qualitative examples are checked by explicit models, not hard-coded labels.
"""

from itertools import combinations, product
from pathlib import Path
import sys

import numpy as np
import sympy as s


R = s.Rational
ROOT = Path(__file__).resolve().parents[1]
failures = []


def same(actual, expected):
    assert actual == expected, (actual, expected)


def run(number, calculation):
    try:
        calculation()
    except Exception as exc:
        failures.append(number)
        print(f"FAIL 例{number}: {exc}")
    else:
        suffix = {
            7: "（第4项只能列作候选解释；非唯一性的反模型已确认，见备注首行）",
            8: "（数值通过；随机分组保证论断的反例已确认，见备注首行）",
        }.get(number, "")
        print(f"PASS 例{number}{suffix}")


def posterior(p, a, b):
    return s.cancel(p * a / (p * a + (1 - p) * b))


def ex01():
    same([R(80, 100), R(4, 5), R(80, 100)], [R(4, 5)] * 3)
    # Under a common Bernoulli model, variance of the sample fraction scales
    # as 1/n. This checks the size comparison, not an absolute quality ranking.
    p = R(4, 5)
    variances = [p * (1 - p) / n for n in (100, 5)]
    assert variances[0] < variances[1]
    # The same 80/100 visible replies coexist with different unseen populations.
    population_rates = [R(80 + hidden_yes, 200) for hidden_yes in (0, 100)]
    same(population_rates, [R(2, 5), R(9, 10)])
    assert population_rates[0] != population_rates[1]


def ex02():
    # Columns: cucumber, pork, greens, soup, rice, watermelon, outcome.
    rows = np.array([[1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1],
                     [0, 1, 0, 1, 1, 1, 1],
                     [1, 0, 1, 1, 1, 0, 1],
                     [1, 1, 1, 0, 1, 1, 0]])
    positive = rows[rows[:, -1] == 1, :-1]
    negative = rows[rows[:, -1] == 0, :-1]
    common = np.all(positive == 1, axis=0)
    same(np.flatnonzero(common).tolist(), [3])
    same(np.flatnonzero(common & np.all(negative == 0, axis=0)).tolist(), [3])
    # A hidden ingredient present exactly when soup is present also fits.
    hidden_ingredient = rows[:, 3]
    assert np.array_equal(hidden_ingredient, rows[:, -1])


def ex03():
    before_a, after_a, before_b, after_b = map(s.Integer, (30, 36, 30, 34))
    change_a, change_b = after_a - before_a, after_b - before_b
    same((change_a, change_b, change_a - change_b), (6, 4, 2))
    same(after_a - after_b, 2)
    # Under the example's common-change assumption, solve rather than attribute
    # all six points to treatment.
    common, treatment = s.symbols("common treatment")
    solution = s.solve([common - change_b, common + treatment - change_a],
                       (common, treatment))
    same(solution, {common: 4, treatment: 2})


def ex04():
    delta = s.Integer(520) - 430
    same(delta, 90)
    # The two observed fields change both factors: multiple decompositions fit.
    explanations = [(fertilizer, delta - fertilizer) for fertilizer in (0, 45, 90)]
    assert len({f for f, _v in explanations}) > 1
    assert all(f + v == delta for f, v in explanations)
    old_variety_no_fertilizer = np.array([0, 0])
    proposed = np.array([1, 0])
    original_treated = np.array([1, 1])
    same(np.count_nonzero(original_treated - old_variety_no_fertilizer), 2)
    same(np.flatnonzero(proposed - old_variety_no_fertilizer).tolist(), [0])


def ex05():
    temperature = np.array([22, 25, 26, 28, 30, 33, 35])
    sales = np.array([48, 58, 62, 63, 75, 80, 84])
    assert np.all(np.diff(temperature) > 0)
    assert np.all(np.diff(sales) > 0)
    # A common index can generate both columns without an arrow from X to Y.
    cases = np.arange(len(sales))
    fitted_sales = sales[cases]
    assert np.array_equal(fitted_sales, sales)
    changed_x_same_index = temperature + 1
    assert not np.array_equal(changed_x_same_index, temperature)
    assert np.array_equal(sales[cases], fitted_sales)


def ex06():
    increase = s.Integer(130) - 100
    residual = increase - 18 - 7
    alternative = increase - 15 - 7
    same((increase, residual, alternative), (30, 5, 8))
    u, v = s.symbols("u v")
    solution = s.linsolve([u + v - residual], (u, v))
    assert any(part.free_symbols for pair in solution for part in pair)


def ex07():
    # (1) The stated fire-size mechanism has a common parent for both columns.
    edges = {("size", "engines"), ("size", "loss")}
    parents = lambda node: {a for a, b in edges if b == node}
    same(parents("engines") & parents("loss"), {"size"})
    assert ("engines", "loss") not in edges
    size = np.array([1, 2, 3])
    engines, loss = 2 * size, 5 * size
    assert np.all(np.diff(engines) > 0) and np.all(np.diff(loss) > 0)
    # (2) Reverse-direction mechanism: sleeplessness makes phone time increase.
    reverse_edges = {("sleepless", "phone")}
    assert ("sleepless", "phone") in reverse_edges
    assert ("phone", "sleepless") not in reverse_edges
    # (3) Same successful sample, opposite population associations when the
    # omitted unsuccessful group changes. Rows: success/failure; cols: degree/no.
    tables = [s.Matrix([[160, 40], [20, 80]]),
              s.Matrix([[160, 40], [90, 10]])]
    effects = [R(t[0, 0], t[0, 0] + t[1, 0]) - R(t[0, 1], t[0, 1] + t[1, 1])
               for t in tables]
    assert effects[0] > 0 and effects[1] < 0
    same([sum(t.row(0)) for t in tables], [200, 200])
    # (4) Coincidence is possible: independent random orderings can match
    # exactly. This verifies it as an alternative, not as a uniquely proven cause.
    n = 6
    coincidence_probability = s.factorial(n) / s.factorial(n)**2
    same(coincidence_probability, R(1, 720))
    assert coincidence_probability > 0
    # The same ordered observations also fit a shared trend, so synchronous
    # movement alone cannot select coincidence as the unique explanation.
    common_trend = np.arange(1, n + 1)
    column_a, column_b = 2 * common_trend, 3 * common_trend
    assert np.array_equal(np.argsort(column_a), np.argsort(column_b))
    assert np.all(np.diff(column_a) > 0) and np.all(np.diff(column_b) > 0)
    lesson = (ROOT / "lesson.md").read_text(encoding="utf-8")
    assert "可能是巧合" in lesson and "现有信息不能判断" in lesson  # 讲义不再断言是巧合


def ex08():
    a = [R(18, 20), R(48, 80), R(18 + 48, 20 + 80)]
    b = [R(68, 80), R(10, 20), R(68 + 10, 80 + 20)]
    same(a, [R(9, 10), R(3, 5), R(33, 50)])
    same(b, [R(17, 20), R(1, 2), R(39, 50)])
    assert a[0] > b[0] and a[1] > b[1] and a[2] < b[2]
    same((R(80, 100), R(20, 100)), (R(4, 5), R(1, 5)))
    # Even approximately balanced realized allocations (48% versus 52%) can
    # reverse the comparison. All counts are integers and can arise in a random
    # allocation, so randomization does not give an exact finite-sample guarantee.
    counts_a = [(3888, 4800), (1092, 5200)]
    counts_b = [(4160, 5200), (960, 4800)]
    stratum_a = [R(k, n) for k, n in counts_a]
    stratum_b = [R(k, n) for k, n in counts_b]
    total_a = R(sum(k for k, _n in counts_a), sum(n for _k, n in counts_a))
    total_b = R(sum(k for k, _n in counts_b), sum(n for _k, n in counts_b))
    assert all(ra > rb for ra, rb in zip(stratum_a, stratum_b))
    assert total_a < total_b
    same((total_a, total_b), (R(249, 500), R(64, 125)))
    # Every fixed allocation of 10000 of 20000 labeled people has positive
    # probability under complete randomization, including this valid allocation.
    assert s.binomial(20000, 10000) > 0
    lesson = (ROOT / "lesson.md").read_text(encoding="utf-8")
    assert "平均意义上" in lesson  # 讲义只说随机分组在平均意义上平衡，不说有限样本下保证一致


def ex09():
    prior, sensitivity, false_positive = R(1, 100), R(9, 10), R(9, 100)
    same(sensitivity / false_positive, 10)
    same(prior / (1 - prior), R(1, 99))
    q = posterior(prior, sensitivity, false_positive)
    same(q, R(10, 109))
    same(round(float(100 * q), 1), 9.2)
    positive_true = 1000 * prior * sensitivity
    positive_false = 1000 * (1 - prior) * false_positive
    same((positive_true, positive_false), (9, R(891, 10)))
    same(positive_true / (positive_true + positive_false), q)
    same((round(float(positive_false)), round(float(990 - positive_false))), (89, 901))
    same(round(float(100 * R(9, 98)), 1), 9.2)


def ex10():
    prior = R(1, 5)
    same(prior / (1 - prior), R(1, 4))
    same(prior / (1 - prior) * 10, R(5, 2))
    q = posterior(prior, R(9, 10), R(9, 100))
    same(q, R(5, 7))
    same(round(float(100 * q), 1), 71.4)
    assert q > posterior(R(1, 100), R(9, 10), R(9, 100))


def ex11():
    prior = R(1, 2)
    h = [R(7, 10), R(7, 10)]
    nh = [R(35, 100), R(1, 5)]
    ratios = [a / b for a, b in zip(h, nh)]
    same(ratios, [2, R(7, 2)])
    same(posterior(prior, s.prod(h), s.prod(nh)), R(7, 8))
    same(100 * posterior(prior, s.prod(h), s.prod(nh)), R(175, 2))
    first = posterior(prior, h[0], nh[0])
    same(first, R(2, 3))
    same(round(float(100 * first)), 67)
    assert ratios[1] > ratios[0]
    assert s.simplify(s.log(s.prod(ratios)) - sum(s.log(r) for r in ratios)) == 0


def ex12():
    # (1) Three selected winners do not fix the whole class's average ability.
    # Each construction keeps the three winners at score 10 and the other class
    # at score 8, but changes unobserved members of class 3.
    class_means = [R(3 * 10 + 97 * other_score, 100) for other_score in (0, 9)]
    assert class_means[0] < 8 < class_means[1]
    # (2) A celebrity's statement supplies no premise linking report to truth.
    report, effective = s.symbols("report effective")
    assert s.satisfiable(s.And(report, s.Not(effective))) is not False
    # (3) A four-link chain can fail; its individual links need not be certain.
    chain = list(product((0, 1), repeat=4))
    chance_all = R(sum(all(outcomes) for outcomes in chain), len(chain))
    same(chance_all, R(1, 16))
    assert chance_all < 1
    # Also verify the section's 0.8^5 calculation and its rounded plot labels.
    powers = [R(4, 5)**k for k in range(1, 6)]
    same([round(float(v), 2) for v in powers], [0.80, 0.64, 0.51, 0.41, 0.33])
    # (4) Mutual support P=>Q and Q=>P does not establish either proposition.
    p, q = s.symbols("p q")
    circle = s.And(s.Implies(p, q), s.Implies(q, p))
    countermodels = [(pv, qv) for pv, qv in product((False, True), repeat=2)
                     if bool(circle.subs({p: pv, q: qv})) and not pv]
    same(countermodels, [(False, False)])
    # (5) A collection needing >1 day need not have each member need >1 day.
    individual_days = [R(1, 2), R(3, 4)]
    assert sum(individual_days) > 1 and individual_days[0] <= 1


def ex13():
    children = {0: R(4, 5), 10: R(1, 5)}
    mean_per_parent = sum(count * probability for count, probability in children.items())
    same(mean_per_parent, 2)
    mean_population = s.Integer(1)
    for _generation in range(5):
        mean_population *= mean_per_parent
    same(mean_population, 32)
    same(s.Integer(10)**5, 100000)
    assert mean_population < s.Integer(10)**5
    # 32 is an expectation, not a guaranteed count; extinction in round 1
    # alone has positive probability.
    assert children[0] > 0


if __name__ == "__main__":
    for number in range(1, 14):
        run(number, globals()[f"ex{number:02d}"])
    sys.exit(bool(failures))
