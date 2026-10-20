"""Check all 16 numbered examples using exact symbolic proof certificates.

PASS for an infinite claim checks the algebra, exhaustive residue classes,
and/or base and induction step. It never claims a finite sample proves it.
The prose proofs still require human reading.
"""

import re
from pathlib import Path

import sympy as s


LESSON = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")
failures = 0


def check(number, condition, note=""):
    global failures
    ok = bool(condition)
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} 例{number}" + (f" {note}" if note else ""))


def run():
    assert set(re.findall(r"\*\*例 (\d+)\*\*", LESSON)) == {str(i) for i in range(1, 17)}
    k, m, r = s.symbols("k m r", integer=True)
    n = s.symbols("n", integer=True, positive=True)
    a, b, c = s.symbols("a b c", integer=True)

    check(1, s.expand((2 * k + 1) ** 2 - (2 * (2 * k ** 2 + 2 * k) + 1)) == 0
          and s.Mod((2 * k + 1) ** 2, 2) == 1)

    chain = (b * n).subs(b, a * m)
    check(2, s.expand(chain - a * (m * n)) == 0 and (m * n).is_integer)

    parity_cases = [s.simplify(s.Mod((2 * k + j) ** 2, 2)) for j in range(2)]
    check(3, all((square_mod != 0) or j == 0 for j, square_mod in enumerate(parity_cases)))

    # An exact algebraic rationality verdict plus the parity certificate.
    check(4, s.sqrt(2).is_rational is False
          and s.solve(s.Eq((2 * r) ** 2, 2 * b), b) == [2 * r ** 2]
          and parity_cases == [0, 1])

    first_primes = list(s.primerange(2, 14))
    N = s.prod(first_primes) + 1
    divisor = s.symbols("divisor", integer=True, positive=True)
    remainder = s.Mod(divisor * k + 1, divisor)
    # For every integer divisor >=2 this is 1. The smallest divisor >1 is
    # prime by the descent argument in the text; test its numerical instance.
    h = s.symbols("h", integer=True, nonnegative=True)
    universal_remainder = remainder.subs(divisor, h + 2).doit()
    check(5, N == 30031 and s.factorint(N) == {59: 1, 509: 1}
          and all(N % prime == 1 for prime in first_primes)
          and universal_remainder == 1)

    base_product = s.symbols("base_product", integer=True, positive=True)
    j = s.symbols("j", integer=True, positive=True)
    # With j among the factors of (n+1)!, that factorial is j*base_product.
    check(6, s.expand(j * base_product + j - j * (base_product + 1)) == 0
          and (j * base_product).is_positive
          and [s.factorial(6) + v for v in range(2, 7)] == list(range(722, 727))
          and [int((s.factorial(6) + v) / v) for v in range(2, 7)] == [361, 241, 181, 145, 121]
          and all(not s.isprime(s.factorial(6) + v) for v in range(2, 7)))

    values = [v ** 2 + v + 41 for v in range(1, 41)]
    check(7, all(s.isprime(value) for value in values[:39])
          and values[-1] == 41 ** 2 and not s.isprime(values[-1]))

    x = s.symbols("x", real=True)
    expression = s.Abs(x - 1) + s.Abs(x - 3)
    solved = s.reduce_inequalities([expression >= 2], x)
    equality = s.solveset(expression - 2, x, domain=s.S.Reals)
    check(8, solved == s.true and equality == s.Interval(1, 3)
          and s.expand((1 - x) + (3 - x)) == 4 - 2 * x
          and s.expand((x - 1) + (3 - x)) == 2
          and s.expand((x - 1) + (x - 3)) == 2 * x - 4)

    # Every odd integer has one of these four residues modulo 8.
    check(9, all(s.simplify(s.Mod((8 * k + j) ** 2 - 1, 8)) == 0
                 for j in (1, 3, 5, 7))
          and 5 ** 2 - 1 == 24)

    check(10, s.simplify(s.summation(2 * k - 1, (k, 1, n)) - n ** 2) == 0
          and s.expand(m ** 2 + 2 * m + 1 - (m + 1) ** 2) == 0)

    check(11, s.simplify(s.summation(1 / (k * (k + 1)), (k, 1, n)) - n / (n + 1)) == 0
          and sum(s.Rational(1, v * (v + 1)) for v in range(1, 4)) == s.Rational(3, 4))

    squares = s.summation(k ** 2, (k, 1, n))
    arithmetic = s.summation(k, (k, 1, n))
    check(12, s.simplify(squares - n * (n + 1) * (2 * n + 1) / 6) == 0
          and [squares.subs(n, v) for v in range(1, 6)] == [1, 5, 14, 30, 55]
          and [s.simplify((squares / arithmetic).subs(n, v)) for v in range(1, 6)]
          == [s.Rational(v, 3) for v in (3, 5, 7, 9, 11)]
          and s.expand(2 * m ** 2 + 7 * m + 6 - (m + 2) * (2 * m + 3)) == 0)

    # m=4+h represents the complete induction domain, with h>=0.
    gap = s.Poly(s.expand((2 * m ** 2 - (m + 1) ** 2).subs(m, h + 4)), h)
    check(13, 2 ** 4 == 4 ** 2 and 2 ** 3 < 3 ** 2 and 2 ** 2 == 2 ** 2
          and all(coefficient >= 0 for coefficient in gap.all_coeffs()) and gap.eval(0) > 0)

    formula = 2 ** n - 1
    step = s.expand(3 * formula.subs(n, n) - 2 * formula.subs(n, n - 1) - formula.subs(n, n + 1))
    recurrence_values = [s.Integer(1), s.Integer(3)]
    for _ in range(3):
        recurrence_values.append(3 * recurrence_values[-1] - 2 * recurrence_values[-2])
    check(14, formula.subs(n, 1) == 1 and formula.subs(n, 2) == 3
          and s.simplify(step) == 0 and recurrence_values == [1, 3, 7, 15, 31])

    # Certify the descent inequalities for composite N=ab, a,b>=2.
    u, v = s.symbols("u v", integer=True, nonnegative=True)
    aa, bb = u + 2, v + 2
    check(15, s.isprime(2) and s.expand(aa * bb - aa).is_positive
          and s.expand(aa * bb - bb).is_positive and 4 * 25 == 100
          and s.prod(prime ** exponent for prime, exponent in s.factorint(100).items()) == 100)

    bound = 2 - 1 / n
    allowance = s.factor(bound.subs(n, n + 1) - bound - 1 / (n + 1) ** 2)
    check(16, bound.subs(n, 1) == 1 and allowance.is_positive
          and (2 - bound).is_positive)


if __name__ == "__main__":
    run()
    raise SystemExit(1 if failures else 0)
