"""Independent executions for all 17 worked examples and their follow-ups."""
from itertools import combinations, combinations_with_replacement
from math import isqrt

import numpy as np
import sympy as sp


BASE = [5, 2, 8, 1, 9, 3]
FAILURES = []


def check(number, fn):
    try:
        fn()
    except Exception as exc:
        FAILURES.append(number)
        print(f"FAIL 例{number}: {exc!r}")
    else:
        print(f"PASS 例{number}")


def ex01():
    def digits(n):
        s, trace = 0, []
        while n > 0:
            before = n
            digit = n % 10
            s += digit
            n //= 10
            trace.append((before, digit, s, n))
        return s, trace
    assert digits(2748) == (21, [(2748, 8, 8, 274), (274, 4, 12, 27),
                               (27, 7, 19, 2), (2, 2, 21, 0)])
    assert digits(905)[0] == 14
    for n in range(1000):
        assert digits(n)[0] == sum(map(int, str(n)))


def ex02():
    a, trace = BASE.copy(), []
    for i in range(1, len(a)):
        a[i] += a[i - 1]
        trace.append(a.copy())
        assert np.array_equal(a[:i + 1], np.cumsum(BASE[:i + 1]))
        assert a[i + 1:] == BASE[i + 1:]
    assert trace == [[5, 7, 8, 1, 9, 3], [5, 7, 15, 1, 9, 3],
                     [5, 7, 15, 16, 9, 3], [5, 7, 15, 16, 25, 3],
                     [5, 7, 15, 16, 25, 28]]


def ex03():
    x, values = 1, []
    for n in range(1, 30):
        x = 2 * x + 1
        values.append(x)
        assert x == 2 ** (n + 1) - 1
    assert values[:5] == [3, 7, 15, 31, 63]
    i = sp.symbols("i", integer=True, nonnegative=True)
    assert sp.simplify(2 * (2 ** i - 1) + 1 - (2 ** (i + 1) - 1)) == 0


def reverse(a):
    a, i, j, trace = list(a), 0, len(a) - 1, []
    while i < j:
        a[i], a[j] = a[j], a[i]
        trace.append(a.copy())
        i += 1
        j -= 1
    return a, trace


def ex04():
    a, trace = reverse(BASE)
    assert trace == [[3, 2, 8, 1, 9, 5], [3, 9, 8, 1, 2, 5], [3, 9, 1, 8, 2, 5]]
    assert len(trace) == 3 and a == BASE[::-1]
    for n in range(30):
        a, trace = reverse(range(n))
        assert a == list(range(n))[::-1] and len(trace) == n // 2


def show(n, second=True):
    calls, exits, out = 0, 0, []
    def visit(n):
        nonlocal calls, exits
        calls += 1
        if n <= 0:
            exits += 1
            return
        out.append(n)
        visit(n - 1)
        if second:
            out.append(n)
        visit(n - 2)
    visit(n)
    return out, calls, exits


def ex05():
    assert show(3) == ([3, 2, 1, 1, 2, 3, 1, 1], 9, 5)
    assert show(3, False) == ([3, 2, 1, 1], 9, 5)
    assert show(2) == ([2, 1, 1, 2], 5, 3)


def fib_count(n):
    calls = 0
    def visit(n):
        nonlocal calls
        calls += 1
        if n <= 1:
            return n
        return visit(n - 1) + visit(n - 2)
    result = visit(n)
    return result, calls


def ex06():
    counts = [fib_count(n)[1] for n in range(13)]
    assert counts[:6] == [1, 1, 3, 5, 9, 15] and counts[10] == 177
    for n, count in enumerate(counts):
        assert count == 2 * sp.fibonacci(n + 1) - 1
        assert fib_count(n)[0] == sp.fibonacci(n)
        if n >= 2:
            assert count == 1 + counts[n - 1] + counts[n - 2]


def hanoi(n):
    out, calls, exits = [], 0, 0
    def visit(n, source, target, spare):
        nonlocal calls, exits
        calls += 1
        if n == 0:
            exits += 1
            return
        visit(n - 1, source, spare, target)
        out.append((source, target))
        visit(n - 1, spare, target, source)
    visit(n, "A", "C", "B")
    return out, calls, exits


def ex07():
    assert hanoi(3) == ([("A", "C"), ("A", "B"), ("C", "B"), ("A", "C"),
                         ("B", "A"), ("B", "C"), ("A", "C")], 15, 8)
    for n in range(8):
        moves, calls, exits = hanoi(n)
        assert (len(moves), calls, exits) == (2 ** n - 1, 2 ** (n + 1) - 1, 2 ** n)
        pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
        for source, target in moves:
            disk = pegs[source].pop()
            assert not pegs[target] or pegs[target][-1] > disk
            pegs[target].append(disk)
        assert pegs["C"] == list(range(n, 0, -1))


def euclid(a, b):
    initial, trace = sp.gcd(a, b), []
    while b != 0:
        old_a, old_b = a, b
        t = a % b
        a = b
        b = t
        trace.append((old_a, old_b, t, a, b))
        assert sp.gcd(a, b) == initial and 0 <= b < old_b
    return a, trace


def ex08():
    assert euclid(252, 105) == (21, [(252, 105, 42, 105, 42),
                                   (105, 42, 21, 42, 21), (42, 21, 0, 21, 0)])
    for a in range(1, 30):
        for b in range(30):
            assert euclid(a, b)[0] == sp.gcd(a, b)


def power(a, n):
    r, g, e, trace = 1, a, n, []
    while e > 0:
        if e % 2 == 1:
            r *= g
        g *= g
        e //= 2
        trace.append((r, g, e))
        assert r * g ** e == a ** n
    return r, trace


def ex09():
    assert power(3, 13) == (1594323, [(3, 9, 6), (3, 81, 3),
                                     (243, 6561, 1), (1594323, 43046721, 0)])
    assert bin(13)[2:] == "1101"
    for a in range(-3, 6):
        for n in range(16):
            result, trace = power(a, n)
            assert result == sp.Integer(a) ** n
            assert len(trace) == n.bit_length()
    # The logarithmic round formula is only used for positive n.
    r, g, k = sp.symbols("r g k", positive=True, integer=True)
    assert sp.simplify(r * (g ** 2) ** k - r * g ** (2 * k)) == 0
    assert sp.simplify(r * g * (g ** 2) ** k - r * g ** (2 * k + 1)) == 0


def ex10():
    a, b, trace = 0, 1, []
    for i in range(1, 31):
        a, b = b, a + b
        trace.append((a, b))
        assert (a, b) == (sp.fibonacci(i), sp.fibonacci(i + 1))
    assert trace[:7] == [(1, 1), (1, 2), (2, 3), (3, 5), (5, 8), (8, 13), (13, 21)]


def logarithmic_loops(n, dependent=False):
    c = 0
    for i in range(1, n + 1):
        j = 1
        while j <= (i if dependent else n):
            c += 1
            j *= 2
    return c


def ex11():
    assert logarithmic_loops(8) == 32 and logarithmic_loops(9) == 36
    for n in range(1, 200):
        c = logarithmic_loops(n)
        assert c == n * n.bit_length()
        assert n * np.log2(n) < c <= n * np.log2(n) + n + 1e-10
        d = logarithmic_loops(n, True)
        assert d == sum(i.bit_length() for i in range(1, n + 1))
        if n >= 2:
            assert d > (n / 2) * np.log2(n / 2)
            assert d <= n * (np.log2(n) + 1)


def square_count(n):
    c = 0
    for i in range(1, n + 1):
        if isqrt(i) ** 2 == i:
            for _ in range(i):
                c += 1
    return c


def ex12():
    assert square_count(100) == 385
    k, m = sp.symbols("k m", integer=True, positive=True)
    assert sp.simplify(sp.summation(k ** 2, (k, 1, m)) - m * (m + 1) * (2 * m + 1) / 6) == 0
    for n in range(1, 201):
        m, c = isqrt(n), square_count(n)
        assert c == m * (m + 1) * (2 * m + 1) // 6
        assert c <= n ** 1.5
        if n >= 4:
            assert c >= n ** 1.5 / 24


def linear_find(a, x):
    comparisons = 0
    for i, value in enumerate(a, 1):
        comparisons += 1
        if value == x:
            return i, comparisons
    return 0, comparisons


def ex13():
    assert linear_find(BASE, 9) == (5, 5)
    assert linear_find(BASE, 5) == (1, 1)
    assert linear_find(BASE, 10) == (0, 6)
    for n in range(1, 30):
        a = list(range(n))
        assert linear_find(a, 0)[1] == 1
        assert linear_find(a, n)[1] == n


def bad_max(a):
    m = 0
    for value in a:
        if value > m:
            m = value
    return m


def good_max(a):
    m = a[0]
    for value in a[1:]:
        if value > m:
            m = value
    return m


def ex14():
    assert bad_max(BASE) == 9
    assert bad_max([-3, -1, -2]) == 0
    assert good_max([-3, -1, -2]) == -1
    assert bad_max([]) == 0
    try:
        good_max([])
    except IndexError:
        pass
    else:
        raise AssertionError("empty input should fail at a[1]")


def binary_find(a, target, fixed=False):
    lo, hi, trace, seen = 1, len(a), [], set()
    while lo <= hi:
        if (lo, hi) in seen:
            return "cycle", trace
        seen.add((lo, hi))
        mid = (lo + hi) // 2
        trace.append((lo, hi, mid, a[mid - 1]))
        if a[mid - 1] == target:
            return mid, trace
        if a[mid - 1] < target:
            lo = mid + 1 if fixed else mid
        else:
            hi = mid - 1
    return 0, trace


def ex15():
    a = sorted(BASE)
    assert binary_find(a, 8)[0] == 5 and len(binary_find(a, 8)[1]) == 3
    assert binary_find(a, 9) == ("cycle", [(1, 6, 3, 3), (3, 6, 4, 5),
                                          (4, 6, 5, 8), (5, 6, 5, 8)])
    for n in range(7):
        for a in combinations_with_replacement(range(-2, 3), n):
            for target in range(-3, 4):
                result, trace = binary_find(a, target, True)
                assert (result != 0) == (target in a)
                if result:
                    assert a[result - 1] == target
                sizes = [hi - lo + 1 for lo, hi, _, _ in trace]
                assert all(x > y for x, y in zip(sizes, sizes[1:]))


def insertion(a, fixed=False):
    a = list(a)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= (0 if fixed else 1) and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def ex16():
    assert insertion([1, 5, 2]) == [1, 2, 5]
    assert insertion(BASE) == [5, 1, 2, 3, 8, 9]
    assert insertion([2, 1]) == [2, 1]
    assert insertion([2, 1], True) == [1, 2]
    assert insertion(BASE, True) == [1, 2, 3, 5, 8, 9]
    for a in [[], [1], [0], [-1], [2, 2], [3, 2, 1], [1, 3, 2]]:
        assert insertion(a, True) == sorted(a)


def two_sum(a, target, count=False):
    lo, hi, trace, found = 0, len(a) - 1, [], 0
    while lo < hi:
        total = a[lo] + a[hi]
        trace.append((lo + 1, hi + 1, total))
        if total == target:
            if not count:
                return (lo + 1, hi + 1), trace
            found += 1
            lo += 1
            hi -= 1
        elif total < target:
            lo += 1
        else:
            hi -= 1
    return (found if count else (0, 0)), trace


def ex17():
    a = sorted(BASE)
    assert two_sum(a, 12) == ((3, 6), [(1, 6, 10), (2, 6, 11), (3, 6, 12)])
    assert two_sum(a, 15) == ((0, 0), [(1, 6, 10), (2, 6, 11), (3, 6, 12),
                                     (4, 6, 14), (5, 6, 17)])
    for n in range(7):
        for a in combinations_with_replacement(range(-2, 3), n):
            for target in range(-5, 6):
                pairs = [(i + 1, j + 1) for i, j in combinations(range(n), 2)
                         if a[i] + a[j] == target]
                result, trace = two_sum(a, target)
                assert (result in pairs) if pairs else (result == (0, 0))
                assert len(trace) <= max(n - 1, 0)
                if len(set(a)) == len(a):
                    assert two_sum(a, target, True)[0] == len(pairs)
    for n in range(1, 30):
        assert len(two_sum(list(range(n)), 2 * n)[1]) == n - 1


if __name__ == "__main__":
    for number in range(1, 18):
        check(number, globals()[f"ex{number:02d}"])
    raise SystemExit(bool(FAILURES))
