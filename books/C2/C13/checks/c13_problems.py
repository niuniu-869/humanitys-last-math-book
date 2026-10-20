"""Independently compute the exercises; expected values follow answers.md.

Choice values are read from problems.md. Text anchors bind the other expected
values to the published answer; they are not substitutes for computation.
"""
from pathlib import Path
import re
import sys

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
x, y, t = s.symbols("x y t", real=True)
b, h = s.symbols("b h", positive=True)
n = s.symbols("n", integer=True, positive=True)
pi = s.pi
R = s.Rational
failures = 0
seen = set()


def blocks(text):
    return {
        m[1]: m[2] for m in re.finditer(
            r"(?ms)^\*\*(C13-\d+)\*\*(.*?)(?=^\*\*C13-\d+\*\*|\Z)", text
        )
    }


PB, AB = blocks(PROBLEMS), blocks(ANSWERS)


def eq(actual, expected):
    if actual == expected:
        return True
    return s.simplify(actual - expected) == 0


def report(pid, tests, detail=""):
    global failures
    seen.add(pid)
    bad = [label for label, result in tests if not bool(result)]
    failures += bool(bad)
    print(f"{'FAIL' if bad else 'PASS'} {pid}"
          + (f" {detail}" if detail else "")
          + (f" -- {', '.join(bad)}" if bad else ""))


def claims(pid, *strings):
    return [(f"answer anchor {v}", v in AB[pid]) for v in strings]


def read_choice_value(latex):
    """The choice grammar here is integers, pi, and a single fraction."""
    if latex.isdigit():
        return s.Integer(latex)
    if latex == r"\pi":
        return pi
    m = re.fullmatch(r"\\frac(?:\{([^}]+)\}|(\\pi|\d))"
                     r"(?:\{(\d+)\}|(\d+))", latex)
    if not m:
        raise ValueError(f"Unsupported choice expression: {latex!r}")
    numerator = m[1] or m[2]
    denominator = s.Integer(m[3] or m[4])
    if numerator.endswith(r"\pi"):
        coefficient = numerator[:-3]
        numerator = s.Integer(coefficient or "1") * pi
    else:
        numerator = s.Integer(numerator)
    return numerator / denominator


def check_choices(pid, actual, misconceptions):
    chosen = re.search(r"\*\*答案：\*\* \(([ABCD])\)", AB[pid])[1]
    options = re.findall(r"(?m)^\(([ABCD])\) \$(.*?)\$", PB[pid])
    tests = [("four options", len(options) == 4)]
    for letter, latex in options:
        value = read_choice_value(latex)
        truth = eq(value, actual)
        option_tests = [
            ("truth matches answer", truth == (letter == chosen)),
            ("option arithmetic", eq(value, misconceptions[letter])),
        ]
        report(pid, option_tests, f"选项 {letter}")
        tests.append((letter, all(ok for _, ok in option_tests)))
    report(pid, tests)


# C13-01: only the two signed integrals are given; apply area additivity.
negative, positive = s.Integer(-2), s.Integer(5)
area = -negative + positive
check_choices("C13-01", area, {
    "A": negative + positive, "B": positive, "C": area / 3, "D": area,
})

# C13-02: derive each proposed answer from its cross-sectional model.
outer, inner = 1 + x, s.Integer(1)
volume = pi * s.integrate(outer**2 - inner**2, (x, 0, 1))
check_choices("C13-02", volume, {
    "A": pi * s.integrate((outer-inner)**2, (x, 0, 1)),
    "B": volume,
    "C": pi * s.integrate(outer**2, (x, 0, 1)),
    "D": pi * s.integrate(outer-inner, (x, 0, 1)),
})

curve = 3*x
ds = s.sqrt(1+s.diff(curve, x)**2)
length = s.integrate(ds, (x, 1, 2))
surface = s.integrate(2*pi*curve*ds, (x, 1, 2))
wrong = s.integrate(2*pi*curve, (x, 1, 2))
report("C13-03", [
    ("length", eq(length, s.sqrt(10))),
    ("surface", eq(surface, 9*pi*s.sqrt(10))),
    ("wrong formula rejected", not eq(surface, wrong)),
    ("error order", eq((ds*h-h)/h, s.sqrt(10)-1)),
] + claims("C13-03", "列式不成立", r"\sqrt{10}", r"9\sqrt{10}\pi"))

radius = 2*s.cos(t)
area = s.integrate(radius**2/2, (t, 0, pi/2))
check_choices("C13-04", area, {
    "A": area, "B": s.integrate(radius**2, (t, 0, pi/2)),
    "C": s.integrate(radius/2, (t, 0, pi/2)),
    "D": s.integrate(radius, (t, 0, pi/2)),
})

c = s.symbols("c", real=True)
avg = s.integrate(x+c, (x, 0, 2))/2
solutions = s.solve(s.Eq(avg, 3), c)
report("C13-05", [("solve average condition", solutions == [2])]
       + claims("C13-05", "$c=2$"))

# The sole proof is checked by reading the complete argument, not sampling.
print("MANUAL C13-06 证明：可加性、统一误差上界与黎曼和极限")
seen.add("C13-06")

param_x, param_y = t**2, t**3
# Horizontal slices avoid using the same area derivation as the answer.
area = 2*s.integrate(1-y**R(2, 3), (y, 0, 1))
speed_squared = s.diff(param_x, t)**2+s.diff(param_y, t)**2
speed = s.Abs(t)*s.sqrt(4+9*t**2)
length = 2*s.integrate(t*s.sqrt(4+9*t**2), (t, 0, 1))
report("C13-07", [
    ("endpoints", (param_x.subs(t, -1), param_y.subs(t, -1),
                   param_x.subs(t, 1), param_y.subs(t, 1)) == (1, -1, 1, 1)),
    ("area", eq(area, R(4, 5))),
    ("parameter area", eq(2*s.integrate(param_y*s.diff(param_x, t), (t, 0, 1)), area)),
    ("speed identity", eq(speed**2, speed_squared)),
    ("length", eq(length, 2*(13*s.sqrt(13)-8)/27)),
] + claims("C13-07", "$4/5$", "$2(13\\sqrt{13}-8)/27$"))

total_volume = s.integrate(pi, (y, 0, 2))
level = s.solve(s.Eq(pi*h, total_volume/2), h)[0]
first = s.integrate(10000*pi*(3-y), (y, level, 2))
second = s.integrate(10000*pi*(3-y), (y, 0, level))
# Also check by change in gravitational potential energy of all the water.
total_work = 10000*(total_volume*3-s.integrate(pi*y, (y, 0, 2)))
report("C13-08", [
    ("half-volume level", eq(level, 1)), ("first", eq(first, 15000*pi)),
    ("second", eq(second, 25000*pi)),
    ("difference", eq(second-first, 10000*pi)),
    ("energy balance", eq(first+second, total_work)),
] + claims("C13-08", "$15000\\pi$", "$25000\\pi$", "$10000\\pi$"))

w1 = 2+(4-2)*(x-1)/3
w2 = 4+(2-4)*(x-1)/3
f1 = 10000*s.integrate(x*w1, (x, 1, 4))
f2 = 10000*s.integrate(x*w2, (x, 1, 4))
report("C13-09", [
    ("width endpoints", [w1.subs(x, 1), w1.subs(x, 4),
                         w2.subs(x, 1), w2.subs(x, 4)] == [2, 4, 4, 2]),
    ("first force", eq(f1, 240000)), ("second force", eq(f2, 210000)),
    ("difference", eq(f1-f2, 30000)),
    ("same area", eq(s.integrate(w1-w2, (x, 1, 4)), 0)),
] + claims("C13-09", "$240000$", "$210000$", "$30000$"))

# Divide both components by G m lambda, retaining the signed directions.
kx = -1/(1+y*y)**R(3, 2)
ky = y/(1+y*y)**R(3, 2)
fx = s.integrate(kx, (y, -s.sqrt(3), -b))+s.integrate(kx, (y, b, s.sqrt(3)))
fy = s.integrate(ky, (y, -s.sqrt(3), -b))+s.integrate(ky, (y, b, s.sqrt(3)))
original = s.integrate(kx, (y, -s.sqrt(3), s.sqrt(3)))
solutions = s.solve(s.Eq(fx, original/2), b)
report("C13-10", [
    ("positive solution", solutions == [s.sqrt(R(3, 13))]),
    ("vertical cancellation", eq(fy, 0)),
    ("original magnitude", eq(-original, s.sqrt(3))),
    ("remaining force formula", eq(fx, -2*(s.sqrt(3)/2-b/s.sqrt(1+b*b)))),
    ("admissible", 0 < solutions[0] < s.sqrt(3)),
    ("substitute unsquared equation", eq(fx.subs(b, solutions[0]), original/2)),
    ("force magnitude halved",
     eq(s.sqrt((fx**2+fy**2).subs(b, solutions[0])), s.Abs(original)/2)),
] + claims("C13-10", r"$b=\sqrt{3/13}$", "$F_y=0$", "$F_x<0$"))

pieces = [(0, 1, x**2, x), (1, 2, s.Integer(0), x)]
area = sum(s.integrate(hi-lo, (x, a, z)) for a, z, lo, hi in pieces)
mx = sum(s.integrate(x*(hi-lo), (x, a, z)) for a, z, lo, hi in pieces)
my = sum(s.integrate((hi**2-lo**2)/2, (x, a, z)) for a, z, lo, hi in pieces)
volume = sum(pi*s.integrate((hi+1)**2-(lo+1)**2, (x, a, z))
             for a, z, lo, hi in pieces)
report("C13-11", [
    ("area", eq(area, R(5, 3))), ("x centroid", eq(mx/area, R(29, 20))),
    ("y centroid", eq(my/area, R(37, 50))),
    ("washers", eq(volume, 29*pi/5)),
    ("Pappus", eq(volume, 2*pi*(area+my))),
] + claims("C13-11", "$5/3$", "$(29/20,37/50)$", "$29\\pi/5$"))

theta_cross = s.acos(R(1, 2))
polar_area = s.integrate(s.Integer(1)/2, (t, 0, theta_cross)) + \
    s.integrate((2*s.cos(t))**2/2, (t, theta_cross, pi/2))
cross = s.solve(s.Eq(1-x*x, 2*x-x*x), x)[0]
cart_area = s.integrate(s.sqrt(2*x-x*x), (x, 0, cross)) + \
    s.integrate(s.sqrt(1-x*x), (x, cross, 1))
volume = pi*(s.integrate(2*x-x*x, (x, 0, cross))
             + s.integrate(1-x*x, (x, cross, 1)))
report("C13-12", [
    ("angle", eq(theta_cross, pi/3)), ("x switch", eq(cross, R(1, 2))),
    ("area", eq(polar_area, pi/3-s.sqrt(3)/4)),
    ("independent Cartesian area", eq(cart_area, polar_area)),
    ("volume", eq(volume, 5*pi/12)),
] + claims("C13-12", r"$\pi/3-\sqrt3/4$", r"$5\pi/12$"))

volume = 2*pi*(s.integrate(x*x*(1-x), (x, 0, t))
               + s.integrate((1-x)*x*(1-x), (x, t, 1)))
dv = s.diff(volume, t)
stationary = s.solve(dv, t)
candidates = sorted(set([s.Integer(0), s.Integer(1)] + stationary))
values = {z: s.simplify(volume.subs(t, z)) for z in candidates}
minimizers = [z for z in candidates if all(values[z] <= v for v in values.values())]
report("C13-13", [
    ("polynomial", eq(volume, pi*(R(1, 6)-t*t+2*t**3-t**4))),
    ("derivative", eq(dv, 2*pi*t*(1-t)*(2*t-1))),
    ("unique minimizer", minimizers == [R(1, 2)]),
    ("minimum", eq(values[R(1, 2)], 5*pi/48)),
    ("both endpoints", eq(values[0], pi/6) and eq(values[1], pi/6)),
] + claims("C13-13", r"\frac16-t^2+2t^3-t^4", "$t=1/2$", "$5\\pi/48$"))

tp = s.symbols("tp", positive=True)
average = s.integrate(s.log(1+x), (x, 0, tp))/tp
derivative = s.diff(average, tp)
numerator = s.simplify(derivative*tp**2)
# Numerator starts at 0 and has a strictly positive derivative for tp > 0.
report("C13-14", [
    ("average", eq(average, ((1+tp)*s.log(1+tp)-tp)/tp)),
    ("derivative", eq(derivative, (tp-s.log(1+tp))/tp**2)),
    ("limit", eq(s.limit(average/tp, tp, 0, dir="+"), R(1, 2))),
    ("numerator starts at zero", eq(s.limit(numerator, tp, 0), 0)),
    ("monotonicity", s.simplify(s.diff(numerator, tp)).is_positive is True),
] + claims("C13-14", r"\frac{(1+t)\ln(1+t)-t}{t}",
           r"\frac{t-\ln(1+t)}{t^2}", "$1/2$", "严格递增"))

xp = s.symbols("xp", positive=True)
surface_integrand = 2*pi/xp*s.sqrt(1+s.diff(1/xp, xp)**2)
comparison = 2*pi/xp
# Squaring is valid since both factors are positive; this proves domination.
report("C13-15", [
    ("volume", eq(pi*s.integrate(xp**-2, (xp, 1, s.oo)), pi)),
    ("surface integrand", eq(surface_integrand, 2*pi/xp*s.sqrt(1+xp**-4))),
    ("positive comparison", comparison.is_positive is True),
    ("squared ratio exceeds one", s.simplify((surface_integrand/comparison)**2-1).is_positive is True),
    ("comparison diverges", s.integrate(comparison, (xp, 1, s.oo)) == s.oo),
] + claims("C13-15", r"体积为 $\pi$", "曲面面积无限",
           r"\frac1x\sqrt{1+\frac1{x^4}}"))

f = s.exp(x)
tangent = f.subs(x, 0)+s.diff(f, x).subs(x, 0)*x
height = f-tangent
report("C13-16", [
    ("tangent", eq(tangent, 1+x)),
    ("height at zero", eq(height.subs(x, 0), 0)),
    ("height derivative positive",
     s.solve_univariate_inequality(s.diff(height, x) > 0, x, relational=False)
     == s.Interval.open(0, s.oo)),
    ("area", eq(s.integrate(height, (x, 0, 1)), s.E-R(5, 2))),
    ("volume", eq(2*pi*s.integrate(x*height, (x, 0, 1)), pi/3)),
    ("integration by parts", eq(s.integrate(x*s.exp(x), (x, 0, 1)), 1)),
] + claims("C13-16", "$y=1+x$", r"$\mathrm{e}-5/2$", r"$\pi/3$"))

a = s.symbols("a", real=True)
i = s.symbols("i", integer=True)
local_error = s.integrate(x*x, (x, a, a+h))-h*(a+h/2)**2
midpoint_sum = s.summation(((i-R(1, 2))/n)**2/n, (i, 1, n))
total_error = s.integrate(x*x, (x, 0, 1))-midpoint_sum
report("C13-17", [
    ("local error", eq(local_error, h**3/12)),
    ("explicit sum", eq(midpoint_sum, R(1, 3)-1/(12*n*n))),
    ("total error", eq(total_error, 1/(12*n*n))),
    ("sum of local errors", eq(total_error, n*local_error.subs(h, 1/n))),
    ("scaled limit", eq(s.limit(n*n*total_error, n, s.oo), R(1, 12))),
] + claims("C13-17", "$h^3/12$", "$M_n=1/3-1/(12n^2)$", "$1/12$"))

if seen != set(PB) or set(PB) != set(AB):
    print(f"FAIL C13-coverage problems={set(PB)} answers={set(AB)} checked={seen}")
    failures += 1
sys.exit(bool(failures))
