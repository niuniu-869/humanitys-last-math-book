"""Enumerate small instances independently, then compare with answers.md.

Expected values are read from the answer text where practical. Exhaustive
enumeration, rather than the proposed recurrence, supplies the reference.
"""

from collections import Counter
from itertools import combinations, product
from pathlib import Path
import re
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]


def blocks(filename):
    text = (ROOT / filename).read_text(encoding="utf-8")
    return {
        match[1]: match[2]
        for match in re.finditer(
            r"^\*\*(K34-\d+)\*\*(.*?)(?=^\*\*K34-\d+\*\*|\Z)",
            text, re.M | re.S,
        )
    }


def number(text):
    return sp.sympify(text.strip().strip("$").replace(r"\infty", "oo"))


def arrays(text):
    return [
        [number(value) for value in row.split(",")]
        for row in re.findall(r"\$\$\[([^\]]+)\]\.\$\$", text)
    ]


def table_row(text, label):
    line = next(line for line in text.splitlines() if line.startswith(f"| ${label}$ |"))
    return [number(value) for value in line.split("|")[2:-1]]


def equal(actual, expected):
    assert actual == expected, f"computed={actual!r}; printed={expected!r}"


def contains(text, fragment):
    assert fragment in text, f"Answer no longer contains checked claim: {fragment}"


def coin_vectors(coins, amount):
    return [
        counts for counts in product(*(range(amount // c + 1) for c in coins))
        if sum(c * n for c, n in zip(coins, counts)) == amount
    ]


def min_terms(coins, amount):
    return min((sum(counts) for counts in coin_vectors(coins, amount)), default=sp.oo)


def ordered_sums(amount, parts):
    if amount == 0:
        return [()]
    return [
        (first,) + rest
        for first in parts if first <= amount
        for rest in ordered_sums(amount - first, parts)
    ]


def subsets(n):
    return [indices for size in range(n + 1) for indices in combinations(range(n), size)]


def grid_paths(rows, cols):
    paths = []
    for down in combinations(range(rows + cols - 2), rows - 1):
        i, j = 1, 1
        path = [(i, j)]
        for step in range(rows + cols - 2):
            if step in down:
                i += 1
            else:
                j += 1
            path.append((i, j))
        paths.append(tuple(path))
    return paths


def interval_subsets(intervals):
    return [
        choice for choice in subsets(len(intervals))
        if all(
            intervals[i][1] <= intervals[j][0] or intervals[j][1] <= intervals[i][0]
            for i, j in combinations(choice, 2)
        )
    ]


def pack_enumerated(items, capacity, limits=None, exact=False):
    if limits is None:
        limits = [1] * len(items)
    candidates = []
    for counts in product(*(
        range(capacity // w + 1 if limit is None else limit + 1)
        for (w, _), limit in zip(items, limits)
    )):
        weight = sum(w * n for (w, _), n in zip(items, counts))
        feasible = weight == capacity if exact else weight <= capacity
        if feasible:
            value = sum(v * n for (_, v), n in zip(items, counts))
            candidates.append((value, counts))
    best = max((v for v, _ in candidates), default=-sp.oo)
    return best, [counts for v, counts in candidates if v == best]


def roll(items, capacity, ascending):
    row = [sp.Integer(0)] * (capacity + 1)
    for (w, v), forward in zip(items, ascending):
        order = range(w, capacity + 1) if forward else range(capacity, w - 1, -1)
        for c in order:
            row[c] = max(row[c], row[c - w] + v)
    return row


def choice_check(pid, truth, answer):
    correct = [letter for letter, value in zip("ABCD", truth) if value]
    equal(len(correct), 1)
    equal(re.search(r"选 ([ABCD])", answer)[1], correct[0])
    for letter, value in zip("ABCD", truth):
        print(f"PASS {pid} 选项{letter}={'真' if value else '假'}")


def check_01(p, a):
    equal([min_terms((3, 5), n) for n in range(11)], arrays(a)[0])
    contains(a, r"m(a)=1+\min\{m(a-3),m(a-5)\}")
    for n in range(1, 11):
        previous = [min_terms((3, 5), n - c) if n >= c else sp.oo for c in (3, 5)]
        equal(min_terms((3, 5), n), 1 + min(previous))


def check_02(p, a):
    cache, stats = {}, Counter()

    def fib(n):
        stats["calls"] += 1
        if n <= 1:
            return sp.Integer(n)
        if n in cache:
            stats["hits"] += 1
            return cache[n]
        value = fib(n - 1) + fib(n - 2)
        stats["adds"] += 1
        cache[n] = value
        return value

    value = fib(6)
    options = [int(x) for x in re.findall(r"\([ABCD]\) \$(\d+)\$ 次", p)]
    equal(len(options), 4)
    choice_check("K34-02", [stats["adds"] == x for x in options], a)
    equal(value, sp.fibonacci(6))
    equal(stats["calls"], int(re.search(r"C 的 \$(\d+)\$", a)[1]))
    equal(value, int(re.search(r"F\(6\)=(\d+)", a)[1]))
    equal(sorted(cache), list(range(2, 7)))


def check_03(p, a):
    row = [sum((1, 3) not in path for path in grid_paths(1, j)) for j in range(1, 5)]
    options = [[int(x) for x in group.split(",")]
               for group in re.findall(r"\([ABCD]\) \$\(([^)]+)\)", p)]
    equal(len(options), 4)
    choice_check("K34-03", [row == option for option in options], a)


def check_04(p, a):
    values = [2, 4, 7]
    totals = {sum(values[i] for i in chosen) for chosen in subsets(3)}
    truth = [s in totals for s in (0, 6, 8)]
    printed = [x == "真" for x in re.search(r"依次为([真假、]+)", a)[1].split("、")]
    equal(truth, printed)
    contains(a, r"\{2,4\}")


def check_05(p, a):
    intervals = [(0, 3), (1, 3), (3, 5), (2, 6)]
    feasible = interval_subsets(intervals)
    best = max(map(len, feasible))
    actual = {tuple(i + 1 for i in choice) for choice in feasible if len(choice) == best}
    printed = {tuple(map(int, pair)) for pair in re.findall(r"\\\{I_(\d),I_(\d)\\\}", a)}
    equal(actual, printed)
    equal(best, int(re.search(r"最大个数为 \$(\d+)\$", a)[1]))


def check_06(p, a):
    feasible = interval_subsets([(0, 2), (2, 5), (0, 5)])
    rewards = sp.Matrix([3, 4, 9])
    optimum = (max(map(len, feasible)), max(sum(rewards[i] for i in s) for s in feasible))
    options = [(int(count), int(value)) for count, value in re.findall(
        r"\([ABCD]\) 最多安排 \$(\d+)\$ 个，最高收益为 \$(\d+)\$", p)]
    equal(len(options), 4)
    choice_check("K34-06", [optimum == option for option in options], a)
    equal(sum(rewards[i] for i in (0, 1)), 7)
    assert (0, 1) in feasible and (2,) in feasible and (0, 1, 2) not in feasible


def check_07(p, a):
    candidates = [{k for k in range(2, 8) if min_terms((1, k, 8), target) == 2}
                  for target in (10, 12)]
    printed = [{int(x) for x in group.split(",")} for group in re.findall(r"p\\in\\\{([^}]+)\\\}", a)]
    equal(candidates, printed)
    equal(candidates[0] & candidates[1], set())
    contains(a, "不存在这样的")


def check_08(p, a):
    t = sp.Symbol("t", real=True)
    costs = sp.Matrix([[1, 2, 4], [2, t, 2], [4, 2, 1]])
    groups = {True: set(), False: set()}
    for path in grid_paths(3, 3):
        groups[(2, 2) in path].add(sp.expand(sum(costs[i - 1, j - 1] for i, j in path)))
    equal(groups, {True: {t + 6}, False: {sp.Integer(10)}})
    equal(sp.solve(t + 6 - 10, t), [sp.Integer(4)])
    actual_range = sp.reduce_inequalities([t >= 0, t + 6 < 10], t)
    equal(actual_range.as_set(), sp.Interval.Ropen(0, 4))
    contains(a, r"g(t)=\min(t+6,10)")
    for fragment in (r"0\le t<4", "$t=4$", "$t>4$"):
        contains(a, fragment)


def check_09(p, a):
    items = [(2, 4), (3, 8), (5, 9)]
    best, choices = pack_enumerated(items, 6)
    equal(best, int(re.search(r"最大值为 \$(\d+)\$", a)[1]))
    printed = tuple(map(int, re.search(r"\(x_1,x_2,x_3\)=\(([^)]+)\)", a)[1].split(",")))
    equal(choices, [printed])
    equal([pack_enumerated(items, c, exact=True)[0] for c in range(7)], arrays(a)[0])
    equal(pack_enumerated(items, 6, exact=True)[1], [])
    equal(roll(items, 6, [False] * 3)[6], best)
    contains(a, "权重和恰为 $6$ 时无解")


def check_10(p, a):
    items = [(2, 3), (3, 5)]
    good = [pack_enumerated(items, c, [None, 1])[0] for c in range(8)]
    bad = [pack_enumerated(items, c, [None, None])[0] for c in range(8)]
    equal([good, bad], arrays(a))
    equal(roll(items, 7, [True, False]), good)
    equal(roll(items, 7, [True, True]), bad)
    first = next(c for c in range(8) if good[c] != bad[c])
    equal(first, int(re.search(r"错误下标为 \$(\d+)\$", a)[1]))
    equal(good[7], bad[7])


def check_12(p, a):
    def legal(seq):
        return all(pair != (2, 2) for pair in zip(seq, seq[1:]))

    all_legal = [[seq for seq in ordered_sums(n, (1, 2)) if legal(seq)] for n in range(9)]
    u = [1] + [sum(seq[-1] == 1 for seq in row) for row in all_legal[1:]]
    v = [0] + [sum(seq[-1] == 2 for seq in row) for row in all_legal[1:]]
    equal(u, table_row(a, "u(n)"))
    equal(v, table_row(a, "v(n)"))
    for n in range(1, 9):
        equal(u[n], u[n - 1] + v[n - 1])
        equal(v[n], u[n - 2] if n >= 2 else 0)
    counts = Counter(seq.count(2) for seq in all_legal[8])
    equal(sorted(counts), list(range(4)))
    equal([counts[k] for k in range(4)], [sp.binomial(9 - 2 * k, k) for k in range(4)])
    equal(len(all_legal[8]), int(re.search(r"共 \$(\d+)\$ 种", a)[1]))
    printed = [int(x) for x in re.search(r"分别有 \$([\d,]+)\$", a)[1].split(",")]
    equal([counts[k] for k in range(4)], printed)
    equal(set(ordered_sums(4, (1, 2))) - set(all_legal[4]), {(2, 2)})


def check_13(p, a):
    special = {(2, 2), (3, 3)}
    paths = grid_paths(4, 5)
    counts = Counter(len(set(path) & special) for path in paths)
    printed = tuple(map(int, re.search(r"值为 \$\(([\d,]+)\)\$", a)[1].split(",")))
    equal(tuple(counts[k] for k in range(3)), printed)
    via_p = sum((2, 2) in path for path in paths)
    via_q = sum((3, 3) in path for path in paths)
    both = counts[2]
    equal(via_p, sp.binomial(2, 1) * sp.binomial(5, 2))
    equal(via_q, sp.binomial(4, 2) * sp.binomial(3, 1))
    equal(both, sp.binomial(2, 1) ** 2 * sp.binomial(3, 1))
    equal(via_p + via_q - 2 * both, counts[1])
    contains(a, f"{via_p}+{via_q}-2\\times{both}={counts[1]}")
    equal(len(paths), sp.binomial(7, 3))
    table = {}
    for i in range(1, 5):
        for j in range(1, 6):
            for k in range(3):
                if (i, j) == (1, 1):
                    value = int(k == 0)
                else:
                    previous = k - int((i, j) in special)
                    value = table.get((i - 1, j, previous), 0) + table.get((i, j - 1, previous), 0)
                table[i, j, k] = value
                equal(value, sum(len(set(path) & special) == k for path in grid_paths(i, j)))


def check_14(p, a):
    values = [1, 2, 2, 3, 4, 5]
    m = [[sp.oo] * 8 for _ in range(7)]
    q = [[0] * 8 for _ in range(7)]
    m[0][0], q[0][0] = 0, 1
    for i, value in enumerate(values, 1):
        for s in range(8):
            u, v = m[i - 1][s], 1 + m[i - 1][s - value] if s >= value else sp.oo
            m[i][s] = min(u, v)
            q[i][s] = 0 if m[i][s] == sp.oo else (
                (q[i - 1][s] if u == m[i][s] else 0)
                + (q[i - 1][s - value] if s >= value and v == m[i][s] else 0)
            )
    for i in range(7):
        for s in range(8):
            candidates = [indices for indices in subsets(i) if sum(values[j] for j in indices) == s]
            best = min(map(len, candidates), default=sp.oo)
            equal(m[i][s], best)
            equal(q[i][s], sum(len(indices) == best for indices in candidates))
    winners = [tuple(i + 1 for i in indices) for indices in subsets(6)
               if len(indices) == m[6][7] and sum(values[i] for i in indices) == 7]
    printed = [tuple(map(int, pair)) for pair in re.findall(r"\\\{(\d),(\d)\\\}", a)]
    equal(winners, printed)
    equal([row[7] for row in m], table_row(a, "m_i(7)"))
    equal([row[7] for row in q], table_row(a, "q_i(7)"))
    equal(m[6][7], int(re.search(r"最少选 \$(\d+)\$", a)[1]))
    equal(q[6][7], int(re.search(r"共 \$(\d+)\$ 种", a)[1]))
    mr, qr = [0] + [sp.oo] * 7, [1] + [0] * 7
    for i, value in enumerate(values, 1):
        for s in range(7, value - 1, -1):
            old, take = mr[s], mr[s - value] + 1
            best = min(old, take)
            count = 0 if best == sp.oo else (
                (qr[s] if old == best else 0) + (qr[s - value] if take == best else 0)
            )
            mr[s], qr[s] = best, count
        equal(mr, m[i])
        equal(qr, q[i])


def main():
    problems, answers = blocks("problems.md"), blocks("answers.md")
    expected_ids = {f"K34-{i:02}" for i in range(1, 15)}
    equal(set(problems), expected_ids)
    equal(set(answers), expected_ids)
    failures = 0
    for i in range(1, 15):
        pid = f"K34-{i:02}"
        if i == 11:
            print(f"MANUAL {pid} 逐段检查必选区间分组及交换论证")
            continue
        try:
            globals()[f"check_{i:02}"](problems[pid], answers[pid])
            print(f"PASS {pid}")
        except Exception as error:
            failures += 1
            print(f"FAIL {pid} {type(error).__name__}: {error}")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
