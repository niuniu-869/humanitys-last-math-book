"""Check the current lesson examples, transferred exercise and figure data."""
import ast
from collections import Counter
from itertools import product
from math import gcd
from pathlib import Path
import re
import sys

import sympy as s
import numpy as np

R, M = s.Rational, s.Matrix
ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
EXAMPLES = dict(re.findall(r"\*\*例 (\d+)\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON, re.S))
failures = 0
covered = set()
P = M([[R(4, 5), R(1, 5)], [R(3, 10), R(7, 10)]])
WEATHER = M([[R(6, 10), R(3, 10), R(1, 10)],
             [R(3, 10), R(4, 10), R(3, 10)],
             [R(2, 10), R(4, 10), R(4, 10)]])
Q9 = M([[R(1, 2), R(1, 5)], [R(1, 10), R(1, 2)]])
Q11 = M([[R(3, 5), R(1, 5)], [R(3, 10), R(2, 5)]])
LINKS = M([[0, R(1, 2), R(1, 2)], [0, 0, 1], [1, 0, 0]])


def eq(a, b):
    if isinstance(a, s.MatrixBase):
        assert a.shape == b.shape
        assert all(s.simplify(v) == 0 for v in a-b), (a, b)
    else:
        assert s.simplify(a-b) == 0, (a, b)


def approx(a, b, digits):
    assert abs(float(a)-b) <= 0.5*10**(-digits), (a, b)


def stationary(p):
    vectors = (p.T-s.eye(p.rows)).nullspace()
    assert len(vectors) == 1
    return (vectors[0]/sum(vectors[0])).T


def run(number, fn):
    global failures
    covered.add(str(number))
    try:
        note = fn()
        print(f"PASS 例{number}" + (f" {note}" if note else ""))
    except Exception as exc:
        failures += 1
        print(f"FAIL 例{number} {type(exc).__name__}: {exc}")


def ex01():
    source = EXAMPLES["1"]
    labels = re.search(r"依次是 \$([12],[12],[12])\$ 的概率", source)[1].split(",")
    start = int(re.search(r"\$X_0=([12])\$", source)[1])-1
    path = [start] + [int(label)-1 for label in labels]
    actual = s.prod(P[i, j] for i, j in zip(path, path[1:]))
    claimed = R(re.search(r"\$\$0\.8.*?=([0-9.]+)\.", source)[1])
    eq(actual, R(14, 125))
    eq(actual, claimed)
    eq(P[0, 0]**2*P[0, 1], R(16, 125))  # Following practice exercise.
    assert "=0.128" in source


def ex02():
    states = list(product([0, 1], repeat=2))
    probabilities = s.symbols("q00 q01 q10 q11")
    p = s.zeros(4)
    for i, (old, current) in enumerate(states):
        for new in [0, 1]:
            p[i, states.index((current, new))] = probabilities[i] if new else 1-probabilities[i]
    eq(p*s.ones(4, 1), s.ones(4, 1))
    assert p[1, 0] == p[1, 1] == 0
    assert set(j for j in range(4) if p[1, j] != 0) == {2, 3}


def ex03():
    # Enumerate independent +/-1 increments and condition on each reachable history.
    weights = Counter()
    for increments in product([-1, 1], repeat=5):
        positions = [0]
        for dx in increments:
            positions.append(positions[-1]+dx)
        weights[(tuple(positions[:-1]), positions[-1])] += 1
    for history in {h for h, _ in weights}:
        outgoing = {end: count for (h, end), count in weights.items() if h == history}
        assert set(outgoing) == {history[-1]-1, history[-1]+1}
        for count in outgoing.values():
            eq(R(count, sum(outgoing.values())), R(1, 2))
    return "转移概率核对；一般马尔可夫性证明另列 MANUAL"


def ex04():
    eq(WEATHER*s.ones(3, 1), s.ones(3, 1))
    initial = M([[1, 0, 0]])
    eq(initial*WEATHER, M([[R(6, 10), R(3, 10), R(1, 10)]]))
    eq(initial*WEATHER**2, M([[R(47, 100), R(34, 100), R(19, 100)]]))
    a, b = s.symbols("a b")
    practice = M([[R(1, 2), a, R(1, 5)], [R(1, 10), R(3, 5), b], [0, R(1, 2), R(1, 2)]])
    result = s.solve(list(practice*s.ones(3, 1)-s.ones(3, 1)), [a, b])
    assert result == {a: R(3, 10), b: R(3, 10)}


def inverse_practice():
    x = s.symbols("x", real=True)
    p = M([[R(1, 3), R(2, 3)], [R(1, 3), R(2, 3)]])
    image = M([[x, 1-x]])*p
    eq(image, M([[R(1, 3), R(2, 3)]]))
    assert s.solve(list(image-M([[R(1, 2), R(1, 2)]])), x) == []
    assert s.reduce_inequalities([x >= 0, 1-x >= 0], x).as_set() == s.Interval(0, 1)
    assert r"所有 $(x,1-x)$ 都可以" in EXAMPLES["4"]
    assert "不可能出现，无解" in EXAMPLES["4"]


def ex05():
    sentences = ["猫 吃 鱼", "猫 吃 肉", "猫 睡 觉", "狗 吃 肉", "狗 吃 肉", "狗 睡 觉"]
    edges, totals = Counter(), Counter()
    for sentence in sentences:
        words = ["始"] + sentence.split() + ["终"]
        for left, right in zip(words, words[1:]):
            edges[left, right] += 1
            totals[left] += 1
    probs = [R(edges[a, b], totals[a]) for a, b in [("始", "猫"), ("猫", "吃"), ("吃", "肉")]]
    assert probs == [R(1, 2), R(2, 3), R(3, 4)]
    eq(s.prod(probs), R(1, 4))


def ex06():
    eq((WEATHER**2)[0, 2], R(19, 100))
    eq((WEATHER**2)[1, 0], R(9, 25))


def ex07():
    p = M([[R(9, 10), R(1, 10)], [R(2, 5), R(3, 5)]])
    n = s.symbols("n", integer=True, nonnegative=True)
    eq((p**n)[0, 0], R(4, 5)+R(1, 5)*R(1, 2)**n)
    eq(p**2, M([[R(85, 100), R(15, 100)], [R(3, 5), R(2, 5)]]))
    eq((p**3)[0, 0], R(33, 40))


def ex08():
    n = s.symbols("n", integer=True, nonnegative=True)
    initial = M([[R(1, 2), R(1, 2)]])
    target = M([[R(3, 5), R(2, 5)]])+R(1, 2)**n*M([[-R(1, 10), R(1, 10)]])
    eq(initial*P**n, target)
    eq(initial*P, M([[R(55, 100), R(45, 100)]]))


def ex09():
    exits = M([[R(3, 10), 0], [0, R(2, 5)]])
    absorption = (s.eye(2)-Q9).inv()*exits
    eq(absorption, M([[R(15, 23), R(8, 23)], [R(3, 23), R(20, 23)]]))


def gambler(target, win):
    q = s.zeros(target-1)
    right_exit = s.zeros(target-1, 1)
    for i in range(1, target):
        for destination, probability in [(i+1, win), (i-1, 1-win)]:
            if destination == target:
                right_exit[i-1] += probability
            elif destination > 0:
                q[i-1, destination-1] += probability
    inverse = (s.eye(target-1)-q).inv()
    return inverse*right_exit, inverse*s.ones(target-1, 1)


def ex10():
    h, _ = gambler(4, R(3, 5))
    eq(h[0], R(27, 65))
    eq(h[1], R(9, 13))
    approx(h[0], .415, 3)
    approx(h[1], .692, 3)
    practice, _ = gambler(10, R(1, 2))
    eq(practice[2], R(3, 10))


def ex11():
    inverse = (s.eye(2)-Q11).inv()
    eq(inverse*s.ones(2, 1), M([R(40, 9), R(35, 9)]))
    eq(inverse, M([[R(10, 3), R(10, 9)], [R(5, 3), R(20, 9)]]))
    eq(inverse*M([[R(1, 5), 0], [0, R(3, 10)]]), M([[R(2, 3), R(1, 3)], [R(1, 3), R(2, 3)]]))
    eq((s.eye(2)-Q9).inv()*s.ones(2, 1), M([R(70, 23), R(60, 23)]))
    approx(R(40, 9), 4.44, 2)
    approx(R(35, 9), 3.89, 2)


def ex12():
    i, n = s.symbols("i n", integer=True)
    formula = i*(n-i)
    eq(formula, 1+(formula.subs(i, i+1)+formula.subs(i, i-1))/2)
    eq(formula.subs(i, 0), 0)
    eq(formula.subs(i, n), 0)
    _, times = gambler(10, R(1, 2))
    eq(times, M([j*(10-j) for j in range(1, 10)]))
    eq(times[4], 25)


def pattern_times(pattern):
    # Build states from proper prefixes; retain the longest suffix after each toss.
    prefixes = [pattern[:i] for i in range(len(pattern))]
    q = s.zeros(len(prefixes))
    for i, prefix in enumerate(prefixes):
        for toss in "HT":
            sequence = prefix+toss
            if sequence.endswith(pattern):
                continue
            new = max((p for p in prefixes if sequence.endswith(p)), key=len)
            q[i, prefixes.index(new)] += R(1, 2)
    return (s.eye(len(prefixes))-q).inv()*s.ones(len(prefixes), 1)


def ex13():
    eq(pattern_times("HH"), M([6, 4]))
    eq(pattern_times("HT"), M([4, 2]))


def ex14():
    eq(stationary(P), M([[R(3, 5), R(2, 5)]]))
    p = M([[R(9, 10), R(1, 10)], [R(2, 5), R(3, 5)]])
    eq(stationary(p), M([[R(4, 5), R(1, 5)]]))


def ex15():
    pi = stationary(WEATHER)
    eq(pi, M([[R(24, 61), R(22, 61), R(15, 61)]]))
    for value, rounded in zip(pi, [.393, .361, .246]):
        approx(value, rounded, 3)


def ex16():
    eq(stationary(LINKS), M([[R(2, 5), R(1, 5), R(2, 5)]]))
    p = R(85, 100)*LINKS+R(15, 100)*s.ones(3)/3
    for value, rounded in zip(stationary(p), [.388, .215, .397]):
        approx(value, rounded, 3)
    hitting = (s.eye(1)-P.extract([1], [1])).inv()[0]
    eq(hitting, R(10, 3))
    eq(1+P[0, 1]*hitting, R(5, 3))
    eq(1+P[0, 1]*hitting, 1/stationary(P)[0])


def irreducible(p):
    reachable = s.eye(p.rows)
    for k in range(1, p.rows):
        reachable += p**k
    return all(v > 0 for v in reachable)


def periods(p):
    # For these explicit 3-state graphs all simple cycles have length <=3.
    result = []
    for i in range(p.rows):
        period = 0
        for k in range(1, 19):
            if (p**k)[i, i] > 0:
                period = gcd(period, k)
        result.append(period)
    return result


def ex17():
    a = M([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    b = M([[R(1, 2), R(1, 2), 0], [0, 0, 1], [1, 0, 0]])
    c = M([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    assert [irreducible(p) for p in [a, b, c]] == [True, True, False]
    assert periods(a) == [3, 3, 3]
    assert periods(b) == [1, 1, 1]
    assert periods(c) == [1, 2, 2]
    assert len((c.T-s.eye(3)).nullspace()) == 2
    for pi in [M([[1, 0, 0]]), M([[0, R(1, 2), R(1, 2)]])]:
        eq(pi*c, pi)
    uniform = stationary(a)
    eq(uniform*a, uniform)
    initial = M([[1, 0, 0]])
    assert initial*a != initial and initial*a**3 == initial
    assert "从非平稳的初始分布" in EXAMPLES["17"]
    assert "每三步轮回一次" in EXAMPLES["17"]
    x, y = s.symbols("x y", real=True)
    pi0 = M([[x, y, 1-x-y]])
    eq(pi0*a**3, pi0)
    assert s.solve(list(pi0*a-pi0), [x, y]) == {x: R(1, 3), y: R(1, 3)}


def ex18():
    count = s.symbols("count", positive=True)
    delta = R(15, 100)/count
    eq(1-count*delta, R(85, 100))
    p = R(85, 100)*LINKS+R(15, 100)*s.ones(3)/3
    assert all(v >= delta.subs(count, 3) for v in p)
    pi = stationary(p)
    assert all(v > 0 for v in pi)
    eq(pi*p, pi)


def poisson(mean, k):
    return s.exp(-mean)*mean**k/s.factorial(k)


def ex19():
    rate, duration = s.Integer(3), R(1, 2)
    count_zero = poisson(rate*duration, 0)
    x = s.symbols("x", nonnegative=True)
    waiting_tail = s.integrate(rate*s.exp(-rate*x), (x, duration, s.oo))
    eq(count_zero, s.exp(-R(3, 2)))
    eq(waiting_tail, count_zero)
    approx(count_zero, .2231, 4)
    approx(sum(poisson(6, k) for k in range(5)), .2851, 4)


def ex20():
    third_arrived = 1-sum(poisson(3, k) for k in range(3))
    eq(third_arrived, 1-R(17, 2)*s.exp(-3))
    approx(third_arrived, .5768, 4)
    approx(1-third_arrived, .4232, 4)
    x = s.symbols("x", nonnegative=True)
    eq(3*s.integrate(x*3*s.exp(-3*x), (x, 0, s.oo)), 1)


def ex21():
    t, z = s.symbols("t z", positive=True)
    generating_product = s.exp(3*t*(z-1))*s.exp(2*t*(z-1))
    eq(generating_product, s.exp(5*t*(z-1)))
    eq(s.diff(generating_product, z).subs(z, 1), 5*t)
    actual = poisson(3*R(1, 5), 0)*poisson(2*R(1, 5), 0)
    eq(actual, s.exp(-1))
    approx(actual, .3679, 4)


def ex22():
    x = s.symbols("x", real=True)
    density4 = s.exp(-x*x/8)/s.sqrt(8*s.pi)
    tail = s.integrate(density4, (x, 2, s.oo))
    eq(tail, (1-s.erf(1/s.sqrt(2)))/2)
    approx(tail, .1587, 4)
    density9 = s.exp(-x*x/18)/s.sqrt(18*s.pi)
    approx(s.integrate(density9, (x, -3, 3)), .6827, 4)


def ex23():
    covariance = M([[min(i, j) for j in [1, 2, 3]] for i in [1, 2, 3]])
    summed, increment, first = M([[1, 1, 0]]), M([[-1, 0, 1]]), M([[1, 0, 0]])
    eq((summed*covariance*summed.T)[0], 5)
    eq((increment*covariance*increment.T)[0], 2)
    eq((increment*covariance*first.T)[0], 0)
    # Disjoint increment coefficient supports establish independence directly.
    disjoint_basis = M([[1, 0, 0], [1, 1, 0], [1, 1, 1]])
    a, b = increment*disjoint_basis, first*disjoint_basis
    assert all(a[j]*b[j] == 0 for j in range(3))


def figure_n4():
    p = M([[R(1, 2), R(1, 2), 0], [0, 0, 1], [1, 0, 0]])
    source = (ROOT / "figs/P9-n4.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    dist_node = next(node for node in tree.body if isinstance(node, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "dist" for t in node.targets))
    dist = ast.literal_eval(dist_node.value)
    for n, row in enumerate(dist):
        eq(M([[1, 0, 0]])*p**n, M([[R(str(v)) for v in row]]))
    claim = re.search(r"趋于 \(([^)]+)\)", source)[1]
    eq(stationary(p), M([[R(v.strip()) for v in claim.split(",")]]))
    assert "(1/2, 1/4, 1/4)" in LESSON


def figure_n5():
    tree = ast.parse((ROOT / "figs/P9-n5.py").read_text(encoding="utf-8"))
    loop = next(node for node in tree.body if isinstance(node, ast.For))
    counts = ast.literal_eval(loop.iter.args[1])
    # Execute only numerical assignments; never import or run plotting code.
    numeric = [node for node in loop.body if isinstance(node, ast.Assign)
               and all(isinstance(t, ast.Name) and t.id in {"dt", "rng", "steps", "x", "path"}
                       for t in node.targets)]
    code = compile(ast.Module(body=numeric, type_ignores=[]), "P9-n5-data", "exec")
    for n in counts:
        namespace = {"np": np, "n": n}
        exec(code, namespace)
        steps, path = namespace["steps"], namespace["path"]
        assert len(steps) == n and len(path) == n+1
        assert np.allclose(steps**2, 1/n, rtol=0, atol=1e-14)
        assert np.allclose(np.diff(path), steps)
        assert path[0] == 0 and np.isfinite(path).all()
        assert min(path) >= -3 and max(path) <= 3
    assert "不是同一条路径的逐步细化" in LESSON
    assert "并不是路径不能越过的边界" in LESSON


def edit_numbers():
    """编辑稿新增的数字：例 7 后随堂题、章末回收开头的问题。"""
    q = M([[R(7, 10), R(3, 10)], [R(2, 10), R(8, 10)]])
    eq((q**2)[1, 1], R(7, 10))
    eq(R(6, 10)+R(4, 10)*R(1, 2)**2, R(7, 10))
    eq((P**12)[0, 0], R(6, 10)+R(4, 10)*R(1, 2)**12)
    approx((P**12)[0, 0], 0.6001, 4)
    approx((P**12)[0, 1], 0.3999, 4)
    approx((P**12)[1, 0], 0.5999, 4)
    approx((P**12)[1, 1], 0.4001, 4)
    qa = M([[R(6, 10), R(2, 10)], [R(3, 10), R(4, 10)]])
    left = (qa**12)*M([1, 1])
    approx(left[0], 0.043, 3)
    approx(left[1], 0.035, 3)
    approx(R(35, 9), 3.9, 1)
    approx(R(40, 9), 4.4, 1)
    # 例 13 前的 CK 反例：X_{n+2}=X_n 的两步回到原处概率为 1，而方程给出 1/2
    assert R(1, 2)*R(1, 2)+R(1, 2)*R(1, 2) == R(1, 2)


if __name__ == "__main__":
    for number in range(1, 24):
        run(number, globals()[f"ex{number:02d}"])
    print("MANUAL 例3 一般证明：新增量独立于过去增量，过去状态由过去增量决定")
    for name, check in [("例4后随堂题", inverse_practice), ("图P9-n4数据", figure_n4),
                        ("图P9-n5步长", figure_n5), ("编辑稿新增数字", edit_numbers)]:
        try:
            check()
            print(f"PASS {name}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {name} {type(exc).__name__}: {exc}")
    if covered != set(EXAMPLES):
        failures += 1
        print("FAIL 例题覆盖 讲义编号与脚本不一致")
    sys.exit(bool(failures))
