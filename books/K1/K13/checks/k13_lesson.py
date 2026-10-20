"""Check all ten examples, their option values, and the numerical side exercises."""

from itertools import permutations, product
from pathlib import Path
import re

import numpy as np
from sympy import Implies, factorial


failures = []


def check(label, condition):
    ok = bool(condition)
    print(f"{'PASS' if ok else 'FAIL'} {label}")
    if not ok:
        failures.append(label)
    return ok


def implication(p, q):
    return bool(Implies(bool(p), bool(q)))


def rowset(values):
    return {tuple(int(v) for v in row) for row in values}


def assignments(capacities):
    possible = np.array(list(product(range(1, len(capacities) + 1), repeat=sum(capacities))))
    mask = np.ones(len(possible), dtype=bool)
    for group, capacity in enumerate(capacities, 1):
        mask &= (possible == group).sum(axis=1) == capacity
    return possible[mask]


P4 = np.array(list(permutations(range(1, 5))))
POS4 = np.argsort(P4, axis=1) + 1
P5 = np.array(list(permutations(range(1, 6))))
POS5 = np.argsort(P5, axis=1) + 1
# Cities 1,2,3,4 denote Beijing, Shanghai, Guangzhou, Chengdu.


def example1():
    feasible = P4[(P4[:, 1] == 1) & (P4[:, 0] != 3)
                  & (P4[:, 2] != 2) & (P4[:, 2] != 3)]
    return rowset(feasible) == {(2, 1, 4, 3)}


def example2():
    # Jobs 1,2,3,4 denote teacher, doctor, accountant, engineer.
    feasible = set()
    for cities in P4:
        for jobs in P4:
            linked = all(implication(cities[i] == city, jobs[i] == job)
                         for i in range(4) for city, job in [(1, 2), (2, 1), (4, 3)])
            if cities[1] == 1 and linked and cities[3] not in (2, 4) and jobs[0] != 3:
                feasible.add((tuple(cities), tuple(jobs)))
    return feasible == {((2, 1, 4, 3), (1, 2, 3, 4))}


def example3():
    a, b, c, d = POS4.T
    conditions = [c != 1, abs(b - d) == 1, a < c, b == a + 1]
    counts = []
    for sequence in [(0, 1, 2, 3), (3, 1, 0, 2)]:
        mask = np.ones(len(P4), dtype=bool)
        remaining = []
        for index in sequence:
            mask &= conditions[index]
            remaining.append(int(mask.sum()))
        counts.append(remaining)
    return (counts == [[18, 8, 6, 1], [6, 2, 1, 1]]
            and 24 + sum(counts[0][:-1]) == 56
            and 24 + sum(counts[1][:-1]) == 33
            and rowset(P4[np.logical_and.reduce(conditions)]) == {(1, 2, 4, 3)})


def example4():
    a, b, c, d, e = POS5.T
    mask = (e == 3) & (abs(a - b) == 1) & (abs(c - d) == 1) & (a < c) & (b < a) & (c < d)
    return rowset(P5[mask]) == {(2, 1, 5, 3, 4)}


def ex5_conditions(cities):
    a, b, c, d = cities
    return [implication(b == 1, d == 3), a not in (1, 4), c in (4, 2), d != 2]


EX5_FEASIBLE = np.array([row for row in P4 if all(ex5_conditions(row))])
EX5_PRINTED = np.array([[2, 1, 4, 3], [2, 3, 4, 1], [3, 2, 4, 1], [3, 4, 2, 1]])


def example5():
    options = [(1, 2, 4, 3), (3, 1, 2, 4), (2, 3, 1, 4), (3, 1, 4, 2), (2, 1, 4, 3)]
    ok = [check(f'例5({letter})', all(ex5_conditions(row)) == (letter == 'E'))
          for letter, row in zip('ABCDE', options)]
    # The displayed elimination order is condition 2, then 3, then 1, then 4.
    conditions = np.array([ex5_conditions(row) for row in options])
    mask = np.ones(5, dtype=bool)
    remaining = []
    for index in (1, 2, 0, 3):
        mask &= conditions[:, index]
        remaining.append(int(mask.sum()))
    return (all(ok) and remaining == [4, 3, 1, 1]
            and rowset(EX5_FEASIBLE) == rowset(EX5_PRINTED))


def example6():
    options = [(1, 3, 2, 4), (1, 4, 3, 2), (2, 1, 3, 4), (3, 2, 1, 4), (1, 4, 2, 3)]
    results = []
    for letter, order in zip('ABCDE', options):
        a, b, c, d = np.argsort(order) + 1
        conditions = [implication(c == 3, b == 1), implication(d == 4, a == 2), abs(a - b) != 1]
        results.append(check(f'例6({letter})', all(conditions) == (letter == 'E')))
    return all(results)


def example7():
    g = assignments([2, 2, 2])
    a, b, c, d, e, f = g.T
    feasible = g[(a != b) & (c == d) & (e != 1) & (f == 2) & (b != 2)]
    return rowset(feasible) == {(2, 3, 1, 1, 3, 2)}


def example8():
    g = assignments([3, 2, 2])
    a, b, c, d, e, f, h = g.T
    feasible = g[(c == d) & (e != 1) & (h == 3) & (c != 1)]
    return rowset(feasible) == {(1, 1, 2, 2, 3, 1, 3)}


def example9():
    a, b, c, d = EX5_PRINTED.T
    values = np.column_stack([a == 2, c == 4, b != 1, d == 1, np.isin(d, [1, 3])])
    expected = np.array([[1, 1, 0, 0, 1], [1, 1, 1, 1, 1],
                         [0, 1, 1, 1, 1], [0, 0, 1, 1, 1]], dtype=bool)
    results = [check(f'例9({letter})', np.array_equal(values[:, i], expected[:, i])
                     and bool(values[:, i].all()) == (letter == 'E')
                     and values[:, i].any()) for i, letter in enumerate('ABCDE')]
    return rowset(EX5_FEASIBLE) == rowset(EX5_PRINTED) and all(results)


def example10():
    restricted = EX5_FEASIBLE[EX5_FEASIBLE[:, 3] == 1]
    a, b, c, d = restricted.T
    values = np.column_stack([a == 2, b != 1, c == 4, b == 4])
    results = [check(f'例10({letter})', bool(values[:, i].all()) == (letter == 'B')
                     and values[:, i].any()) for i, letter in enumerate('ABCD')]
    return len(restricted) == 3 and all(results)


def side_checks():
    lesson = (Path(__file__).resolve().parents[1] / 'lesson.md').read_text(encoding='utf-8')
    printed = re.search(r'120\^5=(\d+)', lesson)
    attribute_orders = len(list(permutations(range(5))))
    check('计数引入', len(P4) == factorial(4) == 24 and len(P4) ** 2 == 576
          and attribute_orders == factorial(5) == 120
          and printed is not None and attribute_orders ** 5 == int(printed[1]))
    # Five independent attributes; fixing one leaves four freely permutable.
    check('固定一类属性后的计数', attribute_orders ** 5 // attribute_orders
          == attribute_orders ** 4 == 207360000)
    a, b, c, d = POS4.T
    counts = [np.count_nonzero(test) for test in
              [a == 1, b == a + 1, abs(a - b) == 1, a < b, np.isin(a, [2, 3]), a != 1]]
    check('信息量表', counts == [6, 6, 12, 12, 12, 18])

    # Roles: host, recorder, timer, coordinator are 1,2,3,4.
    a, b, c, d = P4.T
    roles = P4[(c != 1) & (c != 2) & (d == 3) & (a != 4) & (b != 2)]
    check('随堂1', rowset(roles) == {(2, 1, 4, 3)})

    # Pets: cat, dog, fish, bird are 1,2,3,4.
    homes = set()
    for room in P4:
        for pet in P4:
            if (room[0] == 1 and pet[2] == 4 and room[1] != 3
                    and all(implication(room[i] == 2, pet[i] == 2)
                            and implication(room[i] == 3, pet[i] == 3) for i in range(4))):
                homes.add((tuple(room), tuple(pet)))
    check('随堂2', homes == {((1, 2, 4, 3), (1, 2, 4, 3))})

    a, b, c, d = POS4.T
    queue = P4[(d == 4) & (abs(a - c) == 1) & (b != 1)]
    check('随堂3', rowset(queue) == {(1, 3, 2, 4), (3, 1, 2, 4)})

    options = [(2, 4, 1, 3), (3, 4, 2, 1), (4, 1, 2, 3)]
    for letter, option in zip('ABC', options):
        check(f'随堂4({letter})', all(ex5_conditions(option)) == (letter == 'B'))

    g = assignments([3, 2])
    a, b, c, d, e = g.T
    small = g[(a == b) & (c != d) & (e == 2) & (c == 1)]
    check('随堂5', rowset(small) == {(1, 1, 1, 2, 2)})

    restricted = EX5_FEASIBLE[EX5_FEASIBLE[:, 0] == 3]
    check('随堂6', len(restricted) == 2 and set(restricted[:, 3]) == {1}
          and set(restricted[:, 1]) == {2, 4})


if __name__ == '__main__':
    for i, operation in enumerate([example1, example2, example3, example4, example5,
                                    example6, example7, example8, example9, example10], 1):
        try:
            check(f'例{i}', operation())
        except Exception as error:
            check(f'例{i}', False)
            print(f'DETAIL 例{i}: {type(error).__name__}: {error}')
    side_checks()
    raise SystemExit(bool(failures))
