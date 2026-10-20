import sympy as sp


def main() -> None:
    x = sp.symbols("x", real=True)
    n, k = sp.symbols("n k", positive=True, integer=True)

    # 例 1
    assert sp.solve_univariate_inequality(4 - x**2 >= 0, x, relational=False) == sp.Interval(-2, 2)
    assert sp.solve_univariate_inequality(x + 1 > 0, x, relational=False) == sp.Interval.open(-1, sp.oo)
    print("PASS 例1")

    # 例 2
    assert sp.simplify(sp.Rational(3, 100) * 3000) == 90
    assert sp.simplify(90 + sp.Rational(1, 10) * (5000 - 3000)) == 290
    print("PASS 例2")

    # 例 3
    z = sp.symbols("z", real=True)
    assert sp.solve_univariate_inequality(abs(z) / (1 + z**2) <= sp.Rational(1, 2), z, relational=False) == sp.S.Reals
    assert 1 / sp.Rational(1, 2) > 1
    print("PASS 例3")

    # 例 4
    assert sp.factor(x**2 + x - 6) == (x - 2) * (x + 3)
    assert sp.Interval.open(1, 3).contains(sp.Rational(2))
    assert not sp.Interval.open(1, 3).contains(sp.Rational(3))
    print("PASS 例4")

    # 例 5
    y = sp.symbols("y")
    inv = sp.solve(sp.Eq(y, (2 * x + 1) / (x - 1)), x)[0]
    assert sp.simplify(inv - (y + 1) / (y - 2)) == 0
    print("PASS 例5")

    # 例 6
    assert sp.simplify(sp.sin(sp.acos(-sp.Rational(1, 3))) - 2 * sp.sqrt(2) / 3) == 0
    assert sp.asin(sp.sin(5 * sp.pi / 6)) == sp.pi / 6
    print("PASS 例6")

    # 例 7
    assert sp.simplify((sp.Rational(1, 2) + sp.Rational(1, 3)) / (1 - sp.Rational(1, 2) * sp.Rational(1, 3))) == 1
    print("PASS 例7")

    # 例 8
    f = 1 / (1 - x)
    assert sp.simplify(1 / (1 - f) - (x - 1) / x) == 0
    print("PASS 例8")

    # 例 9
    assert sp.sqrt(sp.Rational(25, 9) - 1) == sp.Rational(4, 3)
    assert sp.Rational(1, 1) / sp.Rational(4, 5) == sp.Rational(5, 4)
    print("PASS 例9")

    # 例 10
    s = sp.symbols("s")
    assert sp.simplify(1 / (1 - s) + 1 / (1 + s) - 2 / (1 - s**2)) == 0
    print("PASS 例10")

    # 例 11
    assert sp.limit((3 * n + 1) / (n + 2), n, sp.oo) == 3
    print("PASS 例11")

    # 例 12
    assert sp.limit(sp.sqrt(n + 1) - sp.sqrt(n), n, sp.oo) == 0
    print("PASS 例12")

    # 例 13
    assert sp.limit(sp.Rational(2, 3) ** n, n, sp.oo) == 0
    print("PASS 例13")

    # 例 14
    assert sp.limit(1 - sp.Rational(9, 10) ** n, n, sp.oo) == 1
    assert sp.Rational(9, 10) ** 66 < sp.Rational(1, 1000)
    assert sp.Rational(9, 10) ** 65 > sp.Rational(1, 1000)
    print("PASS 例14")

    # 例 15
    assert (-1) ** (2 * k) == 1
    assert (-1) ** (2 * k + 1) == -1
    print("PASS 例15")

    # 例 16
    assert sp.limit((2 * k) / (2 * k + 1), k, sp.oo) == 1
    assert sp.limit(-(2 * k - 1) / (2 * k), k, sp.oo) == -1
    print("PASS 例16")

    # 例 17
    assert ((-1) ** n) ** 2 == 1
    print("PASS 例17")

    # 例 18
    assert sp.limit((2 * n**2 + 3 * n + 1) / (5 * n**2 - n + 4), n, sp.oo) == sp.Rational(2, 5)
    print("PASS 例18")

    # 例 19
    assert sp.limit(n * (sp.sqrt(n**2 + 1) - n), n, sp.oo) == sp.Rational(1, 2)
    print("PASS 例19")

    # 例 20
    assert sp.summation(1 / (k * (k + 1)), (k, 1, n)) == 1 - 1 / (n + 1)
    assert sp.limit((2**n + 3**n) / (2 ** (n + 1) + 3 ** (n + 1)), n, sp.oo) == sp.Rational(1, 3)
    print("PASS 例20")

    # 例 21
    lower = sp.Rational(1, 2)
    upper = sp.limit(n * (n + 1) / (2 * (n**2 + 1)), n, sp.oo)
    assert upper == lower
    print("PASS 例21")

    # 例 22
    for N in range(1, 20):
        value = float((2**N + 3**N + 5**N) ** (1 / N))
        assert 5 <= value <= 5 * 3 ** (1 / N)
    print("PASS 例22")

    # 例 23
    assert sp.limit(n ** (sp.Rational(1, 1) / n), n, sp.oo) == 1
    print("PASS 例23")

    # 例 24
    A = sp.symbols("A")
    assert sp.solve(A**2 - A - 2, A) == [-1, 2]
    assert sp.sqrt(2 + 2) == 2
    print("PASS 例24")

    # 例 25
    assert sp.solve(sp.Eq(A, (A + 2 / A) / 2), A) == [-sp.sqrt(2), sp.sqrt(2)]
    print("PASS 例25")

    # 例 26
    assert sp.limit((1 - 1 / n) ** n, n, sp.oo) == sp.exp(-1)
    print("PASS 例26")

    # 例 27
    assert sp.N(10000 * sp.exp(sp.Rational(6, 100)), 8) > 10618
    assert sp.N(10000 * sp.exp(sp.Rational(6, 100)), 8) < 10619
    print("PASS 例27")


if __name__ == "__main__":
    main()
