import sympy as sp


def check(i, cond):
    if bool(cond):
        print(f"PASS {i}")
    else:
        print(f"FAIL {i}")
        raise AssertionError(i)

# L10-01
A = sp.Matrix([[1,1],[0,1],[1,0]])
b = sp.Matrix([1,2,0])
G = A.T*A
x = G.inv() * A.T*b
p = A*x
e = b-p
check('L10-01', x == sp.Matrix([-sp.Rational(1,3), sp.Rational(5,3)]) and p == sp.Matrix([sp.Rational(4,3),sp.Rational(5,3),-sp.Rational(1,3)]) and e.dot(A[:,0]) == 0 and e.dot(A[:,1]) == 0 and (e.dot(e) == sp.Rational(1,3)))

# L10-02
q1 = sp.Matrix([1,1,0])/sp.sqrt(2)
q2 = sp.Matrix([1,-1,2])/sp.sqrt(6)
b = sp.Matrix([2,0,1])
p = (q1.dot(b))*q1 + (q2.dot(b))*q2
check('L10-02', sp.simplify(p-sp.Matrix([sp.Rational(5,3),sp.Rational(1,3),sp.Rational(4,3)])) == sp.zeros(3,1) and q1.dot(q2) == 0 and q1.dot(q1) == 1 and q2.dot(q2) == 1)

# L10-03: every option checked
A = sp.Matrix([[1,0],[0,1],[1,1]])
P = A*(A.T*A).inv()*A.T
opts = [P.det() != 0, P**2 == P and P.T == P, P == sp.eye(3), P.T*P == sp.eye(3)]
check('L10-03', opts == [False, True, False, False])

# L10-04
t = sp.Matrix([0,1,2,3]); y = sp.Matrix([1,2,2,4])
A = sp.Matrix([[1,ti] for ti in t])
x = (A.T*A).inv()*A.T*y
res = y-A*x
check('L10-04', x == sp.Matrix([sp.Rational(9,10),sp.Rational(9,10)]) and res == sp.Matrix([sp.Rational(1,10),sp.Rational(1,5),-sp.Rational(7,10),sp.Rational(2,5)]) and sum(res) == 0 and (t.dot(res) == 0))

# L10-05
A = sp.Matrix([[1,1],[2,2],[3,3]]); b = sp.Matrix([1,2,4])
G = A.T*A; rhs = A.T*b
normal_solvable = G.rank() == G.row_join(rhs).rank()
null_dim = len(G.nullspace())
p = A * sp.Matrix([sp.Rational(17,28), sp.Rational(17,28)])
check('L10-05', G.det() == 0 and rhs == sp.Matrix([17,17]) and normal_solvable and null_dim == 1 and p == sp.Matrix([sp.Rational(17,14),sp.Rational(17,7),sp.Rational(51,14)]))
# explicit option truth values: A, B, C, D
option_truth = [not normal_solvable, null_dim == 0, normal_solvable and null_dim > 0 and p == A*sp.Matrix([sp.Rational(17,28),sp.Rational(17,28)]), G.det() != 0]
check('L10-05-options', option_truth == [False,False,True,False])

# L10-06
# The rank-chain existence proof and the null-space characterization require a written proof.
print('MANUAL L10-06')

# L10-07
Q = sp.diag(1,1,-1)
# A is true for the given Q; B and D fail on this Q. C is a universal claim, refuted by a determinant -1 shear.
S = sp.Matrix([[1,1,0],[0,1,0],[0,0,-1]])
opts = [Q.T*Q == sp.eye(3) and Q.det() == -1, (Q+sp.eye(3)).T*(Q+sp.eye(3)) == sp.eye(3), S.T*S == sp.eye(3), Q*sp.Matrix([0,0,1]) == sp.Matrix([0,0,1])]
check('L10-07', opts == [True,False,False,False])

# L10-08
b1 = sp.Matrix([1,1,0]); b2 = sp.Matrix([1,-1,2]); b3 = sp.Matrix([-1,1,1])
check('L10-08', b1.dot(b2)==0 and b1.dot(b3)==0 and b2.dot(b3)==0 and b1.dot(b1)==2 and b2.dot(b2)==6 and b3.dot(b3)==3)

# L10-09
T = [-2,-1,0,1,2]; Y = [4,1,0,2,5]
A = sp.Matrix([[1,t,t*t] for t in T]); y = sp.Matrix(Y)
x = (A.T*A).inv()*A.T*y; res=y-A*x
check('L10-09', x == sp.Matrix([sp.Rational(9,35),sp.Rational(3,10),sp.Rational(15,14)]) and y-A*x == sp.Matrix([sp.Rational(2,35),-sp.Rational(1,35),-sp.Rational(9,35),sp.Rational(13,35),-sp.Rational(1,7)]) and res.dot(res) == sp.Rational(8,35) and A.T*res == sp.zeros(3,1))

# L10-10
n=3; alpha=sp.Matrix([1,2,2])/3
H=sp.eye(n)-2*alpha*alpha.T
check('L10-10', H.T == H and H.T*H == sp.eye(n) and H*H == sp.eye(n))

# L10-11
A=sp.Matrix([[1,2],[2,4],[3,6]]); b=sp.Matrix([1,0,1]); a=sp.Matrix([1,2,3])
z=(a.dot(b))/(a.dot(a)); p=z*a; e=b-p
check('L10-11', z==sp.Rational(2,7) and p==sp.Matrix([sp.Rational(2,7),sp.Rational(4,7),sp.Rational(6,7)]) and e==sp.Matrix([sp.Rational(5,7),-sp.Rational(4,7),sp.Rational(1,7)]) and e.dot(e)==sp.Rational(6,7) and (A.T*A).det()==0)

# L10-12
b1=sp.Matrix([1,1,0,0]); b2=sp.Matrix([1,-1,2,0]); b3=sp.Matrix([1,-1,-1,3]); b=sp.Matrix([1,2,3,4])
q1=b1/sp.sqrt(2); q2=b2/sp.sqrt(6); q3=b3/sp.sqrt(12); p=sum([q1.dot(b)*q1,q2.dot(b)*q2,q3.dot(b)*q3], sp.zeros(4,1)); e=b-p
check('L10-12', b1.dot(b2)==0 and b1.dot(b3)==0 and b2.dot(b3)==0 and p==sp.Matrix([3,0,1,2]) and e==sp.Matrix([-2,2,2,2]))

# L10-13
A=sp.Matrix([[1,-1],[1,0],[1,1]]); b=sp.Matrix([2,0,3]); f=lambda x: (A*x-b).dot(A*x-b)
grad0=2*A.T*(A*sp.zeros(2,1)-b); x01=-sp.Rational(1,10)*grad0; x005=-sp.Rational(1,20)*grad0; xstar=(A.T*A).inv()*A.T*b
eta=sp.symbols('eta', positive=True); one_step=sp.expand(f(-eta*grad0))
check('L10-13', grad0==sp.Matrix([-10,-2]) and x01==sp.Matrix([1,sp.Rational(1,5)]) and x005==sp.Matrix([sp.Rational(1,2),sp.Rational(1,10)]) and f(x01)==sp.Rational(142,25) and f(x005)==sp.Rational(857,100) and xstar==sp.Matrix([sp.Rational(5,3),sp.Rational(1,2)]) and f(xstar)==sp.Rational(25,6) and one_step==308*eta**2-104*eta+13)

# L10-14
A=sp.Matrix([[1,0],[1,1],[2,1]]); b=sp.Matrix([1,2,0]); G=A.T*A; rhs=A.T*b; x=G.inv()*rhs; p=A*x; e=b-p
check('L10-14', A.rank()==2 and G.rank()==2 and x==sp.Matrix([0,1]) and p==sp.Matrix([0,1,1]) and e==sp.Matrix([1,1,-1]) and G.rank()==A.rank())

# L10-15
n=sp.Matrix([1,-1,1]); b=sp.Matrix([2,1,0]); e=(b.dot(n)/n.dot(n))*n; p=b-e
check('L10-15', p==sp.Matrix([sp.Rational(5,3),sp.Rational(4,3),-sp.Rational(1,3)]) and e==sp.Matrix([sp.Rational(1,3),-sp.Rational(1,3),sp.Rational(1,3)]) and p.dot(n)==0 and e.dot(e)==sp.Rational(1,3))

# L10-16
v=sp.Matrix([sp.Rational(5,13),sp.Rational(12,13)])
w1=sp.Matrix([-sp.Rational(12,13),sp.Rational(5,13)]); w2=-w1
check('L10-16', v.dot(w1)==0 and w1.dot(w1)==1 and w2.dot(w2)==1 and sp.Matrix.hstack(v,w1).det()==1 and sp.Matrix.hstack(v,w2).det()==-1)

# L10-17
A=sp.Matrix([[1,0],[0,1],[1,1]])
P=A*(A.T*A).inv()*A.T
check('L10-17', P*P==P and P.T==P and P.rank()==2 and P.det()==0)
