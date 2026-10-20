"""Check all ten numbered examples, plus the three unnumbered exercises."""

import sympy as s

x, y, z, t, p, r = s.symbols("x y z t p r", real=True)
a = s.symbols("a", positive=True)
xyz = (x, y, z)
failures = 0


def check(label, actual, expected):
    global failures
    actuals = list(actual) if isinstance(actual, (tuple, list, s.MatrixBase)) else [actual]
    expects = list(expected) if isinstance(expected, (tuple, list, s.MatrixBase)) else [expected]
    ok = len(actuals) == len(expects) and all(
        s.simplify(v-w) == 0 for v, w in zip(actuals, expects)
    )
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} {label} computed={actual}")


def curl(field):
    P, Q, R = field
    return s.Matrix([s.diff(R, y)-s.diff(Q, z),
                     s.diff(P, z)-s.diff(R, x),
                     s.diff(Q, x)-s.diff(P, y)])


def line_integral(field, curve):
    value = s.Matrix(field).subs(dict(zip(xyz, curve)), simultaneous=True)
    return s.integrate(s.trigsimp(value.dot(curve.diff(t))), (t, 0, 2*s.pi))


def graph_flux(field, height, side):
    normal_area = side*s.Matrix([-s.diff(height, x), -s.diff(height, y), 1])
    density = s.Matrix(field).subs(z, height).dot(normal_area)
    polar = density.subs({x: r*s.cos(t), y: r*s.sin(t)})*r
    return s.integrate(s.trigsimp(polar), (r, 0, 1), (t, 0, 2*s.pi))


# The spherical area factor follows from the tangent cross product.
sphere = s.Matrix([a*s.sin(p)*s.cos(t), a*s.sin(p)*s.sin(t), a*s.cos(p)])
cross = sphere.diff(p).cross(sphere.diff(t)).applyfunc(s.trigsimp)
jacobian = a**2*s.sin(p)  # Nonnegative for 0 <= p <= pi.
assert s.trigsimp(cross.dot(cross)-jacobian**2) == 0


def scalar_sphere(expr, upper=s.pi):
    values = s.sympify(expr).subs(dict(zip(xyz, sphere)), simultaneous=True)
    return s.integrate(s.expand_trig(values*jacobian), (p, 0, upper), (t, 0, 2*s.pi))


check("例1", scalar_sphere(z, s.pi/2), s.pi*a**3)
check("例2", (scalar_sphere(x**2+z), scalar_sphere(z),
               scalar_sphere(x**2), scalar_sphere(y**2), scalar_sphere(z**2)),
      (4*s.pi*a**4/3, 0, *([4*s.pi*a**4/3]*3)))
check("例3", graph_flux((0, 0, z+1), x**2+y**2, -1), -3*s.pi/2)
check("例4", graph_flux((x, y, z), x**2+y**2, -1), s.pi/2)

# 5: direct sphere flux, independent of the lesson's volume-integral route.
cubic = s.Matrix([q**3 for q in sphere])
surface_flux = s.integrate(s.expand_trig(cubic.dot(cross)),
                           (p, 0, s.pi), (t, 0, 2*s.pi))
check("例5", surface_flux, 12*s.pi*a**5/5)

# 6: compute the three pieces separately, including the nonzero cap.
volume = s.integrate(3*r, (z, r**2, 1), (r, 0, 1), (t, 0, 2*s.pi))
cap = graph_flux((x, y, z), s.Integer(1), 1)
check("例6", (volume, cap, volume-cap, graph_flux((x, y, z), x**2+y**2, -1)),
      (3*s.pi/2, s.pi, s.pi/2, s.pi/2))

# 7: the two basis vectors induce the specified positive-x normal.
u = s.Matrix([1, -1, 0])/s.sqrt(2)
v = s.Matrix([1, 1, -2])/s.sqrt(6)
curve = a*(u*s.cos(t)+v*s.sin(t))
normal = u.cross(v)
check("例7", (line_integral((y, z, x), curve), *normal),
      (-s.sqrt(3)*s.pi*a**2, *([1/s.sqrt(3)]*3)))

data = []
for field in ((-y, x, 0), (x, y, 0)):
    data.append(sum(s.diff(field[i], xyz[i]) for i in range(3)))
    data.extend(curl(field))
check("例8", data, [0, 0, 0, 2, 2, 0, 0, 0])

# 9: gradient identity, curl and a straight path are all checked.
field = s.Matrix([2*x*y+z**3, x**2, 3*x*z**2])
potential = x**2*y+x*z**3
gradient_error = s.Matrix([s.diff(potential, q) for q in xyz])-field
curve = s.Matrix([t, t, t])
value = field.subs(dict(zip(xyz, curve)), simultaneous=True).dot(curve.diff(t))
check("例9", [*gradient_error, *curl(field), s.integrate(value, (t, 0, 1))],
      [0, 0, 0, 0, 0, 0, 2])

mass = scalar_sphere(1, s.pi/2)
moments = [scalar_sphere(q, s.pi/2) for q in xyz]
check("例10", [mass, *[s.simplify(q/mass) for q in moments]],
      [2*s.pi*a**2, 0, 0, a/2])

# Unnumbered exercises are checked as well, not silently omitted.
plane_value = s.integrate((1-x-y)*s.sqrt(3), (y, 0, 1-x), (x, 0, 1))
check("例1随堂题", plane_value, s.sqrt(3)/6)
hemisphere_flux = s.integrate(sphere[2]*cross[2], (p, 0, s.pi/2), (t, 0, 2*s.pi))
check("例3随堂题", hemisphere_flux, 2*s.pi*a**3/3)
triangle = [s.Matrix([1-t, t, 0]), s.Matrix([0, 1-t, t]), s.Matrix([t, 0, 1-t])]
triangle_field = s.Matrix([z, x, y])
triangle_value = 0
for edge in triangle:
    field_on_edge = triangle_field.subs(dict(zip(xyz, edge)), simultaneous=True)
    triangle_value += s.integrate(field_on_edge.dot(edge.diff(t)), (t, 0, 1))
check("例7随堂题", (triangle_value, *curl(triangle_field)), (s.Rational(3, 2), 1, 1, 1))

raise SystemExit(1 if failures else 0)
