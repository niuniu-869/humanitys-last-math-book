"""P.2 讲义里的模拟表（固定随机种子）与例题数值的独立核对。"""
import itertools
from fractions import Fraction as F
from math import comb
import numpy as np

def ok(tag, cond):
    print(f"PASS {tag}" if bool(cond) else f"FAIL {tag}")

# 第 4 节：10 万人的检测模拟
rng = np.random.default_rng(2025)
N = 100000
sick = rng.random(N) < 0.01
pos = np.where(sick, rng.random(N) < 0.95, rng.random(N) < 0.05)
a, b, c = int((sick & pos).sum()), int((~sick & pos).sum()), int(sick.sum())
print(f"表1 模拟10万人：患病 {c}，患病且阳性 {a}，健康且阳性 {b}，阳性共 {a+b}，阳性中患病的比例 {a/(a+b):.4f}")
ok("表1 接近19/118", abs(a/(a+b) - 19/118) < 0.02)

# 第 6 节：投篮 10000 轮
rng = np.random.default_rng(11)
x = (rng.random((10000, 10)) < 0.7).sum(1)
print(f"表2 投篮：X=7 的频率 {(x==7).mean():.4f}，X>=8 的频率 {(x>=8).mean():.4f}")
ok("表2 接近精确值", abs((x==7).mean() - 0.2668) < 0.01 and abs((x>=8).mean() - 0.3828) < 0.01)

# 第 1 节
O = list(itertools.product(range(1, 7), repeat=2))
Bset = [o for o in O if sum(o) >= 10]
ok("例1 缩小样本空间", len(Bset) == 6 and sum(6 in o for o in Bset) == 5)
# 两个孩子
kids = list(itertools.product("男女", repeat=2))
ok("两孩 至少一男", F(sum(k == ("男", "男") for k in kids if "男" in k), sum("男" in k for k in kids)) == F(1, 3))
ok("两孩 老大是男", F(1, 2) == F(sum(k == ("男", "男") for k in kids if k[0] == "男"), sum(k[0] == "男" for k in kids)))
PA, PB, PU = F(5, 10), F(4, 10), F(8, 10)
PAB = PA + PB - PU
ok("例3", (PAB, PAB/PB, PAB/PA, (PB-PAB)/(1-PA), (1-PU)/(1-PB)) == (F(1, 10), F(1, 4), F(1, 5), F(3, 5), F(1, 3)))
# 疾病
pd, se, fp = F(1, 100), F(95, 100), F(5, 100)
pp = pd*se + (1-pd)*fp
ok("疾病 P(阳)", pp == F(59, 1000))
ok("疾病 后验", pd*se/pp == F(19, 118))
ok("疾病 四格", (100000*pd, 100000*pd*se, 100000*(1-pd)*fp) == (1000, 950, 4950))
# 第 2 节
ok("例4 先白后红", F(5, 8)*F(3, 7) == F(15, 56))
ok("例5 三张黑桃", F(13, 52)*F(12, 51)*F(11, 50) == F(11, 850))
ok("例6 语言模型", F(2, 10)*F(5, 10)*F(3, 10) == F(3, 100))
# 第 3 节
ok("例7 两个袋", F(1, 2)*F(3, 5) + F(1, 2)*F(1, 5) == F(2, 5))
ok("例8 移球", F(2, 3)*F(1, 2) + F(1, 3)*F(1, 4) == F(5, 12))
ok("例9 抽签第二人", F(3, 10)*F(2, 9) + F(7, 10)*F(3, 9) == F(3, 10))
# 第 4 节
pw = F(1, 3)*(F(2, 3) + F(1, 3) + 0)
ok("例10 三箱", pw == F(1, 3) and [F(1, 3)*q/pw for q in (F(2, 3), F(1, 3), 0)] == [F(2, 3), F(1, 3), 0])
ok("例12 双头币", F(1, 3)/(F(1, 3) + F(2, 3)*F(1, 2)) == F(1, 2))
post = [(p*se)/(p*se + (1-p)*fp) for p in (F(1, 1000), F(1, 100), F(1, 10), F(1, 2))]
print("先验-后验", [float(round(float(v), 4)) for v in post])
ok("先验-后验", [round(float(v), 4) for v in post] == [0.0187, 0.161, 0.6786, 0.95])
# 第 5 节
Aodd = {o for o in O if o[0] % 2 == 1}
S7 = {o for o in O if sum(o) == 7}; S8 = {o for o in O if sum(o) == 8}
ok("例13 和为7独立", F(len(Aodd & S7), 36) == F(1, 2)*F(len(S7), 36))
ok("例13 和为8不独立", F(len(Aodd & S8), 36) != F(1, 2)*F(len(S8), 36) and len(Aodd & S8) == 2)
pa, pb = F(4, 10), F(7, 10)
ok("例14", (pa*pb, 1-(1-pa)*(1-pb), pa*(1-pb), (1-pa)*(1-pb)) == (F(28, 100), F(82, 100), F(12, 100), F(18, 100)))
C2 = list(itertools.product("HT", repeat=2))
A_ = {o for o in C2 if o[0] == "H"}; B_ = {o for o in C2 if o[1] == "H"}; Cc = {o for o in C2 if o[0] == o[1]}
P = lambda E: F(len(E), 4)
ok("例15 两两独立", P(A_&B_) == P(A_)*P(B_) and P(A_&Cc) == P(A_)*P(Cc) and P(B_&Cc) == P(B_)*P(Cc))
ok("例15 不相互独立", P(A_&B_&Cc) == F(1, 4) and P(A_)*P(B_)*P(Cc) == F(1, 8))
ok("例16", (F(9, 10)**3, 1-F(1, 10)**3, 3*F(9, 10)**2*F(1, 10)) == (F(729, 1000), F(999, 1000), F(243, 1000)))
# 第 6 节
b = lambda n, k, p: comb(n, k)*p**k*(1-p)**(n-k)
p7 = F(7, 10)
ok("例17 X=7", abs(float(b(10, 7, p7)) - 0.26683) < 1e-5)
ok("例17 X>=8", abs(float(sum(b(10, k, p7) for k in range(8, 11))) - 0.38278) < 1e-5)
ok("例17 总和1", sum(b(10, k, p7) for k in range(11)) == 1)
ok("例17 众数7", max(range(11), key=lambda k: b(10, k, p7)) == 7)
print("n=10 p=0.7 分布", [round(float(b(10, k, p7)), 4) for k in range(11)])
ok("例18 梅雷", round(1-(5/6)**4, 4) == 0.5177 and round(1-(35/36)**24, 4) == 0.4914)
p6 = F(6, 10)
ok("例19 七局四胜", round(float(sum(b(7, k, p6) for k in range(4, 8))), 4) == 0.7102)
ok("例20 第5次第3个命中", abs(float(comb(4, 2)*p7**3*(1-p7)**2) - 0.18522) < 1e-9)
# 第 7 节
pp2 = pd*se**2 + (1-pd)*fp**2
ok("例21 两次阳性", (pp2, pd*se**2/pp2) == (F(115, 10000), F(361, 460)))
ok("例21 不独立", pp2 != pp**2 and float(pp**2) < 0.0035)
Cone = {o for o in C2 if o[0] != o[1]}
ok("例22 条件不独立", F(len(A_&B_&Cone), len(Cone)) == 0 and F(len(A_&Cone), len(Cone)) == F(1, 2))
num = F(3, 10)*F(6, 10)*F(4, 10); den = num + F(7, 10)*F(5, 100)*F(2, 100)
ok("例23 朴素贝叶斯", abs(float(num/den) - 0.9904) < 1e-4)
one = F(3, 10)*F(6, 10)/(F(3, 10)*F(6, 10) + F(7, 10)*F(5, 100))
ok("例23 只看免费", abs(float(one) - 0.8372) < 1e-4)
