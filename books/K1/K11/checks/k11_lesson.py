"""用真值枚举和布尔闭包复核 lesson.md 中例 1--14 的结论。"""
from itertools import product
import sympy as sp
from sympy.logic.boolalg import Equivalent, Implies

p, q, r, s = sp.symbols("p q r s")


def vals(expr, symbols):
    return [i for i, bits in enumerate(product([0, 1], repeat=len(symbols)))
            if bool(expr.subs(dict(zip(symbols, bits))))]


def tautology(expr, symbols):
    return len(vals(expr, symbols)) == 2 ** len(symbols)


def check(n, predicate):
    try:
        assert predicate()
        print(f"PASS 例{n}")
    except Exception as exc:
        print(f"FAIL 例{n}: {exc}")


check(1, lambda: tautology(Equivalent((Implies(p, q) & Implies(p, r)), Implies(p, q & r)), (p, q, r)))

f2 = (p & q) | (p & ~q) | (~p & q & r)
check(2, lambda: all(bool(Equivalent(f2, p | (q & r)).subs(dict(zip((p, q, r), bits))))
                     for bits in product([0, 1], repeat=3)))

check(3, lambda: tautology(Equivalent(~Equivalent(p, q), (p & ~q) | (~p & q)), (p, q)))

f4 = Implies(Implies(p, q) & Implies(q, r), Implies(p, r))
check(4, lambda: tautology(f4, (p, q, r)))

f5 = Implies(Implies(p, q) & q, p)
check(5, lambda: not tautology(f5, (p, q)) and not bool(f5.subs({p: 0, q: 1})))

f6 = (p | q) & ~p & ~q
check(6, lambda: vals(f6, (p, q)) == [])

f7 = Implies(p, q & r)
check(7, lambda: vals(f7, (p, q, r)) == [0, 1, 2, 3, 7])

f8 = Implies(p & q, p | r)
check(8, lambda: tautology(f8, (p, q, r)))

def unary_closure(ops):
    # 枚举一个字母上由给定联结词生成的所有函数，并检查不变量。
    funcs = {(False, True)}
    changed = True
    while changed:
        changed = False
        old = list(funcs)
        for a in old:
            for b in old:
                if "and" in ops:
                    funcs.add(tuple(x and y for x, y in zip(a, b)))
                if "or" in ops:
                    funcs.add(tuple(x or y for x, y in zip(a, b)))
                if "implies" in ops:
                    funcs.add(tuple((not x) or y for x, y in zip(a, b)))
        changed = len(funcs) != len(old)
    return funcs


def not_complete_and_or():
    funcs = unary_closure({"and", "or"})
    return (True, False) not in funcs and all(f[1] for f in funcs)


check(9, not_complete_and_or)

nand = lambda a, b: ~(a & b)
t = nand(p, q)
xor4 = nand(nand(p, t), nand(q, t))
check(10, lambda: tautology(Equivalent(nand(p, p), ~p), (p,)) and
                   tautology(Equivalent(nand(p, q), ~ (p & q)), (p, q)) and
                   tautology(Equivalent(xor4, ~Equivalent(p, q)), (p, q)))

prem11 = [Implies(p, q), Implies(q, r), p]
check(11, lambda: not any(all(bool(x.subs({p: a, q: b, r: c})) for x in prem11) and not c
                          for a, b, c in product([0, 1], repeat=3)))

prem12 = [(p | q) >> r, ~r]
check(12, lambda: not any(bool(((p | q) >> r).subs({p: a, q: b, r: c})) and c == 0
                          and not bool((~p).subs({p: a}))
                          for a, b, c in product([0, 1], repeat=3)))

prem13 = [Implies(p, q), q]
check(13, lambda: any(all(bool(x.subs({p: a, q: b})) for x in prem13) and a == 0
                       for a, b in product([0, 1], repeat=2)))

clauses14 = [p | q, p | ~q, ~p | q, ~p | ~q]
check(14, lambda: not any(all(bool(c.subs({p: a, q: b})) for c in clauses14)
                          for a, b in product([0, 1], repeat=2)))
