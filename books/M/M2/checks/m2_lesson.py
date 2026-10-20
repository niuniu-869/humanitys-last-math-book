"""Independently check all ten worked examples, including their numerical tables.

Printed values are checked using the rounding convention stated in the lesson.
"""
from pathlib import Path
import re

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
EXAMPLES = {int(m[1]): m[2] for m in re.finditer(
    r"(?s)\*\*例 (\d+)\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON)}
failed = 0
x = np.arange(1.,6.)
X = np.column_stack([x,np.ones(5)])
y = np.array([0,0,1,0,1])
trained = np.array([1.0904,-3.894])


def contains(text,*parts):
    text = re.sub(r"\s+","",text)
    for part in parts:
        assert re.sub(r"\s+","",part) in text, f"Missing text: {part}"


def near(actual,expected,tol):
    assert np.allclose(actual,expected,rtol=0,atol=tol), (actual,expected)


def sig(z):
    return 1/(1+np.exp(-np.asarray(z)))


def loss(theta):
    z=X@theta
    return float(np.mean(np.logaddexp(0,z)-y*z))


def numerical_grad(f,t,h=1e-6):
    return np.array([(f(t+h*e)-f(t-h*e))/(2*h) for e in np.eye(len(t))])


def report(k,fn):
    global failed
    try:
        fn()
    except Exception as exc:
        failed+=1
        print(f"FAIL 例{k}: {exc}")
    else:
        print(f"PASS 例{k}")


def example1():
    target=np.array([2,3,5,6,9])
    values=[]
    variance=s.symbols("v",positive=True)
    for theta,ss_expected,v_expected,ll_expected in [
        ([1.7,-.1],1.1,.22,-3.309),([2,0],7,1.4,-7.936)]:
        ss=float(np.sum((X@theta-target)**2))
        near(ss,ss_expected,1e-12)
        likelihood=-s.Rational(5,2)*s.log(2*s.pi*variance)-ss/(2*variance)
        best=float(s.solve(s.diff(likelihood,variance),variance)[0])
        near(best,v_expected,1e-12)
        ll=float(likelihood.subs(variance,best))
        near(ll,ll_expected,.0005)
        values.append(ll)
    assert values[0]>values[1]
    contains(EXAMPLES[1],"1.1","0.22","-3.309","1.4","-7.936")
    # The matrix-gradient calculation adjacent to example 1.
    near(numerical_grad(lambda t:np.mean((X@t-target)**2),np.zeros(2)),
         [-36.8,-10],1e-7)


def example2():
    prior=.3
    numerators=np.array([prior*.6*.9,(1-prior)*.05*.6])
    near(numerators,[.162,.021],1e-12)
    post=numerators[0]/sum(numerators)
    near(post,.8852,.00005)
    assert post>.5
    both=np.array([prior*.6*.1,(1-prior)*.05*.4])
    near(both,[.018,.014],1e-12)
    near(both[0]/sum(both),.5625,1e-12)
    near(np.log(both[0]/both[1]),.251,.0005)
    near(both[0]/both[1],1.286,.0005)
    contains(EXAMPLES[2],"0.162","0.021","0.8852","0.018","0.014","0.5625","判为垃圾邮件")


def example3():
    z=X@trained
    p=sig(z)
    near(z,[-2.804,-1.713,-.623,.468,1.558],.0005)
    near(p,[.057,.153,.349,.615,.826],.0005)
    near(-trained[1]/trained[0],3.571,.0005)
    assert np.array_equal(p>=.5,[False,False,False,True,True])
    assert np.array_equal(np.flatnonzero((p>=.5)!=y),[2,3])
    contains(EXAMPLES[3],r"\approx0.3491","3.571","0.057","0.153","0.349","0.615","0.826")
    # The displayed parameters differ from the unrounded fit in example 7.
    exact=float(1/(1+s.exp(s.Rational(6228,10000))))
    near(p[2],exact,1e-14)
    assert round(exact,4)==.3491 and round(exact,4)!=.3492


def example4():
    u,v=s.symbols("u v")
    boundary=u+2*v-4
    assert boundary.subs({u:2,v:1})==0
    near(sig([float(boundary.subs({u:2,v:1})),
              float(boundary.subs({u:3,v:2}))]),[.5,.9526],.00005)
    near(sig(np.dot([1,-1],[0,2])+1),.2689,.00005)
    contains(EXAMPLES[4],"x_1+2x_2=4","0.9526","0.2689")


def example5():
    near(loss(np.zeros(2)),.6931,.00005)
    near(loss(trained),.4844,.00005)
    assert loss(trained)<loss(np.zeros(2))
    z=X@trained
    terms=np.logaddexp(0,z)-y*z
    # Read every row of the printed example, not just the average.
    rows=re.findall(r"(?m)^\| ([1-5]) \| ([01]) \| ([\d.]+) \| \$.*?=([\d.]+)\$",EXAMPLES[5])
    assert len(rows)==5
    for i,label,prob,term in rows:
        j=int(i)-1
        assert int(label)==y[j]
        near(sig(z[j]),float(prob),.0005)
        near(terms[j],float(term),.0005)
    contains(EXAMPLES[5],"单样本损失用不舍入的概率算")
    trial=np.array([1.,-3.])
    trial_z=X@trial
    near(sig(trial_z),[.119,.269,.5,.731,.881],.0005)
    near(np.logaddexp(0,trial_z)-y*trial_z,[.127,.313,.693,1.313,.127],.0005)
    near(loss(trial),.5147,.00005)
    assert loss(trained)<loss(trial)<loss(np.zeros(2))
    contains(EXAMPLES[5],"0.6931","0.4844","0.5147")


def example6():
    grad=numerical_grad(loss,np.zeros(2))
    near(grad,[-.1,.1],1e-9)
    updated=-.5*grad
    near(updated,[.05,-.05],1e-9)
    near(loss(updated),.6850,.00005)
    assert loss(updated)<loss(np.zeros(2))
    single=lambda t:float(np.logaddexp(0,4*t[0]+t[1]))
    near(numerical_grad(single,np.zeros(2)),[2,.5],1e-9)
    contains(EXAMPLES[6],"(-0.1,\\,0.1)","(0.05,\\,-0.05)","0.6850")
    # Also check the separability calculation immediately before example 7.
    yy=np.array([0,0,0,1,1])
    values=[]
    for c,expected,tol in [(1,.146,.0005),(2,.0518,.00005),
                           (4,.00726,.000005),(8,.000134,.0000005)]:
        z=X@(c*np.array([2.,-7.]))
        value=float(np.mean(np.logaddexp(0,-(2*yy-1)*z)))
        near(value,expected,tol)
        values.append(value)
    assert all(a>b>0 for a,b in zip(values,values[1:]))


def example7():
    gram=X.T@X/5
    near(gram,[[11,3],[3,1]],1e-12)
    eig=np.linalg.eigvalsh(gram)
    near(eig,[6-np.sqrt(34),6+np.sqrt(34)],1e-12)
    near(eig[1]/4,2.958,.0005)
    near(8/eig[1],.676,.0005)
    # Parse and independently reproduce all five rows, including parameters.
    rows={}
    for step,w,b,l in re.findall(r"(?m)^\| (\d+) \| ([\d.$-]+) \| ([\d.$-]+) \| ([\d.]+) \|",EXAMPLES[7]):
        rows[int(step)]=[w.strip("$"),b.strip("$"),l]
    assert set(rows)=={0,1,10,100,1000}
    theta=np.zeros(2)
    for step in range(10001):
        if step in rows:
            actual=[*theta,loss(theta)]
            for a,display in zip(actual,rows[step]):
                decimals=len(display.split(".")[1]) if "." in display else 0
                near(a,float(display),.5*10**(-decimals)+1e-12)
        if step<10000:
            theta-=.5*(X.T@(sig(X@theta)-y))/5
    near(theta,[1.0904,-3.894],[.00005,.0005])
    near(loss(theta),.48439,.000005)
    near(sig(X@theta)[2],.3492,.00005)
    near(X.T@(sig(X@theta)-y)/5,[0,0],1e-12)
    d=sig(X@theta)*(1-sig(X@theta))
    heig=np.linalg.eigvalsh(X.T@np.diag(d)@X/5)
    near(heig[0],.0155,.00005)
    # "About 140" is stated to two significant digits.
    assert round((heig[1]/heig[0])/10)*10==140
    contains(EXAMPLES[7],"0.676","0.0155","140")


def example8():
    W=np.array([[0.,1.],[1.,0.],[0.,0.]])
    feature=np.array([1.,2.])
    z=W@feature
    near(z,[2,1,0],1e-12)
    p=np.exp(z)/np.exp(z).sum()
    near(p,[.6652,.2447,.0900],.00005)
    near(-np.log(p[0]),.4076,.00005)
    cross_entropy=lambda zz:float(np.logaddexp.reduce(zz)-zz[0])
    g=numerical_grad(cross_entropy,z)
    near(g,[-.3348,.2447,.0900],.00005)
    near(np.sum(g),0,1e-9)
    weight_loss=lambda ww:cross_entropy(ww.reshape(3,2)@feature)
    gw=numerical_grad(weight_loss,W.flatten()).reshape(3,2)
    near(gw,[[-.3348,-.6695],[.2447,.4895],[.0900,.1801]],.00005)
    near(-np.log(p[1]),1.4076,.00005)
    near(p-np.array([0,1,0]),[.6652,-.7553,.0900],.00005)
    near(np.log(np.exp(z).sum()),2.4076,.00005)
    assert np.all(gw[0]<0)
    contains(EXAMPLES[8],"0.4076","1.4076","2.4076","-0.6695","0.4895","0.1801")


def classification_counts(probs,labels,threshold):
    pred=np.asarray(probs)>=threshold
    actual=np.asarray(labels,dtype=bool)
    return tuple(int(mask.sum()) for mask in
                 [pred&actual,pred&~actual,~pred&actual,~pred&~actual])


def example9():
    probs=sig(X@trained)
    precisions=[]
    for threshold,expected_counts,expected_metrics in [
        (.5,(1,1,1,2),[3/5,1/2,1/2]),(.3,(2,1,0,2),[4/5,2/3,1])]:
        c=classification_counts(probs,y,threshold)
        assert c==expected_counts
        tp,fp,fn,tn=c
        near([(tp+tn)/5,tp/(tp+fp),tp/(tp+fn)],expected_metrics,1e-12)
        precisions.append(tp/(tp+fp))
    contains(EXAMPLES[9],r"\frac35",r"\frac12",r"\frac45",r"\frac23",
             "TP = 2","FP = 1","FN = 0","TN = 2")
    # Lowering the threshold can increase precision, as this example shows.
    assert precisions[1]>precisions[0]
    contains(EXAMPLES[9],"阈值降低","召回率不会下降","精确率则可升可降")


def example10():
    labels=np.r_[np.ones(10),np.zeros(990)]
    c=classification_counts(np.zeros(1000),labels,.5)
    assert c==(0,0,10,990)
    tp,fp,fn,tn=c
    near((tp+tn)/1000,.99,1e-12)
    assert tp+fp==0 and tp/(tp+fn)==0
    predictions=np.r_[np.ones(8),np.zeros(2),np.ones(12),np.zeros(978)]
    tp,fp,fn,tn=classification_counts(predictions,labels,.5)
    assert (tp,fp,fn,tn)==(8,12,2,978)
    near([tp/(tp+fp),tp/(tp+fn)],[.4,.8],1e-12)
    contains(EXAMPLES[10],"99\\%","精确率 $0/0$","0/10=0","8/20=0.4","8/10=0.8")


assert set(EXAMPLES)==set(range(1,11))
for k in range(1,11):
    report(k,globals()[f"example{k}"])
raise SystemExit(1 if failed else 0)
