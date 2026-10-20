"""独立重算 C.18 题目，并把结果与 answers.md 中的结论对照。"""

from pathlib import Path
import re
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = {
    m[1]: m[2]
    for m in re.finditer(r"(?ms)^\*\*(C18-\d+)\*\*\n(.*?)(?=^\*\*C18-\d+\*\*|\Z)", ANSWERS)
}

failures = 0
x, t = s.symbols("x t", real=True)
C1, C2, C3 = s.symbols("C_1 C_2 C_3")


def eq(left, right):
    return s.simplify(left - right) == 0


def report(pid, condition, detail=""):
    global failures
    ok = bool(condition)
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} {pid}" + (f" {detail}" if detail else ""))


def answer_has(pid, *claims):
    return all(claim in BLOCKS[pid] for claim in claims)


def selected(pid):
    match = re.search(r"\*\*答案：\*\*\s*\(([A-D])\)", BLOCKS[pid])
    return match.group(1) if match else "?"


def choice(pid, truth):
    picked = selected(pid)
    for letter, actual in zip("ABCD", truth):
        report(pid, bool(actual) == (letter == picked), f"选项 {letter}: {bool(actual)}")
    report(pid, sum(bool(v) for v in truth) == 1, f"答案 ({picked})")


# C18-01: integrate three times and impose the three initial values.
y01 = s.Rational(1, 2) * x**4 - s.Rational(1, 3) * x**3 + x**2 + 1
report("C18-01", eq(s.diff(y01, x, 3), 12*x - 2)
       and y01.subs(x, 0) == 1
       and s.diff(y01, x).subs(x, 0) == 0
       and s.diff(y01, x, 2).subs(x, 0) == 2
       and answer_has("C18-01", r"\frac12x^4", r"-\frac13x^3"))

# C18-02: use the missing-x reduction and check the selected hyperbolic branch.
y02 = s.sinh(x)
v02 = s.diff(y02, x)
report("C18-02", eq(s.diff(y02, x, 2), y02)
       and y02.subs(x, 0) == 0 and v02.subs(x, 0) == 1
       and eq(v02, s.sqrt(1 + y02**2))
       and answer_has("C18-02", r"\sinh x", r"v\dfrac{\mathrm{d}v}{\mathrm{d}y"))

# C18-03: derive the repeated characteristic root and test each proposed family.
r = s.symbols("r")
characteristic = s.expand(r**3 - 3*r**2 + 3*r - 1)
basis = [s.exp(x), x*s.exp(x), x**2*s.exp(x), x**3*s.exp(x)]
residual = lambda z: s.simplify(s.diff(z, x, 3) - 3*s.diff(z, x, 2) + 3*s.diff(z, x) - z)
option_families = [
    [basis[0], basis[1]],
    [basis[0], basis[1], basis[2]],
    [basis[0], basis[0], basis[1]],
    [basis[0], basis[1], basis[3]],
]
family_truth = []
for family in option_families:
    solves = all(eq(residual(z), 0) for z in family)
    if len(family) == 3:
        wronskian = s.Matrix([[s.diff(z, x, j).subs(x, 0) for z in family] for j in range(3)]).det()
        independent = wronskian != 0
    else:
        independent = False
    family_truth.append(solves and independent)
choice("C18-03", family_truth)
report("C18-03-特征根", s.expand(characteristic - (r - 1)**3) == 0
       and answer_has("C18-03", "(B)"))

# C18-04: classify the right sides by which variable is missing.
v, yy = s.symbols("v y")
cases = [
    (2*x*v/(1 + x**2), "x"),
    (3*s.sqrt(yy), "y"),
    (x + yy, "both"),
    (4*v, "x"),
]
usable = []
for rhs, kind in cases:
    has_x = rhs.has(x)
    has_y = rhs.has(yy)
    usable.append((kind == "x" and not has_y) or (kind == "y" and not has_x))
choice("C18-04", [not value for value in usable])
report("C18-04-判别", usable == [True, True, False, True]
       and answer_has("C18-04", "(C)"))

# C18-05: substitute each actual trial expression and solve its coefficients.
poly = s.Poly(r**2 - 2*r + 1, r)
root_mult = s.roots(poly.as_expr(), r)[1]
lambda_is_root = s.simplify(poly.as_expr().subs(r, 1)) == 0
cos_is_root = s.simplify(poly.as_expr().subs(r, s.I)) == 0
required = (root_mult == 2, lambda_is_root, cos_is_root)
A, B, C, D = s.symbols("A B C D")
trig = C*s.cos(x) + D*s.sin(x)
trials = [
    (r"x(Ax+B)e^x+C\cos x+D\sin x", x*(A*x+B)*s.exp(x) + trig),
    (r"x^2(Ax+B)e^x+C\cos x+D\sin x", x**2*(A*x+B)*s.exp(x) + trig),
    (r"x(Ax+B)e^x+C\cos x", x*(A*x+B)*s.exp(x) + C*s.cos(x)),
    (r"x^2Ae^x+C\cos x+D\sin x", x**2*A*s.exp(x) + trig),
]
E, S, T = s.symbols("E S T")
coefficient_solutions = []
for letter, (printed, trial) in zip("ABCD", trials):
    residual05 = s.expand(s.diff(trial, x, 2) - 2*s.diff(trial, x)
                          + trial - x*s.exp(x) - s.cos(x))
    polynomial = s.Poly(residual05.subs({s.exp(x): E, s.sin(x): S, s.cos(x): T}),
                        x, E, S, T)
    solution = s.solve(polynomial.coeffs(), (A, B, C, D), dict=True)
    coefficient_solutions.append(solution)
    report("C18-05-题干" + letter, f"({letter}) $y^*={printed}$" in PROBLEMS)
choice("C18-05", [bool(solution) for solution in coefficient_solutions])
report("C18-05-系数", coefficient_solutions[1] == [
    {A: s.Rational(1, 6), B: 0, C: 0, D: -s.Rational(1, 2)}]
    and answer_has("C18-05", "A=1/6,B=C=0,D=-1/2"))
report("C18-05-结构", required == (True, True, False)
       and answer_has("C18-05", "(B)", "x^2(Ax+B)e^x", "C\\cos x+D\\sin x"))

# Necessity uses a point where f is nonzero; sufficiency follows by linearity.
print("MANUAL C18-06 非零右端系数和为1的必要性、充分性及零右端对照")

# C18-07: Euler substitution followed by a resonant double-root particular solution.
Y = s.Function("Y")(t)
y07 = C1*x**2 + C2*x**2*s.log(x) + s.Rational(1, 2)*x**2*s.log(x)**2
ode07 = x**2*s.diff(y07, x, 2) - 3*x*s.diff(y07, x) + 4*y07
report("C18-07", eq(ode07, x**2)
       and eq(s.diff(y07, x).subs({C1: 0, C2: 0}),
              s.diff(s.Rational(1, 2)*x**2*s.log(x)**2, x))
       and answer_has("C18-07", r"C_1x^2", r"C_2x^2\ln x", r"\frac12x^2(\ln x)^2"))

# C18-08: derive the initial coefficients and test both directions of decay.
u, v = s.symbols("u v", real=True)
initial_coefficients = s.solve([A+B-u, A-3*B-v], (A, B))
x08 = (A*s.exp(2*t) + B*s.exp(-2*t)).subs(initial_coefficients)
y08 = s.diff(x08, t) - x08
report("C18-08-通解", eq(s.diff(x08, t), x08 + y08)
       and eq(s.diff(y08, t), 3*x08 - y08)
       and eq(x08.subs(t, 0), u) and eq(y08.subs(t, 0), v)
       and eq(s.diff(x08, t, 2), 4*x08))
# If x tends to zero, x/exp(2t) must tend to zero, forcing A=0.
growth = s.limit(x08/s.exp(2*t), t, s.oo)
decay_condition = s.solve(growth, v)
report("C18-08-必要性", eq(growth, (3*u+v)/4)
       and decay_condition == [-3*u]
       and answer_has("C18-08", "A=(3u+v)/4", "(u,-3u)"))
stable_x, stable_y = x08.subs(v, -3*u), y08.subs(v, -3*u)
report("C18-08-充分性", eq(stable_x, u*s.exp(-2*t))
       and eq(stable_y, -3*u*s.exp(-2*t))
       and eq(s.diff(stable_x, t), stable_x+stable_y)
       and eq(s.diff(stable_y, t), 3*stable_x-stable_y)
       and s.limit(stable_x, t, s.oo) == 0
       and s.limit(stable_y, t, s.oo) == 0
       and answer_has("C18-08", "x(t)=ue^{-2t}", "y(t)=-3ue^{-2t}"))


# Check the required ordering, tier limits, answer markers, and banned wording.
tiers = dict(re.findall(r"\*\*(C18-\d+)\*\*〔([AB])", PROBLEMS))
table = re.findall(r"(?m)^\| (C18-\d+) \| ([AB]) \| (.*?) \|$", PROBLEMS)
headers = dict(re.findall(r"\*\*(C18-\d+)\*\*〔[AB]｜(.*?) · 考查：", PROBLEMS))
report("题号与方法表", [(pid, tier) for pid, tier, _ in table] == list(tiers.items())
       and list(tiers) == list(BLOCKS)
       and all(method.split("（")[0] == headers[pid]
               for pid, _, method in table))
assert list(tiers) == [f"C18-{i:02}" for i in range(1, 9)]
assert list(tiers.values()).count("A") == 5 and list(tiers.values()).count("B") == 3
assert set(tiers) == set(BLOCKS)
for pid, body in BLOCKS.items():
    body = re.split(r"(?m)^### ", body)[0].strip()
    assert body.startswith("**答案：**") and body.splitlines()[-1].startswith("区分点：")
    assert len(body) <= {"A": 400, "B": 900}[tiers[pid]], pid
assert not re.search(r"高中|初中|中学课本|备考|考研|数学一|真题|考纲|应试|常考|考试要求", PROBLEMS + ANSWERS)

sys.exit(bool(failures))
