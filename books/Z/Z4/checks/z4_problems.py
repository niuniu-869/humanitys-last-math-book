"""Exact checks of all determinate parts; MANUAL is reserved for proofs.

Expected values below are transcribed from answers.md and checked against its
text. Actual values come from symbolic algebra, exhaustive finite domains, or
base/step certificates, never from a numerical sample standing in for a proof.
"""

import re
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = {
    m[1]: m[2]
    for m in re.finditer(
        r"\*\*(Z4-\d+)\*\*\n(.*?)(?=\n\*\*Z4-|\Z)", ANS, re.S
    )
}
failures = 0


def check(pid, condition, detail=""):
    global failures
    ok = bool(condition)
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} {pid}" + (f" {detail}" if detail else ""))


def has(pid, *fragments):
    return all(fragment in BLOCKS[pid] for fragment in fragments)


def choice(pid, actual):
    selected = re.search(r"选 ([ABCD])", BLOCKS[pid]).group(1)
    for label, value in zip("ABCD", actual):
        check(pid, bool(value) == (label == selected), f"选项 {label}")


def manual(pid):
    print(f"MANUAL {pid} 证明文字需人工复核")


def equivalent(left, right):
    return s.satisfiable(s.Xor(left, right)) is False


def run():
    assert set(BLOCKS) == {f"Z4-{i:02d}" for i in range(1, 14)}, "答案题号未完整覆盖"
    manual("Z4-01")

    # Treat the clauses as independent propositions: the question asks for
    # the contraposition rule, not which numerical statements happen to hold.
    p, q, r = s.symbols("p q r")
    target = s.Implies(p, q | r)
    forms = [s.Implies(q & r, p), s.Implies(~p, ~q & ~r),
             s.Implies(~q & ~r, ~p), s.Implies(~q | ~r, ~p)]
    choice("Z4-02", [equivalent(expr, target) for expr in forms])
    parity_truths = []
    for form in forms:
        parity_truths.append(all(bool(form.subs({
            p: a * b % 2 == 0, q: a % 2 == 0, r: b % 2 == 0
        })) for a in range(2) for b in range(2)))
    check("Z4-02", parity_truths == [True, True, True, False], "逐项奇偶含义")

    triples = [(6, 2, 5), (6, 2, 3), (6, 6, 5), (6, 6, 12)]
    counterexamples = []
    for a, b, c in triples:
        premise = s.Mod(b * c, a) == 0
        conclusion = s.Mod(b, a) == 0 or s.Mod(c, a) == 0
        counterexamples.append(premise and not conclusion)
    choice("Z4-03", counterexamples)

    n = s.symbols("n", integer=True, positive=True)
    total, first, last = s.symbols("total first last", real=True)
    # total = a_2 + ... + a_(n+1); the original sum has n constant terms.
    original = 2 * total + s.summation(1, (s.Symbol("k"), 1, n))
    candidates = [2 * total + 1, 2 * (total + first - last) + n,
                  total + 2 * n, 2 * total + n]
    choice("Z4-04", [s.expand(expr - original) == 0 for expr in candidates])

    k = s.symbols("k", integer=True)
    residues = [s.simplify(s.Mod((2 * k + j) ** 2 + (2 * k + j), 2))
                for j in range(2)]
    has_base = any(residue == 1 for residue in residues)
    all_true = all(residue == 1 for residue in residues)
    delta = s.expand((n + 1) ** 2 + n + 1 - (n ** 2 + n))
    step = s.simplify(s.Mod(delta, 2)) == 0
    check("Z4-05", (step, has_base, all_true) == (True, False, False)
          and has("Z4-05", "归纳步成立", "不存在可以奠基", "全称结论为假"))

    x, y = s.symbols("x y", real=True)
    difference = x ** 2 + y ** 2 - 2 * x * y
    # These identities are uniform in arbitrary real x and y.
    p_witness = s.expand(difference.subs(y, x + 1))
    q_counterexample = s.expand(difference.subs(x, y))
    check("Z4-06", p_witness > 0 and q_counterexample <= 0
          and has("Z4-06", "$P$ 真，$Q$ 假", "取 $y=x+1$", "取 $x=y$"), "真假与构造")
    # Quantifier negation is De Morgan's law; verify the Boolean law itself.
    cells = s.symbols("r00 r01 r10 r11")
    rows = [cells[:2], cells[2:]]
    p_form = s.And(*(s.Or(*row) for row in rows))
    not_p = s.Or(*(s.And(*(~cell for cell in row)) for row in rows))
    q_form = s.Or(*(s.And(*(rows[i][j] for i in range(2))) for j in range(2)))
    not_q = s.And(*(s.Or(*(~rows[i][j] for i in range(2))) for j in range(2)))
    check("Z4-06", equivalent(~p_form, not_p) and equivalent(~q_form, not_q)
          and has("Z4-06", r"\neg P:\ \exists x\in\mathbb R\,\forall y",
                  r"\neg Q:\ \forall y\in\mathbb R\,\exists x")
          and BLOCKS["Z4-06"].count(r"x^2+y^2\le2xy") == 2, "否定式")

    roots = s.solveset(s.Abs(x - 1) - 2 * s.Abs(x + 1), x, domain=s.S.Reals)
    expected_roots = s.FiniteSet(-3, -s.Rational(1, 3))
    check("Z4-07", roots == expected_roots
          and roots.intersect(s.Interval(-1, s.oo)) != roots
          and has("Z4-07", r"x=-3", r"x=-\frac13", "不能只设"))

    manual("Z4-08")
    # Supplemental exact check of the expansion used in the written proof.
    check("Z4-08", s.expand((1 + n * x) * (1 + x) - (1 + (n + 1) * x))
          == n * x ** 2, "归纳余项恒等式")

    t, r = s.symbols("t r")
    odd = 1 + s.summation(2, (k, 1, r - 1))
    even = t + s.summation(2, (k, 1, r - 1))
    t_values = s.solve(even - 2 * r, t)
    check("Z4-09", s.expand(odd - (2 * r - 1)) == 0
          and s.expand(even - (t + 2 * r - 2)) == 0 and t_values == [2]
          and has("Z4-09", "$t=2$", "$a_{2r-1}=2r-1$", "$a_{2r}=t+2r-2$"))

    c = s.symbols("c", real=True)
    allowed = s.solve_univariate_inequality(s.Rational(1, 4) <= 1 / (3 + c), c,
                                          relational=False).intersect(s.Interval(0, s.oo))
    best = allowed.sup
    gap = s.expand((2 * n + 2) ** 2 * (3 * n + best)
                   - (2 * n + 1) ** 2 * (3 * n + 3 + best))
    check("Z4-10", best == 1 and gap == n and gap.is_positive
          and has("Z4-10", "$c=1$", r"1/\sqrt{3n+1}",
                  "(2m+2)^2(3m+1)-(2m+1)^2(3m+4)=m>0"), "参数与归纳比较")
    manual("Z4-10")

    a, b = s.symbols("a b")
    solution = s.solve([a + 2 * b - 3, a + b - 1], [a, b])
    residual = s.expand(((a + b * s.sqrt(2)) * (1 + s.sqrt(2)) - 3 - s.sqrt(2)).subs(solution))
    check("Z4-11", solution == {a: -1, b: 2} and residual == 0
          and has("Z4-11", "$(a,b)=(-1,2)$"), "数对及代回检验")
    manual("Z4-11")

    A, B, C = s.symbols("A B C")
    polynomial = s.Poly(A * (k + 2) * (k + 3) + B * (k + 1) * (k + 3)
                        + C * (k + 1) * (k + 2) - k, k)
    coefficients = s.solve(polynomial.all_coeffs(), [A, B, C])
    quadratic, linear, constant = polynomial.all_coeffs()
    check("Z4-12", s.expand(linear - 3 * quadratic) == 2 * A + B - 1
          and s.expand(constant - 2 * quadratic) == 4 * A + B,
          "消元的两条等式")
    term = k / ((k + 1) * (k + 2) * (k + 3))
    actual_sum = s.summation(term, (k, 1, n))
    expected_sum = n * (n + 1) / (4 * (n + 2) * (n + 3))
    H = s.symbols("H")
    boundary_sum = (A * H + B * (H - s.Rational(1, 2) + 1 / (n + 2))
                    + C * (H - s.Rational(1, 2) - s.Rational(1, 3)
                           + 1 / (n + 2) + 1 / (n + 3))).subs(coefficients)
    check("Z4-12", s.expand(boundary_sum).coeff(H) == 0
          and s.simplify(boundary_sum - expected_sum) == 0
          and (-B / 2 - C * (s.Rational(1, 2) + s.Rational(1, 3))).subs(coefficients)
          == s.Rational(1, 4), "公共和抵消与边界项合并")
    check("Z4-12", coefficients == {A: -s.Rational(1, 2), B: 2, C: -s.Rational(3, 2)}
          and s.simplify(actual_sum - expected_sum) == 0
          and expected_sum.subs(n, 1) == s.Rational(1, 24)
          and has("Z4-12", r"A=-\frac12", "B=2", r"C=-\frac32",
                  r"T_n=\frac{n(n+1)}{4(n+2)(n+3)}"))

    def representations(value):
        return [(int((value - 7 * bj) / 4), bj) for bj in range(value // 7 + 1)
                if s.Mod(value - 7 * bj, 4) == 0]

    # Search only locates a candidate. Four consecutive bases and closure
    # under +4 certify the entire infinite tail; the predecessor is checked
    # exhaustively, so it certifies minimality rather than a sampled guess.
    candidate = next(value for value in range(1, 100)
                     if all(representations(value + offset) for offset in range(4)))
    bases = [representations(candidate + offset)[0] for offset in range(4)]
    tail_certificate = all(4 * ai + 7 * bi == candidate + offset
                           for offset, (ai, bi) in enumerate(bases))
    closure = s.expand(4 * (a + 1) + 7 * b - (4 * a + 7 * b)) == 4
    check("Z4-13", candidate == 18 and tail_certificate and closure
          and not representations(candidate - 1)
          and has("Z4-13", "$N=18$", "17 不能表示"), "最小起点与完整尾部证书")
    manual("Z4-13")


if __name__ == "__main__":
    run()
    raise SystemExit(1 if failures else 0)
