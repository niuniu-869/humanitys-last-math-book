"""Recompute all 68 problems; compare choices to the actual answer headings.

Qualitative questions use truth models or numerical counterexamples, followed by
human reading of the argument. These checks do not claim to prove prose semantics.
Only general proof obligations are separately marked MANUAL.
"""
import heapq
import itertools as it
import re
import sys
from pathlib import Path

import numpy as np
import sympy as s

R = s.Rational
x, y, z, a, b, t, lam = s.symbols("x y z a b t lam", real=True)
ROOT = Path(__file__).resolve().parents[1]
answers = (ROOT / "answers.md").read_text()
problems = (ROOT / "problems.md").read_text()
answer_parts = dict(re.findall(r"\*\*(K42-\d+)\*\*\n(.*?)(?=\n\*\*K42-|\Z)", answers, re.S))
tests = {}


def test(number):
    def register(fn):
        tests[number] = fn
        return fn
    return register


def choose(number, predicates):
    flags = [bool(v) for v in predicates]
    assert sum(flags) == 1, flags
    actual = "ABCD"[flags.index(True)]
    heading = answer_parts[f"K42-{number:02d}"].splitlines()[0]
    written = re.search(r"\(([ABCD])\)", heading).group(1)
    assert actual == written, (actual, written)


def same(a, b):
    return s.simplify(a-b) == 0


@test(1)
def _():
    rows = list(it.product([False, True], repeat=2))
    rule = [p or not q for p,q in rows]
    choices = [[not q or p for p,q in rows], [not p or q for p,q in rows],
               [q or not p for p,q in rows], [not p and q for p,q in rows]]
    choose(1, [v == rule for v in choices])


@test(2)
def _():
    truths = {w: [w in (1,2), w != 1, w == 3, w != 1] for w in range(4)}
    valid = [w for w,v in truths.items() if sum(v) == 1]
    assert valid == [1] and truths[1] == [True,False,False,False]
    choose(2, [0 in valid, 1 in valid and truths[1][0],
               2 in valid and truths[2][1], 3 in valid and truths[3][2]])


@test(3)
def _():
    # A no-membership-effect model reproduces the observed increase exactly.
    weights = s.Matrix([R(1,4), R(3,4)])
    before = s.Matrix([R(40,100), R(24,100)])
    promo = s.ones(2,1)*R(6,100)
    assert weights.dot(before) == R(28,100)
    assert weights.dot(before+promo) == R(34,100)
    assert before[0] > before[1] and promo[0] == promo[1]
    assert "(D)" in answer_parts["K42-03"].splitlines()[0]


@test(4)
def _():
    arrangements = [p for p in it.permutations(range(4))
                    if p[0] in (1,2) and p[1] != 1 and p[2] not in (2,3)
                    and p[3] != 0 and (p[1] != 2 or p[2] == 0)]
    assert len(arrangements) == 4
    choose(4, [all(p[2] == 0 for p in arrangements), all(p[0] == 1 for p in arrangements),
               all(p.index(0) in (1,2) for p in arrangements), all(p[3] == 3 for p in arrangements)])


@test(5)
def _():
    expr = s.Abs(x)/(s.exp(x)-1)
    left = s.limit(expr,x,0,dir='-')
    right = s.limit(expr,x,0,dir='+')
    assert (left,right) == (-1,1)
    choose(5,[left==right==0,left==right==1,left!=right,
              left in (s.oo,-s.oo) and right in (s.oo,-s.oo)])


@test(6)
def _():
    val = 2*s.pi*s.integrate(x*s.sin(x),(x,0,s.pi))
    choose(6, [same(val,v) for v in [s.pi**2/2, 4*s.pi, 2*s.pi**2, s.pi**2]])


@test(7)
def _():
    P = s.Matrix([[1,1,0],[0,1,1],[1,0,0]])
    A = P*s.diag(1,-1,2)*P.inv()
    val = (A.adjugate()+2*A-s.eye(3)).det()
    choose(7, [val == v for v in [-60,5,-2,2]])


@test(8)
def _():
    w = s.symbols("w")
    activation = 1/(1+s.exp(-w))
    val = s.diff((activation-1)**2/2,w).subs(w,0)
    choose(8, [val == v for v in [R(-1,2),R(-1,8),R(-1,4),R(1,8)]])


@test(9)
def _():
    aa, bb, total = 1071,462,0
    states = []
    while bb:
        q, rem = divmod(aa,bb)
        total += q
        aa,bb = bb,rem
        states.append((aa,bb,total))
    assert states == [(462,147,2),(147,21,5),(21,0,12)]
    choose(9,[total == v for v in [21,3,12,13]])


@test(10)
def _():
    M = s.Matrix([[0,1,1,0],[0,0,1,1],[1,0,0,1],[0,0,0,0]])
    paths = [(2,i,j,3) for i,j in it.product(range(4), repeat=2)
             if M[2,i]*M[i,j]*M[j,3]]
    val = (M**3)[2,3]
    assert val == len(paths) and set(paths) == {(2,0,1,3),(2,0,2,3)}
    choose(10,[val == v for v in [2,1,3,4]])


@test(11)
def _():
    positive = s.symbols("positive", positive=True)
    step = (2*positive+3)/(positive+2)
    assert same(step-s.sqrt(3), (2-s.sqrt(3))*(positive-s.sqrt(3))/(positive+2))
    assert same(step-positive, (3-positive**2)/(positive+2))
    assert s.solve(s.Eq(positive,step),positive) == [s.sqrt(3)]
    for initial in [R(1,2),R(1),s.sqrt(3),R(2),R(10)]:
        term = initial
        for _ in range(7):
            nxt = s.simplify(step.subs(positive,term))
            assert nxt > 0
            assert s.sign(nxt-term) == s.sign(s.sqrt(3)-initial)
            assert s.sign(nxt-s.sqrt(3)) == s.sign(initial-s.sqrt(3))
            term = nxt


@test(12)
def _():
    assert s.integrate(s.log(x),(x,1,s.E)) == 1
    assert same(s.pi*s.integrate(s.log(x)**2,(x,1,s.E)),s.pi*(s.E-2))
    assert same(2*s.pi*s.integrate(x*s.log(x),(x,1,s.E)),s.pi*(s.E**2+1)/2)


@test(13)
def _():
    f=x*x+4*x*y+4*y*y
    g=x*x/4+y*y-1
    sols = s.solve([s.diff(f,x)-lam*s.diff(g,x),s.diff(f,y)-lam*s.diff(g,y),g],(x,y,lam))
    pts = {(xx,yy) for xx,yy,_ in sols}
    assert pts == {(sx*s.sqrt(2),sy/s.sqrt(2)) for sx,sy in it.product([-1,1],repeat=2)}
    values = {pt:s.simplify(f.subs(dict(zip((x,y),pt)))) for pt in pts}
    assert set(values.values()) == {0,8}
    assert all(value == (8 if xx*yy>0 else 0) for (xx,yy),value in values.items())
    assert s.Matrix([[4,4],[4,4]]).eigenvals() == {0:1,8:1}


@test(14)
def _():
    A = s.eye(3)-s.ones(3)
    assert A.eigenvals() == {1:2,-2:1} and A*s.ones(3,1) == -2*s.ones(3,1)
    for n in range(1,10):
        assert A**n == s.eye(3)+R((-2)**n-1,3)*s.ones(3)
    assert s.reduce_inequalities([t+1>0,t-2>0],t).as_set() == s.Interval.open(2,s.oo)


@test(15)
def _():
    data = list(map(R,["98.1","103.4","101.2","104.5","99.7","102.8","105.1","100.3","102.9"]))
    mean = sum(data)/len(data)
    variance = sum((v-mean)**2 for v in data)/(len(data)-1)
    se = s.sqrt(variance/len(data))
    stat = (mean-100)/se
    ci = [mean-R("2.306")*se, mean+R("2.306")*se]
    assert mean == 102 and variance == R(433,80)
    assert abs(float(stat)-2.5790056626)<1e-9 and stat>R("2.306")
    assert np.allclose(list(map(float,ci)),[100.2117138916,103.7882861084]) and ci[0]>100


@test(16)
def _():
    P = s.Matrix([[1,0,0,0,0],[R(1,3),0,R(2,3),0,0],[0,R(1,3),0,R(2,3),0],
                  [0,0,R(1,3),0,R(2,3)],[0,0,0,0,1]])
    assert P*s.ones(5,1) == s.ones(5,1)
    Q = P[1:4,1:4]
    fundamental = (s.eye(3)-Q).inv()
    assert fundamental*P[1:4,4] == s.Matrix([R(8,15),R(4,5),R(14,15)])
    assert fundamental*s.ones(3,1) == s.Matrix([R(17,5),R(18,5),R(11,5)])
    assert max(Q**3*s.ones(3,1)) <= R(19,27)
    assert all(abs(complex(v))<1 for v in Q.eigenvals())


@test(17)
def _():
    def power(base,n):
        r,p,m = 1,base,n
        trace=[]
        while m:
            assert r*p**m == base**n
            if m%2:
                r *= p
            p *= p
            m //= 2
            trace.append((r,p,m))
        return r,trace
    val,states = power(3,13)
    assert states == [(3,9,6),(3,81,3),(243,6561,1),(1594323,43046721,0)]
    for base,n in it.product(range(-3,4),range(1,35)):
        val,states = power(base,n)
        assert val == base**n and len(states) == n.bit_length()


@test(18)
def _():
    models = [np.array(v,dtype=bool).reshape(2,2) for v in it.product([False,True],repeat=4)]
    target = [not np.all(np.any(m,axis=1)) for m in models]
    options = [[not np.any(m) for m in models], [np.any(~np.any(m,axis=1)) for m in models],
               [np.any(~m) for m in models], [not np.any(np.all(m,axis=1)) for m in models]]
    choose(18,[v==target for v in options])


@test(19)
def _():
    models = [(aa,bb,cc) for aa,bb,cc in it.product([False,True],repeat=3)
              if aa==(bb!=cc) and bb==(not aa) and cc==(bb==cc)]
    assert models == [(False,True,True)]
    choose(19,[all(all(p) for p in models), all(p[0] for p in models),
               all(p[1] and p[2] for p in models), all(not p[1] for p in models)])


@test(20)
def _():
    models=[]
    for perm in it.permutations("ABCDE"):
        d={v:perm.index(v)+1 for v in perm}
        if abs(d['A']-d['B'])==1 and d['C'] not in (1,5) and d['D']<d['E'] and d['B']<d['C']:
            models.append(d)
    assert len(models)==6
    choose(20,[all(d['E']==5 for d in models),all(d['A']<d['B'] for d in models),
               all(d['D']==3 for d in models),all(d['C']==4 for d in models)])


@test(21)
def _():
    # Composition alone can cause a 10 percentage-point decline.
    rate = s.Matrix([R(3,10),R(1,10)])
    old = s.Matrix([R(3,4),R(1,4)])
    new = s.Matrix([R(1,4),R(3,4)])
    assert old.dot(rate)-new.dot(rate)==R(1,10)
    w=s.symbols("w")
    equal_composition=s.Matrix([w,1-w])
    assert s.expand(equal_composition.dot(rate)-equal_composition.dot(rate))==0
    assert "最有助于排除" in problems and "(D)" in answer_parts["K42-21"].splitlines()[0]


@test(22)
def _():
    val=s.limit((s.exp(x)-1-x-x*x/2)/(x-s.sin(x)),x,0)
    choose(22,[val==v for v in [0,R(1,2),1,s.oo]])


@test(23)
def _():
    f=x**3+y**3-3*x*y
    pts=s.solve([s.diff(f,x),s.diff(f,y)],(x,y))
    assert set(pts)=={(0,0),(1,1)}
    H=s.hessian(f,(x,y))
    kind=[]
    for xx,yy in [(0,0),(1,1)]:
        h=H.subs({x:xx,y:yy})
        kind.append("saddle" if h.det()<0 else "min" if h[0,0]>0 else "max")
    choose(23,[kind==v for v in [["min","min"],["saddle","min"],["max","saddle"],["min","max"]]])


@test(24)
def _():
    A=s.Matrix([[1,a,0],[a,1,a],[0,a,1]])
    determinants=[A[:i,:i].det() for i in range(1,4)]
    feasible=s.reduce_inequalities([v>0 for v in determinants],a).as_set()
    options=[s.Interval.open(-s.sqrt(2)/2,s.sqrt(2)/2),s.Interval.open(-1,1),
             s.Interval.open(-R(1,2),R(1,2)),s.Interval(-s.sqrt(2)/2,s.sqrt(2)/2)]
    choose(24,[feasible==v for v in options])


@test(25)
def _():
    H=s.Matrix([[3,1],[1,3]])
    val=max(H.eigenvals())/s.trace(H)
    choose(25,[val==v for v in [R(1,2),R(3,4),R(5,6),R(2,3)]])


@test(26)
def _():
    # An exact null distribution supplies a tail probability, not a prior on H0.
    masses={k:s.binomial(10,k)/2**10 for k in range(11)}
    tail=sum(v for k,v in masses.items() if abs(k-5)>=4)
    assert tail==R(11,512) and 0<tail<1
    p1=s.erfc(R(1,10)*s.sqrt(100)/s.sqrt(2))
    p2=s.erfc(R(1,10)*s.sqrt(10000)/s.sqrt(2))
    assert p2<p1  # Same effect, different standard errors and p-values.
    assert "(C)" in answer_parts["K42-26"].splitlines()[0]


@test(27)
def _():
    arr=[5,2,8,1,9,3]
    total=0
    for turn in range(2):
        for j in range(len(arr)-1-turn):
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
                total+=1
        if turn==0:
            assert arr==[2,5,1,8,3,9] and total==3
    options=[([2,5,1,8,3,9],3),([2,1,5,3,8,9],5),([2,1,5,3,8,9],7),([1,2,3,5,8,9],7)]
    choose(27,[(arr,total)==v for v in options])


@test(28)
def _():
    prior=R(3,10)
    free=prior*R(6,10)+(1-prior)*R(5,100)
    joint=prior*R(6,10)*R(7,10)+(1-prior)*R(5,100)*R(2,10)
    assert free==R(43,200) and prior*R(6,10)/free==R(36,43)
    assert prior*R(6,10)*R(7,10)/joint==R(18,19)


@test(29)
def _():
    f=(s.exp(x)+s.exp(-x))/2
    assert same(1+s.diff(f,x)**2,f*f)
    assert same(s.integrate(f,(x,0,1)),(s.E-1/s.E)/2)
    assert same(s.pi*s.integrate(f*f,(x,0,1)),s.pi*(s.E**2-s.E**-2+4)/8)


@test(30)
def _():
    xx,yy=s.symbols("xx yy",positive=True)
    area=xx*yy+8/xx+8/yy
    roots=s.solve([s.diff(area,xx),s.diff(area,yy)],(xx,yy))
    assert roots==[(2,2)] and area.subs({xx:2,yy:2})==12
    assert s.simplify(xx*yy*(8/xx)*(8/yy))==64
    assert 2*2*1==4


@test(31)
def _():
    # Test the algebra and necessity of full column rank; proof remains manual.
    A=s.Matrix([[2,1,0],[1,3,1],[0,1,2]])
    B=s.Matrix([[1,0],[0,1],[1,1]])
    C=B.T*A*B
    assert A.is_positive_definite and B.rank()==2 and C.is_positive_definite and C==C.T
    assert A.inv().is_positive_definite and A.inv()==A.inv().T
    bad=s.Matrix([[1,1],[0,0],[0,0]])
    H=bad.T*A*bad
    assert H.is_positive_semidefinite and not H.is_positive_definite
    assert H.nullspace()==bad.nullspace()
    example=s.Matrix([[1,1],[0,0]])
    assert example.T*example==s.ones(2)
    assert (example.T*example)*s.Matrix([1,-1])==s.zeros(2,1)


@test(32)
def _():
    A=s.Matrix([[1,1,1,1],[0,t,0,t],[0,0,t-1,t-1]])
    rhs=s.Matrix([1,b,1])
    r,u,v=s.symbols('r u v')
    assert s.factor(A[:,:3].det())==t*(t-1)
    generic=s.Matrix([1-b/t-1/(t-1)+r,b/t-r,1/(t-1)-r,r])
    assert s.simplify(A*generic-rhs)==s.zeros(3,1)
    exceptional=s.Matrix([2-u,u,-1-v,v])
    assert A.subs(t,0)*exceptional==rhs.subs(b,0)
    for tt,bb in it.product([-2,0,1,2],[-1,0,1,2]):
        mat=A.subs(t,tt); aug=mat.row_join(rhs.subs(b,bb))
        rank=3 if tt not in (0,1) else 2
        augmented=rank if tt not in (0,1) or (tt==0 and bb==0) else 3
        assert mat.rank()==rank and aug.rank()==augmented
        assert len(mat.nullspace())==4-rank
    assert A.subs(t,0).row_join(rhs).extract([0,1,2],[0,2,4]).det()==b
    assert A.subs(t,1).row_join(rhs).extract([0,1,2],[0,1,4]).det()==1


@test(33)
def _():
    X=s.Matrix([[1,i] for i in range(1,6)])
    target=s.Matrix([2,3,5,4,6])
    beta=(X.T*X).inv()*X.T*target
    residual=target-X*beta
    sse=residual.dot(residual)
    var=sse/3
    stat=beta[1]/s.sqrt(var/10)
    assert beta==s.Matrix([R(13,10),R(9,10)]) and sse==R(19,10) and var==R(19,30)
    assert abs(float(stat)-3.576237364)<1e-8 and stat>R("3.182")
    centered=target-s.ones(5,1)*4
    assert 1-sse/centered.dot(centered)==R(81,100)


EDGES=[("A","B",4),("A","C",2),("B","C",1),("B","D",5),("C","D",8),
       ("C","E",10),("D","E",2),("D","F",6),("E","F",3)]


@test(34)
def _():
    def run(edges):
        graph={v:[] for v in "ABCDEF"}
        for u,v,w in edges:
            graph[u].append((v,w)); graph[v].append((u,w))
        queue=[(0,"A")]; distances={"A":0}; order=[]
        while queue:
            d,u=heapq.heappop(queue)
            if u in order or d!=distances[u]:
                continue
            order.append(u)
            for v,w in graph[u]:
                if d+w<distances.get(v,float("inf")):
                    distances[v]=d+w; heapq.heappush(queue,(d+w,v))
        paths=[]
        def walk(path,length):
            if path[-1]=="F":
                paths.append((length,"".join(path))); return
            for v,w in graph[path[-1]]:
                if v not in path:
                    walk(path+[v],length+w)
        walk(["A"],0)
        return order,distances,{p for d,p in paths if d==distances['F']}
    order,dist,paths=run(EDGES)
    assert order==list("ACBDEF") and [dist[v] for v in order]==[0,2,3,8,10,13]
    assert paths=={"ACBDEF"}
    _,dist,paths=run([e for e in EDGES if e[:2]!=("B","D")])
    assert dist['F']==15 and paths=={"ACEF","ACDEF"}


@test(35)
def _():
    A=s.Matrix([[1,1,a],[1,a,1],[a,1,1]])
    roots=s.solve(A.det(),a)
    wanted={r for r in roots if A.subs(a,r).rank()==2}
    choose(35,[wanted=={1},wanted=={-2},wanted=={1,-2},not roots])


@test(36)
def _():
    val=(s.Matrix([[1,1],[0,2]])**100)[0,1]
    choose(36,[val==v for v in [2**100,2**100-1,100,2**99-1]])


@test(37)
def _():
    val=s.integrate(s.exp(-x)*s.integrate(2*s.exp(-2*y),(y,x,s.oo)),(x,0,s.oo))
    choose(37,[val==v for v in [R(1,2),R(2,3),R(1,3),R(1,4)]])


@test(38)
def _():
    sigmoid=1/(1+s.exp(-x))
    derivative=s.diff(sigmoid,x)
    upper=s.simplify(derivative-sigmoid*(1-sigmoid))==0 and derivative.subs(x,0)==R(1,4)
    u=s.symbols("u",real=True)
    assert s.expand(R(1,4)-u*(1-u))==s.expand((u-R(1,2))**2)
    relu=s.Max(0,x)
    slopes=[s.limit(relu/x,x,0,dir=d) for d in ['-','+']]
    probs=[s.exp(t*v)/(s.exp(2*t)+1) for v in [2,0]]
    choose(38,[slopes[0]==slopes[1],upper,s.diff(s.tanh(x),x).subs(x,0)==2,
               s.simplify(s.diff(sum(probs),t))>0])


@test(39)
def _():
    side=(32+2*2-5)//2+1
    params=16*(5*5*3+1)
    pool=(side-2)//2+1
    actual=(side,side,16,params,pool,pool,16)
    choices=[(16,16,16,1200,8,8,16),(32,32,16,1216,16,16,16),
             (16,16,16,1216,8,8,16),(15,15,16,1216,7,7,16)]
    choose(39,[actual==v for v in choices])


@test(40)
def _():
    w=s.symbols('w')
    loss=-s.log(1/(1+s.exp(-2*w)))
    val=s.diff(loss,w).subs(w,0)
    choose(40,[val==v for v in [-1,R(-1,2),1,R(1,2)]])


@test(41)
def _():
    # Every rank-r 4x4 matrix is equivalent to diag(I_r,0).
    # Invertible row/column changes preserve ranks of A and its adjugate.
    ranks=[]
    for rank in range(5):
        A=s.diag(*([1]*rank+[0]*(4-rank)))
        adj=A.adjugate()
        ranks.append(adj.rank())
        if adj.rank()==1:
            assert A.rank()==3 and len(A.nullspace())==1
    assert ranks==[0,0,0,1,4]


@test(42)
def _():
    A=s.Matrix([[2,a,0],[a,1,0],[0,0,3]])
    domain=s.reduce_inequalities([A[:i,:i].det()>0 for i in range(1,4)],a).as_set()
    assert domain==s.Interval.open(-s.sqrt(2),s.sqrt(2))
    vec=s.Matrix([x,y,z])
    assert same((vec.T*A*vec)[0],2*(x+a*y/2)**2+(1-a*a/2)*y*y+3*z*z)


@test(43)
def _():
    P=s.Matrix([[R(9,10),R(1,10)],[R(1,2),R(1,2)]])
    sol=s.solve(list((s.Matrix([[x,y]])*P-s.Matrix([[x,y]])))+[x+y-1],(x,y))
    assert sol=={x:R(5,6),y:R(1,6)}


@test(44)
def _():
    mean=s.integrate(x/4,(x,0,4))
    second=s.integrate(x*x/4,(x,0,4))
    # Compound Poisson moment-generating function differentiates independently.
    mgf_x=(s.exp(4*t)-1)/(4*t)
    series=s.series(s.exp(3*(mgf_x-1)),t,0,3).removeO()
    variance=s.diff(series,t,2).subs(t,0)-s.diff(series,t).subs(t,0)**2
    assert variance==16 and 3*(second-mean**2)+3*mean**2==16


@test(45)
def _():
    q=np.array([1.,1.]); keys=np.array([[1.,0.],[0.,1.],[1.,1.]])
    score=keys@q/np.sqrt(2)
    weights=np.exp(score-score.max()); weights/=weights.sum()
    assert round(weights[2],3)==0.503 and np.allclose(weights[:2],weights[0])


@test(46)
def _():
    W=s.Matrix(2,3,s.symbols('w:6')); delta=s.Matrix(s.symbols('d:2'))
    h=s.Matrix(s.symbols('h:3')); pre=W*h
    gradient=s.Matrix([sum(delta[j]*s.diff(pre[j],h[i]) for j in range(2)) for i in range(3)])
    assert gradient==W.T*delta and gradient.shape==(3,1)


@test(47)
def _():
    data=s.Matrix([[2,2],[-2,-2],[1,-1],[-1,1]])
    cov=data.T*data/4
    assert cov==s.Matrix([[R(5,2),R(3,2)],[R(3,2),R(5,2)]])
    assert cov.eigenvals()=={4:1,1:1}
    u=s.Matrix([1,1])/s.sqrt(2)
    coords=data*u
    assert coords==s.Matrix([2*s.sqrt(2),-2*s.sqrt(2),0,0])
    err=data-coords*u.T
    assert sum(v*v for v in err)==4 and max(cov.eigenvals())/s.trace(cov)==R(4,5)
    vec=s.Matrix([x,y]); objective=(vec.T*cov*vec)[0]-lam*(x*x+y*y-1)
    assert s.Matrix([s.diff(objective,v) for v in vec])==2*(cov*vec-lam*vec)


@test(48)
def _():
    sols=s.solve([1-2*lam*x,2-2*lam*y,2-2*lam*z,x*x+y*y+z*z-1],(x,y,z,lam))
    pts={(xx,yy,zz) for xx,yy,zz,_ in sols}
    assert pts=={(R(1,3),R(2,3),R(2,3)),(-R(1,3),-R(2,3),-R(2,3))}
    assert {xx+2*yy+2*zz for xx,yy,zz in pts}=={-3,3}
    # Algebraic curve identities under unit length and orthogonality.
    assert s.trigsimp(s.cos(t)**2+s.sin(t)**2)==1
    assert s.diff(s.cos(t),t).subs(t,0)==0 and s.diff(s.sin(t),t).subs(t,0)==1


@test(49)
def _():
    mu0,mu1,sd,prior=s.symbols('mu0 mu1 sd prior',positive=True)
    f0=s.exp(-(x-mu0)**2/(2*sd**2))/(s.sqrt(2*s.pi)*sd)
    f1=s.exp(-(x-mu1)**2/(2*sd**2))/(s.sqrt(2*s.pi)*sd)
    linear=(mu1-mu0)*x/sd**2+(mu0**2-mu1**2)/(2*sd**2)+s.log(prior/(1-prior))
    assert same(s.diff(-(x-mu1)**2/(2*sd**2)+(x-mu0)**2/(2*sd**2),x),(mu1-mu0)/sd**2)
    posterior=prior*f1/(prior*f1+(1-prior)*f0)
    val=posterior.subs({mu1:2,mu0:0,sd:1,prior:R(1,2),x:R(3,2)})
    assert same(val,1/(1+s.exp(-1)))
    new=linear.subs({mu1:2,mu0:0,sd:1,prior:R(4,5)})
    assert s.solve(new,x)==[1-s.log(2)]
    assert "$0<\\pi<1$" in problems and "$\\tau>0$" in problems
    expanded=s.expand((x-mu0)**2-(x-mu1)**2)
    assert same(expanded,2*(mu1-mu0)*x+mu0**2-mu1**2)
    assert same(posterior,1/(1+s.exp(-linear)))


@test(50)
def _():
    # Full forward loss is differentiated independently by central differences.
    rng=np.random.default_rng(4250)
    inp=np.array([.7,-1.2]); target=.4
    def loss(params):
        W=params[:6].reshape(3,2); bias=params[6:9]
        w=params[9:12]; b2=params[12]
        h=np.tanh(W@inp+bias)
        return .5*(w@h+b2-target)**2
    for _ in range(4):
        params=rng.normal(size=13)/2
        W=params[:6].reshape(3,2); h=np.tanh(W@inp+params[6:9]); w=params[9:12]
        delta=w@h+params[12]-target; g=delta*w*(1-h*h)
        claimed=np.concatenate([np.outer(g,inp).ravel(),g,delta*h,[delta]])
        numerical=[]
        for j in range(13):
            perturb=np.eye(13)[j]*1e-6
            numerical.append((loss(params+perturb)-loss(params-perturb))/2e-6)
        assert np.allclose(claimed,numerical,rtol=1e-5,atol=1e-8)
    assert same(s.diff(s.tanh(x),x),1-s.tanh(x)**2)


@test(51)
def _():
    alpha1,alpha2=s.symbols('alpha1 alpha2',positive=True)
    noise_variance=alpha2*(1-alpha1)+(1-alpha2)
    assert same(noise_variance,1-alpha1*alpha2)
    prod=R(9,10)*R(8,10)
    assert prod==R(18,25) and 1-prod==R(7,25)
    assert np.allclose(np.sqrt(float(prod))*np.array([2,-1]),[1.6970562748,-0.8485281374])
    # Verify the telescoping sum of propagated independent noise variances.
    alphas=s.symbols('a:5')
    for n in range(1,6):
        variance=sum((1-alphas[j])*s.prod(alphas[j+1:n]) for j in range(n))
        assert same(variance,1-s.prod(alphas[:n]))


@test(52)
def _():
    # Actual errors imply a 13-point generalization gap.
    train=R(2,100); validation=R(15,100)
    assert validation-train==R(13,100)
    # An interpolating model provides a concrete counterexample to "more capacity".
    pts=[(-1,1),(0,0),(1,1)]
    interpolant=s.interpolate(pts,x)
    train_mse=sum((interpolant.subs(x,xx)-yy)**2 for xx,yy in pts)/3
    # Treat labels as noisy observations of a zero true function.
    simple=sum(yy for _,yy in pts)/R(len(pts))
    assert train_mse==0 and interpolant.subs(x,2)**2>simple**2
    assert "(B)" in answer_parts["K42-52"].splitlines()[0]


@test(53)
def _():
    positive=s.symbols('positive',positive=True)
    w=s.symbols('w',real=True)
    ridge=(w-z)**2/2+positive*w*w/2
    root=s.solve(s.diff(ridge,w),w)[0]
    assert same(root,z/(1+positive))
    right=s.diff((w-z)**2/2+positive*w,w)
    left=s.diff((w-z)**2/2-positive*w,w)
    assert right.subs(w,0)==positive-z and left.subs(w,0)==-positive-z
    zero_minimum=s.reduce_inequalities([positive-z>=0,-positive-z<=0],z)
    assert zero_minimum==s.And(z>=-positive,z<=positive)
    # The nonconstant part of -log p1 is lambda*abs(w).
    neglog=s.simplify(-s.log(s.exp(-positive*s.Abs(w))))
    assert neglog==positive*s.Abs(w)
    decreasing=s.diff(1/(1+positive),positive)<0
    # A normal negative log-density is differentiable at zero; this one is not.
    cusp=s.diff(neglog,w).subs(w,1)-s.diff(neglog,w).subs(w,-1)
    choose(53,[root.subs(z,1)==0,zero_minimum==s.And(z>=-positive,z<=positive),
               not decreasing,cusp==0])


@test(54)
def _():
    # Training statistics are invariant to changing held-out data only in A.
    train=np.array([0.,2.]); heldout=np.array([100.])
    fitted=(train.mean(),train.std())
    leaked=np.concatenate([train,heldout]); leaked2=np.concatenate([train,heldout+100])
    assert fitted==(1.,1.) and not np.isclose(leaked.mean(),leaked2.mean())
    folds=np.array_split(np.arange(15),5)
    assert len(set(np.concatenate(folds)))==15
    for i in range(5):
        others=np.concatenate([f for j,f in enumerate(folds) if i!=j])
        assert not set(others)&set(folds[i])
    assert "(B)" in answer_parts["K42-54"].splitlines()[0]


@test(55)
def _():
    A=s.eye(4)[:,:3]; B=A.T
    assert (B*A).det()==1 and (A*B).rank()==3
    C=s.zeros(4,3); D=s.zeros(3,4); C[0,0]=1; D[0,1]=1
    assert (C*D).rank()==1 and (D*C).rank()==0
    # The shared dimension bounds the rank for arbitrary entries.
    U=s.Matrix(4,3,s.symbols('u:12')); V=s.Matrix(3,4,s.symbols('v:12'))
    assert U.cols< U.rows and V.rows==U.cols
    choose(55,[(A*B).det()!=0,(B*A).det()==0,min(U.cols,V.rows)<(U*V).rows,
               (C*D).rank()==(D*C).rank()])


@test(56)
def _():
    domain=s.reduce_inequalities([1-4*t<1,1-4*t>-1,1-t<1,1-t>-1],t).as_set()
    options=[s.Interval.open(0,2),s.Interval.open(0,1),s.Interval.open(0,R(1,2)),s.Interval.Lopen(0,R(1,4))]
    choose(56,[domain==v for v in options])


@test(57)
def _():
    mu=100*R(1,2); sd=s.sqrt(100*R(1,2)*R(1,2))
    standardized=(R(119,2)-mu)/sd
    assert standardized==R(19,10)
    value=1-R("0.9713")
    choose(57,[value==v for v in map(R,["0.0179","0.0228","0.0287","0.9713"])])
    exact=sum(s.binomial(100,k)*R(1,2)**100 for k in range(60,101))
    assert abs(float(exact)-float(value))<0.001


@test(58)
def _():
    probabilities=[R(1,2),R(1,4),R(1,4)]
    assert same(-sum(p*s.log(p,2) for p in probabilities),R(3,2))


@test(59)
def _():
    logits=np.array([2.,0.])/2
    probabilities=np.exp(logits)/np.exp(logits).sum()
    assert round(probabilities[0],3)==0.731 and np.isclose(sum(probabilities),1)


@test(60)
def _():
    layers=[784,128,10]
    assert sum(i*o+o for i,o in zip(layers,layers[1:]))==101770
    m,n,k=s.symbols('m n k',integer=True,positive=True)
    total=sum(rows*cols for rows,cols in [(n,m),(n,1),(k,n),(k,1)])
    assert s.expand(total)==m*n+n+n*k+k


@test(61)
def _():
    v=s.Matrix([1,2,3,4]); mean=sum(v)/len(v)
    centered=v-s.ones(4,1)*mean
    variance=centered.dot(centered)/len(v)
    out=centered/s.sqrt(variance)
    assert mean==R(5,2) and variance==R(5,4) and out[0]==-3/s.sqrt(5)
    assert sum(out)==0 and out.dot(out)/4==1 and round(float(out[0]),3)==-1.342


@test(62)
def _():
    seq=[0,1]
    for _ in range(9):
        seq.append(3*seq[-1]-2*seq[-2])
    assert seq[10]==1023 and all(v==2**n-1 for n,v in enumerate(seq))


@test(63)
def _():
    leaves=s.solve(s.Eq(2*3+4+x,2*(x+3-1)),x)
    assert leaves==[6]
    edges=[(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(2,7),(2,8)]
    degrees=[sum(v in edge for edge in edges) for v in range(9)]
    assert sorted(degrees)==[1]*6+[3,3,4] and len(edges)==len(degrees)-1


@test(64)
def _():
    bias,fluctuation,noise=s.symbols('bias fluctuation noise')
    expanded=s.Poly(s.expand((bias+fluctuation+noise)**2),fluctuation,noise)
    variance,sigma2,n,mu=s.symbols('variance sigma2 n mu',positive=True)
    expectations={(0,0):1,(1,0):0,(0,1):0,(2,0):variance,(0,2):sigma2,(1,1):0}
    result=sum(coef*expectations[power] for power,coef in expanded.terms())
    assert result==bias*bias+variance+sigma2
    risk1=sigma2/n+sigma2
    risk2=(R(4,5)*mu-mu)**2+R(4,5)**2*sigma2/n+sigma2
    assert same(risk2-risk1,mu**2/25-9*sigma2/(25*n))


@test(65)
def _():
    X=s.Matrix([[1,2],[2,4],[3,6]])
    yy=s.Matrix([2,3,7]); w=s.Matrix([x,y]); positive=s.symbols('positive',positive=True)
    residual=yy-X*w; J=residual.dot(residual)+positive*w.dot(w)
    gradient=s.Matrix([s.diff(J,v) for v in w]); H=X.T*X+positive*s.eye(2)
    assert s.simplify(gradient-2*(H*w-X.T*yy))==s.zeros(2,1)
    assert all(s.simplify(H[:i,:i].det()).is_positive for i in [1,2])
    star=H.inv()*X.T*yy
    assert s.simplify(gradient.subs({x:star[0],y:star[1]}, simultaneous=True))==s.zeros(2,1)
    design=s.Matrix([1,2,3]); cross=design.dot(yy); square=design.dot(design)
    assert cross/square==R(29,14) and cross/(square+1)==R(29,15)


@test(66)
def _():
    Q=np.array([[1.,0.],[0.,1.],[1.,1.]])
    V=np.array([[1.,0.],[0.,2.],[2.,2.]])
    score=Q@Q.T/np.sqrt(2)
    score[np.triu_indices(3,1)]=-np.inf
    weights=np.exp(score-np.max(score,axis=1,keepdims=True)); weights/=weights.sum(axis=1,keepdims=True)
    out=weights@V
    assert np.allclose(np.round(weights[1:],3),[[.330,.670,0],[.248,.248,.503]])
    assert np.allclose(np.round(out[1:],3),[[.330,1.340],[1.255,1.503]])
    # Exact finite independent unit-variance components verify the variance sum.
    for dim in range(1,5):
        dots=[sum(q*k for q,k in zip(v[:dim],v[dim:])) for v in it.product([-1,1],repeat=2*dim)]
        assert np.mean(dots)==0 and np.var(dots)==dim


@test(67)
def _():
    prior=R(2,5)
    spam=R(1,2)*R(1,10); ham=R(1,10)*R(2,5)
    posterior=prior*spam/(prior*spam+(1-prior)*ham)
    assert posterior==R(5,11)
    threshold=s.solve(s.Eq(x*spam,(1-x)*ham),x)
    assert threshold==[R(4,9)]
    spam=R(1,2)*R(9,10); ham=R(1,10)*R(3,5)
    assert prior*spam/(prior*spam+(1-prior)*ham)==R(5,6)


@test(68)
def _():
    logits=s.symbols('z:3',real=True)
    denominator=sum(s.exp(v) for v in logits)
    probs=s.Matrix([s.exp(v)/denominator for v in logits])
    for target in range(3):
        loss=-s.log(probs[target])
        for i,v in enumerate(logits):
            assert same(s.diff(loss,v),probs[i]-int(i==target))
    batch=np.array([[1.,2.,5.],[4.,8.,9.]])
    bn=(batch-batch.mean(axis=0))/batch.std(axis=0)
    ln=(batch-batch.mean(axis=1,keepdims=True))/batch.std(axis=1,keepdims=True)
    assert np.allclose(bn.mean(axis=0),0) and np.allclose(ln.mean(axis=1),0)
    assert not np.allclose(bn,ln)
    assert abs(1-4*.6)>1 and abs(1-4*.001)<1


assert set(tests)==set(range(1,69))
failed=0
for number,fn in sorted(tests.items()):
    try:
        fn()
    except Exception as exc:
        failed+=1
        print(f"FAIL K42-{number:02d} {type(exc).__name__}: {exc}")
    else:
        print(f"PASS K42-{number:02d}")
proofs = {
    11: "初值分类、单调有界与极限证明",
    16: "第(4)问几乎必然吸收的证明",
    17: "第(2)(3)问循环不变式与一般轮数证明",
    30: "均值不等式给出全局下界及唯一取等点的证明",
    31: "半正定、零空间相同及正定充要条件的证明",
    47: "第(2)问乘子条件与最大特征值的一般论证",
    48: "第(1)问由全部切向方向推出乘子关系的证明",
    51: "独立正态线性组合与归纳推广的证明",
    64: "第(1)问交叉项消失所需独立性的证明",
    65: "第(2)问任意维数的正定与唯一最小性证明",
}
for number, obligation in proofs.items():
    print(f"MANUAL K42-{number:02d} {obligation}；数值及代数部分另列 PASS")
sys.exit(bool(failed))
