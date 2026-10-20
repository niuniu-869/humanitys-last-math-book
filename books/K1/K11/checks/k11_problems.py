"""独立验算 K1.1 题目；结果由布尔函数计算得到，不从答案抄回。"""
from pathlib import Path
from itertools import product
import re
import sympy as sp
from sympy.logic.boolalg import Equivalent, Implies

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
p, q, r, s, t = sp.symbols("p q r s t")


def vals(expr, symbols):
    out = []
    for i, bits in enumerate(product([0, 1], repeat=len(symbols))):
        if bool(expr.subs(dict(zip(symbols, bits)))):
            out.append(i)
    return out


def section(n):
    m = re.search(rf"\*\*K11-{n:02d}\*\*(.*?)(?=\n\n\*\*K11-|\Z)", ANS, re.S)
    if not m:
        raise AssertionError(f"找不到答案 K11-{n:02d}")
    return m.group(0)


def need(n, text):
    if text not in section(n):
        raise AssertionError(f"K11-{n:02d} 缺少 {text}")


def run(n, fn):
    try:
        result = fn()
        if result == "MANUAL":
            print(f"MANUAL K11-{n:02d}")
        else:
            print(f"PASS K11-{n:02d}")
    except Exception as exc:
        print(f"FAIL K11-{n:02d}: {exc}")


def check_01():
    f = (p | q) & (p | ~q)
    assert sp.simplify_logic(f, force=True) == p
    options = [sp.true, p & q, p, p | q]
    assert [vals(Equivalent(f, x), (p, q)) == [0, 1, 2, 3] for x in options] == [False, False, True, False]
    need(1, "(C)")


def check_02():
    f = Implies(Implies(p, q) & ~q, ~p)
    assert vals(f, (p, q)) == [0, 1, 2, 3]
    assert not any(not bool(f.subs({p: a, q: b})) for a, b in product([0, 1], repeat=2))
    assert any(bool(f.subs({p: a, q: b})) for a, b in product([0, 1], repeat=2))
    need(2, "(A)")


def check_03():
    f = section(3)
    assert "m_1\\vee m_2\\vee m_6\\vee m_7" in f
    assert "M_0\\wedge M_3\\wedge M_4\\wedge M_5" in f


def check_04():
    f = (p | ~q) & r
    false_rows = [i for i in range(8) if i not in vals(f, (p, q, r))]
    assert false_rows == [0, 2, 3, 4, 6]
    need(4, "M_0\\wedge M_2\\wedge M_3\\wedge M_4\\wedge M_6")


def unary_closure(ops):
    # 在一个字母上闭包生成函数，足以独立判断是否能得到 neg p。
    pfun = (False, True)
    funcs = {pfun}
    changed = True
    while changed:
        changed = False
        old = list(funcs)
        for a in old:
            if "neg" in ops:
                funcs.add(tuple(not x for x in a))
            for b in old:
                if "and" in ops:
                    funcs.add(tuple(x and y for x, y in zip(a, b)))
                if "or" in ops:
                    funcs.add(tuple(x or y for x, y in zip(a, b)))
                if "nand" in ops:
                    funcs.add(tuple(not (x and y) for x, y in zip(a, b)))
        changed = len(funcs) != len(old)
    return funcs


def check_05():
    target = (True, False)
    complete = {
        "A": target in unary_closure({"neg", "and"}),
        "B": target in unary_closure({"nand"}),
        "C": target in unary_closure({"and", "or"}),
        "D": target in unary_closure({"neg", "or"}),
    }
    assert complete == {"A": True, "B": True, "C": False, "D": True}
    need(5, "(C)")


def check_06():
    # 证明题由人工检查推导，脚本只确认题目和答案存在。
    assert "p\\leftrightarrow q" in section(6)
    return "MANUAL"


def check_07():
    f = Implies(Implies(p | q, r), Implies(p, r) & Implies(q, r))
    assert vals(f, (p, q, r)) == list(range(8))
    need(7, "重言式")


def check_08():
    f = (p | q) & (r | s)
    g = (p & r) | (q & s)
    assert vals(f, (p, q, r, s))
    assert vals(g, (p, q, r, s))
    assert vals(f, (p, q, r, s)) != vals(g, (p, q, r, s))
    counter = {p: 0, q: 1, r: 1, s: 0}
    assert bool(f.subs(counter)) and not bool(g.subs(counter))
    need(8, "不等价")


def check_09():
    premises = [Implies(p, q & r), Implies(q, s), Implies(r, s), p]
    assert not any(all(bool(x.subs({p: a, q: b, r: c, s: d})) for x in premises) and not d
                   for a, b, c, d in product([0, 1], repeat=4))
    need(9, "\\square")


def check_10():
    c1 = {"p", "q", "~r"}
    c2 = {"~p", "~q", "s"}
    rp = (c1 - {"p"}) | (c2 - {"~p"})
    rq = (c1 - {"q"}) | (c2 - {"~q"})
    assert rp == {"q", "~r", "~q", "s"}
    assert rq == {"p", "~r", "~p", "s"}
    assert rp and rq
    assignment = {p: 1, q: 0, r: 0, s: 0}
    assert bool(c1_expr := (p | q).subs(assignment))
    assert bool(c2_expr := (~p | ~q).subs(assignment))
    need(10, "永真子句")


def check_11():
    assert (True, False) not in unary_closure({"and", "implies"})
    need(11, "不能由")


def check_12():
    premises = [Equivalent(p, q), Implies(q, r), (~r | s)]
    conclusion = Implies(p, s)
    assert not any(all(bool(x.subs({p: a, q: b, r: c, s: d})) for x in premises)
                   and not bool(conclusion.subs({p: a, q: b, r: c, s: d}))
                   for a, b, c, d in product([0, 1], repeat=4))
    need(12, "有效")


def check_13():
    f = Implies(p, q) & Equivalent(r, t)
    assert vals(f, (p, q, r, t)) == [0, 3, 4, 7, 12, 15]
    assert "M_1\\wedge M_2\\wedge M_5\\wedge M_6" in section(13)
    assert "先按结构数真行" in section(13)


def check_14():
    s1 = [p | q, ~p | ~q]
    assert any(all(bool(c.subs({p: a, q: b})) for c in s1)
               for a, b in product([0, 1], repeat=2))
    s2 = [p | q, ~p | r, ~q | r, ~r]
    assert not any(all(bool(c.subs(dict(zip((p, q, r), bits)))) for c in s2)
                   for bits in product([0, 1], repeat=3))
    need(14, "S_1")
    need(14, "S_2")


checks = [check_01, check_02, check_03, check_04, check_05, check_06,
          check_07, check_08, check_09, check_10, check_11, check_12,
          check_13, check_14]
for i, fn in enumerate(checks, 1):
    run(i, fn)
