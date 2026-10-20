"""Recompute every determinate answer; MANUAL is reserved for pure proofs.

Expected values are transcribed answer claims, never computed outputs.
Each claim is bound to its printed answer text before comparison.
"""
from itertools import product
from pathlib import Path
import re

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBS = (ROOT / "problems.md").read_text(encoding="utf-8")
R = s.Rational
failed = 0


def blocks(text):
    return {m[1]: m[2] for m in re.finditer(
        r"(?ms)^\*\*(M2-\d+)\*\*(.*?)(?=^\*\*M2-\d+\*\*|\Z)", text)}


answers = blocks(ANS)
problems = blocks(PROBS)


def compact(text):
    return re.sub(r"\s+", "", text)


def contains(text, *parts):
    for part in parts:
        assert compact(part) in compact(text), f"Printed claim missing: {part}"


def equal(actual, expected):
    if isinstance(actual, (s.MatrixBase, np.ndarray, list, tuple)):
        a, b = s.Matrix(actual), s.Matrix(expected)
        assert a.shape == b.shape, (a.shape, b.shape)
        assert all(s.simplify(v) == 0 for v in a - b), (a, b)
    else:
        assert s.simplify(actual - expected) == 0, (actual, expected)


def claim(q, printed, actual, expected):
    contains(answers[q], printed)
    equal(actual, expected)


def rounded(q, actual, expected, digits):
    assert round(float(actual), digits) == expected, (actual, expected)
    contains(answers[q], f"{expected:.{digits}f}")


def run(q, operation):
    global failed
    try:
        operation()
    except Exception as exc:
        failed += 1
        print(f"FAIL {q}: {exc}")
    else:
        print(f"PASS {q}")


def choice(q, options):
    """Check each printed option against the mathematically computed result."""
    selected = re.search(r"选 \(([A-D])\)", answers[q])[1]
    assert sum(bool(valid) for _, valid in options) == 1
    for letter, (printed, valid) in zip("ABCD", options):
        contains(problems[q], f"({letter}) {printed}")
        run(f"{q}({letter})", lambda v=valid, a=letter:
            equal(int(bool(v)), int(a == selected)))


def sigmoid(z):
    return 1 / (1 + s.exp(-z))


def ce(z, y):
    return s.log(1 + s.exp(z)) - y * z


def q01():
    x, y = s.Matrix([0, 1, 2]), s.Matrix([1, 2, 4])
    likelihoods = []
    for w, b, expected_sse, expected_var, printed_sse, printed_var, expected_ll in [
        (1, R(1, 2), R(11, 4), R(11, 12), r"\frac{11}4", r"\frac{11}{12}", -4.1263),
        (R(3, 2), 0, R(9, 4), R(3, 4), r"\frac94", r"\frac34", -3.8253),
    ]:
        residual = w * x + b * s.ones(3, 1) - y
        ss = residual.dot(residual)
        v = s.symbols("v", positive=True)
        ll = -R(3, 2) * s.log(2 * s.pi * v) - ss / (2 * v)
        best_v = s.solve(s.diff(ll, v), v)[0]
        claim("M2-01", printed_sse, ss, expected_sse)
        claim("M2-01", printed_var, best_v, expected_var)
        rounded("M2-01", ll.subs(v, best_v), expected_ll, 4)
        assert s.diff(ll, v, 2).subs(v, best_v) < 0
        likelihoods.append(ll.subs(v, best_v))
    assert likelihoods[1] > likelihoods[0]
    contains(answers["M2-01"], "第二条直线的最大似然更大")


def q02():
    joint = [R(2, 5) * R(1, 2) * R(4, 5),
             R(3, 5) * R(1, 5) * R(3, 10)]
    p = joint[0] / sum(joint)
    claim("M2-02", r"\frac{40}{49}", p, R(40, 49))
    rounded("M2-02", p, .8163, 4)
    assert p > R(1, 2)
    contains(answers["M2-02"], "应判为第一类")


def q03():
    w, b, x = s.symbols("w b x", real=True)
    logit = lambda p: s.log(p / (1 - p))
    sol = s.solve([b - logit(R(1, 4)), w + b - logit(R(1, 2))], [w, b])
    claim("M2-03", r"w=\ln3", sol[w], s.log(3))
    claim("M2-03", r"b=-\ln3", sol[b], -s.log(3))
    claim("M2-03", r"p(2)=\frac34", sigmoid(2 * sol[w] + sol[b]), R(3, 4))
    interval = s.solve_univariate_inequality(
        sol[w] * x + sol[b] >= logit(R(3, 4)), x, relational=False)
    assert interval == s.Interval(2, s.oo)
    contains(answers["M2-03"], r"x\ge2")


def q04():
    p = [R(3, 4), R(1, 2)]
    y = [1, 0]
    loss = -sum(yi * s.log(pi) + (1 - yi) * s.log(1 - pi)
                for pi, yi in zip(p, y)) / 2
    expressions = [s.log(8)/2, s.log(R(8, 3)), s.log(R(8, 3))/2, s.log(R(8, 5))]
    tex = [r"\frac12\ln8", r"\ln\frac83", r"\frac12\ln\frac83", r"\ln\frac85"]
    choice("M2-04", [("$"+t+"$", s.expand_log(loss - e, force=True) == 0)
                     for t, e in zip(tex, expressions)])
    claim("M2-04", r"\frac12\ln(8/3)", s.expand_log(loss, force=True),
          s.expand_log(s.log(R(8, 3))/2, force=True))
    # Regenerate the three specific mistakes explained in prose.
    equal(s.log(8)/2, -s.log((1-p[0]) * (1-p[1]))/2)
    equal(s.expand_log(expressions[1], force=True), s.expand_log(2*loss, force=True))
    equal(expressions[3], -s.log((p[0] + 1-p[1])/2))


def counts(pred, y):
    pred, y = np.asarray(pred, dtype=bool), np.asarray(y, dtype=bool)
    return tuple(int(np.sum(mask)) for mask in
                 (pred & y, pred & ~y, ~pred & y, ~pred & ~y))


def metrics(c):
    tp, fp, fn, tn = c
    return (R(tp + tn, sum(c)), R(tp, tp+fp) if tp+fp else None,
            R(tp, tp+fn) if tp+fn else None)


def q05():
    c = counts([1, 1, 0, 1, 1, 0, 0], [1, 1, 1, 0, 0, 0, 0])
    expected = [(R(4,7),R(2,3),R(1,2)), (R(4,7),R(1,2),R(2,3)),
                (R(5,7),R(1,2),R(2,3)), (R(4,7),R(2,7),R(2,3))]
    tex = [r"$(\frac47,\frac23,\frac12)$", r"$(\frac47,\frac12,\frac23)$",
           r"$(\frac57,\frac12,\frac23)$", r"$(\frac47,\frac27,\frac23)$"]
    choice("M2-05", [(t, metrics(c) == e) for t, e in zip(tex, expected)])
    claim("M2-05", "TP=2,FP=2,FN=1,TN=2", c, (2,2,1,2))
    contains(answers["M2-05"], "4/7,1/2,2/3")


def q07():
    w1, w2, b = s.symbols("w1 w2 b", real=True)
    X = s.Matrix([[1,0],[0,1],[1,1]])
    params = s.Matrix([w1,w2,b])
    A = X.row_join(s.ones(3,1))
    observed = s.Matrix([-R(1,3),0,-R(1,6)])
    possible = []
    for labels in product((0,1), repeat=3):
        loss = sum(ce(z, yi) for z, yi in zip(A*params, labels))/3
        grad = s.Matrix([s.diff(loss, u) for u in params]).subs(dict.fromkeys(params,0))
        if grad == observed:
            possible.append(labels)
    assert possible == [(1,0,1)], possible
    contains(answers["M2-07"], r"(1,0,1)^{\mathsf T}")
    claim("M2-07", r"\boldsymbol w=(0.2,0)^{\mathsf T}", -R(3,5)*observed[:2,0],
          s.Matrix([R(1,5),0]))
    claim("M2-07", "b=0.1", -R(3,5)*observed[2], R(1,10))
    contrib = [(R(1,2)-yi)*X[i,1] for i,yi in enumerate(possible[0])]
    claim("M2-07", r"(0,\frac12,-\frac12)", contrib, [0,R(1,2),-R(1,2)])


def q08():
    given = s.Matrix([R(1,10),R(1,5),-R(7,10),R(2,5)])
    candidates = []
    for c in range(4):
        p = given + s.eye(4)[:,c]
        if all(0 < v < 1 for v in p) and sum(p) == 1:
            candidates.append((c,p))
    assert len(candidates) == 1
    c,p = candidates[0]
    assert c == 2
    # Differentiate every W entry using log(p) as the initial scores.
    entries = s.symbols("u0:8", real=True)
    W = s.Matrix(4,2,entries)
    z = W*s.Matrix([1,-1]) + p.applyfunc(s.log)
    loss = -z[c] + s.log(sum(s.exp(v) for v in z))
    grad = s.Matrix(4,2,[s.simplify(s.diff(loss,u).subs(dict.fromkeys(entries,0)))
                         for u in entries])
    G = s.Matrix([[1,-1],[2,-2],[-7,7],[4,-4]])/10
    contains(problems["M2-08"], r"G=\frac1{10}\begin{pmatrix}1&-1\\2&-2\\-7&7\\4&-4\end{pmatrix}")
    opts = [(R(3,10),G),(R(7,10),G),(R(3,10),-G),(R(3,10),G.T)]
    tex = [r"$p_3=\frac3{10}$，$\nabla_W\ell=G$",
           r"$p_3=\frac7{10}$，$\nabla_W\ell=G$",
           r"$p_3=\frac3{10}$，$\nabla_W\ell=-G$",
           r"$p_3=\frac3{10}$，$\nabla_W\ell=G^{\mathsf T}$"]
    choice("M2-08", [(t, pv == p[2] and g == grad) for t,(pv,g) in zip(tex,opts)])
    claim("M2-08", r"(1/10,1/5,3/10,2/5)^{\mathsf T}", p,
          [R(1,10),R(1,5),R(3,10),R(2,5)])


def q09():
    t = s.symbols("t", real=True)
    num1 = t * R(3,4)*(1-R(1,3))
    num0 = (1-t)*R(1,4)*(1-R(2,3))
    posterior = s.factor(num1/(num1+num0))
    claim("M2-09", r"\frac{6t}{1+5t}", posterior, 6*t/(1+5*t))
    result = s.solve_univariate_inequality(posterior >= R(3,4),t,relational=False)
    result = result.intersect(s.Interval.open(0,1))
    assert result == s.Interval.Ropen(R(1,3),1)
    contains(answers["M2-09"], r"\frac13\le t<1")


def q10():
    probs = [s.Matrix([R(3,5),R(2,5)]),s.Matrix([R(99,100),R(51,100)])]
    actual_losses = []
    for p, accuracy, like, digits in zip(probs, [1,R(1,2)], [R(9,25),R(4851,10000)],
                                         [.5108,.3617]):
        computed_accuracy = R(int(bool(p[0]>=R(1,2)))+int(bool(p[1]<R(1,2))),2)
        equal(computed_accuracy, accuracy)
        equal(p[0]*(1-p[1]),like)
        loss = -s.log(p[0]*(1-p[1]))/2
        rounded("M2-10",loss,digits,4)
        actual_losses.append(loss)
    assert actual_losses[0] > actual_losses[1]
    contains(answers["M2-10"], "甲的准确率为 $1$", "乙的准确率为 $1/2$",
             r"\frac9{25}", r"\frac{4851}{10000}", "命题不成立")


def q11():
    b = s.symbols("b", real=True)
    loss = sum(ce(b,y) for y in [0,0,0,1])/4
    claim("M2-11", r"L(b)=\ln(1+e^b)-\frac b4",loss,s.log(1+s.exp(b))-b/4)
    first, second = s.diff(loss,b), s.diff(loss,b,2)
    claim("M2-11", r"L'(b)=\sigma(b)-\frac14",first,sigmoid(b)-R(1,4))
    claim("M2-11", r"L''(b)=\sigma(b)(1-\sigma(b))",second,sigmoid(b)*(1-sigmoid(b)))
    root = s.solve(first,b)
    assert len(root)==1
    claim("M2-11", r"b_*=-\ln3",root[0],-s.log(3))
    best = s.expand_log(loss.subs(b,root[0]),force=True)
    claim("M2-11", r"\ln4-\frac34\ln3",best,2*s.log(2)-R(3,4)*s.log(3))
    rounded("M2-11",best,.5623,4)
    assert s.simplify(second).is_positive
    all_one = s.log(1+s.exp(-b))
    equal(s.diff(ce(b,1),b),s.diff(all_one,b))
    claim("M2-11", r"L'(b)=-\frac1{1+e^b}",s.diff(all_one,b),-1/(1+s.exp(b)))
    assert s.diff(all_one,b).is_negative and all_one.is_positive
    assert s.solve(s.diff(all_one,b),b)==[]
    equal(s.limit(all_one,b,s.oo),0)
    contains(answers["M2-11"],"第二组没有有限最优截距","下确界为 $0$")


def q13():
    contains(problems["M2-13"], "两类依次记为 0、1，分数分别为 $a,b$",
             "第二类", "类别 1")
    a,b,d,eta,alpha = s.symbols("a b d eta alpha",real=True)
    loss = -b+s.log(s.exp(a)+s.exp(b))
    p = s.exp(b)/(s.exp(a)+s.exp(b))
    claim("M2-13", r"p=\sigma(\delta)",p.subs(b,a+d),sigmoid(d))
    ga,gb = s.diff(loss,a),s.diff(loss,b)
    claim("M2-13", r"\partial\ell/\partial a=1-p",ga,1-p)
    claim("M2-13", r"\partial\ell/\partial b=p-1",gb,p-1)
    soft_new = s.simplify(((b-eta*gb)-(a-eta*ga)).subs(b,a+d))
    one_new = d-alpha*s.diff(ce(d,1),d)
    claim("M2-13", r"\delta+2\eta(1-p)",soft_new,d+2*eta*(1-sigmoid(d)))
    claim("M2-13", r"\delta+\alpha(1-p)",one_new,d+alpha*(1-sigmoid(d)))
    claim("M2-13", r"\alpha=2\eta",s.solve(soft_new-one_new,alpha)[0],2*eta)
    vsoft = s.simplify(soft_new.subs({d:0,eta:R(1,5)}))
    vone = s.simplify(one_new.subs({d:0,alpha:R(1,5)}))
    equal(vsoft,R(1,5)); equal(vone,R(1,10))
    rounded("M2-13",sigmoid(vsoft),.5498,4)
    rounded("M2-13",sigmoid(vone),.5250,4)


def q14():
    X = s.Matrix([[-1,1],[0,1],[1,1]])
    y = s.Matrix([0,0,1])
    fit = (X.T*X).inv()*X.T*y
    claim("M2-14", r"(\frac12,\frac13)",fit,[R(1,2),R(1,3)])
    out = (s.Matrix([[2,1]])*fit)[0]
    claim("M2-14","4/3",out,R(4,3))
    assert out>1
    w,b = s.symbols("w b",real=True)
    loss = sum(ce(z,yi) for z,yi in zip(X*s.Matrix([w,b]),y))/3
    g = s.Matrix([s.diff(loss,u).subs({w:0,b:0}) for u in [w,b]])
    claim("M2-14",r"(-\tfrac13,\tfrac16)",g,[-R(1,3),R(1,6)])
    claim("M2-14",r"(\frac15,-\frac1{10})",-R(3,5)*g,[R(1,5),-R(1,10)])


def q15():
    x = s.symbols("x",real=True)
    density = lambda mu:s.exp(-(x-mu)**2/2)/s.sqrt(2*s.pi)
    odds = s.simplify(R(1,4)*density(1)/(R(3,4)*density(-1)))
    logit = s.expand_log(s.log(odds),force=True)
    claim("M2-15",r"2x-\ln3",logit,2*x-s.log(3))
    claim("M2-15","w=2",s.diff(logit,x),2)
    claim("M2-15",r"b=-\ln3",logit.subs(x,0),-s.log(3))
    posterior = odds/(1+odds)
    claim("M2-15","p(0)=1/4",posterior.subs(x,0),R(1,4))
    interval = s.solve_univariate_inequality(logit>=s.log(3),x,relational=False)
    assert interval==s.Interval(s.log(3),s.oo)
    contains(answers["M2-15"],r"x\ge\ln3")


def q16():
    p = [R(v,10) for v in [1,3,4,6,8,9]]
    y = [0,1,0,1,0,1]
    edges = [s.S.Zero]+p+[s.S.One]
    acceptable = s.EmptySet
    table = []
    for lo,hi in zip(edges,edges[1:]):
        interval = s.Interval.Lopen(lo,hi).intersect(s.Interval.open(0,1))
        t = (lo+hi)/2
        pred = [pi>=t for pi in p]
        c = counts(pred,y)
        acc,prec,rec = metrics(c)
        table.append((sum(bool(v) for v in pred),prec,rec))
        if prec is not None and prec>=R(2,3) and rec>=R(2,3):
            acceptable = acceptable.union(interval)
            claim("M2-16","TP=2,FP=1,FN=1,TN=2",c,[2,1,1,2])
            claim("M2-16","准确率为 $2/3$",acc,R(2,3))
    assert acceptable==s.Interval.Lopen(R(2,5),R(3,5))
    printed_intervals = re.findall(
        r"0\.4(\\le|<)\\tau(\\le|<)0\.6", compact(answers["M2-16"]))
    assert len(printed_intervals)==2
    for left,right in printed_intervals:
        printed = s.Interval(R(2,5),R(3,5),left_open=left=="<",right_open=right=="<")
        assert printed==acceptable, (printed,acceptable)
    # Check every boundary separately so >= cannot silently become >.
    for t in p:
        c=counts([pi>=t for pi in p],y)
        _,prec,rec=metrics(c)
        valid = prec is not None and prec>=R(2,3) and rec>=R(2,3)
        assert bool(valid)==bool(acceptable.contains(t))
    for k,prec,rec in table:
        fmt = lambda v:"未定义" if v is None else "$"+str(v)+"$"
        contains(answers["M2-16"],f"| {k} | {fmt(prec)} | {fmt(rec)} |")
    contains(answers["M2-16"],r"0.4<\tau\le0.6",
             r"P(Y=1\mid\widehat Y=1)",r"P(\widehat Y=1\mid Y=1)")
    tp,fp,fn,tn = counts([pi>=R(1,2) for pi in p],y)
    equal(R(tp,6)/R(tp+fp,6),R(tp,tp+fp))
    equal(R(tp,6)/R(tp+fn,6),R(tp,tp+fn))


expected_ids = [f"M2-{i:02d}" for i in range(1,17)]
assert list(answers)==expected_ids and list(problems)==expected_ids
table_ids = re.findall(r"(?m)^\| (M2-\d+) \|", PROBS)
summary = (ROOT / "lesson.md").read_text(encoding="utf-8").split("### 本章小结", 1)[1]
summary_ids = set(re.findall(r"M2-\d+", summary))
assert table_ids == expected_ids and summary_ids == set(expected_ids)
main,mixed=PROBS.split("### 章末混合练习")
assert [len(re.findall(rf"\*\*M2-\d+\*\*〔{tier}｜",main)) for tier in "ABC"]==[5,5,3]
assert len(re.findall(r"^\*\*M2-",mixed,re.M))==3 and "方法" not in mixed
for q,body in answers.items():
    tier=re.match(r"〔([ABC])",problems[q])[1]
    assert body.startswith("\n**答案：**"), q
    assert body.strip().splitlines()[-1].startswith("区分点："), q
    assert len(body)+len(q)+4 <= {"A":400,"B":900,"C":1400}[tier], q
for q in ["M2-11","M2-12","M2-13"]:
    assert re.search(r"拆法：先做 M2-\d+、M2-\d+。",problems[q])
assert not re.search(r"高中|初中|中学课本|备考|考研|数学一|真题|考纲|应试|结论：|核心是：",PROBS+ANS)

for num,fn in [(1,q01),(2,q02),(3,q03),(4,q04),(5,q05),(7,q07),(8,q08),
               (9,q09),(10,q10),(11,q11),(13,q13),(14,q14),(15,q15),(16,q16)]:
    run(f"M2-{num:02d}",fn)
for q in ["M2-06","M2-12"]:
    assert "证明" in problems[q]
    print(f"MANUAL {q}")
raise SystemExit(1 if failed else 0)
