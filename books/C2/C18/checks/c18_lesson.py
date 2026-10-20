"""独立核对 C.18 讲义中的十道例题。"""

import sys
import math

import sympy as s


x, t = s.symbols("x t", real=True)
C1, C2 = s.symbols("C_1 C_2")
failures = 0


def eq(left, right):
    return s.simplify(left - right) == 0


def near(value, target, tolerance):
    return abs(float(s.N(value)) - target) <= tolerance


def report(label, condition):
    global failures
    ok = bool(condition)
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'} {label}")


# 例 1
y1 = x**3 + 3*x + 1
report("例1", eq((1 + x**2)*s.diff(y1, x, 2), 2*x*s.diff(y1, x))
       and y1.subs(x, 0) == 1 and s.diff(y1, x).subs(x, 0) == 3)

# 例 2
y2 = (1 + x/2)**4
report("例2", eq(s.diff(y2, x, 2), 3*s.sqrt(y2))
       and y2.subs(x, 0) == 1 and s.diff(y2, x).subs(x, 0) == 2)

# 例 3: use the operator L=D^2-D, for which 1 and e^x are homogeneous solutions.
L = lambda z: s.diff(z, x, 2) - s.diff(z, x)
y31, y32, y33 = x, x + s.exp(x), 1 + x + s.exp(x)
hom1, hom2 = y32 - y31, y33 - y32
wronskian = s.Matrix([[hom1, hom2], [s.diff(hom1, x), s.diff(hom2, x)]]).det()
report("例3", all(eq(L(z), L(y31)) for z in (y31, y32, y33))
       and eq(L(hom1), 0) and eq(L(hom2), 0) and wronskian != 0)

# 例 4
y4 = s.exp(-x)*(s.cos(2*x) + s.sin(2*x))
report("例4", eq(s.diff(y4, x, 2) + 2*s.diff(y4, x) + 5*y4, 0)
       and y4.subs(x, 0) == 1 and s.diff(y4, x).subs(x, 0) == 1)

# 例 5
yp5 = 2*x + 3
report("例5", eq(s.diff(yp5, x, 2) - 3*s.diff(yp5, x) + 2*yp5, 4*x))

# 例 6
yp6 = -(x**2/s.Integer(2) + x)*s.exp(x)
report("例6", eq(s.diff(yp6, x, 2) - 3*s.diff(yp6, x) + 2*yp6, x*s.exp(x)))

# 例 7
y7 = C1*s.cos(x) + C2*s.sin(x) + x*s.sin(x)/2
report("例7", eq(s.diff(y7, x, 2) + y7, s.cos(x)))

# 例 8: exact formulas for c=2,4,10 and the stated qualitative/numerical claims.
y82 = s.exp(-t)*(s.cos(s.sqrt(3)*t) + s.sin(s.sqrt(3)*t)/s.sqrt(3))
y84 = (1 + 2*t)*s.exp(-2*t)
r1, r2 = -5 + s.sqrt(21), -5 - s.sqrt(21)
A = -r2/(r1 - r2)
B = r1/(r1 - r2)
y810 = A*s.exp(r1*t) + B*s.exp(r2*t)
first_min = -s.exp(-s.pi/s.sqrt(3))
report("例8", eq(s.diff(y82, t, 2) + 2*s.diff(y82, t) + 4*y82, 0)
       and y82.subs(t, 0) == 1 and s.diff(y82, t).subs(t, 0) == 0
       and eq(s.diff(y84, t, 2) + 4*s.diff(y84, t) + 4*y84, 0)
       and y84.subs(t, 0) == 1 and s.diff(y84, t).subs(t, 0) == 0
       and eq(s.diff(y810, t, 2) + 10*s.diff(y810, t) + 4*y810, 0)
       and eq(y810.subs(t, 0), 1) and eq(s.diff(y810, t).subs(t, 0), 0)
       and near(first_min, -0.163, 0.002) and near(y810.subs(t, 3), 0.30, 0.01)
       and all(root < 0 for root in (r1, r2)))

# 例 9
y9 = C1*x + C2*x**2 + x**3/2
report("例9", eq(x**2*s.diff(y9, x, 2) - 2*x*s.diff(y9, x) + 2*y9, x**3))

# 例 10
x10 = C1*s.exp(2*t) + C2*s.exp(-t)
y10 = C1*s.exp(2*t)/2 + 2*C2*s.exp(-t)
report("例10", eq(s.diff(x10, t), 3*x10 - 2*y10)
       and eq(s.diff(y10, t), 2*x10 - 2*y10))

# Three classroom exercises and the third-order example.
practice1 = x**3 + s.exp(x) - x
report("第1节小题", eq(s.diff(practice1, x, 2), 6*x+s.exp(x))
       and practice1.subs(x, 0) == 1 and s.diff(practice1, x).subs(x, 0) == 0)
practice3 = (C1+C2*x)*s.exp(-2*x)
report("第3节小题", eq(s.diff(practice3, x, 2)+4*s.diff(practice3, x)+4*practice3, 0)
       and s.wronskian([s.exp(-2*x), x*s.exp(-2*x)], x).subs(x, 0) != 0)
practice4 = s.exp(3*x)/2
report("第4节小题", eq(s.diff(practice4, x, 2)-3*s.diff(practice4, x)+2*practice4,
                     s.exp(3*x)))
third_basis = [s.exp(x), s.cos(x), s.sin(x)]
report("三阶算例", all(eq(s.diff(z, x, 3)-s.diff(z, x, 2)+s.diff(z, x)-z, 0)
                       for z in third_basis)
       and s.wronskian(third_basis, x).subs(x, 0) != 0)

# Recompute all iteration points in [0, 4] without reading or modifying figures.
for h, expected, caption in [(0.1, 0.0842360719, 0.084), (0.05, 0.0414341068, 0.041)]:
    previous = current = 1.0
    maximum_error = 0.0
    for k in range(1, round(4/h)+1):
        following = current - h*h*4*current + (1-2*h)*(current-previous)
        previous, current = current, following
        time = k*h
        exact = math.exp(-time)*(math.cos(math.sqrt(3)*time)
                               + math.sin(math.sqrt(3)*time)/math.sqrt(3))
        maximum_error = max(maximum_error, abs(current-exact))
    report(f"图C18-n2-h={h}", abs(maximum_error-expected) < 1e-9
           and abs(maximum_error-caption) < 0.0005)

sys.exit(bool(failures))
