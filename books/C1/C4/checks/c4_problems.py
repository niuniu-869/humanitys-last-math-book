"""Independent symbolic checks for C.4 problems."""
from pathlib import Path
import re
import sympy as sp

x, h, a, b, p, n = sp.symbols("x h a b p n", real=True)
answers = Path(__file__).resolve().parents[1] / "answers.md"
answer_text = answers.read_text(encoding="utf-8")


def block(qid):
    m = re.search(rf"\*\*{qid}\*\*(.*?)(?=\n\*\*C4-|\Z)", answer_text, re.S)
    return m.group(1) if m else ""


def check(qid, condition):
    ok = bool(condition)
    print(f"{'PASS' if ok else 'FAIL'} {qid}")


f = x**3 - 2*x + 1
check("C4-01", sp.simplify(sp.limit((f.subs(x, 1+h)-f.subs(x, 1))/h, h, 0) - 1) == 0)

# A representative differentiable function makes the reverse coefficient
# calculation concrete: the given limit is 3*f'(3).
fr = 2*(x-3) + 5
q02 = sp.limit((fr.subs(x, 3+2*h)-fr.subs(x, 3-h))/h, h, 0)
options02 = [1, 2, 3, 6]
option_hits02 = [q02 == value for value in options02[:3]] + [False]
check("C4-02", q02 == 6 and sum([sp.Rational(6, 3) == value for value in options02]) == 1 and "(B)" in block("C4-02"))

curve = x**3 - 3*x
roots03 = sp.solve(sp.Eq(sp.diff(curve, x), 0), x)
check("C4-03", set(roots03) == {-1, 1} and {curve.subs(x, r) for r in roots03} == {-2, 2})

right04 = sp.limit((a*h + h**2)/h, h, 0, dir="+")
left04 = sp.limit((-a*h - h**2)/h, h, 0, dir="-")
check("C4-04", right04 == a and left04 == -a and sp.solve(sp.Eq(right04, left04), a) == [0] and "二阶导数不存在" in block("C4-04"))

# For f(0)=0, f'(0)=2 and continuous g with g(0)=3, the direct quotient is 6.
f5 = 2*x
g5 = 3 + x**2
q05 = sp.limit((f5*g5 - f5.subs(x, 0)*g5.subs(x, 0))/x, x, 0)
# Evaluate each claim with an explicit counterexample where needed.
qa = sp.limit(((1+h)*sp.Abs(h)-1*0)/h, h, 0, dir="+")
qa_left = sp.limit(((1+h)*sp.Abs(h)-1*0)/h, h, 0, dir="-")
qc = sp.limit((sp.Abs(h)-0)/h, h, 0, dir="+")
qc_left = sp.limit((sp.Abs(h)-0)/h, h, 0, dir="-")
qd = sp.limit(sp.Abs(h)/h, h, 0, dir="+")
qd_left = sp.limit(sp.Abs(h)/h, h, 0, dir="-")
option_hits05 = [qa == qa_left, q05 == 6, qc == qc_left, qd == qd_left]
check("C4-05", sum(option_hits05) == 1 and option_hits05[1] and "(B)" in block("C4-05"))

left_value = sp.sqrt(3)
right_value = b
left_derivative = 1/(2*sp.sqrt(3)) + a
right_derivative = 1
sol06 = sp.solve([sp.Eq(left_value, right_value), sp.Eq(left_derivative, right_derivative)], [a, b], dict=True)[0]
options06 = [
    (1-1/(2*sp.sqrt(3)), sp.sqrt(3)),
    (1+1/(2*sp.sqrt(3)), sp.sqrt(3)),
    (1-1/(2*sp.sqrt(3)), 0),
    (0, sp.sqrt(3)),
]
option_hits06 = [sp.simplify(av - (1-1/(2*sp.sqrt(3)))) == 0 and bv == sp.sqrt(3) for av, bv in options06]
check("C4-06", sol06 == {a: 1-1/(2*sp.sqrt(3)), b: sp.sqrt(3)} and sum(option_hits06) == 1 and option_hits06[0] and "(A)" in block("C4-06"))

print("MANUAL C4-07")

q08 = sp.simplify(sp.log(a)-sp.log(b))
check("C4-08", sp.expand_log(sp.log(a/b), force=True) == q08 and "\\ln a-\\ln b" in block("C4-08"))

f9 = 1 + 2*x
g9 = 3 + sp.Abs(x)
right9 = sp.limit((f9.subs(x, h)*g9.subs(x, h)-f9.subs(x, 0)*g9.subs(x, 0))/h, h, 0, dir="+")
left9 = sp.limit((f9.subs(x, h)*g9.subs(x, h)-f9.subs(x, 0)*g9.subs(x, 0))/h, h, 0, dir="-")
check("C4-09", right9 == 7 and left9 == 5 and "不必然成立" in block("C4-09"))

finv = x**3 + x
check("C4-10", sp.diff(finv, x) == 3*x**2 + 1 and finv.subs(x, 1) == 2 and 1/sp.diff(finv, x).subs(x, 1) == sp.Rational(1, 4))

print("MANUAL C4-11")

y12 = x**2 * sp.exp(x)
rec12 = sp.diff(y12, x, 3) - 3*sp.diff(y12, x, 2) + 3*sp.diff(y12, x) - y12
check("C4-12", sp.simplify(rec12) == 0 and sp.simplify(sp.diff(y12, x, 5)-sp.exp(x)*(x**2+10*x+20)) == 0 and "x^2+10x+20" in block("C4-12").replace(" ", ""))

F13 = (x**2-4)/(x-2)
check("C4-13", sp.limit(F13, x, 2) == 4 and sp.limit((F13-4)/(x-2), x, 2) == 1 and "a=4" in block("C4-13"))

H14 = x**2*sp.sin(1/x)
continuity14 = sp.limit(H14, x, 0) == 0
diff14 = sp.limit(H14/x, x, 0) == 0
deriv14 = 2*x*sp.sin(1/x)-sp.cos(1/x)
seq1 = -sp.cos(0)
seq2 = -sp.cos(sp.pi)
check("C4-14", continuity14 and diff14 and seq1 == -1 and seq2 == 1 and "不连续" in block("C4-14"))

q15 = sp.limit((sp.log(1+2*h)-sp.log(1-h))/h, h, 0)
check("C4-15", q15 == 3)

results16 = []
for pv in [sp.Rational(1, 2), 1, sp.Rational(3, 2), 2]:
    dq = sp.Abs(h)**pv/h
    results16.append(sp.limit(dq, h, 0) == 0)
check("C4-16", results16 == [False, False, True, True])
