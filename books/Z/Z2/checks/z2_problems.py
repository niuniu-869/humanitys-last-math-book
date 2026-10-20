"""Exhaustive Boolean checks and exact algebra, compared with answers.md.

The formulas below transcribe the questions, not their proposed derivations.
Every truth assignment is evaluated with SymPy.
"""
from itertools import combinations, product
from pathlib import Path
import re
import sys

import sympy as S
from sympy.logic.boolalg import And, Implies as I, Not, Or

ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"\*\*(Z2-\d+)\*\*\n(.*?)(?=\n\*\*Z2-\d+\*\*|\Z)",
    ANSWERS, re.S,
))
p, q, r, s = S.symbols("p q r s")
failures = 0


def truth(formula, variables, row):
    return bool(formula.subs(dict(zip(variables, row))))


def feasible(variables, premises):
    return [row for row in product((0, 1), repeat=len(variables))
            if all(truth(f, variables, row) for f in premises)]


def counterexamples(variables, premises, conclusion):
    return [row for row in feasible(variables, premises)
            if not truth(conclusion, variables, row)]


def entails(variables, premises, conclusion):
    assert feasible(variables, premises), "Unexpected inconsistent premises"
    return not counterexamples(variables, premises, conclusion)


def first(pid):
    return BLOCKS[pid].splitlines()[0]


def answer_rows(pid, width):
    pattern = r"\((?:[01],){" + str(width - 1) + r"}[01]\)"
    return {tuple(map(int, row[1:-1].split(',')))
            for row in re.findall(pattern, first(pid))}


def require(pid, *snippets):
    for snippet in snippets:
        assert snippet in BLOCKS[pid], f"Answer text missing {snippet!r}"


def choice(pid, values):
    actual = [letter for letter, valid in zip("ABCD", values) if valid]
    claimed = re.search(r"\*\*答案：\*\* \(([A-D])\)", first(pid))[1]
    assert actual == [claimed], (actual, claimed, values)


def check(pid, fn):
    global failures
    try:
        fn()
        print(f"PASS {pid}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")


def problem01():
    options = [I(p, r), I(r, p), I(Not(p), Not(r)), I(Not(r), p)]
    choice("Z2-01", [entails((p, q, r), [I(p, q), I(q, r)], option)
                     for option in options])
    for option, row in [(options[1], (0, 0, 1)),
                        (options[2], (0, 1, 1)),
                        (options[3], (0, 0, 0))]:
        assert row in counterexamples((p, q, r), [I(p, q), I(q, r)], option)


def problem02():
    premises = [I(p, Or(q, r)), Not(q)]
    candidates = [(0, 0, 0), (1, 0, 0), (1, 0, 1)]
    invalid = counterexamples((p, q, r), premises, r)
    assert set(invalid) == answer_rows("Z2-02", 3)
    assert [row in invalid for row in candidates] == [True, False, False]
    assert not truth(premises[0], (p, q, r), candidates[1])
    assert truth(r, (p, q, r), candidates[2])


def problem03():
    premises = [Or(p, q), I(r, p), r]
    options = [p, Or(p, r), Or(q, Not(q)), Not(q)]
    choice("Z2-03", [not entails((p, q, r), premises, option)
                     for option in options])
    assert (1, 1, 1) in counterexamples((p, q, r), premises, Not(q))


def problem04():
    premises = [I(p, And(q, r)), Not(r)]
    rows = feasible((p, q, r), premises)
    assert {row[0] for row in rows} == {0}
    assert not entails((p, q, r), premises, Not(q))
    assert (0, 1, 0) in counterexamples((p, q, r), premises, Not(q))


def problem05():
    x = S.symbols("x", real=True)
    f = x**2 + S.Abs(x)
    positive = S.solve_univariate_inequality(f > 0, x, relational=False)
    nonnegative = S.solve_univariate_inequality(f >= 0, x, relational=False)
    assert positive == S.Union(S.Interval.open(-S.oo, 0),
                               S.Interval.open(0, S.oo))
    assert nonnegative == S.S.Reals
    assert S.reduce_inequalities([x > 0, x**2 + x <= 0], x) == S.false
    assert S.reduce_inequalities([x < 0, x**2 - x <= 0], x) == S.false
    assert f.subs(x, 0) == 0
    require("Z2-05", "两条分支都正确", "推断无效", "$x=0$",
            r"$(-\infty,0)\cup(0,+\infty)$", r"$\mathbb{R}$")


def problem06():
    variables = (p, q, r, s)
    premises = [I(p, q), I(And(q, r), s), Not(s)]
    options = [r, q, Not(r), Or(q, r)]
    choice("Z2-06", [entails(variables, premises + [option], Not(p))
                     for option in options])
    for option in options[1:]:
        assert (1, 1, 0, 0) in counterexamples(
            variables, premises + [option], Not(p))


def problem07():
    variables = (p, q, r, s)
    premises = [I(Or(p, q), r), I(r, Or(p, s)), Not(s)]
    assert set(counterexamples(variables, premises, I(r, q))) == answer_rows("Z2-07", 4)
    assert entails(variables, premises, I(q, r))
    require("Z2-07", "(1) 无效", "(2) 有效")


def problem08():
    variables = (p, q, r, s)
    premises = [I(p, q), I(p, r), I(And(q, r), s), I(s, Not(q))]
    literals = [p, Not(p), q, Not(q), r, Not(r), s, Not(s)]
    assert [f for f in literals if entails(variables, premises, f)] == [Not(p)]
    rows = feasible(variables, premises)
    witnesses = [(0, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    assert all(row in rows for row in witnesses)
    assert all({row[i] for row in rows} == {0, 1} for i in (1, 2, 3))
    require("Z2-08", r"只有 $\neg p$ 一定为真")


def problem09():
    variables = (p, q, r, s)
    premises = [Or(p, q), I(p, r), I(q, s), Not(And(r, s))]
    rows = feasible(variables, premises)
    assert set(rows) == answer_rows("Z2-09", 4)
    formulas = [p, q, Or(r, s), S.Equivalent(p, Not(q))]
    values = [[truth(f, variables, row) for row in rows] for f in formulas]
    predicates = [all, lambda vs: not any(vs), any, lambda vs: not all(vs)]
    labels = ["一定为真", "一定为假", "可能为真", "不能推出"]
    for label, predicate in zip(labels, predicates):
        calculated = "".join(mark for mark, vs in zip("①②③④", values) if predicate(vs))
        match = re.search(label + r"：(无|[①②③④]+)", first("Z2-09"))
        claimed = match[1]
        if claimed == "无":
            claimed = ""
        assert calculated == claimed, (label, calculated, claimed)


def problem10():
    variables = (p, q, r)
    premises = [Or(I(p, r), I(q, r)), Or(p, q)]
    assert set(counterexamples(variables, premises, r)) == answer_rows("Z2-10", 3)
    assert entails(variables, [I(Or(p, q), r), Or(p, q)], r)
    require("Z2-10", "(1) 无效", "(2) 有效")


def problem12():
    t = S.Symbol("t")
    variables = (p, q, r, s, t)
    premises = [I(p, q), I(Not(r), p), Or(q, s), I(And(q, r), t), I(s, r), Not(t)]
    rows = feasible(variables, premises)
    assert set(rows) == answer_rows("Z2-12", 5)
    values = [{truth(f, variables, row) for row in rows}
              for f in [Or(p, s), And(p, s), p]]
    assert values == [{True}, {False}, {True, False}]
    extra = Not(And(p, Not(r)))
    assert S.simplify_logic(S.Equivalent(extra, Or(Not(p), r))) == S.true
    final_rows = feasible(variables, premises + [extra])
    claimed = re.search(r"\(3\) 只剩 \$\(([^)]+)\)", first("Z2-12"))[1]
    assert final_rows == [tuple(map(int, claimed.split(',')))]
    require("Z2-12", r"$p\vee s$ 一定为真", r"$p\wedge s$ 一定为假",
            "$p$ 可能为真但不能推出", r"$\neg(p\wedge\neg r)$")


def problem11():
    residues = {0, 1}
    sums = {(a + b) % 4 for a in residues for b in residues}
    assert sums == {0, 1, 2}
    assert 3 not in sums
    for a_parity, b_parity in product((0, 1), repeat=2):
        assert (a_parity + b_parity) % 4 != 3


def problem13():
    variables = (p, q, r, s)
    premises = {1: Or(p, q), 2: I(p, r), 3: I(q, r),
                4: I(r, s), 5: I(p, s), 6: I(q, s)}
    def kept(deleted):
        return [formula for n, formula in premises.items() if n not in deleted]
    assert all(entails(variables, kept({n}), s) for n in range(2, 7))
    failing = {pair for pair in combinations(range(2, 7), 2)
               if not entails(variables, kept(pair), s)}
    marks = dict(zip("①②③④⑤⑥", range(1, 7)))
    claimed = {tuple(marks[c] for c in pair)
               for pair in re.findall(r"删([②③④⑤⑥]{2})", first("Z2-13"))}
    assert failing == claimed
    table = re.findall(r"\| ([②③④⑤⑥]{2}) \| \$\(([^)]+)\)\$ \|", BLOCKS["Z2-13"])
    assert {tuple(marks[c] for c in pair) for pair, _ in table} == failing
    for pair, row in table:
        deleted = {marks[c] for c in pair}
        assert tuple(map(int, row.split(','))) in counterexamples(variables, kept(deleted), s)
    require("Z2-13", "任意删去一条仍能推出")


if __name__ == "__main__":
    tests = {1: problem01, 2: problem02, 3: problem03, 4: problem04,
             5: problem05, 6: problem06, 7: problem07, 8: problem08,
             9: problem09, 10: problem10, 12: problem12, 13: problem13}
    for number in range(1, 14):
        pid = f"Z2-{number:02d}"
        check(pid, problem11 if number == 11 else tests[number])
    sys.exit(bool(failures))
