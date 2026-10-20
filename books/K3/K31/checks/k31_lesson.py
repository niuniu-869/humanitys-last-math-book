"""Recompute lesson examples and check references against the current text.

Historical errata never turn an incorrect textbook formula into a PASS.
Numerical checks supplement, but do not replace, universal proofs.
"""

from collections import Counter
from fractions import Fraction
from pathlib import Path
import re
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
CHEATSHEET = (ROOT / "cheatsheet.md").read_text(encoding="utf-8")
EXAMPLES = dict(re.findall(r"\*\*例 (\d+)\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON, re.S))
n = sp.Symbol("n", integer=True, positive=True)
k = sp.Symbol("k", integer=True, nonnegative=True)
i = sp.Symbol("i", integer=True)
ARRAY = [5, 2, 8, 1, 9, 3]
failures = 0


def equal(actual, expected):
    assert actual == expected or sp.simplify(actual - expected) == 0, (actual, expected)


def anchor(number, *fragments):
    for fragment in fragments:
        assert fragment in EXAMPLES[str(number)], f"source anchor missing: {fragment}"


def run(number, fn, proof=False):
    global failures
    try:
        fn()
        print(f"PASS 例{number} 数值与可计算结论检查通过")
        if proof:
            print(f"MANUAL 例{number} 证明需人工核对；计算或代数核对不能替代证明")
    except Exception as exc:
        failures += 1
        print(f"FAIL 例{number} {type(exc).__name__}: {exc}")


def halve(value):
    states = [value]
    while value > 1:
        value //= 2
        states.append(value)
    return states


def recurrence(a, degree):
    function = sp.Function("T")
    return sp.rsolve(function(k) - a * function(k - 1) - 2**(degree * k),
                     function(k), {function(0): 1})


def example01():
    anchor(1, "返回 9", "| 6 | 3 | 假 | 9 |")
    largest, states, truths = ARRAY[0], [ARRAY[0]], []
    for value in ARRAY[1:]:
        truths.append(value > largest)
        if value > largest:
            largest = value
        states.append(largest)
    assert states == [5, 5, 8, 8, 9, 9]
    assert truths == [False, True, False, True, False]
    assert largest == 9
    # The unnumbered COUNT exercise in the same section.
    count, counts = 0, []
    for value in ARRAY:
        if value > 4:
            count += 1
        counts.append(count)
    assert counts == [1, 1, 2, 2, 3, 3]


def example02():
    anchor(2, "返回 5", r"2^5=32\le37<64=2^6")
    assert halve(37) == [37, 18, 9, 4, 2, 1]
    equal(len(halve(37)) - 1, sp.floor(sp.log(37, 2)))
    assert halve(100) == [100, 50, 25, 12, 6, 3, 1]


def example03():
    anchor(3, "返回 7")
    count, cumulative = 0, []
    for left in range(len(ARRAY) - 1):
        for right in range(left + 1, len(ARRAY)):
            if ARRAY[left] > ARRAY[right]:
                count += 1
        cumulative.append(count)
    assert cumulative == [3, 4, 6, 6, 7]


def example04():
    anchor(4, r"\frac{n(n-1)}{2}", "15", "21")
    equal(sp.summation(n - i, (i, 1, n - 1)), n * (n - 1) / 2)
    equal(sp.summation(i, (i, 1, n)), n * (n + 1) / 2)
    for size in range(1, 41):
        max_comparisons = sum(1 for _ in range(2, size + 1))
        pair_comparisons = sum(1 for left in range(1, size) for _ in range(left + 1, size + 1))
        assert max_comparisons == size - 1
        equal(pair_comparisons, sp.Rational(size * (size - 1), 2))
    assert sum(range(1, 6)) == 15 and sum(range(1, 7)) == 21


def example05():
    anchor(5, r"\lfloor\log_2 n\rfloor+1", r"8\times4=32")
    for size in range(1, 65):
        count = 0
        for _ in range(size):
            value = 1
            while value <= size:
                value *= 2
                count += 1
        equal(count, size * (sp.floor(sp.log(size, 2)) + 1))
    assert 8 * len([1, 2, 4, 8]) == 32


def example06():
    anchor(6, "16\\,384\\,000\\,000", "$128^2=16384$")
    equal(sp.summation(n, (i, 1, n)), n**2)
    assert sp.Integer(1000)**2 == 10**6
    assert sp.Integer(128000)**2 == 16384000000
    assert sp.Integer(128000)**2 / sp.Integer(1000)**2 == 16384
    triangle = sp.summation(i, (i, 1, n))
    ratio = sp.simplify(triangle.subs(n, 2 * n) / triangle)
    equal(ratio, 2 * (2 * n + 1) / (n + 1))
    equal(sp.limit(ratio, n, sp.oo), 4)
    anchor(6, r"\frac{2(2n+1)}{n+1}", "接近翻 4 倍")
    assert "长度翻倍时工作量仍然翻 4 倍" not in LESSON
    assert sp.simplify(4 - ratio).is_positive


def example07():
    anchor(7, "比较 3 次", "比较 6 次", r"\frac{n+1}{2}")

    def search(target):
        count = 0
        for index, value in enumerate(ARRAY, 1):
            count += 1
            if value == target:
                return index, count
        return 0, count

    assert search(8) == (3, 3) and search(7) == (0, 6)
    counts = [search(value)[1] for value in ARRAY]
    assert min(counts) == 1 and max(counts) == 6
    equal(sp.Rational(sum(counts), len(counts)), sp.Rational(7, 2))
    equal(sp.summation(i / n, (i, 1, n)), (n + 1) / 2)


def example08():
    anchor(8, "$c=3$", "$c=4$", "$n_0=8$", "$252\\le256$")
    f = 3 * n**2 + 5 * n + 20
    assert [f.subs(n, x) for x in (10, 100, 1000, 10**6)] == [370, 30520, 3005020, 3000005000020]
    equal(f.subs(n, 8), 252)
    equal(sp.limit(f / n**2, n, sp.oo), 3)
    t = sp.Symbol("t", nonnegative=True)
    assert sp.expand((4 * n**2 - f).subs(n, t + 8)).is_positive
    assert sp.expand(f - 3 * n**2).is_positive
    assert sp.simplify(9 * n - (2 * n + 7)).subs(n, t + 1).is_nonnegative


def example09():
    anchor(9, r"n=\max(n_0,\lceil c\rceil+1)")
    equal(sp.limit(n**2 / n, n, sp.oo), sp.oo)
    for c in [sp.Rational(1, 10), sp.Rational(7, 2), 4, 10**4]:
        for start in (1, 3, 20000):
            witness = max(start, sp.ceiling(c) + 1)
            assert witness >= start and witness**2 > c * witness


def example10():
    anchor(10, r"(\log_2 n)^3\prec n\log_2 n\prec n^{1.5}\prec n^2\prec2^n")
    functions = [sp.log(n, 2)**3, n * sp.log(n, 2), n**sp.Rational(3, 2), n**2, 2**n]
    for left, right in zip(functions, functions[1:]):
        equal(sp.limit(left / right, n, sp.oo), 0)
    # Check all four growth comparisons used before the example.
    equal(sp.limit(sp.log(n) / n**sp.Rational(1, 3), n, sp.oo), 0)
    equal(sp.limit(n**3 / 2**n, n, sp.oo), 0)
    equal(sp.limit(2**n / sp.factorial(n), n, sp.oo), 0)
    equal(sp.limit(sp.factorial(n) / n**n, n, sp.oo), 0)


def example11():
    anchor(11, r"2^{n+1}=\Theta(2^n)", r"2^{2n}\ne O(2^n)")
    equal(sp.simplify(2**(n + 1) / 2**n), 2)
    equal(sp.limit(2**(2 * n) / 2**n, n, sp.oo), sp.oo)
    equal(sp.expand_log(sp.log(n**2), force=True), 2 * sp.log(n))


def example12():
    anchor(12, "空和等于 0", "SUM(A, n−1) + A[n]")

    def recursive_sum(values, length):
        if length == 0:
            return 0
        return recursive_sum(values, length - 1) + values[length - 1]

    returns = [recursive_sum(ARRAY, length) for length in range(7)]
    assert returns == [0, 5, 7, 15, 16, 25, 28]
    assert returns == [sum(ARRAY[:length]) for length in range(7)]
    prefix, last = sp.symbols("prefix last")
    equal((prefix + last) - prefix, last)


def example13():
    anchor(13, "59049", "6 次乘法", "8192", "7 次乘法")

    def power(a, exponent, trace):
        if exponent == 0:
            trace.append((0, 1, 0))
            return 1, 0
        h, previous = power(a, exponent // 2, trace)
        if exponent % 2 == 0:
            value, extra = h * h, 1
        else:
            value, extra = h * h * a, 2
        trace.append((exponent, value, extra))
        return value, previous + extra

    trace = []
    assert power(3, 10, trace) == (59049, 6)
    assert trace == [(0, 1, 0), (1, 3, 2), (2, 9, 1), (5, 243, 2), (10, 59049, 1)]
    trace = []
    assert power(2, 13, trace) == (8192, 7)
    assert [v for _, v, _ in trace] == [1, 2, 8, 64, 8192]
    a = sp.Symbol("a", nonzero=True)
    q = sp.Symbol("q", integer=True, nonnegative=True)
    equal((a**q)**2, a**(2 * q))
    equal((a**q)**2 * a, a**(2 * q + 1))
    for exponent in range(1, 40):
        trace = []
        value, _ = power(3, exponent, trace)
        assert value == 3**exponent
        equal(len(trace), sp.floor(sp.log(exponent, 2)) + 2)


def example14():
    anchor(14, "T(n)=T(0)+n=n", r"\Theta(n)")
    function = sp.Function("T")
    result = sp.rsolve(function(n) - function(n - 1) - 1, function(n), {function(0): 0})
    equal(result, n)
    equal(result.subs(n, 6), 6)


def example15():
    anchor(15, "2^n-1", "1023", r"1.8\times10^{19}")
    function = sp.Function("H")
    result = sp.rsolve(function(n) - 2 * function(n - 1) - 1, function(n), {function(1): 1})
    equal(result, 2**n - 1)
    assert result.subs(n, 3) == 7 and result.subs(n, 10) == 1023
    assert abs(float(result.subs(n, 64)) / 1.8e19 - 1) < 0.03
    equal(sp.limit(result / 2**n, n, sp.oo), 1)


def example16():
    anchor(16, "2F(n+1)-1", "2 692 537", "331 160 281")
    calls = [1, 1]
    for size in range(2, 41):
        calls.append(calls[-1] + calls[-2] + 1)
    assert calls[:11] == [1, 1, 3, 5, 9, 15, 25, 41, 67, 109, 177]
    assert calls[30] == 2692537 and calls[40] == 331160281
    for size, value in enumerate(calls):
        equal(value, 2 * sp.fibonacci(size + 1) - 1)
    nodes = Counter()

    def visit(size):
        nodes[size] += 1
        if size > 1:
            visit(size - 1)
            visit(size - 2)

    visit(5)
    assert sum(nodes.values()) == 15 and nodes[3] == 2 and nodes[2] == 3
    x = sp.Symbol("x")
    phi = max(sp.solve(x**2 - x - 1, x))
    psi = 1 - phi
    equal(phi, (1 + sp.sqrt(5)) / 2)
    assert abs(psi) < 1 < phi
    # Binet's other term and the constant disappear after division by phi**n.
    equal(sp.limit((abs(psi) / phi)**n, n, sp.oo), 0)
    equal(sp.limit(phi**(-n), n, sp.oo), 0)
    anchor(16, r"C(n)=\Theta(\varphi^n)", r"\varphi=\frac{1+\sqrt5}{2}")
    assert r"\Theta(1.618^n)" not in LESSON + CHEATSHEET
    equal(sp.limit((phi / sp.Rational(1618, 1000))**n, n, sp.oo), sp.oo)


def example17():
    anchor(17, r"n(\log_2 n+1)", "T(8)", "32=8")
    closed = recurrence(2, 1)
    equal(closed, 2**k * (k + 1))
    assert [closed.subs(k, value) for value in (1, 2, 3)] == [4, 12, 32]
    equal(sp.summation(2**i * 2**(k - i), (i, 0, k)), closed)
    equal(sp.limit(closed / (2**k * k), k, sp.oo), 1)
    equal(recurrence(2, 0), 2 * 2**k - 1)


def example18():
    anchor(18, r"2n-1=\Theta(n)")
    closed = recurrence(1, 1)
    equal(closed, 2 * 2**k - 1)
    equal(sp.summation(2**(k - i), (i, 0, k)), closed)
    equal(sp.limit(closed / 2**k, k, sp.oo), 2)


def example19():
    anchor(19, r"\Theta(n^{\log_2 3})", r"\Theta(n^3)")
    rows = [(1, 0, k), (2, 1, 2**k * k), (4, 1, 4**k),
            (3, 1, 3**k), (2, 2, 4**k), (8, 2, 8**k)]
    for a, degree, scale in rows:
        closed = recurrence(a, degree)
        ratio = sp.limit(closed / scale, k, sp.oo)
        assert ratio.is_positive and ratio.is_finite, (a, degree, ratio)
        value = 1
        for power in range(10):
            if power:
                value = a * value + 2**(degree * power)
            equal(value, closed.subs(k, power))
    rounded = sp.Rational(1585, 1000)
    mismatch = sp.limit(recurrence(3, 1) / 2**(rounded * k), k, sp.oo)
    equal(mismatch, 0)
    assert r"\Theta(n^{1.585})" not in LESSON + CHEATSHEET
    equal(sp.limit(recurrence(3, 1) / 3**k, k, sp.oo), 3)


def example20():
    anchor(20, r"\Theta(n^2)", r"\Theta(n\log^2 n)", r"\Omega(n\log n)")
    equal(sp.summation(i, (i, 1, n)), n * (n + 1) / 2)
    equal(sp.limit((1 + n * (n + 1) / 2) / n**2, n, sp.oo), sp.Rational(1, 2))
    # Normalize by 2**k: S(k)=S(k-1)+k and S(0)=1.
    closed = 2**k * (1 + sp.summation(i, (i, 1, k)))
    value = 1
    for power in range(20):
        if power:
            value = 2 * value + 2**power * power
        equal(value, closed.subs(k, power))
    internal = sp.summation(2**k * (k - i), (i, 0, k - 1))
    equal(closed - internal, 2**k)
    equal(sp.limit(closed / (2**k * k**2), k, sp.oo), sp.Rational(1, 2))
    anchor(20, r"n(\log_2 n+(\log_2 n-1)+\cdots+1)", "再加上叶子的 $n$")
    anchor(20, r"0<x\le1", "T(x)=1", "$3n$", r"\lceil\log_{3/2}n\rceil")
    # Unequal splitting: exact rational sizes, terminal cost 1 at size<=1.
    # Any leaf has size>1/3. Hence replacing its size by 1 costs <3 times
    # its mass. Each level is bounded by 3n, not an unqualified n.
    for size in (2, 3, 4, 9, 27, 81, 243):
        frontier = [Fraction(size)]
        layer_costs = []
        while frontier:
            layer_costs.append(sum(v if v > 1 else 1 for v in frontier))
            next_level = []
            for value in frontier:
                if value > 1:
                    next_level.extend([value / 3, 2 * value / 3])
                else:
                    assert value > Fraction(1, 3)
            frontier = next_level
        full_levels = 0
        while 3**(full_levels + 1) <= size:
            full_levels += 1
        assert layer_costs[:full_levels] == [size] * full_levels
        assert max(layer_costs) <= 3 * size
        max_depth = int(sp.ceiling(sp.log(size) / sp.log(sp.Rational(3, 2))))
        assert len(layer_costs) <= max_depth + 1
        assert sum(layer_costs) >= size * full_levels
        assert sum(layer_costs) <= 3 * size * (max_depth + 1)
    equal(sp.limit((sp.log(n, 3) - 1) / sp.log(n), n, sp.oo), 1 / sp.log(3))
    equal(sp.limit(3 * (sp.log(n) / sp.log(sp.Rational(3, 2)) + 2) / sp.log(n), n, sp.oo),
          3 / sp.log(sp.Rational(3, 2)))


def growth_boundaries():
    assert "$n=4$ 追平 $n^2$" in LESSON
    assert "$n\\ge5$ 起超过" in LESSON
    assert 2**4 == 4**2
    for size in range(5, 100):
        assert 2**size > size**2
    assert all(2**size < size**3 for size in range(2, 10))
    assert 2**10 == 1024 > 10**3


def geometric_sum():
    assert r"\sum_{i=0}^{k}r^i<\sum_{i=0}^{\infty}r^i=\dfrac1{1-r}" in LESSON
    assert r"\sum_{i\ge0}r^i<\dfrac1{1-r}" not in LESSON
    r = sp.Symbol("r", positive=True)
    finite = sp.summation(r**i, (i, 0, k))
    for ratio in (sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(9, 10)):
        equal(finite.subs(r, ratio), (1 - ratio**(k + 1)) / (1 - ratio))
        for depth in (0, 1, 8, 30):
            assert 1 <= finite.subs({r: ratio, k: depth}) < 1 / (1 - ratio)
        equal(sp.limit(finite.subs(r, ratio), k, sp.oo), 1 / (1 - ratio))


def time_table():
    rows = re.findall(r"^\| (10|20|50|100) \| (.*?) \| (.*?) \| (.*?) \|$", LESSON, re.M)
    assert len(rows) == 4
    units = {"微秒": 1e-6, "毫秒": 1e-3, "秒": 1,
             "天": 86400, "年": 365 * 86400}

    def duration(cell):
        number, unit = cell.strip().split()
        number = number.strip("$")
        match = re.fullmatch(r"(?:(\d+(?:\.\d+)?)\\times)?10\^\{(\d+)\}", number)
        value = float(match[1] or 1) * 10**int(match[2]) if match else float(number)
        return value * units[unit]

    for size, *cells in rows:
        size = int(size)
        for steps, cell in zip((size**2, 2**size, sp.factorial(size)), cells):
            if cell.strip() == "—":
                continue
            actual = float(steps) / 10**9
            assert abs(duration(cell) / actual - 1) < 0.05, (size, cell, actual)
    assert "116 天" in LESSON and "约 2.7 秒" in LESSON
    assert round(10**16 / 10**9 / 86400) == 116
    assert round(float(10**8 * sp.log(10**8, 2) / 10**9), 1) == 2.7
    assert r"5\times10^7" in LESSON and "0.1 秒" in LESSON
    equal(sp.Rational(50, 1000) * 10**9, 5 * 10**7)
    equal(sp.Rational(10**8, 10**9), sp.Rational(1, 10))


def cheat_boundaries():
    for formula in (r"\lfloor\log_2 n\rfloor+1", r"\lceil\log_2 n\rceil",
                    r"\lfloor\log_2 n\rfloor", "T(0)=0", "H(1)=1", "C(0)=C(1)=1"):
        assert formula in CHEATSHEET, formula
    for size in range(1, 130):
        counts = []
        for inclusive in (True, False):
            value, count = 1, 0
            while value <= size if inclusive else value < size:
                value *= 2
                count += 1
            counts.append(count)
        counts.append(len(halve(size)) - 1)
        assert counts == [size.bit_length(), (size - 1).bit_length(), size.bit_length() - 1]
        if size == 8:
            assert counts == [4, 3, 3]


def power_boundaries():
    summary = LESSON.split("### 本章小结", 1)[1]
    assert "每个非出口层做 1 次或 2 次乘法" in summary
    assert "首次命中位置等可能" in summary
    assert r"\Theta(\varphi^n)" in summary
    for exponent in range(130):
        current, multiplications, depth = exponent, 0, 1
        while current:
            multiplications += 1 + current % 2
            current //= 2
            depth += 1
        assert depth == exponent.bit_length() + 1
        assert multiplications == exponent.bit_length() + exponent.bit_count()


def self_exercises():
    anchor(10, r"\log_2 n\prec\sqrt n\prec n\log_2 n")
    equal(sp.limit(sp.log(n, 2) / sp.sqrt(n), n, sp.oo), 0)
    equal(sp.limit(sp.sqrt(n) / (n * sp.log(n, 2)), n, sp.oo), 0)
    anchor(14, "T(n)=T(0)+2n=2n+1")
    function = sp.Function("T")
    equal(sp.rsolve(function(n) - function(n - 1) - 2, function(n), {function(0): 1}), 2*n + 1)


if __name__ == "__main__":
    for number in range(1, 21):
        run(number, globals()[f"example{number:02d}"], proof=number in (8, 9, 12, 13))
    for name, check in (("附项-增长边界", growth_boundaries), ("附项-等比和", geometric_sum),
                        ("附项-时间表", time_table), ("附项-速记表", cheat_boundaries),
                        ("附项-快速幂边界", power_boundaries), ("附项-自做题", self_exercises)):
        run(name, check)
    sys.exit(bool(failures))
