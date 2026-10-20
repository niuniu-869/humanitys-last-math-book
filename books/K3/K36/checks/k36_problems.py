"""Execute the algorithms independently, then compare with answers.md.

Expected constants below are transcribed from the answers, never substituted
for the algorithm under test. Exhaustion checks small inputs; symbolic checks
verify identities. Neither is reported as a proof of an arbitrary program.
"""
from itertools import combinations, combinations_with_replacement, groupby, product
from pathlib import Path
import re

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*(K36-\d+)\*\*\n(.*?)(?=\n\*\*K36-|\Z)", ANS, re.S))
FAILURES = []


def require(pid, *fragments):
    for fragment in fragments:
        assert fragment in BLOCKS[pid], (pid, "answer drift", fragment)


def check(pid, fn):
    try:
        fn()
    except Exception as exc:
        FAILURES.append(pid)
        print(f"FAIL {pid}: {exc!r}")
    else:
        print(f"PASS {pid}")


def choices(pid, actual, candidates, correct):
    require(pid, f"({correct})")
    for letter, candidate in zip("ABCD", candidates):
        def test(letter=letter, candidate=candidate):
            assert (actual == candidate) == (letter == correct), (actual, candidate)
        check(f"{pid}({letter})", test)


def p01():
    x, y = 2, 5
    x = x + y
    y = x - y
    require("K36-01", "$(7,2)$")
    assert (x, y) == (7, 2)
    choices("K36-01", (x, y), [(7, -3), (5, 2), (7, 2), (7, 5)], "C")


def rotate(a):
    a = list(a)
    trace = []
    for i in range(len(a) - 1):
        a[i], a[i + 1] = a[i + 1], a[i]
        trace.append(a.copy())
    return a, trace


def p02():
    result, trace = rotate([4, 1, 6, 2])
    assert trace == [[1, 4, 6, 2], [1, 6, 4, 2], [1, 6, 2, 4]]
    require("K36-02", "$[1,4,6,2]$", "$[1,6,4,2]$", "$[1,6,2,4]$")
    for n in range(1, 25):
        a = np.arange(n)
        assert np.array_equal(rotate(a)[0], np.roll(a, -1))


def reverse_digits(n):
    r, trace = 0, []
    while n > 0:
        r = 10 * r + n % 10
        n //= 10
        trace.append((n, r))
    return r, trace


def p03():
    value, trace = reverse_digits(1204)
    assert trace == [(120, 4), (12, 40), (1, 402), (0, 4021)]
    assert value == 4021 and reverse_digits(1200)[0] == 21
    require("K36-03", "$(120,4)$", "$(12,40)$", "$(1,402)$", "$(0,4021)$", "返回 21")
    for n in range(2001):
        assert reverse_digits(n)[0] == int(str(n)[::-1])


def postorder(n):
    out, calls = [], 0
    def visit(n):
        nonlocal calls
        calls += 1
        if n == 0:
            return
        visit(n // 2)
        out.append(n)
    visit(n)
    return out, calls


def p04():
    actual = postorder(6)
    require("K36-04", "$1,3,6$", "调用 4 次")
    choices("K36-04", actual, [([6, 3, 1], 4), ([1, 3, 6], 4),
                                ([1, 3, 6], 3), ([0, 1, 3, 6], 4)], "B")
    assert actual == ([1, 3, 6], 4)


def p05():
    n, i = sp.symbols("n i", integer=True, positive=True)
    assert sp.simplify(sp.summation(n - i, (i, 1, n)) - n * (n - 1) / 2) == 0
    counts = {n: sum(1 for i in range(1, n + 1) for j in range(i + 1, n + 1))
              for n in range(1, 31)}
    assert counts[5] == 10
    assert all(c == sp.binomial(n, 2) for n, c in counts.items())
    require("K36-05", "返回 10", "$n(n-1)/2$")


def compress_runs(a, fixed=False):
    a = list(a)
    if fixed and not a:
        return 0, []
    k = 1
    for i in range(1, len(a)):
        if a[i] != a[k - 1 if fixed else 0]:
            k += 1
            a[k - 1] = a[i]
    return k, a[:k]


def p06():
    assert compress_runs([]) == (1, [])
    assert compress_runs([1, 2, 1]) == (2, [1, 2])
    assert compress_runs([2, 2, 5, 5, 2]) == (3, [2, 5, 5])
    assert compress_runs([2, 2, 5, 5, 2], True) == (3, [2, 5, 2])
    for n in range(7):
        for a in product(range(-1, 2), repeat=n):
            expected = [value for value, _ in groupby(a)]
            assert compress_runs(a, True) == (len(expected), expected)
            if 1 <= n <= 2:
                assert compress_runs(a) == (len(expected), expected)
    require("K36-06", "$[1,2,1]$", "$[2,5,5]$", "$[2,5,2]$", "a[i] ≠ a[k]", "空数组错误地返回 1")


def differences_then_prefix(a, backward=False):
    a = list(a)
    indices = range(len(a) - 1, 0, -1) if backward else range(1, len(a))
    for i in indices:
        a[i] -= a[i - 1]
    intermediate = a.copy()
    for i in range(1, len(a)):
        a[i] += a[i - 1]
    return intermediate, a


def p07():
    assert differences_then_prefix([3, 8, 6, 11]) == ([3, 5, 1, 10], [3, 8, 9, 19])
    assert differences_then_prefix([3, 8, 6, 11], True) == ([3, 5, -2, 5], [3, 8, 6, 11])
    for n in range(1, 7):
        for a in product(range(-1, 2), repeat=n):
            d, recovered = differences_then_prefix(a, True)
            assert np.array_equal(d, np.diff(a, prepend=0))
            assert recovered == list(a)
    b = sp.symbols("b1:7")
    assert differences_then_prefix(b, True)[1] == list(b)
    require("K36-07", "$[3,5,1,10]$", "$[3,8,9,19]$", "$[3,5,-2,5]$")


def fixed_first_triple(a, target):
    if len(a) < 3:
        return (0, 0, 0), []
    lo, hi, trace = 1, len(a) - 1, []
    while lo < hi:
        s = a[0] + a[lo] + a[hi]
        trace.append((lo + 1, hi + 1, s))
        if s == target:
            return (1, lo + 1, hi + 1), trace
        if s < target:
            lo += 1
        else:
            hi -= 1
    return (0, 0, 0), trace


def brute_triple(a, target):
    tests = 0
    for i in range(len(a) - 2):
        for j in range(i + 1, len(a) - 1):
            for k in range(j + 1, len(a)):
                tests += 1
                if a[i] + a[j] + a[k] == target:
                    return (i + 1, j + 1, k + 1), tests
    return (0, 0, 0), tests


def p08():
    assert fixed_first_triple([1, 2, 4, 6], 12) == ((0, 0, 0), [(2, 4, 9), (3, 4, 11)])
    assert brute_triple([1, 2, 4, 6], 12) == ((2, 3, 4), 4)
    for n in range(7):
        for a in combinations_with_replacement(range(-2, 3), n):
            for target in range(-7, 8):
                triples = [tuple(i + 1 for i in indices)
                           for indices in combinations(range(n), 3)
                           if sum(a[i] for i in indices) == target]
                result, tests = brute_triple(a, target)
                assert result == (triples[0] if triples else (0, 0, 0))
                if not triples:
                    assert tests == sp.binomial(n, 3)
                if n <= 3:
                    assert fixed_first_triple(a, target)[0] == result
    for n in range(4, 80):
        _, tests = brute_triple(list(range(n)), -1)
        assert tests == n * (n - 1) * (n - 2) // 6
        assert sp.Rational(n ** 3, 24) <= tests <= sp.Rational(n ** 3, 6)
    require("K36-08", "$(2,4,9)$", "$(3,4,11)$", "$(0,0,0)$", "$(2,3,4)$", r"\Theta(n^3)")


def condition_counts(n, reset):
    c, j, attempts = 0, 1, 0
    for i in range(1, n + 1):
        if reset:
            j = 1
        while True:
            attempts += 1
            if not j <= i:
                break
            c += 1
            j *= 2
    return c, attempts


def p09():
    samples = range(2, 257)
    observed, candidates = [], [[], [], [], []]
    for n in samples:
        s = sum(i.bit_length() for i in range(1, n + 1))
        length = n.bit_length()
        reset_body, reset_tests = condition_counts(n, True)
        shared_body, shared_tests = condition_counts(n, False)
        assert (reset_body, shared_body) == (s, length)
        assert (reset_tests, shared_tests) == (s + n, length + n)
        assert n <= shared_tests <= 2 * n
        assert s <= n * (np.log2(n) + 1)
        if n >= 4:
            assert s > (n / 2) * np.log2(n / 2)
        observed.append((reset_tests, shared_tests))
        for candidate, pair in zip(candidates, [(s, length), (s + 1, length + 1),
                                                (s + n, s + n), (s + n, length + n)]):
            candidate.append(pair)
    choices("K36-09", observed, candidates, "D")
    assert condition_counts(8, True) == (21, 29)
    assert condition_counts(8, False) == (4, 12)
    require("K36-09", "$S+n$", "$L+n$", "29、12", r"\Theta(n\log n)", r"\Theta(n)")


def parity_count(n):
    c, tests = 0, 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            tests += 1
            if (i + j) % 2 == 1:
                c += 1
    return c, tests


def p10():
    assert parity_count(9) == (20, 36)
    for n in range(2, 100):
        c, tests = parity_count(n)
        m = n // 2
        assert c == (m * m if n % 2 == 0 else m * (m + 1))
        assert c == n * n // 4 and tests == sp.binomial(n, 2)
        assert sp.Rational(n * n, 8) <= c <= sp.Rational(n * n, 4)
    require("K36-10", "返回 20", "判断执行 36 次", r"\lfloor n^2/4\rfloor", "m(m+1)")


def proof11_support():
    b, q, r = sp.symbols("b q r", integer=True)
    assert sp.expand(b * (q + 1) + (r - b) - (b * q + r)) == 0
    for a in range(100):
        for b in range(1, 20):
            q, r = 0, a
            while r >= b:
                old_r = r
                r -= b
                q += 1
                assert a == b * q + r and 0 <= r < old_r
            assert (q, r) == divmod(a, b)
    require("K36-11", "$a=bq+r$", "$0\\le r'<b$", "$q=q'$", "$r=r'$")


def recursive_counts(n):
    calls, out = 0, []
    def visit(size):
        nonlocal calls
        calls += 1
        if size == 1:
            return
        if size % 2 == 0:
            visit(size // 2)
            visit(size // 2)
        else:
            visit(size - 1)
            out.append(size)
    visit(n)
    return out, calls


def p12():
    assert recursive_counts(1) == ([], 1)
    assert recursive_counts(7) == ([3, 3, 7], 10)
    for n in range(2, 300):
        out, calls = recursive_counts(n)
        child_out, child_calls = recursive_counts(n // 2 if n % 2 == 0 else n - 1)
        assert out == (child_out * 2 if n % 2 == 0 else child_out + [n])
        assert calls == (1 + 2 * child_calls if n % 2 == 0 else 1 + child_calls)
    for m in range(1, 11):
        out, calls = recursive_counts(2 ** m - 1)
        assert len(out) == 2 ** (m - 1) - 1
        assert calls == 3 * 2 ** (m - 1) - 2
        assert len(out) < calls
    h = sp.symbols("h", integer=True, nonnegative=True)
    m = sp.symbols("m", integer=True, positive=True)
    total = sp.summation(2 ** h, (h, 0, m - 2))
    assert sp.simplify(total - (2 ** (m - 1) - 1)) == 0
    assert sp.simplify(2 ** (m - 1) + 2 * total - (3 * 2 ** (m - 1) - 2)) == 0
    require("K36-12", "$3,3,7$", "调用 10 次", "P(1)=0,C(1)=1", "3\\cdot2^{m-1}-2")


def interval_count(n):
    c, i, intervals = 0, 1, []
    while i <= n:
        end = min(3 * i - 1, n)
        intervals.append((i, end))
        for j in range(i, end + 1):
            c += 1
        i *= 2
    return c, intervals


def p13():
    assert interval_count(10) == (16, [(1, 2), (2, 5), (4, 10), (8, 10)])
    for n in range(1, 600):
        c, intervals = interval_count(n)
        assert c == sum(min(2 ** (k + 1), n - 2 ** k + 1) for k in range(n.bit_length()))
        assert sp.Rational(n, 2) < c < 4 * n
        if n & (n - 1) == 0:
            assert c == (1 if n == 1 else 3 * n // 2)
    k = sp.symbols("k", integer=True, nonnegative=True)
    m = sp.symbols("m", integer=True, positive=True)
    assert sp.simplify(sp.summation(2 ** (k + 1), (k, 0, m - 2))
                       + 2 ** (m - 1) + 2 - 3 * 2 ** (m - 1)) == 0
    require("K36-13", "$C(10)=16$", "$n/2<C(n)<4n$", r"\Theta(n)", "$C(n)=3n/2$")


def longest(a, fixed):
    if not a:
        return 0, [], 0
    run, best, comparisons = 1, int(fixed), 0
    trace = [(run, best)]
    for i in range(1, len(a)):
        comparisons += 1
        if a[i] == a[i - 1]:
            run += 1
        else:
            if not fixed:
                best = max(best, run)
            run = 1
        if fixed:
            best = max(best, run)
        trace.append((run, best))
    return best, trace, comparisons


def longest_oracle(a):
    return max((j - i for i in range(len(a)) for j in range(i + 1, len(a) + 1)
                if len(set(a[i:j])) == 1), default=0)


def p14():
    assert longest([], False)[0] == longest_oracle([])
    assert longest([7], False)[0] == 0 and longest([7], True)[0] == 1
    a = [2, 2, 5, 5, 5]
    assert longest(a, False) == (2, [(1, 0), (2, 0), (1, 2), (2, 2), (3, 2)], 4)
    assert longest(a, True)[0] == 3
    for n in range(8):
        for a in product(range(3), repeat=n):
            value, trace, comparisons = longest(a, True)
            assert value == longest_oracle(a)
            assert comparisons == max(n - 1, 0)
            for i, (run, best) in enumerate(trace, start=1):
                assert best == longest_oracle(a[:i])
                assert run == max(k for k in range(1, i + 1) if len(set(a[i-k:i])) == 1)
    require("K36-14", "$[7]$", "返回 0", "正确值为 1", "返回 2", "应返回 3",
            "$(1,0),(2,0),(1,2),(2,2),(3,2)$", r"\max(n-1,0)")


if __name__ == "__main__":
    for number, test in [(1, p01), (2, p02), (3, p03), (4, p04), (5, p05),
                         (6, p06), (7, p07), (8, p08), (9, p09), (10, p10),
                         (12, p12), (13, p13), (14, p14)]:
        check(f"K36-{number:02d}", test)
    try:
        proof11_support()
    except Exception as exc:
        FAILURES.append("K36-11")
        print(f"FAIL K36-11: {exc!r}")
    print("MANUAL K36-11 证明：不变量、终止性及唯一性须人工审阅")
    print("MANUAL K36-14 证明部分：一般输入的归纳论证须人工审阅；计算部分另行核对")
    raise SystemExit(bool(FAILURES))
