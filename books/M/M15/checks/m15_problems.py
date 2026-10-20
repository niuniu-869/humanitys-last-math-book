"""独立验算 M.15 题目。"""
import sympy as sp


def report(pid, ok):
    print(f"{'PASS' if ok else 'FAIL'} {pid}")


# M15-01
policy = [(sp.Rational(1, 2), sp.Rational(1, 2)),
          (sp.Rational(1, 3), sp.Rational(2, 3)), (1, 0)]
successors = [(1, 2), (0, 2), (2, 2)]
P = sp.zeros(3)
for state, choices in enumerate(successors):
    for action, next_state in enumerate(choices):
        P[state, next_state] += policy[state][action]
G = sum(sp.Rational(1, 2) ** t * r for t, r in enumerate([0, 0, 1]))
expected_P = sp.Matrix([[0, sp.Rational(1, 2), sp.Rational(1, 2)],
                        [sp.Rational(1, 3), 0, sp.Rational(2, 3)],
                        [0, 0, 1]])
report("M15-01", P == expected_P and G == sp.Rational(1, 4))

# M15-02
v = sp.Rational(1, 4) * 2 + sp.Rational(3, 4) * 0
options = [sp.Eq(v, 2), sp.Eq(v, sp.Rational(1, 2)), sp.Eq(v, sp.Rational(3, 4)), sp.Eq(v, 0)]
report("M15-02", options == [False, True, False, False])

# M15-03
q_new = sp.Rational(2, 5) + sp.Rational(1, 4) * (1 + sp.Rational(4, 5) * sp.Rational(3, 5) - sp.Rational(2, 5))
report("M15-03", sp.simplify(q_new - sp.Rational(67, 100)) == 0)

# M15-04
p_bt = sp.exp(2) / (1 + sp.exp(2))
sigmoid = lambda x: 1 / (1 + sp.exp(-x))
opt04 = [sp.Rational(1, 5), p_bt, sigmoid(sp.Rational(6, 5)) - sigmoid(sp.Rational(-4, 5)), sp.Rational(6, 5) / sp.Rational(-4, 5)]
truth04 = [abs(float(x - p_bt)) < 1e-12 for x in opt04]
report("M15-04", truth04 == [False, True, False, False])

# M15-05
Vu, Vv = sp.symbols("Vu Vv")
sol = sp.solve([
    sp.Eq(Vu, sp.Rational(1, 2) * (1 + sp.Rational(1, 2) * Vu) + sp.Rational(1, 2) * sp.Rational(1, 2) * Vv),
    sp.Eq(Vv, sp.Rational(1, 3) * sp.Rational(1, 2) * Vu + sp.Rational(2, 3) * 2),
], [Vu, Vv], dict=True)[0]
q_vu = sp.Rational(1, 2) * sol[Vu]
q_vt = sp.Integer(2)
report("M15-05", sol[Vu] == sp.Rational(20, 17) and sol[Vv] == sp.Rational(26, 17)
       and q_vu == sp.Rational(10, 17) and q_vt == 2)

# M15-06
eta = sp.symbols("eta", real=True)
pi = sp.Matrix([sp.Rational(3, 4), sp.Rational(1, 4)])
z_new = sp.Matrix([sp.log(3), 0]) + eta * 2 * (sp.Matrix([1, 0]) - pi)
odds = sp.exp(z_new[0] - z_new[1])
eta_sol = sp.solve(sp.Eq(odds, 4), eta)[0]
reward = sp.symbols("reward", real=True)
prob = sigmoid(sp.log(3) + eta * reward / 2)
report("M15-06", sp.simplify(eta_sol - sp.log(sp.Rational(4, 3))) == 0
       and sp.simplify(prob.subs({eta: eta_sol, reward: 2}) - sp.Rational(4, 5)) == 0
       and sp.solve_univariate_inequality(prob.subs(eta, 1) < sp.Rational(3, 4), reward) == (reward < 0))

# M15-07 is a proof exercise.
print("MANUAL M15-07")

# M15-08
rho = sp.symbols("rho", positive=True)
lo, hi = sp.Rational(9, 10), sp.Rational(11, 10)
ok08 = True
for advantage in [sp.Rational(2, 3), -3, 0]:
    for point in [sp.Rational(1, 2), lo, sp.Integer(1), hi, sp.Rational(3, 2)]:
        actual = min(point * advantage, min(max(point, lo), hi) * advantage)
        expected = (advantage * min(point, hi) if advantage > 0
                    else advantage * max(point, lo) if advantage < 0 else 0)
        ok08 &= actual == expected
    # On each open interval the clipped argument is a constant or rho.
    for clip_expr, point in [(lo, sp.Rational(1, 2)), (rho, sp.Integer(1)),
                             (hi, sp.Rational(3, 2))]:
        terms = [advantage * rho, advantage * clip_expr]
        branch = min(terms, key=lambda term: term.subs(rho, point))
        expected_slope = (0 if (advantage > 0 and point > hi)
                          or (advantage < 0 and point < lo) else advantage)
        ok08 &= sp.diff(branch, rho) == expected_slope
    if advantage:
        left, right = ((advantage, 0) if advantage > 0 else (0, advantage))
        ok08 &= left != right
report("M15-08", ok08)

# M15-09
gamma = sp.Rational(9, 10)
next_q = [sp.Rational(2, 5), sp.Rational(-1, 5)]
sarsa_target = 1 + gamma * next_q[1]
q_target = 1 + gamma * max(next_q)
# Two models both permit the observed sample but give different expectations.
targets = sp.Matrix([q_target, 0])
model_targets = [sp.Matrix(row).dot(targets) for row in [(1, 0), (sp.Rational(1, 2), sp.Rational(1, 2))]]
exact_identified = model_targets[0] == model_targets[1]
sample_symbols = sarsa_target.free_symbols | q_target.free_symbols
truth09 = [exact_identified,
           not exact_identified and sarsa_target == sp.Rational(41, 50) and q_target == sp.Rational(34, 25),
           sarsa_target == q_target == sp.Rational(34, 25), bool(sample_symbols)]
report("M15-09", truth09 == [False, True, False, False])

# M15-10
beta = sp.symbols("beta", positive=True)
ref = [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)]
rewards = [0, 1, 1]
weights = [q * sp.exp(r / beta) for q, r in zip(ref, rewards)]
Z = sum(weights)
pi_star = [sp.simplify(w / Z) for w in weights]
objective = sum(p * r - beta * p * sp.log(p / q) for p, r, q in zip(pi_star, rewards, ref))
t = sp.exp(1 / beta)
expected = [1 / (1 + t), 2 * t / (3 * (1 + t)), t / (3 * (1 + t))]
p1, p2 = sp.symbols("p1 p2", positive=True)
ps = [p1, p2, 1 - p1 - p2]
full_objective = sum(p * r - beta * p * sp.log(p / q) for p, r, q in zip(ps, rewards, ref))
stationary = [sp.simplify(sp.expand_log(sp.diff(full_objective, x).subs({p1: pi_star[0], p2: pi_star[1]}), force=True)) == 0 for x in (p1, p2)]
zero_objective = sum(p * r for p, r in zip(ps, rewards))
report("M15-10", all(sp.simplify(a - b) == 0 for a, b in zip(pi_star, expected))
       and sp.simplify(sp.expand_log(objective - beta * sp.log(Z), force=True)) == 0
       and all(stationary)
       and [sp.limit(p, beta, 0, dir="+") for p in pi_star] == [0, sp.Rational(2, 3), sp.Rational(1, 3)]
       and [sp.limit(p, beta, sp.oo) for p in pi_star] == ref
       and sp.simplify(zero_objective - (1 - p1)) == 0)

# M15-11
uw, ul = sp.symbols("uw ul", real=True)
Z1, Z2 = sp.symbols("Z1 Z2", positive=True)
delta = (beta * uw + beta * sp.log(Z1)) - (beta * ul + beta * sp.log(Z2))
expected_delta = beta * (uw - ul) + beta * sp.log(Z1 / Z2)
report("M15-11", sp.simplify(sp.expand_log(delta - expected_delta)) == 0
       and sp.simplify(delta.subs(Z2, Z1) - beta * (uw - ul)) == 0
       and sp.simplify(delta.subs({ul: uw, Z1: 2, Z2: 1})) == beta * sp.log(2)
       and sp.solve(sp.Eq(delta.subs(ul, uw), 0), Z1) == [Z2])

# M15-12
std = sp.sqrt(sp.Rational(2, 3))
w = [sp.simplify((r - 1) / std) for r in (2, 0, 1)]
pi12 = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)])
g = sp.simplify(sum((w[i] * (sp.eye(3)[:, i] - pi12) for i in range(3)), sp.zeros(3, 1)) / 3)
report("M15-12", w == [sp.sqrt(sp.Rational(3, 2)), -sp.sqrt(sp.Rational(3, 2)), 0]
       and g == sp.Matrix([1 / sp.sqrt(6), -1 / sp.sqrt(6), 0]))

# M15-13
z1, z2 = sp.symbols("z1 z2", real=True)
prob1 = sp.exp(z1) / (sp.exp(z1) + sp.exp(z2))
objective13 = 3 * prob1 + (1 - prob1)
J = objective13.subs({z1: 0, z2: sp.log(4)})
dJ = sp.diff(objective13, z1).subs({z1: 0, z2: sp.log(4)})
report("M15-13", J == sp.Rational(7, 5) and dJ == sp.Rational(8, 25))

# M15-14
d1, d2 = sp.symbols("d1 d2", real=True)
delta14 = sp.solve(sp.Eq(sigmoid(d1 - d2), sp.Rational(3, 4)), d1)[0]
solutions14 = sp.linsolve([d1 - d2 - sp.log(3)], (d1, d2))
unique14 = sp.solve([d1 - d2 - sp.log(3), d1 + d2], [d1, d2])
report("M15-14", sp.simplify(delta14 - (d2 + sp.log(3))) == 0
       and solutions14 == sp.FiniteSet((d2 + sp.log(3), d2))
       and unique14 == {d1: sp.log(3) / 2, d2: -sp.log(3) / 2})

# M15-15
G15 = sp.Rational(1, 2) * 2 + sp.Rational(1, 4) * 1
report("M15-15", G15 == sp.Rational(5, 4) and G15 - sp.Rational(1, 2) == sp.Rational(3, 4))
