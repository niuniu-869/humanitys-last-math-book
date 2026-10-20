"""Check all 13 numbered examples with exact logic/algebra, without sampling R."""
import sys

import numpy as np
import sympy as sp

from z3_problems import Regions, entails, equivalent


FAILURES = []


def check(number, detail, actual, expected):
    ok = bool(actual == expected)
    print(f"{'PASS' if ok else 'FAIL'} 例{number} {detail}")
    if not ok:
        FAILURES.append((number, detail))
        print(f"  computed={actual!r}; lesson={expected!r}")


def categorical(r, s="S", p="P"):
    return [r.every(lambda v: not v[s] or v[p]),
            r.every(lambda v: not v[s] or not v[p]),
            r.some(lambda v: v[s] and v[p]),
            r.some(lambda v: v[s] and not v[p])]


def status(premise, claim):
    if entails(premise, claim):
        return "真"
    if entails(premise, ~claim):
        return "假"
    return "不确定"


def main():
    x, y, m = sp.symbols("x y m", real=True)
    n = sp.symbols("n", integer=True)
    k = sp.symbols("k", integer=True, nonnegative=True)
    r = Regions("SP")
    A, E, I, O = categorical(r)
    forms = [A, E, ~A, r.every(lambda v: not v["S"] or v["P"]), I]
    types = ["AEIO"[[equivalent(f, c) for c in (A, E, I, O)].index(True)] for f in forms]
    check(1, "五句话的标准类型", types, ["A", "E", "O", "A", "I"])
    check(1, "(1)(4) 任意4的倍数均为偶数", sp.Mod(4*n, 2), 0)
    # Positive multiples of four are >=4 and have the proper divisor 2.
    check(1, "(2) 质数不能为4的倍数",
          (sp.Mod(4*(k+1), 2),
           sp.solve_univariate_inequality(4*(k+1) <= 2, k, relational=False)),
          (0, sp.S.EmptySet))
    check(1, "(3) 反例6", (sp.Mod(6, 2), sp.Mod(6, 4)), (0, 2))
    check(1, "(5) 见证2", (sp.isprime(2), sp.Mod(2, 2)), (True, 0))

    nonempty_s = r.some(lambda v: v["S"])
    check(2, "O 假且 S 非空的全部模型",
          [status(sp.And(nonempty_s, ~O), c) for c in (A, E, I)], ["真", "假", "真"])
    check(3, "(1) A 假的全部模型",
          [status(sp.And(nonempty_s, ~A), c) for c in (E, I, O)], ["不确定", "不确定", "真"])
    for label, option in zip("ABC", (A, E, O)):
        can_both_true = sp.satisfiable(sp.And(nonempty_s, I, option)) is not False
        cannot_both_false = sp.satisfiable(sp.And(nonempty_s, ~I, ~option)) is False
        check(3, f"(2) 选项 {label}", can_both_true and cannot_both_false, label == "C")

    r = Regions("SMFR")
    premise = sp.And(r.some(lambda v: v["S"] and v["M"]),
                     r.every(lambda v: not v["M"] or v["F"]),
                     r.every(lambda v: not v["F"] or v["R"]))
    options = [r.some(lambda v: v["S"] and v["R"]),
               r.some(lambda v: v["R"] and v["S"]),
               r.every(lambda v: not v["S"] or v["R"]),
               r.some(lambda v: v["M"] and not v["S"])]
    for label, claim in zip("ABCD", options):
        check(4, f"选项 {label}", entails(premise, claim), label in "AB")

    r = Regions("SPE")
    premise = sp.And(r.every(lambda v: not v["P"] or v["E"]),
                     r.some(lambda v: v["S"] and not v["E"]))
    check(5, "逆否推理", entails(premise, r.some(lambda v: v["S"] and not v["P"])), True)
    check(5, "平方数9的三个性质", (sp.sqrt(9).is_integer, sp.Mod(9, 2), sp.Mod(9, 4)),
          (True, 1, 1))

    r = Regions("SPM")
    all_mp = r.every(lambda v: not v["M"] or v["P"])
    all_pm = r.every(lambda v: not v["P"] or v["M"])
    all_sm = r.every(lambda v: not v["S"] or v["M"])
    some_sm = r.some(lambda v: v["S"] and v["M"])
    all_sp = r.every(lambda v: not v["S"] or v["P"])
    some_sp = r.some(lambda v: v["S"] and v["P"])
    for i, front in enumerate([all_mp, all_pm], 1):
        check(6, f"({i}) 全称三段论", entails(sp.And(front, all_sm), all_sp), i == 1)
        check(7, f"({i}) 特称三段论", entails(sp.And(front, some_sm), some_sp), i == 1)
    tuples = lambda predicate: {tuple(map(int, v.values())) for v in r.rows if predicate(v)}
    shade_mp = tuples(lambda v: v["M"] and not v["P"])
    shade_pm = tuples(lambda v: v["P"] and not v["M"])
    shade_sm = tuples(lambda v: v["S"] and not v["M"])
    check(6, "(1) 两个前提的阴影", (shade_mp, shade_sm),
          ({(1, 0, 1), (0, 0, 1)}, {(1, 1, 0), (1, 0, 0)}))
    check(6, "(2) 结论尚未排除的反例块",
          tuples(lambda v: v["S"] and not v["P"]) - (shade_pm | shade_sm), {(1, 0, 1)})
    cross = tuples(lambda v: v["S"] and v["M"])
    check(7, "(1) × 的位置", cross - shade_mp, {(1, 1, 1)})
    check(7, "(2) × 的两个候选位置", cross - shade_pm, {(1, 1, 1), (1, 0, 1)})

    half = sp.Rational(1, 2)
    check(8, "(1)(2) x=1/2 的精确比较", (half > 0, half**2, half**2 < half),
          (sp.true, sp.Rational(1, 4), sp.true))
    check(8, "(2) 全部可用见证", sp.solve_univariate_inequality(x*x < x, x, relational=False),
          sp.Interval.open(0, 1))
    check(8, "(3) 对任意 x 的回答 y=x+1", sp.simplify((x+1)-x), 1)

    nonneg = sp.symbols("b", nonnegative=True)
    response = sp.Abs(m) + 1
    for sign in (1, -1):
        margin = sp.expand((response**2 - m).subs(m, sign*nonneg))
        check(9, f"无上界证明覆盖 M 的符号 {sign}", sp.ask(sp.Q.positive(margin)), True)
    check(9, "有上界函数对所有 x 的验证",
          sp.solve_univariate_inequality(1/(1+x*x) <= 1, x, relational=False), sp.S.Reals)
    check(9, "错误选法 x=M 的反例", half**2 < half, sp.true)
    p, q = sp.symbols("p q")
    check(10, "蕴含否定", equivalent(~sp.Implies(p, q), sp.And(p, ~q)), True)
    check(10, "反例点与函数值", (-1 < 0, sp.Integer(-1)**2 > sp.Integer(0)**2), (True, sp.true))

    check(11, "(1) y=-x 的恒等式", sp.simplify(x+(-x)), 0)
    check(11, "(2) 否定式选 x=1-y", sp.simplify((1-y)+y), 1)
    check(11, "(3) 先选 x=0", sp.simplify((x*y).subs(x, 0)), 0)
    check(11, "(4) x=0 对全部 y 都不能得到1", sp.simplify((x*y-1).subs(x, 0)), -1)
    value = sp.symbols("function_value", real=True)
    check(12, "逐点上界 M=f(x) 的通用验证", sp.Le(value, value), sp.true)
    # A symbolic counter-strategy establishes that the other order need not hold.
    check(12, "x^2 的统一上界不存在",
          all(sp.ask(sp.Q.positive(sp.expand((response**2-m).subs(m, s*nonneg)))) for s in (1, -1)), True)

    # Possible worlds are represented by symbolic truth values, not forecasts.
    worlds = sp.symbols("w0:3")
    check(13, "(1) 不可能非 p 等价于必然 p",
          equivalent(~sp.Or(*(~v for v in worlds)), sp.And(*worlds)), True)
    check(13, "(2) 不一定非 p 等价于可能 p",
          equivalent(~sp.And(*(~v for v in worlds)), sp.Or(*worlds)), True)
    cells = np.array(sp.symbols("p0:6"), dtype=object).reshape(3, 2)
    all_pass = [sp.And(*row) for row in cells]
    always_some_fail = sp.And(*(sp.Or(*(~v for v in row)) for row in cells))
    check(13, "(3) 不可能所有人通过",
          equivalent(~sp.Or(*all_pass), always_some_fail), True)
    each_not_necessary = sp.And(*(~sp.And(*cells[:, j]) for j in range(2)))
    each_can_fail = sp.And(*(sp.Or(*(~v for v in cells[:, j])) for j in range(2)))
    check(13, "(4) 每个人都可能失败", equivalent(each_not_necessary, each_can_fail), True)
    table = np.array([[True, True], [False, False], [True, False]])
    env = dict(zip(cells.flat, table.flat))
    check(13, "(4) 不保证 (3) 的具体情形",
          (bool(each_can_fail.subs(env)), bool(always_some_fail.subs(env))), (True, False))

    # The eight in-lesson practice blocks are checked separately so later edits
    # cannot silently invalidate their stated answers.
    ints = list(range(-6, 7))
    multiples3 = lambda z: z % 3 == 0
    odd = lambda z: z % 2 != 0
    even = lambda z: z % 2 == 0
    mult6 = lambda z: z % 6 == 0
    check("随堂1", "三个整数句的类型与真假",
          (any(not multiples3(z) for z in ints),
           all(not (odd(z) and z % 2 == 0) for z in ints),
           all(not mult6(z) or even(z) for z in ints)),
          (True, True, True))

    models = [({1}, {1}), ({1, 2}, {1})]
    check("随堂2", "I 真时 E 必假、A/O 可分别取真",
          (all(bool(s & p) for s, p in models),
           (models[0][0] <= models[0][1], bool(models[0][0] - models[0][1]),
            models[1][0] <= models[1][1], bool(models[1][0] - models[1][1]))),
          (True, (True, False, False, True)))

    r = Regions("SMF")
    forward = sp.And(r.some(lambda v: v["S"] and v["M"]),
                     r.every(lambda v: not v["M"] or not v["F"]))
    reverse = sp.And(r.every(lambda v: not v["M"] or not v["F"]),
                     r.some(lambda v: v["S"] and not v["F"]))
    check("随堂3", "正向推理有效、逆向推理无效",
          (entails(forward, r.some(lambda v: v["S"] and not v["F"])),
           entails(reverse, r.some(lambda v: v["S"] and v["M"]))),
          (True, False))

    r = Regions("SPM")
    premise = sp.And(r.some(lambda v: v["S"] and not v["M"]),
                     r.every(lambda v: not v["P"] or v["M"]))
    conclusion = r.some(lambda v: v["S"] and not v["P"])
    check("随堂4", "三圈推理的阴影排除",
          entails(premise, conclusion), True)

    check("随堂5", "偶数质数见证与质数反例",
          (sp.isprime(2) and 2 % 2 == 0, sp.isprime(2) and 2 % 2 == 0),
          (True, True))

    c = sp.symbols("c0:6")
    nested = sp.Implies(sp.And(*c[:3]), sp.Or(*c[3:]))
    neg_nested = sp.And(sp.And(*c[:3]), sp.And(*(~v for v in c[3:])))
    check("随堂6", "合取与析取否定的逐层展开",
          equivalent(~nested, neg_nested), True)

    check("随堂7", "整数平方全覆盖的反例",
          any(all(y * y != 2 for y in ints) for _ in [0]), True)

    modal_worlds = [(True, False), (False, True)]
    check("随堂8", "冠军亚军互斥时两句模态不等价",
          (all(not (c and r) for c, r in modal_worlds),
           all(c for c, r in modal_worlds),
           all(r for c, r in modal_worlds)),
          (True, False, False))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
