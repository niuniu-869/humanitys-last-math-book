"""Recompute every numbered example and the numerical in-text exercises."""

import itertools
import sys

import sympy as s


x, y, z, r, theta, phi, rho = s.symbols("x y z r theta phi rho", real=True)
a, b, c, h, mu, G, M = s.symbols("a b c h mu G M", positive=True)
failures = 0


def check(label, pairs):
    global failures
    ok = all(s.simplify(actual-expected) == 0 for actual, expected in pairs)
    failures += int(not ok)
    print(f"{'PASS' if ok else 'FAIL'} {label} "
          + "; ".join(f"{actual} == {expected}" for actual, expected in pairs))


def sphere_integral(f, radius, phi_upper=s.pi):
    return s.integrate(f*rho**2*s.sin(phi), (rho, 0, radius),
                       (phi, 0, phi_upper), (theta, 0, 2*s.pi))


value = s.integrate(x, (z, 0, 1-x-y), (y, 0, 1-x), (x, 0, 1))
check("例1", [(value, s.Rational(1, 24))])

# Elliptical polar coordinates evaluate the section area as well as its moment.
section = s.integrate(a*b*r, (r, 0, s.sqrt(1-z**2/c**2)),
                      (theta, 0, 2*s.pi))
value = s.integrate(z**2*section, (z, -c, c))
check("例2", [(section, s.pi*a*b*(1-z**2/c**2)),
              (value, 4*s.pi*a*b*c**3/15)])

# Horizontal disks provide a different integration order from the lesson.
value = s.integrate(z*r, (r, 0, s.sqrt(z)), (theta, 0, 2*s.pi), (z, 0, 4))
check("例3", [(value, 64*s.pi/3)])

# Above the cone and inside the unit sphere, 0 <= r <= 1/sqrt(2).
value = s.integrate(z*r, (z, r, s.sqrt(1-r**2)),
                     (r, 0, 1/s.sqrt(2)), (theta, 0, 2*s.pi))
check("例4", [(value, s.pi/8)])

u, v, w = s.symbols("u v w", real=True)
transform = s.Matrix([a*u, b*v, c*w])
determinant = transform.jacobian([u, v, w]).det()
volume = s.integrate(section, (z, -c, c))
# Integrate the ellipsoidal quadratic directly using its elliptical slices.
weighted = s.integrate((r**2+z**2/c**2)*a*b*r,
                        (r, 0, s.sqrt(1-z**2/c**2)),
                        (theta, 0, 2*s.pi), (z, -c, c))
check("例5", [(determinant, a*b*c), (volume, 4*s.pi*a*b*c/3),
              (weighted, 4*s.pi*a*b*c/5)])

patch = s.Matrix([r*s.cos(theta), r*s.sin(theta), r**2])
normal = patch.diff(r).cross(patch.diff(theta))
norm_squared = s.trigsimp(normal.dot(normal))
# r >= 0 on the integration domain.
area_element = r*s.sqrt(s.simplify(norm_squared/r**2))
surface = s.integrate(area_element, (r, 0, 1), (theta, 0, 2*s.pi))
check("例6", [(surface, s.pi*(5*s.sqrt(5)-1)/6)])

half_volume = s.integrate(s.pi*(a**2-z**2), (z, 0, a))
z_moment = s.integrate(z*s.pi*(a**2-z**2), (z, 0, a))
x_moment = sphere_integral(rho*s.sin(phi)*s.cos(theta), a, s.pi/2)
y_moment = sphere_integral(rho*s.sin(phi)*s.sin(theta), a, s.pi/2)
check("例7", [(half_volume, 2*s.pi*a**3/3), (z_moment, s.pi*a**4/4),
              (x_moment/half_volume, 0), (y_moment/half_volume, 0),
              (z_moment/half_volume, 3*a/8)])

ball_volume = s.integrate(s.pi*(a**2-z**2), (z, -a, a))
axis_moment = s.integrate(r**3, (r, 0, s.sqrt(a**2-z**2)),
                          (theta, 0, 2*s.pi), (z, -a, a))
inertia = s.simplify(axis_moment*M/ball_volume)
check("例8", [(axis_moment, 8*s.pi*a**5/15), (inertia, 2*M*a**2/5)])

distance_cubed = (r**2+h**2)**s.Rational(3, 2)
force_x = s.integrate(G*mu*r**2*s.cos(theta)/distance_cubed,
                      (theta, 0, 2*s.pi), (r, 0, a))
force_y = s.integrate(G*mu*r**2*s.sin(theta)/distance_cubed,
                      (theta, 0, 2*s.pi), (r, 0, a))
force_z = s.integrate(-G*mu*h*r/distance_cubed,
                      (r, 0, a), (theta, 0, 2*s.pi))
expected = 2*s.pi*G*mu*(1-h/s.sqrt(a**2+h**2))
check("例9", [(force_x, 0), (force_y, 0), (force_z, -expected),
              (s.limit(force_z, a, s.oo), -2*s.pi*G*mu)])

nodes = [s.Rational(1, 4), s.Rational(3, 4)]
midpoint_sum = sum(sum(point)/8 for point in itertools.product(nodes, repeat=3))
cube_integral = s.integrate(x+y+z, (x, 0, 1), (y, 0, 1), (z, 0, 1))
check("例1-定义及随堂", [(midpoint_sum, s.Rational(3, 2)),
                         (cube_integral, midpoint_sum)])

odd_integral = s.integrate(z**3*s.pi*(1-z**2), (z, -1, 1))
check("例1-奇偶练习", [(odd_integral, 0)])

radius_integral = s.integrate(r*r, (r, 0, 1), (theta, 0, 2*s.pi), (z, 0, 2))
check("例3-随堂", [(radius_integral, 4*s.pi/3)])

radial_square = sphere_integral(rho**2, 1)
check("例4-随堂", [(radial_square, 4*s.pi/5)])

cone_patch = s.Matrix([r*s.cos(theta), r*s.sin(theta), r])
cone_normal = cone_patch.diff(r).cross(cone_patch.diff(theta))
cone_factor = s.sqrt(s.trigsimp(cone_normal.dot(cone_normal)/r**2))*r
cone_area = s.integrate(cone_factor, (r, 0, 1), (theta, 0, 2*s.pi))
check("例6-随堂", [(cone_area, s.sqrt(2)*s.pi)])

# New in-text exercises: evaluated by cylindrical coordinates / slicing,
# a different route from the one in the lesson answers.
cone_z = s.integrate(z*r, (z, r, 1), (r, 0, 1), (theta, 0, 2*s.pi))
check("例2-随堂", [(cone_z, s.pi/4)])

ell_volume = s.integrate(s.pi*2*3*(1-z**2/16), (z, -4, 4))
check("例5-随堂", [(ell_volume, 32*s.pi)])

para_volume = s.integrate(r, (z, r**2, 1), (r, 0, 1), (theta, 0, 2*s.pi))
para_z = s.integrate(z*r, (z, r**2, 1), (r, 0, 1), (theta, 0, 2*s.pi))
check("例7-随堂", [(para_volume, s.pi/2), (para_z, s.pi/3),
                   (para_z/para_volume, s.Rational(2, 3))])

# Editor pass: numbers added to the lesson text.
cyl_vol = s.integrate(2*r, (r, 0, 1), (theta, 0, 2*s.pi))
cyl_x2 = s.integrate((r*s.cos(theta))**2*r, (r, 0, 1), (theta, 0, 2*s.pi))
check("编辑-圆柱体积与x^2", [(cyl_vol, 2*s.pi), (cyl_x2, s.pi/4)])
ball_vol = sphere_integral(1, 1)
check("编辑-球体积与漏因子", [(ball_vol, 4*s.pi/3),
                          (s.integrate(1, (rho, 0, 1), (phi, 0, s.pi), (theta, 0, 2*s.pi)), 2*s.pi**2)])
pt = (s.Rational(1, 2), s.Rational(1, 2), s.sqrt(2)/2)
check("编辑-球面坐标取点", [(s.sin(s.pi/4)*s.cos(s.pi/4), pt[0]),
                          (s.cos(s.pi/4), pt[2]), (sum(q**2 for q in pt), 1)])
box = (s.integrate(x, (x, 0, 1), (y, 0, 2), (z, 0, 3)),
       s.integrate(y, (x, 0, 1), (y, 0, 2), (z, 0, 3)))
check("编辑-长方体轮换反例", [(box[0], 3), (box[1], 6)])
slant = s.integrate(s.sqrt(1+1), (x, 0, 1), (y, 0, 1))
check("编辑-斜面面积", [(slant, s.sqrt(2))])
ell_slice = s.integrate(s.pi*a*b*(1-z**2/c**2), (z, -c, c))
check("编辑-椭球截面积分", [(ell_slice, 4*s.pi*a*b*c/3)])
frac = [1-1/s.sqrt(1+k**2) for k in (1, 10, 100)]
check("编辑-圆盘引力数值", [(s.Rational(round(float(f)*1000), 1000), s.Rational(v, 1000))
                          for f, v in zip(frac, (293, 900, 990))])
check("编辑-半球零件", [(round(float(s.Rational(2, 3)*s.pi*1000)), 2094),
                      (s.Rational(3, 8)*10, s.Rational(15, 4))])

sys.exit(bool(failures))
