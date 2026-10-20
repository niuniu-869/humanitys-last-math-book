"""Check all 28 numbered examples and the adjacent numerical exercises.

Integrands are reconstructed from the geometric or physical data. The
right-hand values are the claims in lesson.md, not calculated substitutes.
"""
from pathlib import Path
import re
import sys

import sympy as s

x, y, t, theta, q = s.symbols("x y t theta q", real=True)
a, b, radius, length, G, mass, density, height, base = s.symbols(
    "a b R l G m lambda h S", positive=True
)
pi = s.pi
R = s.Rational
failures = 0
seen = set()


def eq(actual, expected):
    return actual == expected or s.simplify(actual-expected) == 0


def check(number, *pairs):
    global failures
    seen.add(number)
    bad = [j for j, (actual, expected) in enumerate(pairs, 1)
           if not eq(actual, expected)]
    failures += bool(bad)
    print(f"{'FAIL' if bad else 'PASS'} 例{number}"
          + (f" -- 子项 {bad}" if bad else ""))


# 1: exact annulus error, disk, and adjacent spherical-shell exercise.
dr = s.symbols("dr", positive=True)
annulus_error = pi*((x+dr)**2-x**2)-2*pi*x*dr
check(1,
      (s.integrate(2*pi*x, (x, 0, radius)), pi*radius**2),
      (s.expand(annulus_error), pi*dr**2),
      (s.limit(annulus_error/dr, dr, 0), 0),
      (s.integrate(4*pi*x**2, (x, 0, radius)), 4*pi*radius**3/3))

check(2, (s.integrate(x*2*pi*x, (x, 0, 2)), 16*pi/3))

check(3,
      (s.integrate(s.sqrt(x)-x**2, (x, 0, 1)), R(1, 3)),
      (s.integrate(x-x**2, (x, 0, 1)), R(1, 6)))

check(4,
      (s.integrate(y+4-y*y/2, (y, -2, 4)), 18),
      (s.integrate(2*s.sqrt(2*x), (x, 0, 2)), R(16, 3)),
      (s.integrate(s.sqrt(2*x)-x+4, (x, 2, 8)), R(38, 3)))

left = s.integrate(s.cos(x)-s.sin(x), (x, 0, pi/4))
right = s.integrate(s.sin(x)-s.cos(x), (x, pi/4, pi))
check(5, (left, s.sqrt(2)-1), (right, 1+s.sqrt(2)),
      (left+right, 2*s.sqrt(2)),
      (s.integrate(s.sin(x)-s.cos(x), (x, 0, pi)), 2))

market_quantity = s.solve(s.Eq(100-2*q, 40), q)[0]
check(6,
      (s.integrate(x-x*x, (x, 0, 1))/R(1, 2), R(1, 3)),
      (market_quantity, 30),
      (s.integrate((100-2*q)-40, (q, 0, market_quantity)), 900))

ellipse_x, ellipse_y = a*s.cos(t), b*s.sin(t)
ellipse_top = s.integrate(ellipse_y*s.diff(ellipse_x, t), (t, pi, 0))
check(7, (ellipse_top, pi*a*b/2), (2*ellipse_top, pi*a*b))

cycloid_x, cycloid_y = a*(t-s.sin(t)), a*(1-s.cos(t))
check(8, (s.integrate(cycloid_y*s.diff(cycloid_x, t), (t, 0, 2*pi)), 3*pi*a*a))

cardioid = a*(1+s.cos(theta))
check(9, (s.integrate(cardioid**2/2, (theta, 0, 2*pi)), 3*pi*a*a/2))

part1 = s.integrate((1+s.cos(theta))**2, (theta, 0, pi/3))
part2 = s.integrate((3*s.cos(theta))**2, (theta, pi/3, pi/2))
check(10, (part1, pi/2+9*s.sqrt(3)/8),
      (part2, 3*pi/4-9*s.sqrt(3)/8), (part1+part2, 5*pi/4))

rose = s.cos(3*theta)
petal = s.integrate(rose**2/2, (theta, -pi/6, pi/6))
rose_x, rose_y = rose*s.cos(theta), rose*s.sin(theta)
check(11, (petal, pi/12), (3*petal, pi/4),
      (s.integrate(rose**2/2, (theta, 0, 2*pi)), 2*(3*petal)),
      (s.trigsimp(rose_x.subs(theta, theta+pi)-rose_x), 0),
      (s.trigsimp(rose_y.subs(theta, theta+pi)-rose_y), 0))

ball = s.integrate(pi*(radius**2-x*x), (x, -radius, radius))
check(12, (ball, 4*pi*radius**3/3),
      (s.integrate(base*x*x/height**2, (x, 0, height)), base*height/3))

square_sections = s.integrate((2*s.sqrt(radius**2-x*x))**2, (x, -radius, radius))
check(13, (square_sections, 16*radius**3/3), (square_sections/ball, 4/pi))

check(14, (s.integrate(pi*(s.sqrt(x)**2-(x*x)**2), (x, 0, 1)), 3*pi/10))

shell_volume = s.integrate(2*pi*x*s.sin(x), (x, 0, pi))
washer_volume = s.integrate(pi*((pi-s.asin(y))**2-s.asin(y)**2), (y, 0, 1))
check(15, (shell_volume, 2*pi*pi), (washer_volume, shell_volume))

check(16,
      (s.integrate(2*pi*(2-x)*x*x, (x, 0, 1)), 5*pi/6),
      (s.integrate(pi*((2-s.sqrt(y))**2-1), (y, 0, 1)), 5*pi/6))

xp = s.symbols("xp", positive=True)
f = R(2, 3)*xp**R(3, 2)
log_curve = xp*xp/4-s.log(xp)/2
log_speed = s.sqrt(s.factor(1+s.diff(log_curve, xp)**2))
check(17,
      (s.integrate(s.sqrt(1+s.diff(f, xp)**2), (xp, 0, 3)), R(14, 3)),
      (log_speed, xp/2+1/(2*xp)),
      (s.integrate(log_speed, (xp, 1, s.E)), (s.E**2+1)/4))

astroid_x, astroid_y = s.cos(t)**3, s.sin(t)**3
astroid_speed_squared = s.diff(astroid_x, t)**2+s.diff(astroid_y, t)**2
quarter_speed = 3*s.sin(t)*s.cos(t)  # Nonnegative on [0, pi/2].
check(18,
      (s.trigsimp(astroid_speed_squared-quarter_speed**2), 0),
      (4*s.integrate(quarter_speed, (t, 0, pi/2)), 6),
      (s.integrate(quarter_speed, (t, 0, 2*pi)), 0))

cardioid_speed_squared = cardioid**2+s.diff(cardioid, theta)**2
upper_speed = 2*a*s.cos(theta/2)  # Nonnegative on [0, pi].
check(19,
      (s.trigsimp(cardioid_speed_squared-upper_speed**2), 0),
      (2*s.integrate(upper_speed, (theta, 0, pi)), 8*a))

# Normalize x = R u to keep the endpoint radicals real on (-1, 1).
u = s.symbols("u", real=True)
sphere_y = radius*s.sqrt(1-u*u)
sphere_dy_dx = -u/s.sqrt(1-u*u)
sphere_factor_squared = s.simplify(sphere_y**2*(1+sphere_dy_dx**2))
sphere_factor = s.sqrt(sphere_factor_squared)
check(20,
      (sphere_factor, radius),
      (2*pi*s.integrate(sphere_factor*radius, (u, -1, 1)), 4*pi*radius**2),
      (2*pi*s.integrate(radius*s.sqrt(1-u*u)*radius, (u, -1, 1)), pi*pi*radius**2),
      (2*pi*s.integrate(x*s.sqrt(1+s.diff(x, x)**2), (x, 0, 1)), pi*s.sqrt(2)),
      (s.integrate(2*pi*sphere_factor, (x, a, a+height)), 2*pi*radius*height))

upper_surface = 2*2*pi*s.integrate(astroid_y*quarter_speed, (t, 0, pi/2))
# Each lower-half point has the same x and opposite y, hence the same orbit.
check(21, (upper_surface, 12*pi/5),
      (s.trigsimp(astroid_x.subs(t, -t)-astroid_x), 0),
      (s.trigsimp(astroid_y.subs(t, -t)+astroid_y), 0))

exp_average = s.integrate(s.exp(x), (x, 0, 1))
sin_average = s.integrate(s.sin(x)**2, (x, 0, pi))/pi
requests = s.integrate(20+10*s.sin(pi*t/12), (t, 0, 12))
check(22, (exp_average, s.E-1), (sin_average, R(1, 2)),
      (requests, 240+240/pi), (requests/12, 20+20/pi),
      (s.Float(round(float(exp_average), 3)), s.Float("1.718")),
      (s.Float(round(float((1+s.E)/2), 3)), s.Float("1.859")),
      (s.Float(round(float(requests), 1)), s.Float("316.4")),
      (s.Float(round(float(requests/12), 2)), s.Float("26.37")))

pv = s.integrate(s.exp(-t/20), (t, 0, 10))
fv = s.integrate(s.exp((10-t)/20), (t, 0, 10))
check(23, (pv, 20*(1-s.exp(-R(1, 2)))),
      (fv, 20*(s.exp(R(1, 2))-1)), (fv, pv*s.exp(R(1, 2))),
      (s.integrate(s.exp(-t/20), (t, 0, s.oo)), 20),
      (s.Float(round(float(pv), 3)), s.Float("7.869")),
      (s.Float(round(float(fv), 3)), s.Float("12.974")))

work = s.integrate(9800*pi*((4-x)/2)**2*x, (x, 0, 4))
water_volume = s.integrate(pi*((4-x)/2)**2, (x, 0, 4))
check(24, (s.integrate(x*(4-x)**2, (x, 0, 4)), R(64, 3)),
      (work, R(16, 3)*9800*pi), (water_volume, 16*pi/3),
      (work/(9800*water_volume), 1),
      (s.Integer(round(float(work), -2)), 164200),
      (s.integrate(3*(10-x), (x, 0, 10)), 150))

check(25,
      (s.integrate(9800*x*4, (x, 1, 4)), 294000),
      (9800*R(5, 2), 24500),
      (s.integrate(9800*x*(2*x/3), (x, 0, 3)), 58800))

parallel_force = G*mass*density*s.integrate(x**-2, (x, a, a+length))
force_toward_rod = G*mass*density*2*s.integrate(a/(a*a+y*y)**R(3, 2), (y, 0, length/2))
vertical_force = G*mass*density*s.integrate(y/(a*a+y*y)**R(3, 2), (y, -length/2, length/2))
check(26,
      (parallel_force, G*mass*density*length/(a*(a+length))),
      (force_toward_rod, G*mass*density*length/(a*s.sqrt(a*a+length**2/4))),
      (vertical_force, 0),
      (s.limit(force_toward_rod/(G*mass*density*length/a**2), a, s.oo), 1),
      (s.diff(y/(a*a*s.sqrt(a*a+y*y)), y), (a*a+y*y)**(-R(3, 2))))

region_area = s.integrate(s.sqrt(x)-x*x, (x, 0, 1))
x_centroid = s.integrate(x*(s.sqrt(x)-x*x), (x, 0, 1))/region_area
y_centroid = s.integrate((s.sqrt(x)**2-(x*x)**2)/2, (x, 0, 1))/region_area
check(27, (region_area, R(1, 3)), (x_centroid, R(9, 20)), (y_centroid, R(9, 20)))

semidisk_area = radius**2*s.integrate(s.sqrt(1-u*u), (u, -1, 1))
semidisk_y_moment = radius**3*s.integrate((1-u*u)/2, (u, -1, 1))
semidisk_x_moment = radius**3*s.integrate(u*s.sqrt(1-u*u), (u, -1, 1))
check(28, (semidisk_area, pi*radius**2/2),
      (semidisk_x_moment/semidisk_area, 0),
      (semidisk_y_moment/semidisk_area, 4*radius/(3*pi)),
      (2*pi*semidisk_y_moment, ball),
      (s.Float(round(float(4/(3*pi)), 3)), s.Float("0.424")))


# 随堂小题与第 6 节模拟表（编辑稿新增）
def _sphere_sums(n):
    import math
    xs = [-1 + 2*i/n for i in range(n+1)]
    cyl = sum(2*math.pi*math.sqrt(1-((xs[i]+xs[i+1])/2)**2)*(2/n) for i in range(n))
    fr = 0.0
    for i in range(n):
        y1 = math.sqrt(max(0, 1-xs[i]**2)); y2 = math.sqrt(max(0, 1-xs[i+1]**2))
        fr += math.pi*(y1+y2)*math.hypot(2/n, y2-y1)
    return round(cyl, 3), round(fr, 3)

extra = [
    ("表 n=4", _sphere_sums(4), (10.240, 11.510)),
    ("表 n=10", _sphere_sums(10), (9.965, 12.369)),
    ("表 n=100", _sphere_sums(100), (9.873, 12.564)),
    ("单位圆四分之一", s.integrate(s.sin(t)**2, (t, 0, pi/2)), pi/4),
    ("参数小题", s.integrate(2*t*2*t, (t, 0, 1)), R(4, 3)),
    ("极坐标小题", s.integrate(theta**2, (theta, 0, pi))/2, pi**3/6),
    ("圆片小题", pi*s.integrate(x**4, (x, 0, 1)), pi/5),
    ("圆筒小题", 2*pi*s.integrate(x*x, (x, 0, 1)), 2*pi/3),
    ("引力小题", s.simplify(s.Integer(2)/(1*s.sqrt(1+1))), s.sqrt(2)),
    ("形心小题", (3*s.integrate(x**3, (x, 0, 1)), R(3, 2)*s.integrate(x**4, (x, 0, 1))), (R(3, 4), R(3, 10))),
    ("例10原函数", (s.integrate((1+s.cos(theta))**2, theta) - (3*theta/2 + 2*s.sin(theta) + s.sin(2*theta)/4)).simplify(), 0),
]
for name, got, want in extra:
    ok = (abs(got[0]-want[0]) < 1e-9 and abs(got[1]-want[1]) < 1e-9) if isinstance(got, tuple) and isinstance(got[0], float) \
        else (all(eq(g, w) for g, w in zip(got, want)) if isinstance(got, tuple) else eq(got, want))
    failures += not ok
    print(("PASS " if ok else "FAIL ") + "编辑 " + name)

lesson = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")
numbers = {int(k) for k in re.findall(r"\*\*例 (\d+)\*\*", lesson)}
if numbers != seen:
    print(f"FAIL 例覆盖 missing={numbers-seen} extra={seen-numbers}")
    failures += 1
sys.exit(bool(failures))
