import math
import numpy as np

def report(k, ok):
    print(("PASS " if ok else "FAIL ") + f"例{k}")

x = np.arange(1., 6.)
y = np.array([2., 3., 5., 6., 9.])

def loss(theta):
    w, b = theta
    return float(np.mean((w*x + b - y)**2))

def grad(theta):
    w, b = theta
    e = w*x + b - y
    return np.array([2*np.mean(e*x), 2*np.mean(e)])

# 例1
report(1, all(abs(loss(t)-v) < 1e-10 for t, v in [((0,0),31), ((1,0),5.2), ((1.7,-.1),.22)]))

# 例2
g0 = grad((0,0))
theta1 = np.array([0.,0.]) - .02*g0
report(2, np.allclose(g0, [-36.8,-10]) and np.allclose(theta1, [.736,.2])
       and abs(loss(theta1)-8.797) < .002)

# 例3
theta = np.array([0.,0.])
rows = []
for _ in range(5):
    rows.append((theta.copy(), loss(theta), grad(theta).copy()))
    theta = theta - .02*grad(theta)
expected = [31, 8.797, 2.636, .926, .451]
report(3, all(abs(rows[i][1]-expected[i]) < .01 for i in range(5))
       and np.allclose(rows[1][0], [.736,.2], atol=.001))

# 例4
factors = [1-2*.25, 1-2*.75, 1-2*1, 1-2*1.1]
report(4, np.allclose(factors, [.5,-.5,-1,-1.2]))

# 例5
H = np.array([[22.,6.],[6.,2.]])
ev = np.linalg.eigvalsh(H)
report(5, np.allclose(ev, [12-math.sqrt(136), 12+math.sqrt(136)])
       and abs(2/ev[1]-.084526) < .001 and abs(2/(ev.sum())-1/12) < 1e-10)

# 例6
Hp = np.array([[4.,0.],[0.,2.]])
report(6, np.allclose(np.linalg.eigvalsh(Hp), [2,4]) and abs(4/2-2) < 1e-12)

# 例7
eta = 1/ev[1]
theta7 = np.array([0.,0.]) - eta*g0
bound = 31 - eta/2*np.dot(g0,g0)
report(7, np.allclose(theta7, [1.555, .423], atol=.002)
       and abs(loss(theta7)-.2697) < .01 and loss(theta7) <= bound+.002)

# 例8
Hf = np.array([[2.,1.],[1.,2.]])
Hg = np.array([[2.,3.],[3.,2.]])
Hh = np.array([[2.,2.],[2.,2.]])
report(8, np.all(np.linalg.eigvalsh(Hf)>0) and np.linalg.det(Hg)<0
       and np.all(np.linalg.eigvalsh(Hh)>=-1e-12))

# 例9
X = np.column_stack([x, np.ones(5)])
H9 = 2/5*X.T@X
test = np.array([1.7,-.4])
report(9, np.all(np.linalg.eigvalsh(H9)>=-1e-12)
       and float(test@H9@test) >= -1e-12 and np.all(np.linalg.eigvalsh(H9)>0))

# 例10
single = np.array([[-4.,-4.],[-12.,-6.],[-30.,-10.],[-48.,-12.],[-90.,-18.]])
gb = (single[1] + single[3])/2
allg = single.mean(axis=0)
report(10, np.allclose(gb, [-30,-9]) and np.allclose(allg, [-36.8,-10]))

# 例11
theta = np.array([0.,0.])
v = np.array([0.,0.])
vals = [loss(theta)]
for _ in range(3):
    v = .9*v + grad(theta)
    theta = theta - .02*v
    vals.append(loss(theta))
report(11, np.allclose(theta, [2.624,.705], atol=.01)
       and np.allclose(vals, [31,8.80,.946,14.7], atol=.2))

# 例12
theta = np.array([0.,0.])
m = np.array([0.,0.])
vv = np.array([0.,0.])
for t in range(1,4):
    g = grad(theta)
    m = .9*m + .1*g
    vv = .999*vv + .001*g*g
    mh = m/(1-.9**t)
    vh = vv/(1-.999**t)
    theta = theta - .1*mh/(np.sqrt(vh)+1e-8)
report(12, np.allclose(theta, [.2989,.2988], atol=.002))

# 例13
sgd = np.array([1e-3*1000, 1e-3*.001])
adam = np.array([1e-3, 1e-3])
report(13, np.allclose(sgd, [1,1e-6]) and np.allclose(adam, [1e-3,1e-3]))

# 例14
def schedule(t):
    if t <= 100:
        return 3e-4*t/100
    return 3e-5 + .5*(3e-4-3e-5)*(1+math.cos(math.pi*(t-100)/(1100-100)))
report(14, abs(schedule(50)-1.5e-4)<1e-12
       and abs(schedule(600)-1.65e-4)<1e-12
       and abs(schedule(1100)-3e-5)<1e-12)
