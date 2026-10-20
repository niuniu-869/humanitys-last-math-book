"""Independent symbolic/enumerative checks; expected values follow answers.md."""
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import re
import sys

import sympy as s


ANSWERS = (Path(__file__).resolve().parents[1] / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*(K41-\d+)\*\*\n(.*?)(?=\n\*\*K41-|\Z)", ANSWERS, re.S))
failures = 0


def check(pid, work, proof=False):
    global failures
    try:
        work()
        assert "**答案：**" in BLOCKS[pid] and "区分点：" in BLOCKS[pid]
        print(f"{'MANUAL' if proof else 'PASS'} {pid}" + (" 证明骨架需人工复核；代数检查通过" if proof else ""))
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")


def choices(pid, actual, expected):
    assert list(actual) == list(expected), (actual, expected)
    correct = [letter for letter, value in zip("ABCD", actual) if value]
    assert len(correct) == 1
    assert re.search(r"选\s*\(" + correct[0] + r"\)", BLOCKS[pid])
    for letter in "ABCD":
        print(f"PASS {pid}-{letter}")


def p01():
    arr = [2, 2, 5]
    result = tuple(sum(abs(arr[i] - arr[j]) >= t for i, j in combinations(range(3), 2)) for t in (3, 4))
    options = [(2, 0), (4, 0), (0, 0), (2, 1)]
    choices("K41-01", [result == opt for opt in options], [True, False, False, False])


def p02():
    x, y = s.symbols("x y", integer=True)
    options = [x+y, x+2*y, x*y, x-y]
    actual = [all(s.expand(f.subs({x: x+dx, y: y+dy}, simultaneous=True)-f) == 0
                  for dx, dy in ((2, -1), (-2, 1))) for f in options]
    choices("K41-02", actual, [False, True, False, False])


def p03():
    x = s.symbols("x", real=True)
    roots = s.solveset((x+1)**2-2-7, x, domain=s.S.Reals)
    assert roots == s.FiniteSet(-4, 2)
    assert [(v, v+1, (v+1)**2, (v+1)**2-2) for v in sorted(roots)] == [(-4, -3, 9, 7), (2, 3, 9, 7)]


def p04():
    n = s.symbols("n", integer=True, nonnegative=True)
    h = 2**(1-n)
    assert h.subs(n, 0) == 2 and s.simplify(h.subs(n, n+1)-h/2) == 0
    zero_set = s.solveset(h, n, domain=s.S.Naturals0)
    choices("K41-04", [h.subs(n, 2) == 0, zero_set != s.S.EmptySet,
                       h.subs(n, 2).is_integer, h.is_positive], [False, False, False, True])


def p05():
    n = s.symbols("n")
    f = n*n+1
    g = f+n*(n-1)*(n-2)*(n-3)
    assert [f.subs(n, k) for k in range(4)] == [1, 2, 5, 10]
    assert all(f.subs(n, k) == g.subs(n, k) for k in range(4))
    assert (f.subs(n, 4), g.subs(n, 4)) == (17, 41)
    assert s.expand(f-g) != 0


def p06():
    x, y, z = s.symbols("x y z", integer=True, nonnegative=True)
    phi = 2*x+y
    for dx, dy, dz in ((-1, 1, 0), (0, -1, 1)):
        mapping = {x: x+dx, y: y+dy, z: z+dz}
        assert s.expand(phi.subs(mapping, simultaneous=True)-phi) == -1
        assert s.expand((x+y+z).subs(mapping, simultaneous=True)-(x+y+z)) == 0
    assert phi.subs({x: 0, y: 0}) == 0


def p07():
    sample = list(product(range(3), repeat=6))
    count = sum(0 in a and 1 in a for a in sample)
    exact = sum(a.count(0) == 1 and 1 in a for a in sample)
    assert (s.Rational(count, len(sample)), exact) == (s.Rational(602, 729), 186)


def p08():
    # Exhaustive forward search is independent of the answer's reverse subtraction.
    distances = {(1, 1): 0}
    frontier = [(1, 1)]
    for x, y in frontier:
        for nxt in ((x+y, y), (x, x+y)):
            if max(nxt) <= 13 and nxt not in distances:
                distances[nxt] = distances[(x, y)]+1
                frontier.append(nxt)
    assert distances[(13, 8)] == 5
    assert (12, 8) not in distances
    route = [(1, 1), (2, 1), (2, 3), (5, 3), (5, 8), (13, 8)]
    assert all(b in ((a[0]+a[1], a[1]), (a[0], a[0]+a[1])) for a, b in zip(route, route[1:]))


def p09():
    t = s.symbols("t", real=True)
    u, v = (2+3*t*t)/(1+t+t*t), (1+4*t)/(1+t+t*t)
    assert [(u.subs(t, k), v.subs(t, k)) for k in (0, 1)] == [(2, 1), (s.Rational(5, 3), s.Rational(5, 3))]
    domain = s.Interval(0, s.oo)
    greater = s.solve_univariate_inequality(u > v, t, relational=False).intersect(domain)
    lesser = s.solve_univariate_inequality(u < v, t, relational=False).intersect(domain)
    equal = s.solveset(u-v, t, domain=domain)
    assert greater == s.Union(s.Interval.Ropen(0, s.Rational(1, 3)), s.Interval.open(1, s.oo))
    assert lesser == s.Interval.open(s.Rational(1, 3), 1)
    assert equal == s.FiniteSet(s.Rational(1, 3), 1)


def p10():
    states = list(permutations((1, 2, 3)))
    edges = {}
    inv = lambda a, k: sum(a[i]-a[j] >= k for i, j in combinations(range(3), 2))
    for arr in states:
        edges[arr] = []
        for i in range(2):
            if arr[i]-arr[i+1] >= 2:
                nxt = list(arr)
                nxt[i], nxt[i+1] = nxt[i+1], nxt[i]
                edges[arr].append(tuple(nxt))
    terminals = {a for a in states if not edges[a]}
    assert terminals == {(1, 2, 3), (1, 3, 2), (2, 1, 3), (3, 2, 1)}
    decreasing = all(inv(b, 1) == inv(a, 1)-1 for a in states for b in edges[a])
    # Transitive closure checks cycles without assuming the invariant argument.
    reach = {(a, b) for a in states for b in edges[a]}
    while True:
        expanded = reach | {(a, c) for a, b in reach for bb, c in reach if b == bb}
        if expanded == reach:
            break
        reach = expanded
    cyclic = any(a == b for a, b in reach)
    choices("K41-10", [terminals == {(1, 2, 3)},
                       all((not edges[a]) == (inv(a, 2) == 0) for a in states),
                       decreasing and not cyclic and any(a != (1, 2, 3) for a in terminals),
                       cyclic], [False, False, True, False])


def p11():
    critical = s.Rational(2576, 1000)
    z = lambda n: (s.Rational(3, 5)*n-n/2)/s.sqrt(n*s.Rational(1, 4))
    accepted = [n for n in range(10, 501, 10) if z(s.Integer(n)) > critical]
    assert min(accepted) == 170
    assert z(s.Integer(160)) < critical < z(s.Integer(170))
    assert (s.Rational(3, 5)*170, s.Rational(3, 5)*160) == (102, 96)
    n = s.symbols("n", positive=True)
    assert s.simplify(z(n)-s.sqrt(n)/5) == 0
    assert s.diff(z(n), n).is_positive
    assert s.Rational(3, 5)-s.Rational(1, 2) == s.Rational(1, 10)


def p12():
    states = [(s.Integer(1), s.Integer(0))]
    for _ in range(7):
        x, y = states[-1]
        states.append((2*x+y, x+2*y))
    assert states[1:4] == [(2, 1), (5, 4), (14, 13)]
    assert states.index((365, 364)) == 6
    assert (366, 365) not in states and sum(states[6]) < 731 < sum(states[7])
    n = s.symbols("n", integer=True, nonnegative=True)
    x, y = (3**n+1)/2, (3**n-1)/2
    assert (x.subs(n, 0), y.subs(n, 0)) == states[0]
    assert s.simplify(2*x+y-x.subs(n, n+1)) == 0
    assert s.simplify(x+2*y-y.subs(n, n+1)) == 0
    assert s.simplify(x-y) == 1 and s.simplify(x+y) == 3**n


def p13():
    enumerated = {}
    for n in range(9):
        for k in range(-1, n+2):
            enumerated[n, k] = sum(sum(a) == k and all(a[i]*a[i+1] == 0 for i in range(n-1))
                                   for a in product((0, 1), repeat=n))
    assert [enumerated[n, 3] for n in range(5, 9)] == [1, 4, 10, 20]
    assert (enumerated[0, 0], enumerated[1, 0], enumerated[1, 1]) == (1, 1, 1)
    for n in range(2, 9):
        for k in range(n+2):
            assert enumerated[n, k] == enumerated.get((n-1, k), 0)+enumerated.get((n-2, k-1), 0)
    samples = [a for a in product((0, 1), repeat=8) if sum(a) == 3]
    ring = [a for a in samples if all(a[i]*a[(i+1) % 8] == 0 for i in range(8))]
    assert (len(samples), len(ring), s.Rational(len(ring), len(samples))) == (56, 16, s.Rational(2, 7))


def p14():
    @lru_cache(None)
    def winning(n, last_wins):
        return any((last_wins if move == n else not winning(n-move, last_wins))
                   for move in (1, 3, 4) if move <= n)

    def starts(n, last_wins):
        return [m for m in (1, 3, 4) if m <= n and
                (last_wins if m == n else not winning(n-m, last_wins))]

    assert [n for n in range(1, 26) if not winning(n, False)] == [1, 3, 8, 10, 15, 17, 22, 24]
    assert starts(25, False) == [1, 3]
    assert [n for n in range(1, 26) if not winning(n, True)] == [2, 7, 9, 14, 16, 21, 23]
    assert starts(25, True) == [4]
    rows = re.findall(r"^\| (\d+) \| ([\d、]+) \| (胜|败) \|$", BLOCKS["K41-14"], re.M)
    assert len(rows) == 20
    for last_wins, table in zip((False, True), (rows[:10], rows[10:])):
        assert [int(row[0]) for row in table] == list(range(1, 11))
        for raw_n, raw_successors, verdict in table:
            n = int(raw_n)
            assert [int(v) for v in raw_successors.split("、")] == [n-m for m in (1, 3, 4) if m <= n]
            assert (verdict == "胜") == winning(n, last_wins)
    continuations = re.findall(r"继续到 \$25\$：\$([\d,]+)\$ 为败，其余 \$([\d,]+)\$ 为胜", BLOCKS["K41-14"])
    assert len(continuations) == 2
    for last_wins, (lost, won) in zip((False, True), continuations):
        assert list(map(int, lost.split(","))) == [n for n in range(11, 26) if not winning(n, last_wins)]
        assert list(map(int, won.split(","))) == [n for n in range(11, 26) if winning(n, last_wins)]
    # Verify every possible opponent reply along the stated response strategy.
    def force_win(n, last_wins):
        for move in starts(n, last_wins):
            if move == n:
                return last_wins
            remaining = n-move
            if all((not last_wins if reply == remaining else force_win(remaining-reply, last_wins))
                   for reply in (1, 3, 4) if reply <= remaining):
                return True
        return False
    assert force_win(25, False) and force_win(25, True)


if __name__ == "__main__":
    for i in range(1, 15):
        check(f"K41-{i:02}", globals()[f"p{i:02}"], proof=(i == 6))
    print("MANUAL K41-12-(2) 归纳证明需人工复核；数值及递推恒等式已自动核对")
    sys.exit(bool(failures))
