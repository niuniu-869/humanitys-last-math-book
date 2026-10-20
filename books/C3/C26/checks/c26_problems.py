"""Compute from the problem data; compare with the published answers."""

from pathlib import Path
import re
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"\*\*(C26-\d+)\*\*\n(.*?)(?=\n\*\*C26-|\Z)", ANSWERS, re.S
))
x, y, z, r, theta, phi, rho = s.symbols("x y z r theta phi rho", real=True)
failures = 0


def equal(actual, expected):
    return s.simplify(actual - expected) == 0


def report(pid, ok, detail):
    global failures
    failures += int(not ok)
    print(f"{'PASS' if ok else 'FAIL'} {pid} {detail}")


def check(pid, pairs, answer_text):
    ok = all(equal(a, b) for a, b in pairs)
    ok = ok and answer_text in BLOCKS[pid]
    report(pid, ok, "; ".join(f"{a} == {b}" for a, b in pairs))


def choices(pid, actual, candidates, error_integrals):
    selected = re.search(r"\*\*答案：\*\* \(([A-D])\)", BLOCKS[pid])[1]
    truths = [equal(actual, value) for value in candidates]
    for letter, candidate, truth, derived in zip(
        "ABCD", candidates, truths, error_integrals
    ):
        # Each distractor must also equal the result of its stated misconception.
        ok = truth == (letter == selected) and equal(candidate, derived)
        report(pid, ok, f"option {letter}: {candidate}; actual={actual}; true={truth}")
    report(pid, sum(truths) == 1 and truths["ABCD".index(selected)],
           f"unique answer = {selected}")


volume = s.integrate(1, (z, x*y, x), (y, 0, 1), (x, 0, 1))
check("C26-01", [(volume, s.Rational(1, 4))], "体积为 $1/4$")

actual = s.integrate(r**2*r, (z, 0, 1), (r, 1, 2), (theta, 0, s.pi))
choices("C26-02", actual,
        [7*s.pi/3, 15*s.pi/4, 4*s.pi, 15*s.pi/2],
        [s.integrate(r**2, (r, 1, 2), (theta, 0, s.pi)),
         actual,
         s.integrate(r**3, (r, 0, 2), (theta, 0, s.pi)),
         s.integrate(r**3, (r, 1, 2), (theta, 0, 2*s.pi))])

# Slice the two half balls, independently of the spherical-coordinate solution.
actual = (s.integrate(s.pi*(4-z**2), (z, 0, 2))
          - s.integrate(s.pi*(1-z**2), (z, 0, 1)))
jac = rho**2*s.sin(phi)
choices("C26-03", actual,
        [16*s.pi/3, 28*s.pi/3, 7*s.pi**2/3, 14*s.pi/3],
        [s.integrate(jac, (rho, 0, 2), (phi, 0, s.pi/2), (theta, 0, 2*s.pi)),
         s.integrate(jac, (rho, 1, 2), (phi, 0, s.pi), (theta, 0, 2*s.pi)),
         s.integrate(rho**2, (rho, 1, 2), (phi, 0, s.pi/2), (theta, 0, 2*s.pi)),
         s.integrate(jac, (rho, 1, 2), (phi, 0, s.pi/2), (theta, 0, 2*s.pi))])

# Cartesian integration checks the polar-coordinate answer.
actual = s.integrate(2*x**2*s.sqrt(1-x**2), (x, -1, 1), (z, 0, 1))
choices("C26-04", actual,
        [s.S.Zero, s.pi, s.pi/4, s.pi/2],
        [s.integrate((x**2).subs(x, 0)*s.pi, (z, 0, 1)),
         s.integrate(r, (r, 0, 1), (theta, 0, 2*s.pi), (z, 0, 1)),
         s.integrate(r**3*s.cos(theta)**2, (r, 0, 1),
                     (theta, 0, 2*s.pi), (z, 0, 1)),
         s.integrate(r**3, (r, 0, 1), (theta, 0, 2*s.pi), (z, 0, 1))])
report("C26-04", s.diff(x**2, x) != 0 and not equal(actual, 0),
       "the integrand is not constant on a horizontal slice")

print("MANUAL C26-05 geometric proof: radial, meridional and latitudinal lengths")

mu = 1+x/2
box = ((x, -1, 1), (y, -1, 1), (z, 0, 1))
mass = s.integrate(mu, *box)
center = [s.integrate(q*mu, *box)/mass for q in (x, y, z)]
check("C26-06", [(mass, 4), *zip(center, [s.Rational(1, 6), 0, s.Rational(1, 2)])],
      "质心为 $(1/6,0,1/2)$")
report("C26-06", not equal(center[0], 0), "centroid differs from geometric center")

# Parameterize the plane; compute the cross product instead of copying the area factor.
position = s.Matrix([x, y, x])
normal = position.diff(x).cross(position.diff(y))
area_factor = s.sqrt(normal.dot(normal))
projected = s.integrate(2*s.sqrt(2-2*x**2), (x, -1, 1))
surface = s.simplify(area_factor*projected)
check("C26-07", [(projected, s.sqrt(2)*s.pi), (surface, 2*s.pi)],
      "平面片面积为 $2\\pi$")
report("C26-07", (1**2+1**2 <= 2) and (1**2+1**2+1**2 > 2),
       "(1,1) lies in the proposed disk, but (1,1,1) lies outside the sphere")

# Use horizontal disk slices of the shifted ball as an independent reference.
radial_upper_sq = 2*z-z**2
slice_integral = s.integrate((r**2+z**2)*r,
                             (r, 0, s.sqrt(radial_upper_sq)),
                             (theta, 0, 2*s.pi))
actual = s.integrate(slice_integral, (z, 0, 2))
spherical = s.integrate(rho**4*s.sin(phi), (rho, 0, 2*s.cos(phi)),
                       (phi, 0, s.pi/2), (theta, 0, 2*s.pi))
check("C26-08", [(actual, 32*s.pi/15), (spherical, actual)], "$I=32\\pi/15$")
boundary = s.factor(rho**2-2*rho*s.cos(phi))
report("C26-08",
       equal(boundary.subs(rho, 2*s.cos(phi)), 0)
       and s.cos(0) > 0 and equal(s.cos(s.pi/2), 0)
       and (s.Rational(3, 2)**2 <= 2*s.Rational(3, 2))
       and s.Rational(3, 2) > 1,
       "radial boundary is 2*cos(phi); rho=1 would exclude (0,0,3/2)")

sys.exit(bool(failures))
