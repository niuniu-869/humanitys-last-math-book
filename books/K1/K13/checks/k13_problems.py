"""Enumerate the original constraints and compare with the printed answers.

The search does not use the block reductions in answers.md. In particular,
grouping searches assign every element independently before filtering.
"""

from itertools import permutations, product
from pathlib import Path
import re

import numpy as np
from sympy import Implies


ROOT = Path(__file__).resolve().parents[1]
ANSWER_TEXT = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEM_TEXT = (ROOT / "problems.md").read_text(encoding="utf-8")


def sections(text):
    matches = list(re.finditer(r"(?m)^\*\*(K13-\d{2})\*\*", text))
    return {
        m[1]: text[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        for i, m in enumerate(matches)
    }


ANSWERS = sections(ANSWER_TEXT)
PROBLEMS = sections(PROBLEM_TEXT)
failures = []


def check(label, condition):
    ok = bool(condition)
    print(f"{'PASS' if ok else 'FAIL'} {label}")
    if not ok:
        failures.append(label)
    return ok


def run(pid, operation):
    try:
        check(pid, operation())
    except Exception as error:
        check(pid, False)
        print(f"DETAIL {pid}: {type(error).__name__}: {error}")


def implication(p, q):
    return bool(Implies(bool(p), bool(q)))


def rows(n):
    return np.array(list(permutations(range(1, n + 1))), dtype=int)


def rowset(array):
    return {tuple(int(v) for v in row) for row in array}


def answer_tuples(pid, length=4):
    pattern = r"\$\((" + r"[1-4]," * (length - 1) + r"[1-4])\)\$"
    return {tuple(map(int, s.split(','))) for s in re.findall(pattern, ANSWERS[pid])}


def answer_words(pid, length):
    return set(re.findall(r"\$([a-e]{" + str(length) + r"})\$", ANSWERS[pid]))


def words(array):
    return {''.join(chr(96 + int(v)) for v in row) for row in array}


def group_assignments(capacities):
    n = sum(capacities)
    candidates = np.array(list(product(range(len(capacities)), repeat=n)), dtype=int)
    mask = np.ones(len(candidates), dtype=bool)
    for group, capacity in enumerate(capacities):
        mask &= np.sum(candidates == group, axis=1) == capacity
    return candidates[mask]


def group_sets(array, group_count=3):
    return {
        tuple(tuple(np.flatnonzero(row == g) + 1) for g in range(group_count))
        for row in array
    }


def printed_group_rows(pid):
    result = []
    for line in ANSWERS[pid].splitlines():
        if not line.startswith('|'):
            continue
        cells = re.findall(r"\\\{([0-9,]+)\\\}", line)
        if len(cells) == 3:
            result.append(tuple(tuple(map(int, cell.split(','))) for cell in cells))
    return result


def choice(pid, truths):
    match = re.search(r"\*\*答案：\*\* \(([A-D])\)", ANSWERS[pid])
    key = match[1] if match else None
    checks = []
    for letter, truth in zip('ABCD', truths):
        checks.append(check(f"{pid}({letter})", bool(truth) == (letter == key)))
    return all(checks) and sum(map(bool, truths)) == 1


def printed_numeric_options(pid):
    return [tuple(map(int, value.split(','))) for value in
            re.findall(r"- \([A-D]\) \$\(([0-9,]+)\)\$", PROBLEMS[pid])]


P4, P5 = rows(4), rows(5)
POS4, POS5 = np.argsort(P4, axis=1) + 1, np.argsort(P5, axis=1) + 1


def p01():
    feasible = P4[(P4[:, 1] == 2) & (P4[:, 0] != 1)
                  & (P4[:, 2] != 1) & (P4[:, 2] != 3)]
    return len(feasible) == 1 and rowset(feasible) == answer_tuples('K13-01')


def p02():
    base = POS4[:, 2] < POS4[:, 3]
    m = np.count_nonzero(base & (abs(POS4[:, 0] - POS4[:, 1]) == 1))
    n = np.count_nonzero(base & (POS4[:, 1] == POS4[:, 0] + 1))
    options = printed_numeric_options('K13-02')
    return len(options) == 4 and choice('K13-02', [v == (m, n) for v in options])


def p03():
    feasible = P4[np.isin(P4[:, 0], [1, 2]) & np.isin(P4[:, 1], [1, 2])
                  & np.isin(P4[:, 2], [2, 3]) & np.isin(P4[:, 3], [3, 4])]
    fixed = {i + 1: int(col[0]) for i, col in enumerate(feasible.T)
             if len(set(col)) == 1}
    return (rowset(feasible) == answer_tuples('K13-03') and len(feasible) == 2
            and fixed == {3: 3, 4: 4})


def p04():
    candidates = group_assignments([2, 2])
    feasible = candidates[(candidates[:, 0] == candidates[:, 1]) & (candidates[:, 2] == 0)]
    printed = re.findall(r"[PQ]=\\\{([0-9,]+)\\\}", ANSWERS['K13-04'])
    expected = {tuple(tuple(map(int, cell.split(','))) for cell in printed)}
    matrices = np.eye(2, dtype=int)[feasible]
    return (group_sets(feasible, 2) == expected
            and np.all(matrices.sum(axis=2) == 1)
            and np.all(matrices.sum(axis=1) == 2)
            and not np.all(matrices.sum(axis=1) == 1)
            and '每行恰有一个勾，每列恰有两个勾' in ANSWERS['K13-04'])


def p05():
    given = np.array([[1, 2, 3, 4], [2, 1, 3, 4], [3, 1, 2, 4]])
    pos = np.argsort(given, axis=1) + 1
    truths = [implication(not np.all(pos[:, 1] == 4), np.any(pos[:, 1] == 4)), np.all(pos[:, 2] == 3),
              not np.all(pos[:, 0] < pos[:, 1]), np.all(pos[:, 0] != 1)]
    left_of = pos[:, 0] < pos[:, 1]
    explanation = ANSWERS['K13-05']
    stated_true = re.search(r'在 \$([a-d]{4})\$ 和 \$([a-d]{4})\$ 中', explanation)
    stated_false = re.search(r'在 \$([a-d]{4})\$ 中，\$a\$ 在 \$b\$ 右边', explanation)
    return (choice('K13-05', truths)
            and stated_true is not None and stated_false is not None
            and set(stated_true.groups()) == words(given[left_of])
            and {stated_false[1]} == words(given[~left_of]))


def p06():
    a, b, c, d, e = POS5.T
    feasible = P5[(abs(a - b) == 1) & (abs(b - c) == 1) & (d < e) & (b != 3)]
    return len(feasible) == 4 and words(feasible) == answer_words('K13-06', 5)


def p07():
    feasible = np.array([x for x in P4 if x[0] != 4
                         and implication(x[0] == 1, x[1] == 3)
                         and implication(x[2] == 4, x[3] == 2)])
    tests = [lambda x: x[0] == 1, lambda x: x[2] == 4,
             lambda x: x[3] == 3, lambda x: x[1] == 4]
    subsets = [np.array([x for x in feasible if test(x)]) for test in tests]
    counts = [len(subset) for subset in subsets]
    listed = set().union(*(rowset(subset) for subset in subsets))
    return (choice('K13-07', [n == 1 for n in counts])
            and counts == [2, 2, 1, 4]
            and listed == answer_tuples('K13-07'))


def p08():
    domains = [{1, 2}, {2, 3}, {3, 4}, {1, 4}]
    feasible = [x for x in P4 if all(value in domain for value, domain in zip(x, domains))]
    r = [x for x in feasible if implication(x[3] == 4, x[1] == 2)]
    s = [x for x in feasible if implication(x[2] == 4, x[0] == 1)]
    both = [x for x in r if implication(x[2] == 4, x[0] == 1)]
    # A true implication alone allows a false consequent.
    counterexamples = [(p, q) for p, q in product([False, True], repeat=2)
                       if implication(p, q) and not q]
    return (rowset(feasible) == answer_tuples('K13-08')
            and [len(feasible), len(r), len(s), len(both)] == [2, 2, 1, 1]
            and all(x[2] != 4 and x[0] == 1 for x in both)
            and counterexamples == [(False, False)]
            and '仅凭条件句就断定后件成立的推理无效' in ANSWERS['K13-08'])


G8 = group_assignments([3, 3, 2])
G8_PAIRS = G8[(G8[:, 0] == G8[:, 1]) & (G8[:, 2] == G8[:, 3])
             & (G8[:, 4] == G8[:, 5]) & (G8[:, 6] != G8[:, 7])]


def p09():
    feasible = G8_PAIRS[G8_PAIRS[:, 0] == 0]
    partners = {i + 1 for x in feasible for i in range(8) if i != 6 and x[i] == x[6]}
    printed_partners = re.search(r"恰为 \$\\\{([0-9,]+)\\\}\$", ANSWERS['K13-09'])
    return (len(feasible) == 4 and group_sets(feasible) == set(printed_group_rows('K13-09'))
            and partners == set(map(int, printed_partners[1].split(','))))


def p10():
    pos = POS5[POS5[:, 1] == POS5[:, 0] + 1]
    counts = (np.count_nonzero(pos[:, 2] != 1), np.count_nonzero(pos[:, 1] != 1),
              np.count_nonzero(pos[:, 3] == pos[:, 2] + 1))
    options = printed_numeric_options('K13-10')
    return len(options) == 4 and choice('K13-10', [v == counts for v in options])


def p11():
    a, b, c, d = POS4.T
    truths = np.column_stack([a < c, b < d, c < b])
    mask = (abs(a - b) == 1) & (c < d) & (truths.sum(axis=1) == 1)
    feasible = P4[mask]
    return (words(feasible) == answer_words('K13-11', 4) and len(feasible) == 2
            and np.all(POS4[mask, 3] == 2)
            and np.all(truths[mask] == [False, False, True]))


def p13():
    models = set()
    # Search object order, numbers, and marks independently (24^3 trials).
    for order in P4:
        pos = np.argsort(order) + 1
        for numbers in P4:
            for marks in P4:  # p,q,r,s are encoded 1,2,3,4.
                if not all(numbers[np.flatnonzero(marks == mark)[0]] == mark for mark in (1, 2, 3)):
                    continue
                if marks[0] != 1 or marks[3] != 4:
                    continue
                number_pos = {int(number): int(pos[i]) for i, number in enumerate(numbers)}
                if number_pos[3] != number_pos[2] + 1 or pos[0] >= number_pos[3] or pos[3] == 4:
                    continue
                if not implication(pos[1] > pos[2], pos[0] < pos[3]):
                    continue
                models.add((''.join(chr(96 + int(v)) for v in order),
                            int(numbers[1]), 'pqrs'[marks[1] - 1],
                            int(numbers[2]), 'pqrs'[marks[2] - 1]))
    printed = {(word, int(bn), bm, int(cn), cm) for word, bn, bm, cn, cm in
               re.findall(r"\| \$([a-d]{4})\$ \| \$([1-4]),([pqrs])\$ \| \$([1-4]),([pqrs])\$ \|",
                          ANSWERS['K13-13'])}
    b_third = [m for m in models if m[0].index('b') == 2]
    b_r = [m for m in models if m[2] == 'r']
    return (len(models) == 3 and models == printed and len(b_third) == 2
            and not all(m[0][0] == 'a' for m in b_third)
            and {m[2] for m in b_third} == {'q'}
            and len(b_r) == 1 and b_r[0][0] == 'adcb')


def p14():
    truth_counts = np.column_stack([G8_PAIRS[:, 0] == 0, G8_PAIRS[:, 2] == 1,
                                   G8_PAIRS[:, 4] == 2]).sum(axis=1)
    feasible = G8_PAIRS[truth_counts == 1]
    printed = printed_group_rows('K13-14')
    restricted = feasible[feasible[:, 6] == feasible[:, 0]]
    together = restricted[:, 4] == restricted[:, 7]
    return (len(feasible) == 6 and group_sets(feasible) == set(printed)
            and len(restricted) == 2 and group_sets(restricted) == {printed[0], printed[3]}
            and np.all(restricted[:, 7] != 2) and np.any(together) and not np.all(together))


if __name__ == '__main__':
    for number, operation in [(1, p01), (2, p02), (3, p03), (4, p04), (5, p05),
                              (6, p06), (7, p07), (8, p08), (9, p09), (10, p10), (11, p11)]:
        run(f'K13-{number:02d}', operation)
    print('MANUAL K13-12')
    run('K13-13', p13)
    run('K13-14', p14)
    raise SystemExit(bool(failures))
