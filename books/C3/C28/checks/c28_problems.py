"""Independently integrate the exercises; expected values transcribe answers.md."""

import re
from pathlib import Path

import sympy as s

x, y, z, t, r, p, a = s.symbols("x y z t r p a", real=True)
xyz = (x, y, z)
failures = 0
answers = (Path(__file__).resolve().parents[1] / "answers.md").read_text()


def equal(actual, expected):
    if isinstance(actual, (tuple, list)):
        return len(actual) == len(expected) and all(
            equal(v, w) for v, w in zip(actual, expected)
        )
    return s.simplify(actual - expected) == 0


def check(label, condition, detail=""):
    global failures
    ok = bool(condition)
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} {label} {detail}".rstrip())


def choice(pid, truths, expected):
    # Check all four propositions, including the false ones, then the answer key.
    selected = []
    for letter, truth in zip("ABCD", truths):
        check(f"{pid}({letter})", bool(truth) == (letter == expected),
              f"computed={bool(truth)}")
        if truth:
            selected.append(letter)
    match = re.search(rf"\*\*{pid}\*\*\s*\*\*答案：\*\* \(([A-D])\)", answers)
    check(pid, selected == [expected] and match is not None
          and match[1] == expected)


def curl(field):
    P, Q, R = field
    return s.Matrix([s.diff(R, y) - s.diff(Q, z),
                     s.diff(P, z) - s.diff(R, x),
                     s.diff(Q, x) - s.diff(P, y)])


def line_integral(field, curve, bounds):
    values = s.Matrix(field).subs(dict(zip(xyz, curve)), simultaneous=True)
    return s.integrate(s.trigsimp(values.dot(curve.diff(t))), (t, *bounds))


# 01: tangent vectors yield the area and the signed xy projection separately.
plane = s.Matrix([x, y, x])
normal_area = -plane.diff(x).cross(plane.diff(y))
I = s.integrate(s.sqrt(normal_area.dot(normal_area)), (x, 0, 1), (y, 0, 1))
J = s.integrate(normal_area[2], (x, 0, 1), (y, 0, 1))
options = [(s.sqrt(2), -1), (1, -1), (s.sqrt(2), 1), (s.sqrt(2), -s.sqrt(2))]
choice("C28-01", [equal((I, J), option) for option in options], "A")

# 02: integrate BOTH sheets with independently differentiated parametrizations.
sheet_values = []
for sign in (1, -1):
    sheet = s.Matrix([r*s.cos(t), r*s.sin(t), sign*(1-r**2)])
    cross = sheet.diff(r).cross(sheet.diff(t))
    jacobian = s.sqrt(s.trigsimp(cross.dot(cross)))
    density = 1 / s.sqrt(1 + 4*r**2)
    sheet_values.append(s.integrate(s.simplify(density*jacobian),
                                    (r, 0, 1), (t, 0, 2*s.pi)))
check("C28-02", equal(sum(sheet_values), 2*s.pi), str(sheet_values))

# 03: direct clockwise curve parametrization, without Stokes' theorem.
circle = s.Matrix([s.cos(t), -s.sin(t), 2])
circulation = line_integral((0, x, 0), circle, (0, 2*s.pi))
choice("C28-03", [equal(circulation, v) for v in (s.pi, 0, -s.pi, -2*s.pi)], "C")

print("MANUAL C28-04 混合偏导数相等的证明须人工核对")

# 05: solve the curl condition, then integrate along two explicit paths.
field = s.Matrix([2*x*y, x**2+a*z, y+2*z])
parameters = s.solve(list(curl(field)), a)
fixed = field.subs(a, 1)
straight = line_integral(fixed, s.Matrix([t, t, t]), (0, 1))
curved = line_integral(fixed, s.Matrix([t, t**2, t**3]), (0, 1))
potential = x**2*y + y*z + z**2
check("C28-05", parameters == {a: 1}
      and equal(straight, 3) and equal(curved, 3)
      and equal(list(s.Matrix([s.diff(potential, q) for q in xyz]) - fixed), [0, 0, 0]))

# 06: compute regularity failure and surface flux, not a volume integral at a pole.
radius2 = x**2+y**2+z**2
singular = s.Matrix(xyz) / radius2**s.Rational(3, 2)
divergence = s.simplify(sum(s.diff(singular[i], xyz[i]) for i in range(3)))
axis_limit = s.limit(singular[0].subs({y: 0, z: 0}), x, 0, dir="+")
smooth_at_origin = axis_limit.is_finite is True
unit = s.Matrix([s.sin(p)*s.cos(t), s.sin(p)*s.sin(t), s.cos(p)])
on_surface = singular.subs(dict(zip(xyz, unit)), simultaneous=True).applyfunc(s.trigsimp)
normal_dot = s.trigsimp(on_surface.dot(unit))
flux = s.integrate(normal_dot*s.sin(p), (p, 0, s.pi), (t, 0, 2*s.pi))
surface_defined = s.trigsimp(unit.dot(unit)) == 1
choice("C28-06", [equal(divergence, 0) and smooth_at_origin and equal(flux, 0),
                    not smooth_at_origin and equal(normal_dot, 1) and equal(flux, 4*s.pi),
                    equal(flux, -4*s.pi), not surface_defined], "B")

# 07: directly parameterize the inward face, and separately assemble the closed solid.
field = s.Matrix([x**2, y**2, 1])
face = s.Matrix([x, y, 1-x-y])
inward = -face.diff(x).cross(face.diff(y))
face_field = field.subs(z, face[2])
direct = s.integrate(face_field.dot(inward), (y, 0, 1-x), (x, 0, 1))
divergence = sum(s.diff(field[i], xyz[i]) for i in range(3))
volume = s.integrate(divergence, (z, 0, 1-x-y), (y, 0, 1-x), (x, 0, 1))
caps = [s.integrate(-field[0].subs(x, 0), (z, 0, 1-y), (y, 0, 1)),
        s.integrate(-field[1].subs(y, 0), (z, 0, 1-x), (x, 0, 1)),
        s.integrate(-field[2], (y, 0, 1-x), (x, 0, 1))]
check("C28-07", equal((direct, volume, *caps),
                      (-s.Rational(2, 3), s.Rational(1, 6), 0, 0, -s.Rational(1, 2)))
      and equal(direct, -(volume-sum(caps))))

# 08: direct line integral checks both the nonconstant curl and orientation.
curve = s.Matrix([s.cos(t), -s.sin(t), 1+s.cos(t)])
direct = line_integral((0, x*z, 0), curve, (0, 2*s.pi))
disk = s.Matrix([x, y, 1+x])
downward = -disk.diff(x).cross(disk.diff(y))
integrand = curl((0, x*z, 0)).subs(z, 1+x).dot(downward)
projected = integrand.subs({x: r*s.cos(t), y: r*s.sin(t)})*r
stokes = s.integrate(projected, (r, 0, 1), (t, 0, 2*s.pi))
check("C28-08", equal(direct, -s.pi) and equal(stokes, direct))

# The center-value shortcut needs the unit normal and the actual surface area.
area_factor = s.sqrt(downward.dot(downward))
area = s.integrate(area_factor*r, (r, 0, 1), (t, 0, 2*s.pi))
normal_component = integrand / area_factor
center_component = normal_component.subs({x: 0, y: 0})
check("C28-08平均值", equal(stokes/area, center_component)
      and equal(center_component*area, direct)
      and not equal(normal_component.subs({x: s.Rational(1, 2), y: 0})*area, direct))

raise SystemExit(1 if failures else 0)
