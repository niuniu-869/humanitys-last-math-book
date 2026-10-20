"""Check all 24 examples and inline exercises against the revised calculations.

Examples 3 and 15 include boundary checks; example 14 checks rounding order.
Numerical PASS results do not replace review of general proofs or wording.
"""
from collections import deque
from functools import lru_cache
from itertools import combinations, product
from math import erfc, sqrt
import sys

import numpy as np
import sympy as s


failures = 0
A = [5, 2, 8, 1, 9, 3]


def check(number, work):
    global failures
    try:
        work()
        print(f"PASS 例{number}")
    except Exception as exc:
        failures += 1
        print(f"FAIL 例{number} {type(exc).__name__}: {exc}")


def close(actual, expected, atol):
    assert np.allclose(np.asarray(actual, dtype=float), expected, atol=atol, rtol=0), (actual, expected)


def inversions(arr, threshold=1):
    return sum(bool(arr[i]-arr[j] >= threshold) for i, j in combinations(range(len(arr)), 2))


def bubble(arr):
    arr = list(arr)
    swaps, passes = [], []
    while True:
        count = 0
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                swaps.append((arr[i], arr[i+1]))
                arr[i], arr[i+1] = arr[i+1], arr[i]
                count += 1
        passes.append(count)
        if not count:
            return arr, swaps, passes


def e01():
    # Lines y=m*x+m**2: on the new line all earlier intersections are distinct.
    regions = [1]
    for m in range(1, 9):
        intersections = {-s.Integer(m+j) for j in range(1, m)}
        regions.append(regions[-1]+len(intersections)+1)
    assert regions[1:5] == [2, 4, 7, 11]
    assert all(value == 1+n*(n+1)//2 for n, value in enumerate(regions))
    n = s.symbols("n", integer=True, positive=True)
    assert s.simplify((1+n*(n+1)/2)-(1+(n-1)*n/2)) == n
    circles = [2]
    for k in range(2, 9):
        circles.append(circles[-1]+2*(k-1))
    assert circles[:4] == [2, 4, 8, 14]
    assert all(value == k*k-k+2 for k, value in enumerate(circles, 1))


def e02():
    values = [sum(k*s.factorial(k) for k in range(1, n+1)) for n in range(1, 9)]
    assert values[:4] == [1, 5, 23, 119]
    assert all(v == s.factorial(n+1)-1 for n, v in enumerate(values, 1))
    n = s.symbols("n", integer=True, positive=True)
    assert s.simplify((s.factorial(n+1)-1)+(n+1)*s.factorial(n+1)-(s.factorial(n+2)-1)) == 0


def e03():
    counts = []
    for n in range(1, 9):
        chords = list(combinations(range(n), 2))
        crossings = sum(a < c < b < d or c < a < d < b for (a, b), (c, d) in combinations(chords, 2))
        count = 1+len(chords)+crossings
        assert count == 1+s.binomial(n, 2)+s.binomial(n, 4)
        counts.append(count)
    assert counts[:6] == [1, 2, 4, 8, 16, 31]
    assert counts[5] != 2**5
    assert all(s.isprime(n*n+n+41) for n in range(40))
    assert 40**2+40+41 == 41**2
    # Check the first nonzero contribution and the first failed power-of-two guess.
    assert s.binomial(4, 4) == 1
    print("PASS 例3-边界说明 C(4,4)=1；n=6 时块数首次偏离 2^(n-1)")


def e04():
    @lru_cache(None)
    def endpoints(mask):
        if mask & (mask-1) == 0:
            return frozenset((mask.bit_length(),))
        results = set()
        pivot = mask & -mask
        part = (mask-1) & mask
        while part:
            if part & pivot:
                other = mask ^ part
                if other:
                    results.update(abs(x-y) for x in endpoints(part) for y in endpoints(other))
            part = (part-1) & mask
        return frozenset(results)
    assert sum(range(1, 11)) == 55
    assert endpoints((1 << 10)-1) == {1, 3, 5, 7, 9}
    a, b = s.symbols("a b")
    assert s.expand((a+b+a*b+1)-(a+1)*(b+1)) == 0
    arr = list(range(1, 9))
    while len(arr) > 1:
        x, y = arr.pop(), arr.pop()
        arr.append(x+y+x*y)
    assert arr[0] == s.factorial(9)-1 == 362879


def e05():
    cells = {(i, j) for i in range(6) for j in range(6)}-{(0, 0), (5, 5)}
    groups = [sum((i+j) % 2 == parity for i, j in cells) for parity in (0, 1)]
    assert groups == [16, 18]
    placements = [{(i, j), (i+di, j+dj)} for i, j in cells for di, dj in ((1, 0), (0, 1))
                  if (i+di, j+dj) in cells]
    assert all(sum((i+j) % 2 for i, j in tile) == 1 for tile in placements)
    assert len(cells) == 34 and groups[0] != groups[1]


def e06():
    result, swaps, passes = bubble(A)
    assert result == sorted(A) and len(swaps) == inversions(A) == 7
    assert passes == [3, 2, 2, 0]
    @lru_cache(None)
    def possible_lengths(arr):
        nexts = []
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                nxt = list(arr)
                nxt[i], nxt[i+1] = nxt[i+1], nxt[i]
                nexts.append(tuple(nxt))
        if not nexts:
            return frozenset((0,))
        return frozenset(1+n for nxt in nexts for n in possible_lengths(nxt))
    assert possible_lengths(tuple(A)) == {7}


def e07():
    def moves(state):
        for i, j in combinations(range(3), 2):
            if state[i] and state[j]:
                nxt = list(state)
                nxt[i] -= 1
                nxt[j] -= 1
                nxt[3-i-j] += 2
                yield tuple(nxt)
    start = (4, 5, 6)
    seen, queue = {start}, deque([start])
    while queue:
        current = queue.popleft()
        for nxt in moves(current):
            assert all((nxt[i]-nxt[j]-current[i]+current[j]) % 3 == 0 for i, j in combinations(range(3), 2))
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    assert not any(state.count(0) == 2 for state in seen)
    route = [(2, 5, 8), (1, 4, 10), (0, 3, 12), (2, 2, 11), (1, 1, 13), (0, 0, 15)]
    assert all(b in set(moves(a)) for a, b in zip(route, route[1:]))


def e08():
    for maximum, end in ((3, 21), (4, 31)):
        win = [False]
        for n in range(1, end+1):
            win.append(any(not win[n-m] for m in range(1, min(n, maximum)+1)))
        assert all(win[n] == (n % (maximum+1) != 0) for n in range(end+1))
        assert [m for m in range(1, maximum+1) if not win[end-m]] == [1]
        assert all(1 <= maximum+1-m <= maximum for m in range(1, maximum+1))


def e09():
    distance = {1: 0}
    queue = deque([1])
    while queue:
        n = queue.popleft()
        for nxt in (n+1, 2*n):
            if nxt <= 100 and nxt not in distance:
                distance[nxt] = distance[n]+1
                queue.append(nxt)
    assert distance[100] == 8
    path = [1, 2, 3, 6, 12, 24, 25, 50, 100]
    assert all(b in (a+1, 2*a) for a, b in zip(path, path[1:]))
    # 1 -> 2 can be counted as +1, giving the displayed 3 additions and 5 doublings.
    assert sum(b == a+1 for a, b in zip(path, path[1:])) == 3
    n, steps = 1, 0
    while n < 100:
        n = 2*n if 2*n <= 100 else n+1
        steps += 1
    assert steps == 42


def e10():
    total = 12**6
    distinct = s.prod(range(7, 13))
    assert (distinct, total) == (665280, 2985984)
    close(float(distinct/total), 0.2228, 0.00005)
    close(float(1-distinct/total), 0.7772, 0.00005)


def e11():
    a, b = s.symbols("a b", positive=True)
    gap = (a+b)/2-s.sqrt(a*b)
    square = (s.sqrt(a)-s.sqrt(b))**2/2
    assert s.simplify(gap-square) == 0
    assert square.is_nonnegative
    assert gap.subs(b, a) == 0


def e12():
    g = s.symbols("g", positive=True)
    u = s.symbols("u", real=True)
    average = s.integrate(g-u, (u, 0, g))/g
    assert s.simplify(average-g/2) == 0
    assert average.subs(g, 10) == 5 and s.limit(average, g, 0, dir="+") == 0
    for intervals, expected in (([5, 15], s.Rational(25, 4)), ([6, 14], s.Rational(29, 5))):
        area = sum(s.integrate(t-u, (u, 0, t)) for t in intervals)
        assert area/sum(intervals) == expected
    assert (s.Rational(25, 4)-5)/5 == s.Rational(1, 4)


def e13():
    n = np.array([1000, 2000, 4000, 8000])
    observed = np.array([0.8, 3.1, 12.6, 49.5])
    x, y = np.log2(n/1000), np.log2(observed)
    u, b = np.linalg.lstsq(np.column_stack((np.ones(4), x)), y, rcond=None)[0]
    close(y, [-0.322, 1.632, 3.655, 5.629], 0.0005)
    numerator = np.sum((x-x.mean())*(y-y.mean()))
    assert x.mean() == 1.5
    assert [format(v, ".4f") for v in (y.mean(), numerator, b, u)] == [
        "2.6488", "9.9385", "1.9877", "-0.3328"]
    assert [format(v, ".6f") for v in (numerator, b, u)] == [
        "9.938469", "1.987694", "-0.332779"]
    assert np.max(np.abs(y-(u+b*x))) < 0.03
    close(2**b, 3.97, 0.005)
    close(u+4*b, 7.62, 0.005)
    close(2**(u+4*b), 196, 0.5)
    close(0.8*16**2, 205, 0.5)


def e14():
    def dcg(arr):
        return sum((2**r-1)/np.log2(i+2) for i, r in enumerate(arr))
    actual = [3, 2, 3, 0, 1]
    ideal = sorted(actual, reverse=True)
    swapped = [2, 3, 3, 0, 1]
    close([dcg(actual), dcg(ideal)], [12.780, 13.347], 0.0005)
    assert round(dcg(swapped), 3) == 11.303
    rounded_terms = [round((2**r-1)/np.log2(i+2), 3) for i, r in enumerate(swapped)]
    close(sum(rounded_terms), 11.304, 1e-12)
    print("PASS 例14-舍入核对 交换后 DCG=11.303361…；11.304 来自中间项先舍入")
    close(dcg(actual)/dcg(ideal), 0.957, 0.0005)
    close(dcg(swapped)-dcg(actual), -1.476, 0.0006)
    assert dcg(swapped) < dcg(actual)
    close([dcg([1, 3, 2]), dcg([3, 2, 1]), dcg([1, 3, 2])/dcg([3, 2, 1])], [6.917, 9.393, 0.736], 0.0006)


def e15():
    assert [inversions(A, k) for k in (1, 2, 3)] == [7, 6, 5]
    assert [inversions([4, 3, 2, 1], k) for k in (1, 2, 3)] == [6, 3, 1]
    assert [inversions([3, 1, 4, 2], k) for k in (1, 2)] == [3, 2]
    assert all(inversions([1, 2, 3], k) == 0 for k in range(1, 5))
    assert all(inversions(A, k) >= inversions(A, k+1) for k in range(1, 10))
    # Dropping the stated integer assumption breaks equality with ordinary inversions.
    example = [s.Rational(1, 2), s.Integer(0)]
    ordinary = sum(bool(example[i] > example[j]) for i, j in combinations(range(2), 2))
    assert ordinary == 1 and inversions(example, 1) == 0
    print("PASS 例15-边界说明 去掉整数条件时，[1/2,0] 的普通逆序对为 1，I_1=0")


def e16():
    _, swaps, _ = bubble(A)
    assert swaps == [(5, 2), (8, 1), (9, 3), (5, 1), (8, 3), (2, 1), (5, 3)]
    differences = [a-b for a, b in swaps]
    assert differences == [3, 7, 6, 4, 5, 1, 2]
    assert sum(d >= 3 for d in differences) == 5
    arr = A.copy()
    changes = []
    for a, b in swaps:
        i = arr.index(a)
        assert arr[i+1] == b
        old = inversions(arr, 3)
        arr[i], arr[i+1] = arr[i+1], arr[i]
        changes.append(old-inversions(arr, 3))
    assert changes == [1, 1, 1, 1, 1, 0, 0]


def heron(c, initial, count):
    values = [s.Rational(initial)]
    for _ in range(count-1):
        values.append((values[-1]+s.Rational(c)/values[-1])/2)
    return values


def e17():
    values = heron(2, 1, 4)
    assert values[1:] == [s.Rational(3, 2), s.Rational(17, 12), s.Rational(577, 408)]
    close(float(values[1]), 1.5, 0.000001)
    close(float(values[2]), 1.41667, 0.000005)
    close(float(values[3]), 1.414216, 0.0000005)


def e18():
    a = s.symbols("a", positive=True)
    next_error = (a+2/a)/2-s.sqrt(2)
    assert s.simplify(next_error-(a-s.sqrt(2))**2/(2*a)) == 0
    assert ((a-s.sqrt(2))**2/(2*a)).is_nonnegative
    for val in heron(2, 1, 5)[1:]:
        err = val-s.sqrt(2)
        assert err > 0
        assert 0 < err**2/(2*val) < err**2/2


def e19():
    a, c = s.symbols("a c", positive=True)
    assert s.simplify((a+c/a)/2-s.sqrt(c)-(a-s.sqrt(c))**2/(2*a)) == 0
    values = heron(9, 1, 5)
    for val, expected, tol in zip(values, [1, 5, 3.4, 3.0235, 3.00009], [0, 0, 1e-9, 0.00005, 0.000005]):
        close(float(val), expected, tol)
    assert heron(2, -1, 6) == [-v for v in heron(2, 1, 6)]
    close(float(heron(2, -1, 6)[-1]), -sqrt(2), 1e-12)
    assert ((a+c/a)/2).subs(a, 0).has(s.zoo)
    large = heron(2, 1000, 4)
    close([float(v) for v in large], [1000, 500.001, 250.0025, 125.005], 0.0005)


def e20():
    values = heron(2, 1, 5)[1:]
    errors = np.array([float((v-s.sqrt(2)).evalf(40)) for v in values])
    assert [format(e, fmt) for e, fmt in zip(errors, (".4f", ".5f", ".2e", ".2e"))] == [
        "0.0858", "0.00245", "2.12e-06", "1.59e-12"]
    digits = -np.log10(errors)
    close(digits, [1.07, 2.61, 5.67, 11.80], 0.005)
    close(digits[1:]/digits[:-1], [2.45, 2.17, 2.08], 0.005)
    all_errors = [abs(v-s.sqrt(2)) for v in heron(2, 1, 5)]
    threshold = s.Rational(1, 10**6)
    assert all(err > threshold for err in all_errors[:4])
    assert all_errors[4] < threshold
    assert next(i for i, err in enumerate(all_errors, 1) if err < threshold) == 5
    close(digits[1:], 2*digits[:-1]+np.log10(2*np.array(values[:-1], dtype=float)), 1e-12)
    print("PASS 例20-精度检验 第4项未达 10^-6，第5项首次达到")


def e21():
    dot = np.array([4., 0., -4.])
    softmax = lambda v: np.exp(v)/np.exp(v).sum()
    scaled = softmax(dot/sqrt(16))
    raw = softmax(dot)
    close(scaled, [0.665, 0.245, 0.090], 0.0005)
    close(raw, [0.982, 0.018, 0.0003], 0.0005)
    close(scaled.sum(), 1, 1e-12)
    close(raw.sum(), 1, 1e-12)
    assert raw.max() > scaled.max()
    n, d = s.symbols("n d", positive=True)
    cost = n*n*d
    assert s.simplify(cost.subs(n, 2*n)/cost) == 4
    assert (cost.subs({n: 1000, d: 64}), cost.subs({n: 2000, d: 64})) == (64000000, 256000000)
    assert s.simplify(d/s.sqrt(d)**2) == 1


def e22():
    results = []
    exact_tails = []
    for n, observed in ((120, 30), (60, 15)):
        p0 = s.Rational(1, 6)
        mean, var = n*p0, n*p0*(1-p0)
        z = float((observed-mean)/s.sqrt(var))
        p = erfc(z/sqrt(2))/2
        results.append((float(mean), float(s.sqrt(var)), z, p))
        tail = sum(s.binomial(n, k)*p0**k*(1-p0)**(n-k) for k in range(observed, n+1))
        exact_tails.append(tail)
    close(results[0][:3], [20, 4.082, 2.449], 0.0005)
    close(results[1][:3], [10, 2.887, 1.732], 0.0005)
    close([r[3] for r in results], [0.0072, 0.0416], 0.00005)
    assert results[0][3] < 0.01 < results[1][3] < 0.05
    assert [format(float(tail), ".10f") for tail in exact_tails] == ["0.0128816057", "0.0647803752"]
    assert [tail < s.Rational(5, 100) for tail in exact_tails] == [True, False]
    assert [tail < s.Rational(1, 100) for tail in exact_tails] == [False, False]
    print("PASS 例22-精确二项右尾 5%下分别拒绝、不拒绝；1%下均不拒绝")
    print("PASS 例22-近似对照 未修正正态尾概率约为0.00715、0.04163，与精确判定分开")
    p = s.symbols("p", nonnegative=True)
    bernoulli_variance = (1-p)*(0-p)**2+p*(1-p)**2
    assert s.simplify(bernoulli_variance-p*(1-p)) == 0


def e23():
    x, y, lam, b = s.symbols("x y lam b", real=True)
    lagrangian = x*y-lam*(x+2*y-b)
    sol = s.solve([s.diff(lagrangian, v) for v in (x, y, lam)], (x, y, lam), dict=True)[0]
    assert sol == {x: b/2, y: b/4, lam: b/4}
    best = s.simplify((x*y).subs(sol))
    assert best == b*b/8
    assert (best.subs(b, 12), best.subs(b, 13)) == (18, s.Rational(169, 8))
    assert best.subs(b, 13)-best.subs(b, 12) == s.Rational(25, 8)
    assert s.diff(best, b).subs(b, 12) == sol[lam].subs(b, 12) == 3
    reduced = (12-2*y)*y
    assert s.expand(reduced-(18-2*(y-3)**2)) == 0
    assert s.diff(reduced, y, 2) < 0
    assert reduced.subs(y, 0) == reduced.subs(y, 6) == 0


def e24():
    def best_prefix(n, gap):
        scores = []
        for mask in product((0, 1), repeat=n):
            indices = [i for i, chosen in enumerate(mask) if chosen]
            if all(b-a >= gap for a, b in zip(indices, indices[1:])):
                scores.append(sum(A[i] for i in indices))
        return max(scores)
    assert [best_prefix(n, 2) for n in range(1, 7)] == [5, 5, 13, 13, 22, 22]
    assert [best_prefix(n, 3) for n in range(1, 7)] == [5, 5, 8, 8, 14, 14]
    for gap in (2, 3):
        for n in range(1, 7):
            assert best_prefix(n, gap) == max(best_prefix(n-1, gap), best_prefix(max(0, n-gap), gap)+A[n-1])
    assert sum(A[i] for i in (0, 2, 4)) == 22
    assert sum(A[i] for i in (0, 4)) == 14


if __name__ == "__main__":
    for number in range(1, 25):
        check(number, globals()[f"e{number:02}"])
    sys.exit(bool(failures))
