"""Check all numbered examples and the numerical in-text exercises.

Enumeration helpers do not use the lesson's dynamic-programming recurrence.
Proofs are additionally marked MANUAL; finite checks are not a proof substitute.
"""

from collections import Counter
from itertools import product
from pathlib import Path
import re
import sys

import sympy as sp

from k34_problems import (
    coin_vectors, contains, equal, grid_paths, interval_subsets,
    min_terms, ordered_sums, pack_enumerated, roll, subsets,
)


LESSON = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")
EXAMPLES = {
    int(match[1]): match[2]
    for match in re.finditer(r"\*\*例 (\d+)\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON, re.S)
}
ITEMS = [(2, 3), (3, 4), (4, 5), (5, 8)]
EDGES = {
    ("A", "B"): 4, ("A", "C"): 2, ("B", "C"): 1,
    ("B", "D"): 5, ("C", "D"): 8, ("C", "E"): 10,
    ("D", "E"): 2, ("D", "F"): 6, ("E", "F"): 3,
}


def greedy_coins(coins, amount):
    used = []
    for coin in sorted(coins, reverse=True):
        count, amount = divmod(amount, coin)
        used.extend([coin] * count)
    return used if amount == 0 else None


def numeric_row(text, prefix):
    line = next(line for line in text.splitlines() if line.startswith(prefix))
    cells = line.split("|")[2:-1]
    return [sp.oo if cell.strip() == "∞" else sp.Integer(cell.strip()) for cell in cells]


def graph_paths(target):
    def visit(vertex, path, length):
        if vertex == target:
            return [(path, length)]
        result = []
        for (start, end), weight in EDGES.items():
            if start == vertex:
                result.extend(visit(end, path + end, length + weight))
        return result
    return visit("A", "A", 0)


def check_1(text):
    equal(greedy_coins((1, 3, 4), 6), [4, 1, 1])
    equal(min_terms((1, 3, 4), 6), 2)
    equal([counts for counts in coin_vectors((1, 3, 4), 6) if sum(counts) == 2], [(0, 2, 0)])
    contains(text, "共 3 枚")
    contains(text, "共 2 枚")


def check_2(text):
    first_failure = next(amount for amount in range(1, 30)
                         if len(greedy_coins((1, 6, 10), amount)) > min_terms((1, 6, 10), amount))
    equal(first_failure, int(re.search(r"所以 (\d+) 是最小", text)[1]))
    equal(len(greedy_coins((1, 6, 10), first_failure)), 3)
    equal(min_terms((1, 6, 10), first_failure), 2)


def check_3(text):
    values = [len(ordered_sums(n, (1, 2))) for n in range(11)]
    equal(values, [sp.fibonacci(n + 1) for n in range(11)])
    # The following quoted exercise allows three step sizes and has its own check.
    example_body = text.split("\n>", 1)[0]
    for n, expected in re.findall(r"f\((\d+)\)=(\d+)", example_body):
        if int(n) <= 10:
            equal(values[int(n)], int(expected))
    equal(values[10], int(re.search(r"答案 (\d+) 种", text)[1]))


def check_4(text):
    forbidden = {(2, 2), (3, 4)}
    for i in range(1, 5):
        row = [sum(not (set(path) & forbidden) for path in grid_paths(i, j)) for j in range(1, 6)]
        equal(row, numeric_row(text, f"| **{i}** |"))
    equal(row[-1], int(re.search(r"答案 (\d+)", text)[1]))


def check_5(text):
    matrices = re.findall(r"\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", text, re.S)
    parsed = [sp.Matrix([[int(value) for value in row.split("&")]
                         for row in matrix.split(r"\\")]) for matrix in matrices]
    costs, printed = parsed[:2]
    actual = sp.zeros(costs.rows, costs.cols)
    for i in range(1, costs.rows + 1):
        for j in range(1, costs.cols + 1):
            actual[i - 1, j - 1] = min(
                sum(costs[r - 1, c - 1] for r, c in path) for path in grid_paths(i, j)
            )
    equal(actual, printed)
    route = ((1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4))
    assert route in grid_paths(3, 4)
    equal(sum(costs[i - 1, j - 1] for i, j in route), actual[2, 3])
    equal(actual[2, 3], int(re.search(r"右下角的 (\d+)", text)[1]))


def check_6(text):
    coins = (1, 3, 4)
    actual = [min_terms(coins, amount) for amount in range(11)]
    equal(actual, numeric_row(text, "| $dp[a]$ |"))
    line = next(line for line in text.splitlines() if line.startswith("| 最后一枚 |"))
    last_coins = [int(cell.strip()) for cell in line.split("|")[3:-1]]
    for amount, coin in enumerate(last_coins, 1):
        assert coin in coins
        equal(actual[amount - coin] + 1, actual[amount])


def check_7(text):
    actual = [min_terms((2, 5), amount) for amount in range(12)]
    equal(actual, numeric_row(text, "| $dp[a]$ |"))
    equal([i for i, value in enumerate(actual) if value == sp.oo], [1, 3])
    equal(actual[11], len([5, 2, 2, 2]))
    equal(sum([5, 2, 2, 2]), 11)


def check_8(text):
    shortest = [min(length for _, length in graph_paths(v)) for v in "ABCDEF"]
    equal(shortest, [0, 4, 2, 9, 11, 14])
    equal([path for path, length in graph_paths("F") if length == shortest[-1]], ["ABDEF"])
    contains(text, "答案 14，路径 A–B–D–E–F")
    route = "ACBDEF"
    weights = [EDGES.get((u, v), EDGES.get((v, u))) for u, v in zip(route, route[1:])]
    equal(sum(weights), 13)
    assert ("C", "B") not in EDGES


def check_9(text):
    prefixes = ["| 0 |", "| 1（2,3） |", "| 2（3,4） |", "| 3（4,5） |", "| 4（5,8） |"]
    for i, prefix in enumerate(prefixes):
        equal([pack_enumerated(ITEMS[:i], c)[0] for c in range(9)], numeric_row(text, prefix))
    equal(pack_enumerated(ITEMS, 8), (12, [(0, 1, 0, 1)]))
    equal(pack_enumerated(ITEMS, 7), (11, [(1, 0, 0, 1)]))
    left, value, choice = 8, 0, []
    for i in sorted(range(4), key=lambda j: sp.Rational(ITEMS[j][1], ITEMS[j][0]), reverse=True):
        w, v = ITEMS[i]
        if w <= left:
            choice.append(i + 1)
            left -= w
            value += v
    equal((choice, value, left), ([4, 1], 11, 1))


def check_10(text):
    values = [3, 34, 4, 12, 5, 2]
    reachable = []
    for i in range(7):
        sums = {sum(values[j] for j in chosen) for chosen in subsets(i)}
        reachable.append(sorted(s for s in sums if s <= 9))
        line = next(line for line in text.splitlines() if line.startswith(f"| {i} |"))
        printed = line.split("|")[3].split("（")[0]
        equal(reachable[-1], [int(x.strip()) for x in printed.split(",")])
    equal(next(i for i, row in enumerate(reachable) if 9 in row), 5)
    assert any(sum(values[j] for j in chosen) == 9 for chosen in subsets(6))


def check_11(text):
    printed = [[int(x) for x in row.split(",")] for row in re.findall(r"结果 \$\[([^]]+)\]", text)]
    equal(len(printed), 2)
    expected = [[pack_enumerated([(2, 3)], c, limits)[0] for c in range(7)]
                for limits in ([1], [None])]
    equal(expected, printed)
    equal(roll([(2, 3)], 6, [False]), expected[0])
    equal(roll([(2, 3)], 6, [True]), expected[1])


def check_12(text):
    printed = [[int(x) for x in row.split(",")] for row in re.findall(r"\$\[([^]]+)\]", text)]
    expected = [[pack_enumerated(ITEMS, c, limits)[0] for c in range(9)]
                for limits in ([1] * 4, [None] * 4)]
    equal(expected, printed)
    equal(roll(ITEMS, 8, [False] * 4), expected[0])
    equal(roll(ITEMS, 8, [True] * 4), expected[1])
    equal(pack_enumerated(ITEMS, 8, [None] * 4)[0], 12)


def check_13(text):
    combinations_count = [len(coin_vectors((1, 3), a)) for a in range(5)]
    permutations_count = [len(ordered_sums(a, (1, 3))) for a in range(5)]
    printed = [[int(x) for x in row.split(",")]
               for row in re.findall(r"\$ways=\[([^]]+)\]", text)]
    equal(printed, [[len(coin_vectors((1,), a)) for a in range(5)]])
    equal((combinations_count[3], combinations_count[4]), (2, 2))
    contains(text, f"答案 {combinations_count[4]} 种")
    contains(text, "$[" + ",".join(map(str, permutations_count)) + "]$")
    equal(set(ordered_sums(4, (1, 3))), {(1, 1, 1, 1), (1, 3), (3, 1)})


def greedy_intervals(intervals, key):
    chosen = []
    for index in sorted(range(len(intervals)), key=lambda i: key(intervals[i])):
        if all(intervals[index][1] <= intervals[j][0] or intervals[j][1] <= intervals[index][0]
               for j in chosen):
            chosen.append(index)
    return chosen


def check_14(text):
    first = [(1, 10), (2, 4), (5, 7), (8, 9)]
    second = [(1, 5), (4, 7), (6, 10)]
    equal(len(greedy_intervals(first, lambda interval: interval[0])), 1)
    equal(len(greedy_intervals(second, lambda interval: interval[1] - interval[0])), 1)
    equal(max(map(len, interval_subsets(first))), 3)
    equal(max(map(len, interval_subsets(second))), 2)
    for intervals in (first, second):
        equal(len(greedy_intervals(intervals, lambda interval: interval[1])),
              max(map(len, interval_subsets(intervals))))
    contains(text, "它给出 3 个和 2 个")


def check_15(text):
    intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9),
                 (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    chosen = greedy_intervals(intervals, lambda interval: interval[1])
    equal([intervals[i] for i in chosen], [(1, 4), (5, 7), (8, 11), (12, 16)])
    equal(len(chosen), max(map(len, interval_subsets(intervals))))
    contains(text, f"共 {len(chosen)} 个")


def check_16(text):
    coins = sp.Matrix([1, 5, 10, 25])
    exchanges = [((5, 0, 0, 0), (0, 1, 0, 0)),
                 ((0, 2, 0, 0), (0, 0, 1, 0)),
                 ((0, 0, 3, 0), (0, 1, 0, 1)),
                 ((0, 1, 2, 0), (0, 0, 0, 1))]
    for before, after in exchanges:
        equal(coins.dot(sp.Matrix(before)), coins.dot(sp.Matrix(after)))
        assert sum(after) < sum(before)
    normal = [(p, n, d) for p, n, d in product(range(5), range(2), range(3))
              if not (n == 1 and d == 2)]
    residues = [p + 5 * n + 10 * d for p, n, d in normal]
    equal(sorted(residues), list(range(25)))
    equal(max(residues), 24)
    equal(max(p + 5 * n for p, n, _ in normal), 9)
    for (p, n, d), residue in zip(normal, residues):
        greedy = Counter(greedy_coins((1, 5, 10, 25), residue))
        equal((greedy[1], greedy[5], greedy[10]), (p, n, d))
    # Also exercise actual amounts across several 25-unit boundaries.
    for amount in range(151):
        equal(len(greedy_coins((1, 5, 10, 25), amount)), min_terms((1, 5, 10, 25), amount))
    for fragment in (r"p\le4", r"n\le1", r"d\le2", "4+20=24", "4+5+10=19"):
        contains(text, fragment)


def check_extra():
    equal(len(greedy_coins((1, 5, 10, 25), 63)), 6)
    equal(min_terms((1, 5, 10, 25), 63), 6)
    equal(len(greedy_coins((1, 5, 11), 15)), 5)
    equal([min_terms((1, 5, 11), n) for n in range(10, 16)], [2, 1, 2, 3, 4, 3])
    calls = Counter()

    def fib(n):
        calls[n] += 1
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    equal(fib(5), sp.fibonacci(5))
    equal([calls[n] for n in range(5, -1, -1)], [1, 1, 2, 3, 5, 3])
    equal(sum(calls.values()), 15)
    c = [sp.Integer(1), sp.Integer(1)]
    for n in range(2, 51):
        c.append(1 + c[-1] + c[-2])
    equal(c, [2 * sp.fibonacci(n + 1) - 1 for n in range(51)])
    equal(c[30], 2692537)
    assert c[50] > 40_000_000_000
    equal([len(ordered_sums(n, (1, 2, 3))) for n in range(8)], [1, 1, 2, 4, 7, 13, 24, 44])
    equal(len(grid_paths(4, 4)), sp.binomial(6, 3))
    equal([len(graph_paths(v)) for v in "ABCDEF"], [1, 1, 2, 3, 5, 8])
    equal(len(coin_vectors((1, 3, 4), 6)), 4)
    equal(len(ordered_sums(6, (1, 3, 4))), 9)
    intervals = [(1, 3), (2, 5), (4, 6), (6, 8), (5, 9)]
    chosen = greedy_intervals(intervals, lambda interval: interval[1])
    equal([intervals[i] for i in chosen], [(1, 3), (4, 6), (6, 8)])
    equal(len(chosen), max(map(len, interval_subsets(intervals))))
    equal(len(chosen), 3)


def main():
    equal(set(EXAMPLES), set(range(1, 17)))
    failures = 0
    for n, text in EXAMPLES.items():
        try:
            globals()[f"check_{n}"](text)
            print(f"PASS 例{n}")
            if n in (14, 16):
                print(f"MANUAL 例{n} 一般性证明人工逐步复核，数值及交换条件已另行计算")
        except Exception as error:
            failures += 1
            print(f"FAIL 例{n} {type(error).__name__}: {error}")
    try:
        check_extra()
        print("PASS 讲义正文与随堂小题")
    except Exception as error:
        failures += 1
        print(f"FAIL 讲义正文与随堂小题 {type(error).__name__}: {error}")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
