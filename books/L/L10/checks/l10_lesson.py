import sympy as sp

def check(k, cond):
    if cond:
        print(f"PASS 例{k}")
    else:
        print(f"FAIL 例{k}")
        raise AssertionError(k)

# 例1
A=sp.Matrix([[1,0],[1,1],[1,2]]); b=sp.Matrix([6,0,0]); x=(A.T*A).inv()*A.T*b; p=A*x; e=b-p
check(1, x==sp.Matrix([5,-3]) and p==sp.Matrix([5,2,-1]) and e==sp.Matrix([1,-2,1]) and e.dot(e)==6 and A.T*e==sp.zeros(2,1))

# 例2
A=sp.Matrix([[1,1],[1,1],[1,-1],[1,0]]); b=sp.Matrix([3,4,2,0]); x=(A.T*A).inv()*A.T*b; p=A*x; e=b-p
check(2, x==sp.Matrix([2,1]) and p==sp.Matrix([3,3,1,2]) and e==sp.Matrix([0,1,1,-2]) and A.T*e==sp.zeros(2,1))

# 例3
q1=sp.Matrix([1,1,1,1])/2; q2=sp.Matrix([1,1,-1,-1])/2; q3=sp.Matrix([1,-1,1,-1])/2; q4=sp.Matrix([1,-1,-1,1])/2; b=sp.Matrix([5,3,1,-1])
coords=[q.dot(b) for q in [q1,q2,q3,q4]]; p=coords[0]*q1+coords[1]*q2; e=b-p
check(3, coords==[4,4,2,0] and p==sp.Matrix([4,4,0,0]) and e==sp.Matrix([1,-1,1,-1]))

# 例4
# Verify the displayed matrix has the claimed parameter and orthogonality
a=b=c=sp.Rational(1,3); Q=sp.Matrix([[a,sp.Rational(2,3),sp.Rational(2,3)],[sp.Rational(2,3),b,-sp.Rational(2,3)],[sp.Rational(2,3),-sp.Rational(2,3),c]])
check(4, Q.T*Q==sp.eye(3) and Q.inv()==Q.T and Q.det()==-1)

# 例5
# determinant identity for an explicit orthogonal reflection
Q=sp.diag(1,1,-1)
check(5, Q.T*Q==sp.eye(3) and Q.det()==-1 and (sp.eye(3)+Q).det()==0)

# 例6
v1=sp.Matrix([1,1,0]); v2=sp.Matrix([1,-1,2]); v3=sp.Matrix([-1,1,1])
check(6, v1.dot(v2)==0 and v1.dot(v3)==0 and v2.dot(v3)==0 and v1.dot(v1)==2 and v2.dot(v2)==6 and v3.dot(v3)==3)

# 例7
T=[1,2,3,4]; Y=[1,3,4,6]; A=sp.Matrix([[1,t] for t in T]); y=sp.Matrix(Y); x=(A.T*A).inv()*A.T*y; e=y-A*x
check(7, x==sp.Matrix([-sp.Rational(1,2),sp.Rational(8,5)]) and e==sp.Matrix([-sp.Rational(1,10),sp.Rational(3,10),-sp.Rational(3,10),sp.Rational(1,10)]) and sum(e)==0 and sp.Matrix(T).dot(e)==0)

# 例8
T=[0,1,2]; Y=sp.Matrix([1,1,4]); A=sp.Matrix([[1,t] for t in T]); eta=sp.Rational(1,10); x=sp.zeros(2,1)
xs=[]
for _ in range(2):
    x=x-eta*2*A.T*(A*x-Y); xs.append(x)
check(8, xs[0]==sp.Matrix([sp.Rational(6,5),sp.Rational(9,5)]) and xs[1]==sp.Matrix([sp.Rational(3,5),sp.Rational(27,25)]) and (A.T*A).inv()*A.T*Y==sp.Matrix([sp.Rational(1,2),sp.Rational(3,2)]))
