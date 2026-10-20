"""Independently derive results, then compare with the printed answer claims."""

from pathlib import Path
import re
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = {
    m[1]: m[2]
    for m in re.finditer(
        r"(?ms)^\*\*(C17-\d+)\*\*\n(.*?)(?=^\*\*C17-\d+\*\*|\Z)", ANSWERS
    )
}
failures = 0
x = s.Symbol("x", positive=True)
v, u, c = s.symbols("v u c", real=True)


def eq(left, right):
    return s.simplify(left - right) == 0


def answer_has(pid, *claims):
    # Keep the numerical reference values tied to the human-readable answer.
    return all(claim in BLOCKS[pid] for claim in claims)


def report(pid, condition, detail=""):
    global failures
    ok = bool(condition)
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} {pid}" + (f" {detail}" if detail else ""))


def choice(pid, truth):
    selected = re.search(r"\*\*答案：\*\*\s*\(([A-D])\)", BLOCKS[pid]).group(1)
    for letter, actual in zip("ABCD", truth):
        report(pid, actual == (letter == selected), f"选项 {letter}: {bool(actual)}")
    report(pid, sum(bool(t) for t in truth) == 1, f"答案 ({selected})")


# C17-01: test the differential equation AND the initial value for every option.
candidates = [3 * s.exp(2*x), 1 + 2*s.exp(-2*x), 1 + 2*s.exp(2*x), 1+s.exp(2*x)]
choice("C17-01", [eq(s.diff(y, x), 2*(y-1)) and eq(y.subs(x, 0), 3) for y in candidates])

# C17-02: recompute both Euler steps, without using a closed-form solution.
h = s.Rational(1, 2)
xi, yi = s.S.Zero, s.S.One
values, slopes = [], []
for _ in range(2):
    slope = xi - yi
    slopes.append(slope)
    xi, yi = xi+h, yi+h*slope
    values.append(yi)
frozen = 1 + 2*h*slopes[0]
report("C17-02", values == [h, h] and slopes == [-1, 0] and frozen == 0
       and frozen != yi and answer_has("C17-02", r"y_1=\frac12", r"y_2=\frac12"))

# C17-03: derive every constant solution from the original polynomial.
roots = set(s.solve(c*(c-2), c))
constant_options = [{s.S.Zero}, {s.Integer(2)}, {s.S.Zero, s.Integer(2)}]
truth = [option == roots for option in constant_options]
truth.append(eq(c*(c-2), 0))  # The fourth option claims an identity for all c.
choice("C17-03", truth)

# C17-04: substitute y=x*u(x) and compare the four whole equations.
uf = s.Function("u")(x)
transformed = s.diff(x*uf, x) - (1 + (x*uf/x)**2)
derived_v = s.solve(transformed, s.diff(uf, x))[0].subs(uf, u)
option_residuals = [v-1-u**2, x*v-1-u**2, x*v-1-u**2-u, x*v-1-u**2+u]
choice("C17-04", [eq(s.solve(expr, v)[0], derived_v) for expr in option_residuals])

# C17-05: integrate the normalized equation and impose the initial value.
P, Q = -1/x, x
mu = s.exp(s.integrate(P, x))
general = (s.integrate(mu*Q, x) + c)/mu
constant = s.solve(general.subs(x, 1), c)[0]
y = s.simplify(general.subs(c, constant))
report("C17-05", eq(mu, 1/x) and eq(y, x**2-x)
       and eq(x*s.diff(y, x)-y, x**2) and eq(y.subs(x, 1), 0)
       and answer_has("C17-05", r"\mu=1/x", "y=x^2-x"))

# C17-06: obtain the transformed equation by differentiation, not by a template.
x = s.Symbol("x", real=True)
z = s.Function("z")(x)
transformed = s.simplify((s.diff(1/z, x)+2/z-3/z**2)*z**2)
zprime = s.solve(transformed, s.diff(z, x))[0]
mu_z = s.exp(s.integrate(-2, x))
z_general = (s.integrate(-3*mu_z, x)+c)/mu_z
z_constant = s.solve(z_general.subs(x, 0)-s.Rational(1, 2), c)[0]
z_sol = s.simplify(z_general.subs(c, z_constant))
y = s.simplify(1/z_sol)
pole = s.solve(z_sol, x)[0]
positive_domain = s.solve_univariate_inequality(z_sol > 0, x, relational=False)
report("C17-06", eq(zprime, 2*z-3) and eq(y, 2/(3-2*s.exp(2*x)))
       and eq(s.diff(y, x)+2*y, 3*y**2) and eq(y.subs(x, 0), 2)
       and eq(pole, s.log(s.Rational(3, 2))/2) and pole > 0
       and positive_domain.start == -s.oo and eq(positive_domain.end, pole)
       and positive_domain.left_open and positive_domain.right_open
       and s.limit(y, x, pole, dir="-") == s.oo
       and s.diff(3*v**2-2*v, v, 2) != 0
       and "$y'+2y=3y^2$，$y(0)=2$" in PROBLEMS
       and answer_has("C17-06", "z'-2z=-3", "z(0)=1/2", "y=2/(3-2e^{2x})",
                      r"(-\infty,\frac12\ln\frac32)"))

# C17-07 is a general proof; numerical examples would not certify the argument.
print("MANUAL C17-07 证明：逐式相减及特解加齐次解，已人工核对")

# C17-08: derive the tangent intercept, solve the resulting IVP, integrate.
x = s.Symbol("x", positive=True)
Y = s.Function("y")(x)
X = s.Symbol("X", real=True)
tangent = Y+s.diff(Y, x)*(X-x)
ode = s.solve(tangent.subs(X, 0)+x, s.diff(Y, x))[0]
P = -s.diff(ode, Y)
Q = s.simplify(ode+P*Y)
mu = s.exp(s.integrate(P, x))
general = (s.integrate(mu*Q, x)+c)/mu
constant = s.solve(general.subs(x, 1), c)[0]
y = s.simplify(general.subs(c, constant))
area = s.integrate(y, (x, 1, s.E))
nonnegative_domain = s.solve_univariate_inequality(y >= 0, x, relational=False)
report("C17-08", eq(y, x*s.log(x)) and eq(y-x*s.diff(y, x), -x)
       and eq(y.subs(x, 1), 0) and s.Interval(1, s.E).is_subset(nonnegative_domain)
       and eq(area, (s.E**2+1)/4)
       and answer_has("C17-08", r"y=x\ln x", r"\dfrac{e^2+1}{4}"))

# Check book-facing constraints as well; none of these substitute for the math.
tiers = dict(re.findall(r"\*\*(C17-\d+)\*\*〔([ABC])", PROBLEMS))
assert list(tiers) == [f"C17-{i:02}" for i in range(1, 9)]
assert list(tiers.values()).count("A") == 6 and list(tiers.values()).count("B") == 2
assert set(tiers) == set(BLOCKS)
table_ids = re.findall(r"(?m)^\| (C17-\d+) \|", PROBLEMS)
lesson = (ROOT / "lesson.md").read_text(encoding="utf-8")
summary = lesson.split("### 本章小结", 1)[1]
assert table_ids == list(tiers)
assert set(re.findall(r"C17-\d+", summary)) == set(BLOCKS)
for pid, body in BLOCKS.items():
    body = re.split(r"(?m)^### ", body)[0].strip()
    assert body.startswith("**答案：**") and body.splitlines()[-1].startswith("区分点：")
    assert len(body) <= {"A": 400, "B": 900}[tiers[pid]], pid
assert not re.search(r"高中|初中|中学课本|备考|考研|数学一|真题|考纲|应试|常考|考试要求", PROBLEMS+ANSWERS)
sys.exit(bool(failures))
