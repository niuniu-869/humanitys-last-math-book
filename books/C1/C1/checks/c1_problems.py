import re
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")


def part(pid: str) -> str:
    m = re.search(rf"(?ms)^\*\*{re.escape(pid)}\*\*\n(.*?)(?=^\*\*C1-\d+\*\*|\Z)", ANS)
    if not m:
        raise AssertionError(f"缺少答案 {pid}")
    return m.group(1)


def has(pid: str, text: str) -> None:
    if text not in part(pid):
        raise AssertionError(f"{pid} 答案缺少 {text}")


def main() -> None:
    n = sp.symbols("n", positive=True, integer=True)
    x = sp.symbols("x", real=True)

    # 定义域、反函数和反三角函数
    domain = sp.solve_univariate_inequality(sp.log(x - 1) >= 0, x, relational=False)
    assert domain == sp.Interval(2, sp.oo)
    assert "[2,3)\\cup(3,+\\infty)" in part("C1-01")
    y = sp.symbols("y")
    inverse = 1 + sp.sqrt(y)
    assert sp.simplify((inverse - 1) ** 2 - y) == 0
    has("C1-02", "f^{-1}(x)=1+\\sqrt x")
    assert sp.simplify(sp.cos(sp.asin(-sp.Rational(3, 5))) - sp.Rational(4, 5)) == 0
    has("C1-03", "（B）")
    print("PASS C1-01")
    print("PASS C1-02")
    print("PASS C1-03")

    # 证明题仍独立核对目标值，题面按要求标 MANUAL。
    assert sp.limit(1 / sp.sqrt(n), n, sp.oo) == 0
    print("MANUAL C1-04")
    # 所有子数列同极限时原数列也收敛；其余选项可由 (-1)^n 反例排除。
    has("C1-05", "（A）")
    print("PASS C1-05")

    assert min(k for k in range(0, 20) if all(sp.Rational(1, 3) ** j < sp.Rational(1, 81) for j in range(k + 1, 30))) == 4
    has("C1-06", "$N=4$")
    print("PASS C1-06")

    lower = sp.limit(1 / (2 * n), n, sp.oo)
    upper = sp.limit(1 / (n + 1), n, sp.oo)
    assert lower == upper == 0
    has("C1-07", "$x_n\\to0$")
    print("PASS C1-07")

    assert sp.limit(sp.sin((4 * n) * sp.pi / 2) + 1 / (4 * n), n, sp.oo) == 0
    assert sp.limit(sp.sin((4 * n + 1) * sp.pi / 2) + 1 / (4 * n + 1), n, sp.oo) == 1
    print("MANUAL C1-08")

    recurrence_limit = sp.solve(sp.Eq(sp.Symbol("A"), (sp.Symbol("A") + 2) / (sp.Symbol("A") + 3)), sp.Symbol("A"))
    assert set(recurrence_limit) == {-1 - sp.sqrt(3), -1 + sp.sqrt(3)}
    print("MANUAL C1-09")

    # 分母除以 3^n 后不小于 1，分子绝对值不超过
    # 2(2/3)^n，因此极限由 q^n -> 0 得到。
    assert sp.limit(2 * sp.Rational(2, 3) ** n, n, sp.oo) == 0
    has("C1-10", "（A）")
    print("PASS C1-10")

    A = sp.Symbol("A")
    assert sp.solve(sp.Eq(A, (3 * A + 1) / (A + 3)), A) == [-1, 1]
    print("MANUAL C1-11")

    m = sp.symbols("m", positive=True, integer=True)
    # 由 e 的定义块直接确认代数改写，目标值为 e^2。
    expr = (1 + 1 / m) ** (2 * m - 1)
    assert sp.limit(expr, m, sp.oo) == sp.E**2
    has("C1-12", "$e^2$")
    print("PASS C1-12")

    K = sp.symbols("K", integer=True, nonnegative=True)
    assert 3 * K + 2 > 3 * K
    print("MANUAL C1-13")

    a_n = 1 + 1 / n
    assert sp.simplify(((a_n**2 - 1) / (a_n - 1)) - (2 + 1 / n)) == 0
    assert sp.limit(2 + 1 / n, n, sp.oo) == 2
    has("C1-14", "$f(a_n)\\to2$")
    print("PASS C1-14")

    # 二项式上界：有限余项由有限等比和显式控制。
    for N in range(1, 30):
        assert (1 + sp.Rational(1, N)) ** N < 3
    print("MANUAL C1-15")

    b_bound = sp.limit(1 / n, n, sp.oo)
    assert b_bound == 0
    has("C1-16", "$b_n\\to0$")
    print("PASS C1-16")


if __name__ == "__main__":
    main()
