"""Check all nine numbered examples, including each option in example 8.

Boolean conclusions use complete truth tables. Real-number conclusions use
exact sets or symbolic sign certificates; finite residues cover divisibility.
The nearby in-lesson exercises are also checked with the related example.
"""

import sympy as sp
from sympy.calculus.util import continuous_domain

from z1_problems import (
    AND, OR, NOT, IMP, IFF, XOR, p, q, r, x,
    equivalent, real_set, relation, require, rows, truth,
)


def example_1():
    expr = AND(OR(p, q), NOT(AND(p, q)))
    columns = [OR(p, q), AND(p, q), NOT(AND(p, q)), expr]
    computed = [truth(column, (p, q)) for column in columns]
    actual = [row + tuple(column[row] for column in computed) for row in computed[0]]
    expected = [(1, 1, 1, 1, 0, 0), (1, 0, 1, 0, 1, 1),
                (0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 1, 0)]
    require(actual == expected)
    require(equivalent(expr, XOR(p, q)))
    require(equivalent(OR(AND(p, NOT(q)), AND(NOT(p), q)), XOR(p, q)))


def example_2():
    actual = rows(AND(OR(p, q), NOT(r)))
    require(actual == {(1, 1, 0), (1, 0, 0), (0, 1, 0)})
    require(len(truth(AND(OR(p, q), NOT(r)))) - len(actual) == 5)


def example_3():
    pset, qset = real_set(x > 2), real_set(x ** 2 > 4)
    np, nq = sp.S.Reals - pset, sp.S.Reals - qset
    failures = [pset - qset, qset - pset, np - nq, nq - np]
    require([failure == sp.EmptySet for failure in failures] == [True, False, False, True])
    require(-3 in failures[1] and -3 in failures[2])
    require(sp.Integer(-3) ** 2 == 9)
    require(nq == sp.Interval(-2, 2))
    # Multiples of 6 and 3 repeat every 6 integers: residues are exhaustive.
    actual = []
    for kind in range(4):
        values = []
        for n in range(6):
            multiple6, multiple3 = n % 6 == 0, n % 3 == 0
            formulas = (IMP(multiple6, multiple3), IMP(multiple3, multiple6),
                        IMP(not multiple6, not multiple3), IMP(not multiple3, not multiple6))
            values.append(bool(formulas[kind]))
        actual.append(all(values))
    require(actual == [True, False, False, True])
    require(3 % 3 == 0 and 3 % 6 != 0)


def example_4():
    sqrt_domain = continuous_domain(sp.sqrt(x), x, sp.S.Reals)
    log_domain = continuous_domain(sp.log(x), x, sp.S.Reals)
    require(sqrt_domain == real_set(x >= 0))
    require(log_domain == real_set(x > 0))
    require(sqrt_domain - real_set(x >= 0) == sp.EmptySet)
    require(log_domain.intersect(real_set(x <= 0)) == sp.EmptySet)
    # All divisibility states repeat modulo 4, including negative integers.
    require(all(bool(IMP(n % 4 == 0, n % 2 == 0)) for n in range(4)))
    nonzero = sp.S.Reals - sp.FiniteSet(0)
    require(nonzero - real_set(x ** 2 > 0) == sp.EmptySet)
    require(real_set(x ** 2 <= 0) == sp.FiniteSet(0))
    require(equivalent(IMP(NOT(p), NOT(q)), IMP(q, p)))
    # The four translations, independently expressed as absence of a violation.
    translations = (IMP(p, q), IMP(p, q), IMP(NOT(q), NOT(p)), IMP(NOT(p), q))
    violations = (AND(p, NOT(q)), AND(p, NOT(q)),
                  AND(NOT(q), p), AND(NOT(p), NOT(q)))
    require(all(equivalent(statement, NOT(violation))
                for statement, violation in zip(translations, violations)))


def example_5():
    a, b = sp.symbols("a b", real=True)
    first, second = a > b, a ** 2 > b ** 2
    require(bool(first.subs({a: 1, b: -2})) and not bool(second.subs({a: 1, b: -2})))
    require(bool(second.subs({a: -3, b: 1})) and not bool(first.subs({a: -3, b: 1})))
    require([sp.Integer(value) ** 2 for value in (1, -2, -3, 1)] == [1, 4, 9, 1])
    require(sp.simplify(sp.Abs(a) ** 2 - a ** 2) == 0)
    require(sp.simplify(sp.Abs(b) ** 2 - b ** 2) == 0)
    # For u,v >= 0, u>v means u=v+d with d>0. Prove the square
    # difference positive; the two cases u=v and u<v exclude the converse's failure.
    v = sp.Symbol("v", nonnegative=True)
    d = sp.Symbol("d", positive=True)
    forward_difference = sp.expand((v + d) ** 2 - v ** 2)
    reverse_difference = sp.expand(v ** 2 - (v + d) ** 2)
    require(forward_difference.is_positive is True)
    require(reverse_difference.is_negative is True)
    require(sp.simplify(v ** 2 - v ** 2) == 0)


def example_6():
    original = IMP(p, AND(q, r))
    expected = AND(p, OR(NOT(q), NOT(r)))
    require(equivalent(NOT(original), expected))
    violation = real_set(x > 1).intersect(
        real_set(x ** 2 <= 1).union(real_set(x ** 3 <= 1)))
    require(violation == sp.EmptySet)
    require(NOT(x > 1) == (x <= 1))


def example_7():
    originals = (AND(p, q), OR(p, q), IMP(r, OR(p, q)))
    expected = (OR(NOT(p), NOT(q)), AND(NOT(p), NOT(q)), AND(r, NOT(p), NOT(q)))
    require(all(equivalent(NOT(original), result) for original, result in zip(originals, expected)))
    require(NOT(x > 0) == (x <= 0))
    # For every nonzero real y, xy=0 has only x=0, excluded by the claimed negation.
    nonzero_y = sp.Symbol("nonzero_y", real=True, nonzero=True)
    zeros = sp.solveset(x * nonzero_y, x, domain=sp.S.Reals)
    require(zeros == sp.FiniteSet(0))
    require(zeros.intersect(sp.S.Reals - sp.FiniteSet(0)) == sp.EmptySet)
    require(equivalent(NOT(OR(p, AND(q, r))), AND(NOT(p), OR(NOT(q), NOT(r)))))


def example_8():
    original = IMP(p, q)
    options = (OR(NOT(p), q), IMP(p, q), IMP(NOT(q), NOT(p)),
               IMP(NOT(p), NOT(q)), AND(p, NOT(q)))
    expected = ("等价", "等价", "等价", "两者皆非", "矛盾")
    for label, option, result in zip("ABCDE", options, expected):
        require(relation(original, option) == result, f"example 8 option {label}")
    require(rows(original, 0, (p, q)) == {(1, 0)})
    require(rows(options[3], 0, (p, q)) == {(0, 1)})
    require(truth(AND(original, options[3]), (p, q))[(1, 1)] == 1)


def example_9():
    first = real_set(x <= 1).union(real_set(x >= 3))
    # A conditional is false exactly on the intersection of premise and nonconclusion.
    violation = real_set(x > 1).intersect(real_set(x < 3))
    conditional_true = sp.S.Reals - violation
    require(first == conditional_true)
    require(violation == sp.Interval.open(1, 3))
    require(first.intersect(violation) == sp.EmptySet)
    require(first.union(violation) == sp.S.Reals)
    original = OR(p, q)
    options = (AND(NOT(p), NOT(q)), OR(NOT(p), NOT(q)), IMP(NOT(p), NOT(q)))
    require([equivalent(NOT(original), option) for option in options] == [True, False, False])
    require(truth(AND(original, options[1]), (p, q))[(1, 0)] == 1)
    require(truth(AND(original, options[2]), (p, q))[(1, 0)] == 1)


def main():
    failures = 0
    for number in range(1, 10):
        try:
            globals()[f"example_{number}"]()
            print(f"PASS 例{number}")
        except Exception as error:
            failures += 1
            print(f"FAIL 例{number} {error}")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
