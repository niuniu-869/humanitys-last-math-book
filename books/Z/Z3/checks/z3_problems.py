"""Exact checks: Boolean region occupancy, finite relations, symbolic inequalities.

Each unary-predicate region needs only an occupied/empty bit: multiplicities
cannot affect these categorical sentences. SAT therefore checks all models,
not just a sample of small integer sets. Expected values come from answers.md
or are accompanied by an exact answer-text anchor.
"""
from itertools import product
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"\*\*(Z3-\d+)\*\*\n(.*?)(?=\n\*\*Z3-|\Z)", ANSWERS, re.S
))
FAILURES = []


def check(pid, detail, actual, expected, anchors=()):
    body = BLOCKS.get(pid, "")
    ok = bool(actual == expected) and all(s in body for s in anchors)
    print(f"{'PASS' if ok else 'FAIL'} {pid} {detail}")
    if not ok:
        FAILURES.append((pid, detail))
        print(f"  computed={actual!r}; expected={expected!r}; "
              f"missing={[s for s in anchors if s not in body]!r}")


class Regions:
    def __init__(self, names):
        self.names = names
        self.rows = [dict(zip(names, row))
                     for row in product((False, True), repeat=len(names))]
        self.occupied = sp.symbols(f"v0:{len(self.rows)}")

    def every(self, predicate):
        return sp.And(*(~v for v, row in zip(self.occupied, self.rows)
                        if not predicate(row)))

    def some(self, predicate):
        return sp.Or(*(v for v, row in zip(self.occupied, self.rows)
                       if predicate(row)))


def entails(premise, conclusion):
    return sp.satisfiable(sp.And(premise, ~conclusion)) is False


def equivalent(left, right):
    return sp.satisfiable(sp.Xor(left, right)) is False


def aeio(s, p):
    return (s <= p, not bool(s & p), bool(s & p), bool(s - p))


def choice(pid, results):
    selected = re.search(r"\*\*答案：\*\* ([A-D])。", BLOCKS[pid]).group(1)
    for label, result in zip("ABCD", results):
        check(pid, f"选项 {label}", result, label == selected)
    check(pid, "唯一正确选项", sum(results), 1)


def main():
    x, y, a = sp.symbols("x y a", real=True)
    check("Z3-01", "(1) 平方非负", sp.ask(sp.Q.nonnegative(x**2)), True,
          ("(1) A 型，真",))
    roots = sp.solveset(x**2 - 1, x, domain=sp.S.Reals)
    check("Z3-01", "(2) 求出全部根后找非正根",
          any(r <= 0 for r in roots), True, ("(2) O 型，真", "$x=-1$"))

    r = Regions("SP")
    target = r.some(lambda t: t["S"] and not t["P"])
    expressions = [
        r.some(lambda t: not t["S"] or not t["P"]),
        r.every(lambda t: not t["S"] or not t["P"]),
        target,
        r.some(lambda t: t["P"] and not t["S"]),
    ]
    choice("Z3-02", [equivalent(e, target) for e in expressions])

    worlds = []
    for bits in product((False, True), repeat=4):
        s = {i for i, (b, t) in enumerate(zip(bits, r.rows)) if b and t["S"]}
        p = {i for i, (b, t) in enumerate(zip(bits, r.rows)) if b and t["P"]}
        if not aeio(s, p)[0] and not aeio(s, p)[1]:
            worlds.append((aeio(s, p), len(s)))
    check("Z3-03", "双假前提的全部区域模型",
          (all(v[2] and v[3] for v, _ in worlds), min(n for _, n in worlds)),
          (True, 2), ("I、O 都真", "至少有 2 个",))
    check("Z3-03", "达到最小值的集合", aeio({0, 1}, {0}),
          (False, False, True, True), (r"S=\{0,1\}", r"P=\{0\}"))

    vals = np.array([-1, 0, 1])
    check("Z3-04", "两句模态命题",
          (bool(~np.all(vals != 0)), bool(~np.any(vals == 0))),
          (True, False), ("第一句真", "第二句假", "a 可能为零", "a 必然非零"))

    # These are symbolic partitions of all real a, not numerical samples.
    t = sp.symbols("t", positive=True)
    root_sets = [sp.solveset(x*x + t, x, domain=sp.S.Reals),
                 sp.solveset(x*x, x, domain=sp.S.Reals),
                 sp.solveset(x*x - t, x, domain=sp.S.Reals)]
    computed = [aeio(set(rs), {v for v in rs if v.is_positive}) for rs in root_sets]
    expected = [tuple(v == "真" for v in row) for row in re.findall(
        r"\| \$a[><=]0\$ \| (真|假) \| (真|假) \| (真|假) \| (真|假) \|",
        BLOCKS["Z3-05"])]
    check("Z3-05", "三个参数分区的真假表", computed, expected)
    choice("Z3-05", [all(not (v[0] and v[1]) for v in computed),
                     all(not v[0] or v[2] for v in computed),
                     all(v[2] or v[3] for v in computed),
                     all(v[0] != v[3] for v in computed)])

    r = Regions("SPM")
    universal = lambda j, k: r.every(lambda t: not t[j] or t[k])
    exists = lambda j, k: r.some(lambda t: t[j] and t[k])
    conclusion = r.some(lambda t: t["S"] and not t["P"])
    premises = [sp.And(universal("S", "M"), universal("P", "M")),
                sp.And(exists("S", "M"), r.some(lambda t: t["M"] and not t["P"])),
                sp.And(r.every(lambda t: not (t["M"] and t["P"])), exists("S", "M")),
                sp.And(universal("M", "P"), r.some(lambda t: t["S"] and not t["M"]))]
    choice("Z3-06", [entails(p, conclusion) for p in premises])
    shaded = [tuple(map(int, row.values())) for row in r.rows if row["M"] and row["P"]]
    forced = [tuple(map(int, row.values())) for row in r.rows
              if row["S"] and row["M"] and not row["P"]]
    check("Z3-06", "阴影与强制落点", (shaded, forced),
          ([(0, 1, 1), (1, 1, 1)], [(1, 0, 1)]),
          ("$(0,1,1)$、$(1,1,1)$", "$(1,0,1)$"))
    models = [(0, {1}, {1}, {1}), (1, {1}, {1}, {1, 2}),
              (3, {1}, {1, 2}, {2})]
    for index, s, p, m in models:
        occupied = {tuple(v in c for c in (s, p, m)) for v in s | p | m}
        env = {v: tuple(row.values()) in occupied for v, row in zip(r.occupied, r.rows)}
        check("Z3-06", f"选项 {'ABCD'[index]} 的具体反例",
              (bool(premises[index].subs(env)), bool(conclusion.subs(env))), (True, False))

    candidates = []
    for bits in product((False, True), repeat=4):
        m = {i + 1 for i, bit in enumerate(bits) if bit}
        if {1, 2} & m and m & {2, 3} and not ({1, 2} & m & {2, 3}):
            candidates.append(tuple(sorted(m)))
    check("Z3-07", "全部符合要求的 M", sorted(candidates), [(1, 3), (1, 3, 4)],
          (r"M=\{1,3\}", r"M=\{1,3,4\}"))
    repair = sp.And(exists("S", "M"), exists("M", "P"), universal("M", "S"))
    check("Z3-07", "补充前提后的所有模型",
          entails(repair, r.some(lambda t: all(t.values()))), True,
          ("(2) 能", "应从「有的 M 是 P」出发"))

    u = np.array([-1, 0, 1])
    relation = (u[:, None] + u[None, :])**2 == 1
    implication = (u[:, None] == u[None, :]) | relation
    results = [relation.any(axis=1).all(), relation.all(axis=0).any(),
               implication.all(axis=0).any(), ((u[:, None] != u[None, :]) & ~relation).any(axis=0).all()]
    check("Z3-08", "三个量词句与否定式", list(map(bool, results)),
          [True, False, True, False], ("(1) 真；(2) 假；(3) 真", "否定为假"))
    check("Z3-08", "逐个检查回答与统一回答",
          (all(relation[i, j] for i, j in enumerate([1, 2, 1])),
           bool(implication[:, 1].all()), bool((~relation.diagonal()).all())),
          (True, True, True), ("$y=0,1,0$", "$y=0$", "$x=y$"))
    # Symbolic cells check the written negation, independently of this R.
    cells = np.array(sp.symbols("c0:9"), dtype=object).reshape(3, 3)
    sentence = sp.Or(*(sp.And(*(sp.Implies(i != j, cells[i, j]) for i in range(3))) for j in range(3)))
    denial = sp.And(*(sp.Or(*(sp.And(i != j, ~cells[i, j]) for i in range(3))) for j in range(3)))
    check("Z3-08", "否定式的逻辑等价", equivalent(~sentence, denial), True,
          (r"\forall y\in U\ \exists x\in U\ (x\ne y\wedge (x+y)^2\ne1)",))

    f = (x - 1)**2
    lower_failures = sp.solveset(sp.Lt((y - 1)**2, f.subs(x, 1)), y, domain=sp.Interval(0, 2))
    check("Z3-09", "(1) 最小值反例覆盖整个区间", lower_failures, sp.S.EmptySet,
          ("(1) 原句假、否定真", r"f(y)\ge f(x)",))
    check("Z3-09", "(2) 对角线选择", sp.simplify(f.subs(x, y).subs(y, x) - f), 0,
          ("(2) 原句真、否定假", "$y=x$", r"f(y)>f(x)",))
    p, q = sp.symbols("p q", real=True)
    check("Z3-09", "严格与非严格比较的否定",
          (sp.Not(p < q), sp.Not(p <= q)), (p >= q, p > q))

    # At x=0 any admissible y <=1; conversely y=1 works on the full interval.
    necessary = sp.solve_univariate_inequality(1 >= a, a, relational=False)
    xpos = sp.symbols("xpos", nonnegative=True)
    check("Z3-10", "两句的参数边界", necessary, sp.Interval(-sp.oo, 1),
          (r"a\le1", "两句都恰在",))
    b = sp.symbols("b", nonnegative=True)
    check("Z3-10", "统一 y=1 的符号证书",
          sp.ask(sp.Q.nonnegative(xpos + 1 - (1 - b))), True, ("$y=1$",))
    check("Z3-10", "a>1 时 x=0 的所有 y 均失败",
          sp.ask(sp.Q.positive((1 + t) - (1 - b))), True)

    r = Regions("SMPQRT")
    prem = sp.And(r.some(lambda v: v["S"] and v["M"]),
                  r.every(lambda v: not v["S"] or v["P"] or v["Q"]),
                  r.every(lambda v: not v["P"] or v["R"]),
                  r.every(lambda v: not v["M"] or not v["R"]),
                  r.every(lambda v: not v["Q"] or v["T"]))
    options = [r.some(lambda v: v["T"] and not v["P"]),
               r.every(lambda v: not v["S"] or v["T"]),
               r.some(lambda v: v["T"] and not v["S"]),
               r.some(lambda v: v["P"] and not v["S"])]
    choice("Z3-11", [entails(prem, c) for c in options])
    sets = {"S": {1, 2}, "M": {1}, "P": {2}, "Q": {1}, "R": {2}, "T": {1}}
    rows = {tuple(i in sets[k] for k in r.names) for i in (1, 2)}
    env = {v: tuple(row.values()) in rows for v, row in zip(r.occupied, r.rows)}
    check("Z3-11", "共同反例", [bool(e.subs(env)) for e in [prem] + options],
          [True, True, False, False, False],
          (r"S=\{1,2\}", r"M=Q=T=\{1\}", r"P=R=\{2\}"))

    # The quantifier proof is reviewed manually; its algebra is also checked.
    xp = sp.symbols("xp", positive=True)
    fx = xp + 1 / xp
    check("Z3-12", "证明中的下界恒等式", sp.simplify(fx - 2 - (xp - 1)**2 / xp), 0,
          (r"\frac{(x-1)^2}{x}",))
    check("Z3-12", "证明中的两对函数值",
          [fx.subs(xp, v) for v in [sp.Rational(1, 2), 1, 2]],
          [sp.Rational(5, 2), sp.Integer(2), sp.Rational(5, 2)])
    m = sp.symbols("m", real=True)
    response = sp.Abs(m) + 1
    margins = [(response + 1 / response - m).subs(m, b),
               (response + 1 / response - m).subs(m, -b)]
    check("Z3-12", "无上界选法覆盖 M 的正负两类",
          all(sp.ask(sp.Q.positive(v)) for v in margins), True, (r"x=|M|+1",))
    print("MANUAL Z3-12 四个量词句与完整证明的推理衔接")

    h_range = sp.solve_univariate_inequality(0 <= a, a, relational=False)
    k_range = sp.solve_univariate_inequality(1 - a <= a, a, relational=False)
    check("Z3-13", "H 的全部参数", h_range, sp.Interval(0, sp.oo), (r"a\ge0",))
    check("Z3-13", "H 的逐点选择 y=x", sp.Abs(x-y).subs(y, x), 0)
    check("Z3-13", "K 的全部参数", k_range, sp.Interval(sp.Rational(1, 2), sp.oo),
          (r"a\ge\frac12",))
    bounds = sp.reduce_inequalities([y >= 0, y <= 1, y <= a, 1 - y <= a], y)
    proposed = sp.And(y >= 0, y <= 1, y >= 1 - a, y <= a)
    check("Z3-13", "全部 y 的范围", sp.simplify(sp.Equivalent(bounds, proposed)), sp.true,
          (r"[0,1]\cap[1-a,a]",))
    check("Z3-13", "K 的参数范围内总有 y=1/2 可选",
          sp.simplify(proposed.subs({y: sp.Rational(1, 2), a: sp.Rational(1, 2)+b})),
          sp.true)
    # Endpoint inequalities suffice: x-y lies between -y and 1-y for 0<=x<=1.
    failures = sp.And(x >= 0, x <= 1, proposed, sp.Or(x - y > a, y - x > a))
    check("Z3-13", "端点条件控制整个区间",
          sp.satisfiable(failures, use_lra_theory=True), False)
    for condition, distance in [(y >= sp.Rational(1, 2), y), (y < sp.Rational(1, 2), 1-y)]:
        failure = sp.And(y >= 0, y <= 1, a < sp.Rational(1, 2), condition, distance <= a)
        check("Z3-13", f"否定式回应分支 {condition}",
              sp.satisfiable(failure, use_lra_theory=True), False,
              (r"\forall y\in[0,1]\ \exists x\in[0,1]\ (|x-y|>a)",))
    check("Z3-13", "a=1/3", (h_range.contains(sp.Rational(1, 3)), k_range.contains(sp.Rational(1, 3))),
          (sp.true, sp.false), (r"a=\frac13", "$H_a$ 真、$K_a$ 假"))

    problem_text = (ROOT / "problems.md").read_text(encoding="utf-8")
    tiers = dict(re.findall(r"\*\*(Z3-\d+)\*\*〔([ABC])", problem_text))
    for pid, tier in tiers.items():
        body = BLOCKS[pid].split("\n### ")[0].strip()
        limit = {"A": 400, "B": 900, "C": 1400}[tier]
        check(pid, "答案格式及字符上限",
              body.startswith("**答案：**") and body.splitlines()[-1].startswith("区分点：")
              and len(body) + len(pid) + 5 <= limit, True)
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
