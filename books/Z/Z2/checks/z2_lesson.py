"""Independently verify all 11 numbered lesson examples with SymPy.

Truth tables enumerate every assignment; real-number claims use exact
inequality solving. Expected rows and values are transcribed from lesson.md.
"""
from itertools import product
import sys

import sympy as S
from sympy.logic.boolalg import And, Implies as I, Not, Or

p, q, r, s = S.symbols("p q r s")
a, b, c, d, e = S.symbols("a b c d e")
failures = 0


def value(formula, variables, row):
    return int(bool(formula.subs(dict(zip(variables, row)))))


def rows(variables, premises):
    return [row for row in product((0, 1), repeat=len(variables))
            if all(value(f, variables, row) for f in premises)]


def invalid(variables, premises, conclusion):
    return [row for row in rows(variables, premises)
            if not value(conclusion, variables, row)]


def fixed(variables, premises):
    feasible = rows(variables, premises)
    assert feasible
    return {v: next(iter(vs)) for i, v in enumerate(variables)
            if len(vs := {row[i] for row in feasible}) == 1}


def example01():
    premises = [I(p, q), Or(p, r), Not(r)]
    assert rows((p, q, r), premises) == [(1, 1, 0)]
    assert not invalid((p, q, r), premises, q)
    printed = [(1, 1, 0, 1), (1, 1, 1, 1), (0, 1, 0, 0), (0, 1, 1, 0),
               (1, 1, 0, 1), (1, 0, 1, 1), (1, 1, 0, 0), (1, 0, 1, 0)]
    calculated = [tuple(value(f, (p, q, r), row) for f in premises + [q])
                  for row in product((1, 0), repeat=3)]
    assert calculated == printed


def example02():
    assert invalid((p, q, r), [I(p, q), Or(q, r)], Or(p, r)) == [(0, 1, 0)]


def example03():
    conclusion = Or(And(p, q), And(Not(p), Not(q)))
    assert not invalid((p, q), [I(p, q), I(q, p)], conclusion)
    assert rows((p, q), [Not(conclusion)]) == [(0, 1), (1, 0)]
    assert not invalid((p, q), [Not(And(p, q)), p], Not(q))
    assert invalid((p, q), [Not(And(p, q)), Not(p)], q) == [(0, 0)]


def example04():
    # Logical validity of all four argument forms.
    ev, four, nonpositive, square_positive = S.symbols("ev four nonpositive square_positive")
    assert not invalid((ev, four), [I(four, ev), four], ev)
    assert invalid((ev, four), [I(four, ev), ev], four) == [(1, 0)]
    rule = I(Not(nonpositive), square_positive)
    assert not invalid((nonpositive, square_positive), [rule, Not(square_positive)], nonpositive)
    assert invalid((nonpositive, square_positive), [rule, nonpositive], Not(square_positive)) == [(1, 1)]
    # Exact arithmetic counterexamples and real-domain implication checks.
    assert 6 % 2 == 0 and 6 % 4 != 0
    x = S.symbols("x", real=True)
    assert S.reduce_inequalities([x > 0, x**2 <= 0], x) == S.false
    assert (-S.Integer(1))**2 == 1
    assert S.reduce_inequalities([x**2 <= 0, x > 0], x) == S.false
    assert (-S.Integer(3))**2 == 9 and -3 <= 2
    assert S.reduce_inequalities([x**2 <= 4, x > 2], x) == S.false


def example05():
    x = S.symbols("x", real=True)
    polynomial = x**2 - 3*x + 2
    assert S.expand((x-1)*(x-2) - polynomial) == 0
    roots = S.solveset(polynomial, x, domain=S.S.Reals)
    assert roots == S.FiniteSet(1, 2)
    assert roots.intersect(S.Interval.open(1, S.oo)) == S.FiniteSet(2)
    aa, bb = S.symbols("aa bb", real=True)
    assert (aa*bb).subs({aa: 0, bb: 0}) == 0
    assert S.Ne(bb, 0).subs(bb, 0) == S.false


def example06():
    ee, ss, oo, ww = S.symbols("ee ss oo ww")
    variables = (ee, ss, oo, ww)
    first = [Or(ee, ss, oo), Not(ee)]
    assert not invalid(variables, first, Or(ss, oo))
    assert invalid(variables, first, ss) and invalid(variables, first, oo)
    full = first + [I(ss, ww), Not(ww)]
    assert fixed(variables, full) == {ee: 0, ss: 0, oo: 1, ww: 0}
    assert (0, 1, 1) in invalid((ee, ss, oo), first + [ss], Not(oo))


def example07():
    variables = (a, b, c, d, e)
    premises = [I(a, b), I(b, Not(c)), I(d, c), I(Not(a), e)]
    assert fixed(variables, premises + [a]) == {a: 1, b: 1, c: 0, d: 0}
    assert rows(variables, premises + [a]) == [(1, 1, 0, 0, 0), (1, 1, 0, 0, 1)]
    assert fixed(variables, premises + [d]) == {a: 0, b: 0, c: 1, d: 1, e: 1}
    contrapositives = [I(Not(b), Not(a)), I(c, Not(b)), I(Not(c), Not(d)), I(Not(e), a)]
    assert rows(variables, premises) == rows(variables, contrapositives)


def example08():
    k, z, t, j = S.symbols("k z t j")
    premises = [I(z, k), I(z, t), I(Not(t), Not(j)), Not(t)]
    assert rows((k, z, t, j), premises) == [(0, 0, 0, 0), (1, 0, 0, 0)]
    assert not invalid((p, q, r, s), [I(p, q), I(r, Not(q)), I(Not(r), s), p], s)


def example09():
    premises = [I(p, r), I(q, s), Or(Not(r), Not(s))]
    conclusion = Or(Not(p), Not(q))
    assert not invalid((p, q, r, s), premises, conclusion)
    assert invalid((p, q, r, s), premises[:2], conclusion) == [(1, 1, 1, 1)]
    x = S.symbols("x", real=True)
    # Check each exact branch; SymPy's direct Abs inequality solver does not
    # implement this identity on every version.
    assert S.reduce_inequalities([x >= 0, x - x < 0], x) == S.false
    assert S.reduce_inequalities([x < 0, -x - x < 0], x) == S.false
    k = S.symbols("k", integer=True)
    assert S.expand((2*k)**2 + 2*k - 2*k*(2*k+1)) == 0
    assert S.expand((2*k+1)**2 + (2*k+1) - 2*(2*k+1)*(k+1)) == 0


def example10():
    premises = [I(p, q), I(q, r), I(r, Not(p))]
    assert rows((p, q, r), premises) == [(0, 0, 0), (0, 0, 1), (0, 1, 1)]
    assert fixed((p, q, r), premises) == {p: 0}
    # The three truth tellers: each person's truth value equals their statement.
    statements = [S.Equivalent(a, Not(b)), S.Equivalent(b, Not(c)),
                  S.Equivalent(c, And(Not(a), Not(b)))]
    assert rows((a, b, c), statements) == [(0, 1, 0)]
    positive = S.symbols("positive", positive=True)
    assert S.simplify(positive/2 > 0) == S.true
    assert S.simplify(positive/2 < positive) == S.true


def example11():
    variables = (a, b, c)
    premises = [Or(a, b, c), I(a, Not(b)), I(b, c)]
    feasible = rows(variables, premises)
    expected_rows = [(1, 0, 1), (1, 0, 0), (0, 1, 1), (0, 0, 1)]
    assert set(feasible) == set(expected_rows)
    options = [Not(And(a, b)), c, And(b, Not(c)), I(Not(b), a), Or(a, c)]
    table = [tuple(value(f, variables, row) for f in options) for row in expected_rows]
    assert table == [(1, 1, 0, 1, 1), (1, 0, 0, 1, 1),
                     (1, 1, 0, 1, 1), (1, 1, 0, 0, 1)]
    columns = list(zip(*table))
    assert [i for i, col in enumerate(columns) if all(col)] == [0, 4]
    assert [i for i, col in enumerate(columns) if not any(col)] == [2]
    assert [i for i, col in enumerate(columns) if any(col) and not all(col)] == [1, 3]
    assert rows(variables, premises + [Not(c)]) == [(1, 0, 0)]


if __name__ == "__main__":
    for number, fn in enumerate([example01, example02, example03, example04,
                                 example05, example06, example07, example08,
                                 example09, example10, example11], 1):
        try:
            fn()
            print(f"PASS 例{number}")
        except Exception as exc:
            failures += 1
            print(f"FAIL 例{number} {type(exc).__name__}: {exc}")
    sys.exit(bool(failures))
