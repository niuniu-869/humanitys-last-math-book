"""Exact, independent checks of all determinate questions and all MC options.

Expected values are transcribed from answers.md; text anchors ensure that the
checked answer is still the published answer. Only P9-08 is a manual proof.
"""
from itertools import product
from pathlib import Path
import re
import sys

import sympy as s

R = s.Rational
M = s.Matrix
ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
parts = dict(re.findall(r"\*\*(P9-\d+)\*\*\n(.*?)(?=\n\*\*P9-|\Z)", ANSWERS, re.S))
failures = 0
covered = set()


def eq(actual, expected):
    if isinstance(actual, s.MatrixBase):
        assert actual.shape == expected.shape
        assert all(s.simplify(v) == 0 for v in actual - expected), (actual, expected)
    else:
        assert s.simplify(actual - expected) == 0, (actual, expected)


def anchor(number, *texts):
    for text in texts:
        assert text in parts[f"P9-{number:02d}"], f"answer text changed: {text}"


def run(number, calculation):
    global failures
    pid = f"P9-{number:02d}"
    covered.add(pid)
    try:
        calculation()
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")
    else:
        print(f"PASS {pid}")


def choices(number, truth):
    global failures
    selected = re.search(r"选 ([A-D])", parts[f"P9-{number:02d}"])[1]
    for letter, value in zip("ABCD", truth):
        good = bool(value) == (letter == selected)
        print(f"{'PASS' if good else 'FAIL'} P9-{number:02d} 选项{letter}")
        if not good:
            failures += 1
    assert sum(bool(t) for t in truth) == 1
    assert truth["ABCD".index(selected)]


def stochastic(p):
    return all(x >= 0 for x in p) and p * s.ones(p.cols, 1) == s.ones(p.rows, 1)


def stationary(p):
    v = (p.T - s.eye(p.rows)).nullspace()
    assert len(v) == 1
    return (v[0] / sum(v[0])).T


P = M([[R(3, 4), R(1, 4)], [R(1, 2), R(1, 2)]])


def q01():
    options = [M([[R(1, 2), R(1, 4)], [R(1, 2), R(3, 4)]]),
               M([[R(6, 5), -R(1, 5)], [R(2, 5), R(3, 5)]]),
               M([[R(1, 2), R(1, 2)], [R(1, 4), R(3, 4)]]),
               M([[R(1, 2), R(1, 2)], [R(1, 4), R(1, 2)]])]
    choices(1, [stochastic(p) for p in options])


def q02():
    p = M([[R(2, 3), R(1, 3)], [R(1, 4), R(3, 4)]])
    prior = M([[R(3, 5), R(2, 5)]])
    conditional = s.prod(p[i, j] for i, j in [(1, 0), (0, 1)])
    eq(prior[1] * conditional, R(1, 30))
    eq(conditional, R(1, 12))
    anchor(2, "$1/30$", "$1/12$")


def q03():
    actual = (P ** 2)[0, 0]
    choices(3, [actual == v for v in [R(9, 16), R(11, 16), R(3, 4), R(1, 8)]])


def q04():
    a = s.symbols("a", real=True)
    p = M([[1-a, a], [R(1, 3), R(2, 3)]])
    pi = M([[R(2, 3), R(1, 3)]])
    solution = s.solve(list(pi*p-pi), a)
    eq(solution[a], R(1, 6))
    assert stochastic(p.subs(solution))
    eq(pi*p.subs(solution), pi)
    anchor(4, "$a=1/6$")


def q05():
    p = M([[0, R(1, 2), R(1, 2)], [1, 0, 0], [1, 0, 0]])
    uniform = s.ones(1, 3) / 3
    pi = stationary(p)
    eq(pi, M([[R(1, 2), R(1, 4), R(1, 4)]]))
    u, v = M([[0, R(1, 2), R(1, 2)]]), M([[1, 0, 0]])
    cycle = u*p == v and v*p == u and u != v
    # A stationary witness disproves B; the exact 2-cycle disproves C.
    choices(5, [uniform*p == uniform, pi*p != pi, not cycle, cycle])
    eq(uniform*p, M([[R(2, 3), R(1, 6), R(1, 6)]]))
    anchor(5, "唯一的 $\\pi=(1/2,1/4,1/4)$")


def q06():
    c = s.symbols("c", positive=True)
    q = M([[1-c]])
    inverse = (s.eye(1)-q).inv()
    h = (inverse*M([c/3]))[0]
    m = (inverse*s.ones(1, 1))[0]
    eq(h, R(1, 3))
    eq(m, 1/c)
    assert s.solve(h-R(1, 2), c) == []
    assert s.solve(m-4, c) == [R(1, 4)]
    anchor(6, "$h_1=1/3$", "$m_1=1/c$", "$c=1/4$")


def q07():
    p = M([[R(1, 2), R(1, 2), 0], [0, 0, 1], [1, 0, 0]])
    # Remove the return state after the mandatory first step.
    transient = [0, 2]
    q = p.extract(transient, transient)
    initial = p.extract([1], transient)
    exits = p.extract(transient, [1])
    eq(p[1, 1], 0)
    eq((initial*exits)[0], 0)
    k = s.symbols("k", integer=True, positive=True)
    path_mass = p[1, 2]*p[2, 0]*p[0, 0]**(k-3)*p[0, 1]
    eq(path_mass, 2**(-(k-2)))
    # Matrix powers count all paths with no earlier return, independently.
    for step in range(3, 13):
        eq((initial*q**(step-2)*exits)[0], path_mass.subs(k, step))
    eq(s.summation(path_mass, (k, 3, s.oo)), 1)
    tail3 = (initial*q**2*s.ones(2, 1))[0]
    tail5 = (initial*q**4*s.ones(2, 1))[0]
    eq(tail5/tail3, R(1, 4))
    eq(s.summation(k*path_mass, (k, 3, s.oo)), 4)
    anchor(7, "$P(T=k)=2^{-(k-2)}$", "(2) $1/4$", "$E(T)=4$")


def q09():
    b, x = s.symbols("b x", real=True)
    n = s.symbols("n", integer=True, nonnegative=True)
    p = M([[R(3, 4), R(1, 4)], [b, 1-b]])
    b_value = s.solve((p**2)[0, 0]-R(11, 16), b)
    assert b_value == [R(1, 2)]
    p = p.subs(b, b_value[0])
    computed = (M([[x, 1-x]]) * p**n)[0]
    eq(computed, R(2, 3)+(x-R(2, 3))/4**n)
    # The expression is affine in x; the maximum absolute value is at an endpoint.
    assert s.diff(computed, x, 2) == 0
    errors = [abs((computed-R(2, 3)).subs(x, k)) for k in [0, 1]]
    first = next(k for k in range(10) if max(v.subs(n, k) for v in errors) <= R(1, 96))
    assert first == 3
    eq(max(v.subs(n, 2) for v in errors), R(1, 24))
    anchor(9, "最小的 $n$ 是 3", r"\frac23+(x-\frac23)4^{-n}")


def q10():
    c = s.symbols("c", positive=True)
    q = M([[1-c, 3*c/4], [R(1, 2), 0]])
    exits = M([[c/4, 0], [0, R(1, 2)]])
    inverse = (s.eye(2)-q).inv()
    absorption = s.simplify(inverse*exits)
    eq(absorption, M([[R(2, 5), R(3, 5)], [R(1, 5), R(4, 5)]]))
    times = inverse*s.ones(2, 1)
    eq(times, M([8/(5*c)+R(6, 5), 4/(5*c)+R(8, 5)]))
    roots = s.solve(times[0]-times[1]-1, c)
    assert roots == [R(4, 7)] and 0 < roots[0] <= 1
    eq(times.subs(c, roots[0]), M([4, 3]))
    initial = M([[R(1, 2), R(1, 2)]])
    eq((initial*absorption)[1], R(7, 10))
    eq((initial*times.subs(c, roots[0]))[0], R(7, 2))
    anchor(10, "$h_1=3/5,h_2=4/5$", r"\frac8{5c}+\frac65",
           r"\frac4{5c}+\frac85", "$c=4/7$", "$7/10$", "$7/2$")


def q11():
    states = list(product([0, 1], repeat=2))
    next_one = [R(1, 2), R(1, 2), R(1, 4), R(3, 4)]
    p = s.zeros(4)
    for i, pair in enumerate(states):
        for bit in [0, 1]:
            j = states.index((pair[1], bit))
            p[i, j] = next_one[i] if bit else 1-next_one[i]
    assert stochastic(p)
    assert next_one[1] != next_one[3]  # Positive histories with identical current value.
    expected = M([[R(1, 2), R(1, 2), 0, 0], [0, 0, R(1, 2), R(1, 2)],
                  [R(3, 4), R(1, 4), 0, 0], [0, 0, R(1, 4), R(3, 4)]])
    eq(p, expected)
    pi = stationary(p)
    eq(pi, M([[3, 2, 2, 4]])/11)
    # Positivity of a power independently verifies irreducibility and aperiodicity.
    assert all(v > 0 for v in p**2)
    eq(sum(pi[j] for j, pair in enumerate(states) if pair[1] == 1), R(6, 11))
    anchor(11, "(1) 不能", "$(3,2,2,4)/11$", "$6/11$")


def q12():
    paths = {path: R(1, 2)*P[path[0], path[1]]*P[path[1], path[2]]
             for path in product(range(2), repeat=3)}
    def conditional(event, condition):
        return sum(w for path, w in paths.items() if event(path) and condition(path)) / sum(
            w for path, w in paths.items() if condition(path))
    first = conditional(lambda p: p[0] == 0, lambda p: p[2] == 0)
    second = conditional(lambda p: p[0] == 0, lambda p: p[1:] == (1, 0))
    eq(first, R(11, 21))
    eq(second, R(1, 3))
    assert first != second
    anchor(12, "$11/21$", "$1/3$", "不相等")


def q13():
    q = M([[R(1, 4), R(1, 2)], [R(1, 4), R(1, 4)]])
    m1, m2, r1, r2 = s.symbols("m1 m2 r1 r2")
    # Solve first-step equations, rather than reusing the answer's inverse.
    equations = list(M([m1, m2])-s.ones(2, 1)-q*M([m1, m2]))
    equations += list(M([r1, r2])-M([2, 5])-q*M([r1, r2]))
    solution = s.solve(equations, [m1, m2, r1, r2])
    eq(solution[m1], R(20, 7))
    eq(solution[r1], R(64, 7))
    eq((s.eye(2)-q).inv(), M([[12, 8], [4, 12]])/7)
    anchor(13, "$E(T)=20/7$", "$E(Y)=64/7$")


def q14():
    rate, elapsed, already = s.Integer(2), s.Integer(3)-1, 1
    mean = rate*elapsed
    def pmf(k):
        return s.exp(-mean)*mean**k/s.factorial(k)
    exact_three = pmf(3-already)
    third_later = sum(pmf(k) for k in range(3-already))
    eq(exact_three, 8*s.exp(-4))
    eq(third_later, 5*s.exp(-4))
    anchor(14, "$8e^{-4}$", "$5e^{-4}$")


def q15():
    covariance = M([[min(i, j) for j in [1, 2, 3]] for i in [1, 2, 3]])
    u, v = M([[-1, 0, 1]]), M([[0, 1, 0]])
    cov = (u*covariance*v.T)[0]
    variance = ((u-v)*covariance*(u-v).T)[0]
    eq(cov, 1)
    eq(variance, 2)
    assert cov != 0
    anchor(15, r"\operatorname{Cov}(U,V)=1", r"\operatorname{Var}(U-V)=2", "不独立")


if __name__ == "__main__":
    for number, calculation in [(1, q01), (2, q02), (3, q03), (4, q04),
                                (5, q05), (6, q06), (7, q07), (9, q09), (10, q10),
                                (11, q11), (12, q12), (13, q13), (14, q14), (15, q15)]:
        run(number, calculation)
    print("MANUAL P9-08 双向证明：核对自环消去、行和与逆向推回")
    covered.add("P9-08")
    ids = set(re.findall(r"^\*\*(P9-\d+)\*\*", PROBLEMS, re.M))
    table_ids = re.findall(r"^\| (P9-\d+) \|", PROBLEMS, re.M)
    ordered_ids = re.findall(r"^\*\*(P9-\d+)\*\*", PROBLEMS, re.M)
    expected_ids = [f"P9-{n:02d}" for n in range(1, 16)]
    if (ids != covered or ids != set(parts) or table_ids != ordered_ids
            or ordered_ids != expected_ids or list(parts) != expected_ids):
        failures += 1
        print("FAIL P9-覆盖 题目、答案与验算编号不一致")
    sys.exit(bool(failures))
