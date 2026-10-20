"""Recompute counts, limits and recurrences; compare with answers.md.

Expected expressions are answer-side references, never the implementation used
to generate the counts. Text anchors keep these references tied to the book.
Only K31-09 is manual: finite execution cannot certify its universal proof.
"""

from itertools import product
from pathlib import Path
import re
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"\*\*(K31-\d+)\*\*[^\n]*\n(.*?)(?=\n\*\*K31-|\Z)", ANSWERS, re.S
))
n = sp.Symbol("n", integer=True, positive=True)
k = sp.Symbol("k", integer=True, nonnegative=True)
i, j, d, r = sp.symbols("i j d r", integer=True)
failures = 0


def anchors(pid, *fragments):
    for fragment in fragments:
        assert fragment in BLOCKS[pid], f"answer reference missing: {fragment}"


def equal(actual, expected):
    assert actual == expected or sp.simplify(actual - expected) == 0, (actual, expected)


def run(pid, fn, manual=False):
    global failures
    try:
        fn()
        if manual:
            print(f"MANUAL {pid} 强归纳证明；有限执行与边界检查通过，不能替代证明")
        else:
            print(f"PASS {pid}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")


def options(pid, actual, expected):
    assert len(actual) == len(expected) == 4
    for label, value, reference in zip("ABCD", actual, expected):
        assert bool(value) == reference, f"option {label}: {value} != {reference}"
        print(f"PASS {pid} 选项 {label}={'真' if value else '假'}")
    chosen = "ABCD"[expected.index(True)]
    assert f"({chosen})" in BLOCKS[pid].splitlines()[0]


def problem01():
    assert "执行 `FIRST(A,4)`" in PROBLEMS
    anchors("K31-01", "返回 $2$", "各执行 $2$ 次", "| 1 | 3 |", "| 2 | $-2$ |")
    total, trace, additions, comparisons, result = 0, [], 0, 0, 0
    for index, value in enumerate([3, -5, 7, -1], 1):
        total += value
        additions += 1
        comparisons += 1
        trace.append((index, total))
        if total < 0:
            result = index
            break
    assert trace == [(1, 3), (2, -2)]
    assert (result, additions, comparisons) == (2, 2, 2)


def problem02():
    anchors("K31-02", "$3,4$ 次", "$1,2,4$", "$8$")
    counts = []
    for size in (8, 9):
        value, count = 1, 0
        while value < size:
            value *= 2
            count += 1
        counts.append(count)
    candidates = [(3, 4), (4, 4), (3, 3), (7, 8)]
    options("K31-02", [tuple(counts) == c for c in candidates], [True, False, False, False])


def problem03():
    anchors("K31-03", "$n^2$", "$16$ 次", r"\sum_{i=1}^n(2i-1)")
    computed = sp.summation(2 * i - 1, (i, 1, n))
    equal(computed, n**2)
    for size in range(1, 41):
        count = sum(1 for outer in range(1, size + 1) for _ in range(1, 2 * outer))
        equal(count, computed.subs(n, size))
    equal(computed.subs(n, 4), 16)


def problem04():
    anchors("K31-04", r"f/n^3=1/n+6/n^2\to0", "$6n>0$")
    f = n**2 + 6 * n
    ratio_n = sp.limit(f / n, n, sp.oo)
    ratio_cube = sp.limit(f / n**3, n, sp.oo)
    difference = sp.simplify(f - n**2)
    truth = [ratio_n.is_finite is True, ratio_cube == 0,
             ratio_cube.is_positive is True, difference == 0]
    options("K31-04", truth, [False, True, False, False])
    assert difference.is_positive
    equal(sp.limit(f / n**2, n, sp.oo), 1)


def problem05():
    anchors("K31-05", "$a=3,b=3,d=2$", r"\Theta(n^2)", "$a/b^d=1/3$")
    total = sp.summation(3**i * (3**k / 3**i)**2, (i, 0, k))
    equal(sp.limit(total / 3**(2 * k), k, sp.oo), sp.Rational(3, 2))
    assert sp.Rational(3, 3**2) < 1
    value = 1
    for level in range(9):
        if level:
            value = 3 * value + (3**level)**2
        equal(value, total.subs(k, level))


def problem06():
    anchors("K31-06", "$f=n^2+n,g=n^2$", "$f=n^2+1,g=n^2$", "$f=2n^2,g=n^2$")
    examples = [(n**2 + n, n**2), (n**2 + 1, n**2), (2 * n**2, n**2)]
    for f, g in examples:
        assert sp.simplify(f - g).is_positive
        for function in (f, g):
            limit = sp.limit(function / n**2, n, sp.oo)
            assert limit.is_positive and limit.is_finite
    counter_a = sp.limit((examples[0][0] - examples[0][1]) / n**2, n, sp.oo)
    counter_c = sp.limit((examples[1][0] - examples[1][1]) / n, n, sp.oo)
    counter_d = sp.limit(examples[2][0] - examples[2][1], n, sp.oo)
    # With f=g+h and g,h>0, h/f<1. Thus any upper bound for f bounds h.
    g, h = sp.symbols("g h", positive=True)
    gap = sp.simplify(1 - h / (g + h))
    truth = [counter_a != 0, gap.is_positive, counter_c != 0, counter_d.is_finite]
    options("K31-06", truth, [False, True, False, False])


def problem07():
    anchors("K31-07", "$N(n)=(m-1)n+m+2$", "$N(8)=21$", r"\Theta(n\log n)")
    closed = (k - 1) * 2**k + k + 2
    equal(sp.summation(2**k - 2**r + 1, (r, 0, k)), closed)
    for m in range(11):
        count = 0
        for outer in range(1, 2**m + 1):
            value = 1
            while value <= outer:
                value *= 2
                count += 1
        equal(count, closed.subs(k, m))
    equal(closed.subs(k, 3), 21)
    equal(sp.limit(closed / (2**k * k), k, sp.oo), 1)


def problem08():
    anchors("K31-08", "$0<a<2$", r"$a\ge2$", "第三问没有符合条件")
    # n=exp(t), a=2-e or a=2+e covers the entire two open ranges.
    t, e = sp.symbols("t e", positive=True)
    limits = [sp.limit(t * sp.exp(-e * t) / sp.log(2), t, sp.oo),
              sp.limit(t / sp.log(2), t, sp.oo),
              sp.limit(t * sp.exp(e * t) / sp.log(2), t, sp.oo)]
    assert limits == [0, sp.oo, sp.oo]
    assert [value.is_finite for value in limits] == [True, False, False]
    assert [value > 0 for value in limits] == [False, True, True]
    assert not any(value.is_positive and value.is_finite for value in limits)


def problem09():
    anchors("K31-09", "对所有长度为 $m$", r"$l\le q<r$", "$q-l+1$", "$r-q$")

    def blockmax(array, left, right):
        if left == right:
            return array[left]
        middle = (left + right) // 2
        assert left <= middle < right
        u = blockmax(array, left, middle)
        v = blockmax(array, middle + 1, right)
        return u if u >= v else v

    for length in range(1, 7):
        for array in product((-1, 0, 1), repeat=length):
            for left in range(length):
                for right in range(left, length):
                    assert blockmax(array, left, right) == max(array[left:right + 1])


def problem10():
    anchors("K31-10", r"1+\frac{k(k+1)(2k+1)}6", "$T(16)=31$", r"\Theta((\log n)^3)", "不能直接套用")
    closed = 1 + k * (k + 1) * (2 * k + 1) / 6
    equal(1 + sp.summation(r**2, (r, 1, k)), closed)
    value = 1
    for level in range(30):
        if level:
            value += level**2
        equal(value, closed.subs(k, level))
    equal(closed.subs(k, 4), 31)
    equal(sp.limit(closed / k**3, k, sp.oo), sp.Rational(1, 3))
    x = sp.Symbol("x", positive=True)
    # A power n^d has constant logarithmic derivative d; this toll does not.
    exponent = sp.simplify(x * sp.diff(sp.log(x, 2)**2, x) / sp.log(x, 2)**2)
    assert x in exponent.free_symbols


def problem11():
    anchors("K31-11", r"\{2,4,8,16\}", r"$k\ge5$", "$n=32$", "没有相等")
    slower_p, slower_q, ties = [], [], []
    for power in range(1, 61):
        size = 2**power
        p, q = 6 * size * power, size**2
        (slower_p if p > q else slower_q if q > p else ties).append(power)
    assert slower_p == [1, 2, 3, 4]
    assert slower_q == list(range(5, 61)) and not ties
    u = sp.Symbol("u", positive=True)
    # k=1+u ensures k>1; positivity proves persistence beyond the tested range.
    growth_minus_one = sp.simplify(2 * (1 + u) / (2 + u) - 1)
    assert growth_minus_one.is_positive
    assert sp.Rational(2**5, 5) > 6
    equal(sp.limit(6 * k / 2**k, k, sp.oo), 0)


def problem12():
    anchors("K31-12", r"\frac{n(n-1)(n+1)}6", "$N(6)=35$", r"\Theta(n^3)")
    by_j = sp.summation(sp.summation(j - i, (i, 1, j - 1)), (j, 2, n))
    by_gap = sp.summation(d * (n - d), (d, 1, n - 1))
    reference = n * (n - 1) * (n + 1) / 6
    equal(by_j, reference)
    equal(by_gap, reference)
    for size in range(2, 25):
        count = sum(1 for end in range(2, size + 1)
                    for start in range(1, end) for _ in range(1, end - start + 1))
        equal(count, reference.subs(n, size))
        assert count != size**3
    equal(reference.subs(n, 6), 35)
    equal(sp.limit(reference / n**3, n, sp.oo), sp.Rational(1, 6))


def problem13():
    anchors("K31-13", "$n(k+1)$", "$2k$", "$2n-2$", "$2n-1$", r"$\Theta(\log n)$", r"$\Theta(n)$")

    def execute(size, repeat):
        if size == 1:
            return 1, 0, 1, 1
        value, adds, calls, depth = execute(size // 2, repeat)
        if repeat:
            value2, adds2, calls2, depth2 = execute(size // 2, repeat)
            return value + value2 + size, adds + adds2 + 2, calls + calls2 + 1, max(depth, depth2) + 1
        return value + value + size, adds + 2, calls + 1, depth + 1

    for power in range(11):
        size = 2**power
        assert execute(size, False) == (size * (power + 1), 2 * power, power + 1, power + 1)
        assert execute(size, True) == (size * (power + 1), 2 * size - 2, 2 * size - 1, power + 1)
    equal(sp.summation(2 * 2**i, (i, 0, k - 1)), 2 * 2**k - 2)
    equal(sp.summation(2**i, (i, 0, k)), 2 * 2**k - 1)
    equal(sp.limit((2 * 2**k - 2) / 2**k, k, sp.oo), 2)
    equal(sp.limit((k + 1) / k, k, sp.oo), 1)
    equal(sp.limit((2 * 2**k - 2) / (2 * k), k, sp.oo), sp.oo)


def problem14():
    anchors("K31-14", "$(1,2),(2,2),(3,2),(4,0),(4,1)$", "$(2,2),(4,1)$",
            "$21,28,37,21,28$", "$T(n)=2n^2-n$", "$120$")
    candidates = set()
    # Solve all three branches; no arbitrary upper cutoff for a.
    leaf_a = sp.solve(sp.Symbol("a", positive=True) - 2**2)[0]
    for degree in range(4):
        if degree == 2:
            candidates.update((a, degree) for a in range(1, 2**degree))
        if leaf_a > 2**degree:
            candidates.add((int(leaf_a), degree))
        ratio_at_equality = sp.limit(n**degree * sp.log(n) / n**2, n, sp.oo)
        assert not (ratio_at_equality.is_positive and ratio_at_equality.is_finite)
    expected = {(1, 2), (2, 2), (3, 2), (4, 0), (4, 1)}
    assert candidates == expected
    values4 = {pair: pair[0] * (pair[0] + 2**pair[1]) + 4**pair[1] for pair in candidates}
    assert [values4[p] for p in sorted(candidates)] == [21, 28, 37, 21, 28]
    remaining = {p for p in candidates if values4[p] == 28}
    assert remaining == {(2, 2), (4, 1)}
    function = sp.Function("T")
    for a, degree in sorted(remaining):
        recurrence = function(k) - a * function(k - 1) - 2**(degree * k)
        closed = sp.rsolve(recurrence, function(k), {function(0): 1})
        equal(closed, 2 * 2**(2 * k) - 2**k)
        equal(closed.subs(k, 3), 120)
        value = 1
        for power in range(12):
            if power:
                value = a * value + (2**power)**degree
            equal(value, closed.subs(k, power))


def cross_references():
    lesson = (ROOT / "lesson.md").read_text(encoding="utf-8")
    ids = [f"K31-{number:02d}" for number in range(1, 15)]
    assert re.findall(r"^\*\*(K31-\d+)\*\*", PROBLEMS, re.M) == ids
    assert re.findall(r"^\*\*(K31-\d+)\*\*", ANSWERS, re.M) == ids
    assert re.findall(r"^\| (K31-\d+) \|", PROBLEMS, re.M) == ids
    summary = lesson.split("### 本章小结", 1)[1]
    assert set(re.findall(r"K31-\d+", summary)) == set(ids)
    answer_headers = dict(re.findall(r"^\*\*(K31-\d+)\*\*([^\n]*)", ANSWERS, re.M))
    for number, methods in ((12, "2、3"), (13, "1、6"), (14, "6、7")):
        pid = f"K31-{number}"
        assert f"| {pid} | C | 章末混合练习 |" in PROBLEMS
        assert f"**{pid}**〔C〕" in PROBLEMS
        assert f"方法 {methods}" in answer_headers[pid]
    for method, line in re.findall(r"^\| 方法 (\d+)[^\n]*?\|[^\n]*?\| ([^\n]*)", summary, re.M):
        for pid in re.findall(r"K31-\d+", line):
            header = re.search(rf"^\*\*{pid}\*\*([^\n]*)", PROBLEMS, re.M)[1]
            if int(pid[-2:]) >= 12:
                header = answer_headers[pid]
            declared = re.search(r"方法 ([\d、]+)", header)[1].split("、")
            assert method in declared, (pid, method, declared)


if __name__ == "__main__":
    for number in range(1, 15):
        run(f"K31-{number:02d}", globals()[f"problem{number:02d}"], manual=number == 9)
    run("题号与方法对应", cross_references)
    sys.exit(bool(failures))
