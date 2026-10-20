import sympy as sp

lam = sp.symbols('lam')

def check(k, cond):
    if not cond:
        print(f'FAIL 例{k}')
        raise AssertionError(f'例{k}')
    print(f'PASS 例{k}')

# 例1
A = sp.Matrix([[2,1,1],[1,2,1],[1,1,2]])
k = sp.symbols('k')
alpha = sp.Matrix([1,k,1])
sol = sp.solve(list(A*alpha - sp.symbols('l')*alpha), [k, sp.symbols('l')], dict=True)
check(1, {tuple(d.values()) for d in sol} == {(1,4),(-2,1)})

# 例2
A = sp.Matrix([[4,-2],[1,1]])
cp = sp.factor((lam*sp.eye(2)-A).det())
check(2, cp == (lam-2)*(lam-3) and (A-sp.Integer(2)*sp.eye(2)).nullspace() == [sp.Matrix([1,1])] and (A-sp.Integer(3)*sp.eye(2)).nullspace() == [sp.Matrix([2,1])])

# 例3
A = sp.Matrix([[2,1,1],[1,2,1],[1,1,2]])
cp = sp.factor((lam*sp.eye(3)-A).det())
check(3, cp == (lam-4)*(lam-1)**2 and (A-sp.eye(3)).nullspace() == [sp.Matrix([-1,1,0]),sp.Matrix([-1,0,1])] and (A-4*sp.eye(3)).nullspace() == [sp.Matrix([1,1,1])])

# 例4
A = sp.Matrix([[2,-1,-2],[1,3,1],[-1,1,3]])
cp = sp.factor((lam*sp.eye(3)-A).det())
vecs = {4:sp.Matrix([1,0,-1]),1:sp.Matrix([1,-1,1]),3:sp.Matrix([1,1,-1])}
check(4, cp == (lam-1)*(lam-3)*(lam-4) and all(A*v == e*v for e,v in vecs.items()))

# 例5
M = sp.Matrix([[0,0,1],[sp.Rational(1,2),0,0],[sp.Rational(1,2),1,0]])
x = sp.Matrix([sp.Rational(2,5),sp.Rational(1,5),sp.Rational(2,5)])
check(5, M*x == x and sum(x) == 1)

# 例6
avec = sp.symbols('a')
A = sp.Matrix([[1,-1,1],[2,4,-2],[-3,-3,avec]])
det = sp.factor(A.det())
sola = sp.solve([sp.Eq(sp.trace(A), 4+sp.symbols('l3')), sp.Eq(det, 4*sp.symbols('l3'))],[avec,sp.symbols('l3')], dict=True)
check(6, sola == [{avec:5, sp.symbols('l3'):6}])

# 例7
spec = [1,-1,2]
detA = sp.prod(spec)
g = [detA/e + 3*e - 2 for e in spec]
check(7, detA == -2 and g == [-1,-3,3] and sp.prod(g) == 9)

# 例8: polynomial restriction, plus a nonzero nilpotent counterexample
N = sp.Matrix([[0,1],[0,0]])
check(8, sp.factor(lam**2-lam) == lam*(lam-1) and N**2 == sp.zeros(2) and N != sp.zeros(2))

# 例9
D = sp.diag(1,2)
v1 = sp.Matrix([1,0]); v2 = sp.Matrix([0,1])
combo = v1+v2
fD = D**2 - 3*D
check(9, D*combo != combo*1 and D*combo != combo*2 and fD*combo == -2*combo)

# 例10
A = sp.Matrix([[1,2,-3],[-1,4,-3],[1,avec,5]])
cp = sp.factor((lam*sp.eye(3)-A).det())
cp2 = sp.factor((lam-2)*(lam**2-8*lam+18+3*avec))
check(10, cp == cp2 and sp.simplify(cp.subs(avec,-2) - (lam-2)**2*(lam-6)) == 0 and sp.simplify(cp.subs(avec,sp.Rational(-2,3)) - (lam-2)*(lam-4)**2) == 0 and (2*sp.eye(3)-A.subs(avec,-2)).rank() == 1 and (4*sp.eye(3)-A.subs(avec,sp.Rational(-2,3))).rank() == 2)
