"""Exhaustive Boolean checks and exact real-set checks against answers.md.

Expected formulas/sets below are transcriptions of the printed answers.
Actual values are computed from the problem statements, never sampled.
"""

from itertools import product
from pathlib import Path
import re

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
p, q, r = sp.symbols("p q r")
x = sp.Symbol("x", real=True)
AND, OR, NOT = sp.And, sp.Or, sp.Not
IMP, IFF, XOR = sp.Implies, sp.Equivalent, sp.Xor


def truth(expr, letters=(p, q, r)):
    return {
        row: int(bool(expr.subs(dict(zip(letters, row)))))
        for row in product((1, 0), repeat=len(letters))
    }


def rows(expr, value=1, letters=(p, q, r)):
    return {row for row, result in truth(expr, letters).items() if result == value}


def equivalent(left, right):
    return sp.satisfiable(XOR(left, right)) is False


def relation(left, right):
    if equivalent(left, right):
        return "等价"
    if equivalent(NOT(left), right):
        return "矛盾"
    return "两者皆非"


def real_set(condition, variable=x):
    return sp.solve_univariate_inequality(condition, variable, relational=False)


def require(condition, message="computed result differs from printed answer"):
    if not bool(condition):
        raise AssertionError(message)


def blocks(path):
    text = path.read_text(encoding="utf-8")
    return {
        match[1]: match[2]
        for match in re.finditer(
            r"^\*\*(Z1-\d+)\*\*\n(.*?)(?=^\*\*Z1-\d+\*\*|\Z)",
            text, re.M | re.S,
        )
    }


def printed_rows(text, size):
    return {
        tuple(map(int, match.split(",")))
        for match in re.findall(r"\(([01](?:,[01]){" + str(size - 1) + r"})\)", text)
    }


def printed_table(text):
    table = []
    for line in text.splitlines():
        if re.fullmatch(r"\|(?:\s*[01]\s*\|)+", line):
            table.append(tuple(int(part.strip()) for part in line.strip("|").split("|")))
    return table


def printed_choice(text):
    return re.search(r"\*\*答案：\*\* \(([A-D])\)", text)[1]


def check_choice(actual, text):
    require(actual == [label == printed_choice(text) for label in "ABCD"])


def check_01(answer):
    assignment = {p: sp.Integer(2) > 5, q: sp.Integer(3) ** 2 == 9}
    actual = tuple(int(bool(expr.subs(assignment))) for expr in
                   (IMP(p, q), IMP(q, p), IMP(NOT(q), NOT(p))))
    options = [(0, 0, 0), (1, 1, 1), (1, 0, 1), (1, 0, 0)]
    check_choice([actual == option for option in options], answer)
    require(actual in printed_rows(answer.split("因为")[0], 3))


def check_02(answer):
    formulas = (IMP(p, q), IMP(q, p), AND(IMP(p, q), IMP(q, p)))
    values = [truth(formula, (p, q)) for formula in formulas]
    actual = [row + tuple(column[row] for column in values) for row in values[0]]
    require(actual == printed_table(answer))
    require(equivalent(formulas[-1], IFF(p, q)))
    require(r"p\leftrightarrow q" in answer)


def check_03(answer):
    # A necessary condition excludes q true and p false.
    first = NOT(AND(q, NOT(p)))
    second = IMP(NOT(p), NOT(q))
    third = AND(IMP(p, q), IMP(q, p))
    require(equivalent(first, IMP(q, p)))
    require(equivalent(first, second))
    require(equivalent(third, IFF(p, q)))
    require(rows(AND(first, second, NOT(third)), letters=(p, q))
            == printed_rows(answer.split("因为")[0], 2))


def check_04(answer):
    y = sp.Symbol("y", real=True)
    premise, conclusion = x <= 0, y > 0
    inverse = IMP(NOT(premise), NOT(conclusion))
    negation = NOT(IMP(premise, conclusion))
    require(NOT(premise) == (x > 0) and NOT(conclusion) == (y <= 0))
    # Check the general transformation independently of the real substitutions.
    require(equivalent(NOT(IMP(p, q)), AND(p, NOT(q))))
    require(all(bool(expr.subs({x: 0, y: 0})) for expr in (inverse, negation)))
    require("两者都为真" in answer)
    require(r"x>0" in answer and r"y\le0" in answer and r"x\le0" in answer)


def check_05(answer):
    target = XOR(p, q)
    incorrect = OR(p, q)
    correct = AND(OR(p, q), NOT(AND(p, q)))
    require(equivalent(target, correct))
    require(equivalent(incorrect, IMP(NOT(p), q)))
    require(rows(XOR(incorrect, target), letters=(p, q)) == printed_rows(answer, 2))


def check_06(answer):
    target = IMP(NOT(AND(p, q)), NOT(r))
    options = (IMP(AND(p, q), r), IMP(r, AND(p, q)),
               IMP(r, OR(p, q)), IFF(r, AND(p, q)))
    check_choice([equivalent(target, option) for option in options], answer)
    require(rows(target, 0) == printed_rows(answer.split("\n\n")[0], 3))
    for option, row in ((options[0], (1, 1, 0)), (options[2], (1, 0, 1)),
                        (options[3], (1, 1, 0))):
        require(truth(target)[row] != truth(option)[row])


def check_07(answer):
    pset = real_set(x ** 2 <= 4)
    qset = real_set(x >= -1).intersect(real_set(x < 2))
    sufficient = qset.is_subset(pset)
    necessary = pset.is_subset(qset)
    require(sufficient and not necessary)
    require("充分不必要" in answer)
    require(2 in pset and 2 not in qset)
    actual = sp.SymmetricDifference(pset, qset)
    expected = sp.Union(sp.Interval(-2, -1, right_open=True), sp.FiniteSet(2))
    require(actual == expected)
    require(r"D=[-2,-1)\cup\{2\}" in answer)
    remaining = sp.S.Reals - expected
    require(pset.intersect(remaining) == qset.intersect(remaining))
    # The disagreement set is exactly the deletion set, proving minimality.
    require(expected - actual == sp.EmptySet and actual - expected == sp.EmptySet)


def check_08(answer):
    target = IMP(OR(p, q), IMP(r, p))
    expected_negation = AND(NOT(p), q, r)
    require(equivalent(NOT(target), expected_negation))
    values = truth(target)
    require([row + (value, 1 - value) for row, value in values.items()]
            == printed_table(answer))
    require(rows(target, 0) == printed_rows(answer.split("\n\n")[0], 3))


def check_09(answer):
    clauses = (IMP(q, p), IMP(NOT(q), NOT(r)), NOT(AND(p, r)))
    target = AND(*clauses)
    expected = AND(IMP(q, p), IMP(r, q), NOT(AND(p, r)))
    require(equivalent(target, expected))
    require(rows(target) == printed_rows(answer.split("对合取")[0], 3))
    require(rows(NOT(target)) == printed_rows(answer.split("它为真的")[1], 3))
    require("q\\to p" in answer and "\\neg q\\to\\neg r" in answer)


def check_10(answer):
    clauses = (IMP(q, p), IMP(NOT(p), NOT(r)), OR(q, r))
    target = AND(*clauses)
    require(equivalent(target, AND(p, OR(q, r))))
    require(rows(target) == printed_rows(answer.split("；三条要求")[0], 3))
    witnesses = [(0, 1, 0), (0, 0, 1), (0, 0, 0)]
    for index, witness in enumerate(witnesses):
        reduced = AND(*(clause for j, clause in enumerate(clauses) if j != index))
        require(not equivalent(reduced, target))
        require(witness in rows(AND(reduced, NOT(target))))
    require(set(witnesses).issubset(printed_rows(answer, 3)))


def check_12(answer):
    universe = sp.Interval(0, 4)
    qset = universe.intersect(real_set(x ** 2 >= 4))
    bad = universe - qset
    # p is x>a: eliminating all bad x requires a >= sup(bad).
    forward = sp.Interval(bad.sup, sp.oo)
    # Every q-object must satisfy x>a; an attained minimum makes this strict.
    reverse = sp.Interval(-sp.oo, qset.inf, right_open=qset.contains(qset.inf) is sp.true)
    require(forward == sp.Interval(2, sp.oo))
    require(reverse == sp.Interval(-sp.oo, 2, right_open=True))
    require(forward.intersect(reverse) == sp.EmptySet)
    require(r"a\ge2" in answer and r"a<2" in answer and "不存在" in answer)
    require(qset - universe.intersect(real_set(x > 2)) == sp.FiniteSet(2))
    require(universe.intersect(real_set(x > 4)) == sp.EmptySet)
    a_negative = sp.Symbol("a_negative", negative=True)
    require((0 > a_negative) is sp.true and (0 in bad))
    a = sp.Symbol("a", real=True)
    witness = (a + 2) / 2
    witness_parameters = real_set(witness > a, a).intersect(real_set(witness < 2, a))
    witness_parameters = witness_parameters.intersect(real_set(witness >= 0, a))
    require(sp.Interval(0, 2, right_open=True).is_subset(witness_parameters))


def check_13(answer):
    target = AND(IFF(p, OR(q, r)), IMP(NOT(q), NOT(r)))
    candidates = (
        AND(IFF(p, q), IMP(r, q)),
        OR(AND(p, NOT(q)), AND(NOT(p), q), AND(r, NOT(q))),
        AND(IMP(p, q), IMP(r, q)),
        AND(p, NOT(q), NOT(r)),
    )
    require(rows(target) == printed_rows(answer.split("\n\n")[0], 3))
    require([relation(target, item) for item in candidates]
            == ["等价", "矛盾", "两者皆非", "两者皆非"])
    require("①等价，②矛盾，③④均为两者皆非" in answer)
    for index, same, different in ((2, (1, 1, 0), (0, 1, 0)),
                                   (3, (0, 1, 0), (0, 0, 0))):
        left, right = truth(target), truth(candidates[index])
        require(left[same] == right[same] and left[different] != right[different])


CHECKS = {1: check_01, 2: check_02, 3: check_03, 4: check_04, 5: check_05,
          6: check_06, 7: check_07, 8: check_08, 9: check_09, 10: check_10,
          12: check_12, 13: check_13}


def main():
    answers = blocks(ROOT / "answers.md")
    problems = (ROOT / "problems.md").read_text(encoding="utf-8")
    expected_ids = {f"Z1-{number:02d}" for number in range(1, 14)}
    require(set(answers) == expected_ids, "answer coverage mismatch")
    require(set(re.findall(r"^\*\*(Z1-\d+)\*\*", problems, re.M)) == expected_ids,
            "problem coverage mismatch")
    failures = 0
    for number in range(1, 14):
        pid = f"Z1-{number:02d}"
        try:
            answer = answers[pid].split("\n### ")[0].strip()
            limit = 400 if number <= 5 else 900 if number <= 10 else 1400
            require(len(answer) <= limit, f"answer has {len(answer)} characters, limit {limit}")
            require(answer.startswith("**答案：**") and "区分点：" in answer.splitlines()[-1],
                    "answer format mismatch")
            if number == 11:
                # Exhaustive corroboration does not replace review of the written proof.
                require(equivalent(IMP(p, IMP(q, r)), IMP(AND(p, q), r)))
                print(f"MANUAL {pid} proof; eight truth rows also checked")
            else:
                CHECKS[number](answer)
                print(f"PASS {pid}")
        except Exception as error:
            failures += 1
            print(f"FAIL {pid} {error}")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
