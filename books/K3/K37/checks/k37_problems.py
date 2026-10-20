"""Exact enumeration/symbolic checks; expected values are the published answers.

The answer-text assertions bind these reference values to answers.md. Numerical
results are computed from the experiments, not copied into a PASS condition.
"""
from collections import Counter
from itertools import permutations, product
from pathlib import Path
import re
import sys

import sympy as sp

Q = sp.Rational
ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*(K37-\d+)\*\*\n(.*?)(?=\n\*\*K37-|\Z)", ANS, re.S))


def published(pid, *fragments):
    for fragment in fragments:
        assert fragment in BLOCKS[pid], (pid, "answer mismatch", fragment)


def choice(pid, actual, expected):
    assert list(map(bool, actual)) == expected, actual
    assert sum(expected) == 1
    selected = "ABCD"[expected.index(True)]
    assert BLOCKS[pid].startswith(f"**答案：** （{selected}）"), pid
    for letter, truth in zip("ABCD", actual):
        print(f"PASS {pid} 选项{letter}={'真' if truth else '假'}")


def quicksort_pairs(order):
    # A uniformly random priority order induces uniform pivots in every segment.
    priority = {key: rank for rank, key in enumerate(order)}
    pairs = set()

    def visit(keys):
        if len(keys) < 2:
            return
        pivot = min(keys, key=priority.get)
        pairs.update(tuple(sorted((pivot, x))) for x in keys if x != pivot)
        visit([x for x in keys if x < pivot])
        visit([x for x in keys if x > pivot])

    visit(sorted(order))
    return pairs


def pass_vectors(matrix):
    return {r for r in product((0, 1), repeat=matrix.cols)
            if matrix * sp.Matrix(r) == sp.zeros(matrix.rows, 1)}


def minimum_rounds(q, threshold):
    t = 1
    while q ** t >= threshold:
        t += 1
    return t


def p01():
    counts = [len(quicksort_pairs(p)) for p in permutations((2, 5, 9))]
    mean = Q(sum(counts), len(counts))
    choice("K37-01", [all(x == 3 for x in counts), mean == Q(8, 3),
                       mean != Q(8, 3), all(x <= mean for x in counts)],
           [False, True, False, False])
    assert Q(counts.count(3), len(counts)) == Q(2, 3)


def p02():
    pairs = [quicksort_pairs(p) for p in permutations(range(1, 6))]
    squared = [quicksort_pairs(p) for p in permutations((1, 4, 9, 16, 25))]
    probs = [Q(sum(pair in s for s in pairs), len(pairs))
             for pair in ((2, 5), (3, 4))]
    after = [Q(sum(pair in s for s in squared), len(squared))
             for pair in ((4, 25), (9, 16))]
    assert probs == [Q(1, 2), 1] and after == probs
    published("K37-02", "$1/2$、$1$", "都不改变")


def p03():
    outcomes = [(0, 0, 0), (1, 1, 1)]
    dist = Counter(map(sum, outcomes))
    mean = sum(Q(s * n, len(outcomes)) for s, n in dist.items())
    independent = Q(sum(a == 1 and b == 1 for a, b, _ in outcomes), 2) == Q(1, 4)
    # A claims non-independence prevents determination; direct enumeration does determine it.
    determinable = sum(dist.values()) == len(outcomes)
    uniform_four = all(Q(dist[x], len(outcomes)) == Q(1, 4) for x in range(4))
    choice("K37-03", [not independent and not determinable, mean == Q(1, 2),
                       mean == Q(3, 2), uniform_four and mean == Q(3, 2)],
           [False, False, True, False])


def p04():
    d = sp.Matrix([[1, -1], [0, 0]])
    accepted = pass_vectors(d)
    q = Q(len(accepted), 4)
    choice("K37-04", [q == 0, q == Q(1, 4), q == 1, q == Q(1, 2)],
           [False, False, False, True])
    assert accepted == {(0, 0), (1, 1)}


def p05():
    p, k = sp.symbols("p k", positive=True)
    roots = [s for s in sp.solve((1 - p) ** 2 - Q(9, 25), p) if 0 < s <= 1]
    assert roots == [Q(2, 5)]
    p = roots[0]
    mean = sp.summation(k * (1 - p) ** (k - 1) * p, (k, 1, sp.oo))
    assert mean == Q(5, 2) and (1 - p) ** 2 * p == Q(18, 125)
    published("K37-05", "$p=2/5$", "$E[N]=5/2$", "$P(N=3)=18/125$")


def p06():
    def stats(outcomes):
        lengths, collisions = [], []
        for slots in outcomes:
            lengths.append(slots.count(0))
            collisions.append(sum(slots[i] == slots[j] for i in range(4) for j in range(i + 1, 4)))
        n = len(lengths)
        return Q(sum(lengths), n), Q(sum(collisions), n), Q(sum(c > 0 for c in collisions), n)

    assert stats(list(product(range(4), repeat=4))) == (1, Q(3, 2), Q(29, 32))
    assert stats([(s,) * 4 for s in range(4)]) == (1, 6, 1)
    published("K37-06", "都是 $1$", "$3/2$、$6$", "$29/32$、$1$", "推断错误")


def p07():
    counts = Counter(sum(u[i] == u[j] for i in range(3) for j in range(i + 1, 3))
                     for u in product(range(1, 4), repeat=3))
    dist = {c: Q(n, 27) for c, n in counts.items()}
    assert dist == {0: Q(2, 9), 1: Q(2, 3), 3: Q(1, 9)}
    assert sum(c * p for c, p in dist.items()) == 1
    assert sum(p for c, p in dist.items() if c >= 1) == Q(7, 9)
    published("K37-07", "$P(C=0)=2/9$", "$P(C=1)=2/3$", "$P(C=3)=1/9$", "$E[C]=1$", "$P(C\\ge1)=7/9$")


def p08():
    d = sp.Matrix([[1, -1], [2, -2]])
    missed = [d * sp.Matrix([b, b]) == sp.zeros(2, 1) for b in (0, 1)]
    single = Q(sum(missed), 2)
    triple = Q(sum(all(missed[b] for b in bits) for bits in product((0, 1), repeat=3)), 8)
    detected = 1 - triple
    choice("K37-08", [single <= Q(1, 2), triple == Q(1, 8), triple == 1,
                       not missed[1] and detected == Q(7, 8)], [False, False, True, False])


def p09():
    vectors = [sp.Matrix(r) for r in ((1, 0), (0, 1), (1, 1))]
    zero = sp.zeros(2, 1)
    A, B = sp.Matrix([[1, 2], [3, 4]]), sp.Matrix([[0, 1], [1, 0]])
    C = A * B
    assert all(A * (B * r) == C * r for r in vectors)

    d = sp.Matrix([[1, 0], [0, 0]])
    A, B, C = d, sp.eye(2), sp.zeros(2)
    actual = [A * (B * r) - C * r for r in vectors]
    assert actual == [sp.Matrix([1, 0]), zero, sp.Matrix([1, 0])]
    assert Q(sum(value == zero for value in actual), len(vectors)) == Q(1, 3)

    # Any two zero products force all four entries to zero, symbolically.
    entries = sp.symbols("d11 d12 d21 d22", real=True)
    symbolic = sp.Matrix(2, 2, entries)
    for i, j in ((0, 1), (0, 2), (1, 2)):
        equations = list(symbolic * vectors[i]) + list(symbolic * vectors[j])
        assert sp.linsolve(equations, entries) == sp.FiniteSet((0, 0, 0, 0))
    published("K37-09", "至多为 $1/3$", "\\begin{pmatrix}1&0\\\\0&0\\end{pmatrix}",
              "恰好一个漏检，概率为 $1/3$")


def p10():
    c = sp.symbols("c", real=True)
    a = sp.symbols("a1:4")
    proposal = [Q(1, 2), Q(1, 3), Q(1, 6)]
    solution = sp.solve([proposal[i] * a[i] - c for i in range(3)], a)
    actual = [solution[x] for x in a]
    assert actual == [2 * c, 3 * c, 6 * c]
    feasible = sp.reduce_inequalities([c > 0] + [x <= 1 for x in actual], c)
    assert feasible.as_set() == sp.Interval.Lopen(0, Q(1, 6))
    acceptance = sp.simplify(sum(proposal[i] * actual[i] for i in range(3)))
    mean = 1 / acceptance
    assert sp.simplify(sp.diff(mean, c)) == -1 / (3 * c ** 2)
    best = [x.subs(c, Q(1, 6)) for x in actual]
    assert best == [Q(1, 3), Q(1, 2), 1] and mean.subs(c, Q(1, 6)) == 2
    assert [sp.simplify(proposal[i] * actual[i] / acceptance) for i in range(3)] == [Q(1, 3)] * 3
    rejection = 1 - acceptance
    termination = sp.reduce_inequalities([rejection >= 0, rejection < 1], c)
    assert feasible.as_set().is_subset(termination.as_set())
    published("K37-10", "(2c,3c,6c)", "0<c\\le1/6", "$(1/3,1/2,1)$", "次数为 $2$")


def p11():
    a = sp.symbols("a", real=True)
    A, B = sp.Matrix([[1, 0], [1, 1]]), sp.eye(2)
    C = sp.Matrix([[0, a], [0, a + 1]])
    d = A * B - C
    assert d == sp.Matrix([[1, -a], [1, -a]])
    # Solve the zero equations for each bit vector, covering all real a.
    loci = []
    for r in product((0, 1), repeat=2):
        solutions = sp.S.Reals
        for entry in d * sp.Matrix(r):
            solutions = solutions.intersect(sp.solveset(entry, a, domain=sp.S.Reals))
        loci.append(solutions)
    assert loci == [sp.S.Reals, sp.FiniteSet(0), sp.S.EmptySet, sp.FiniteSet(1)]
    exceptional = sp.Union(*[s for s in loci if s.is_FiniteSet])
    assert exceptional == sp.FiniteSet(0, 1)
    for value in exceptional:
        q = Q(sum(value in s for s in loci), 4)
        assert q == Q(1, 2) and minimum_rounds(q, Q(1, 100)) == 7
    generic_q = Q(sum(s == sp.S.Reals for s in loci), 4)
    assert generic_q == Q(1, 4) and minimum_rounds(generic_q, Q(1, 100)) == 4
    published("K37-11", "$a=0$ 或 $a=1$", "$q=1/2$", "$7$ 轮", "$q=1/4$", "$4$ 轮")


def p12():
    totals = [0, 0, 0]
    overlaps = [0] * 4
    for order in permutations(range(1, 5)):
        fixed = [x == i + 1 for i, x in enumerate(order)]
        records = [x == max(order[:i + 1]) for i, x in enumerate(order)]
        common = [f and r for f, r in zip(fixed, records)]
        for i, flags in enumerate((fixed, records, common)):
            totals[i] += sum(flags)
        overlaps = [x + y for x, y in zip(overlaps, common)]
    f, r, t = [Q(x, sp.factorial(4)) for x in totals]
    assert (f, r, f + r, t) == (1, Q(25, 12), Q(37, 12), Q(2, 3))
    assert [Q(x, 24) for x in overlaps] == [Q(1, 4), Q(1, 12), Q(1, 12), Q(1, 4)]
    published("K37-12", "$E[F]=1$", "$E[R]=25/12$", "$E[F+R]=37/12$", "$E[T]=2/3$")


def p13():
    # Discover each terminal branch of one round by following the bit decisions.
    terminal = []

    def walk(prefix, prob):
        if prefix == (0,):
            terminal.append((None, len(prefix), prob))
        elif prefix == (1, 0):
            terminal.append((0, len(prefix), prob))
        elif len(prefix) == 3:
            terminal.append((prefix[2], len(prefix), prob))
        else:
            for bit in (0, 1):
                walk(prefix + (bit,), prob / 2)

    walk((), sp.S.One)
    fail = sum(p for out, _, p in terminal if out is None)
    outputs = [sum(p for out, _, p in terminal if out == x) / (1 - fail) for x in (0, 1)]
    n, h = sp.symbols("n h")
    en = sp.solve(n - (1 + fail * n), n)[0]
    eh = sp.solve(h - sum(p * (cost + (h if out is None else 0)) for out, cost, p in terminal), h)[0]
    # Iterate the actual parser over every three-bit prefix, including restarts.
    unfinished = 0
    for bits in product((0, 1), repeat=3):
        state = 0
        done = False
        for b in bits:
            if state == 0:
                state = 0 if b == 0 else 1
            elif state == 1:
                if b == 0:
                    done = True
                    break
                state = 2
            else:
                done = True
                break
        unfinished += not done
    assert outputs == [Q(3, 4), Q(1, 4)] and en == 2
    assert eh == Q(7, 2) and Q(unfinished, 8) == Q(3, 8) and eh != 3 * en
    published("K37-13", "$3/4$、$1/4$", "轮数为 $2$", "$E[H]=7/2$", "$P(H>3)=3/8$", "不能用")


def p14():
    d1 = sp.Matrix([[1, -1, 0], [0, 0, 0], [0, 0, 0]])
    d2 = sp.Matrix([[1, 1, -1], [0, 0, 0], [0, 0, 0]])
    a, b = pass_vectors(d1), pass_vectors(d2)
    p, q, joint = Q(len(a), 8), Q(len(b), 8), Q(len(a & b), 8)
    assert (p, q, joint) == (Q(1, 2), Q(3, 8), Q(1, 8))
    assert joint != p * q
    # Four-state chain tracks which errors are still undetected after each round.
    distribution = {(True, True): sp.S.One}
    for t in range(1, 8):
        next_dist = Counter()
        for (u, v), weight in distribution.items():
            for r in product((0, 1), repeat=3):
                next_dist[(u and r in a, v and r in b)] += weight / 8
        distribution = next_dist
        mean = sum((int(u) + int(v)) * w for (u, v), w in distribution.items())
        union = sum(w for (u, v), w in distribution.items() if u or v)
        assert mean == p ** t + q ** t
        assert union == p ** t + q ** t - joint ** t
        assert (union < Q(1, 100)) == (t >= 7)
    assert union == Q(9285, 1048576)
    published("K37-14", "$1/2,3/8,1/8$", "$E[U_t]=(1/2)^t+(3/8)^t$",
              "$P(U_t\\ge1)=(1/2)^t+(3/8)^t-(1/8)^t$", "$7$ 轮")
    fraction = re.search(r"它等于 \$(\d+)/(\d+)<1/100\$", BLOCKS["K37-14"])
    assert fraction and Q(int(fraction[1]), int(fraction[2])) == union


TESTS = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06, 7: p07,
         8: p08, 9: p09, 10: p10, 11: p11, 12: p12, 13: p13, 14: p14}

if __name__ == "__main__":
    failed = 0
    for number in range(1, 15):
        pid = f"K37-{number:02}"
        try:
            TESTS[number]()
        except Exception as exc:
            failed += 1
            print(f"FAIL {pid} {type(exc).__name__}: {exc}")
        else:
            print(f"PASS {pid}")
            if number == 9:
                print(f"MANUAL {pid} 证明：任意两种乘积为零均迫使两列全零，故至多一个向量漏检")
    sys.exit(bool(failed))
