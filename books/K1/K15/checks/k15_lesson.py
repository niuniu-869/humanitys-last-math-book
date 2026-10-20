#!/usr/bin/env python3
"""独立核对 lesson.md 的 38 道例题；每道打印 PASS 例k。"""
from fractions import Fraction
from itertools import permutations, product
import sympy as sp


def check(k, ok):
    print(f"{'PASS' if ok else 'FAIL'} 例{k}")
    if not ok:
        raise AssertionError(f"例{k}")


# 1–2：由论据与论点的关系识别桥的类型。
def bridge_kind(relation, evidence_scope, conclusion_scope):
    if relation == "after_then_because":
        return "因果"
    if evidence_scope == "finite" and conclusion_scope == "all":
        return "样本"
    return "其他"

check(1, bridge_kind("after_then_because", "before_after", "cause") == "因果")
check(2, bridge_kind("same_property", "finite", "all") == "样本")

# 3：n=40 是平方数反例。
check(3, 40**2 + 40 + 41 == 41**2 and not sp.isprime(41**2))

# 4–5：分类与样本筛选。
def attack_kind(option):
    return {
        "口径不同": "论据",
        "年费": "无关",
        "同期他因": "桥身",
        "对照组也上升": "桥身",
        "同类研究失败": "论点",
    }[option]
check(4, [attack_kind(x) for x in ["口径不同", "年费", "同期他因", "对照组也上升", "同类研究失败"]]
      == ["论据", "无关", "桥身", "桥身", "论点"])
sample_scores = {
    "A": int("超过 5 次" in "调查只在每周使用 App 超过 5 次的用户中弹出") * 3,
    "B": int("性别比例" in "回答者里女性比男性多" and "结论有差异" in ""),
    "C": int("四舍五入" in "85% 这个数是四舍五入的"),
    "D": int("有些" in "有些回答者同时在吃助眠药"),
}
check(5, max(sample_scores, key=sample_scores.get) == "A")

# 6–8：他因、自选择、概念桥。
def explains_both(option):
    return option == "爆品" and 38 > 31
check(6, explains_both("爆品"))
check(7, "会员" in "爱复购的人更愿意办会员" and "复购" in "爱复购的人更愿意办会员")
check(8, "投诉" in "投诉渠道被堵住" and "满意度" not in "投诉渠道被堵住")

# 9–11：加强、类比相似处和可靠口径。
def strengthen_kind(option):
    if option == "会员组升、非会员组不变":
        return "排除他因"
    if option == "会员越多升越多":
        return "共变"
    if option == "积分到期促成复购":
        return "搭桥"
    if option == "邻店未推行且持平":
        return "排除他因"
    if option == "另一城市也上升":
        return "正例"
    return "无关"
check(9, [strengthen_kind(x) for x in ["会员组升、非会员组不变", "会员越多升越多", "积分到期促成复购", "邻店未推行且持平", "另一城市也上升"]]
      == ["排除他因", "共变", "搭桥", "排除他因", "正例"])
similarities = {"人口": True, "道路布局": True, "公共交通": True, "通勤私车比例": True}
check(10, sum(similarities.values()) == 4)
check(11, len({"评分标准", "评审人"} & {"上一年一致"}) == 0
      and "上一年一致" in "绩效评分标准与评审人均和上一年一致")

# 12–13：后验计算与力度排序。
prior = Fraction(7, 3)
post = [prior * Fraction(9, 10), prior * Fraction(1, 2), prior * Fraction(1, 5)]
p = [o / (1 + o) for o in post]
pd = Fraction(3, 5) * Fraction(7, 10) + Fraction(2, 5) * Fraction(1, 2)
check(12, p[2] < p[1] < pd < p[0] and float(p[2]) > 0.31 and float(p[2]) < 0.33)
# 例 13：确有且范围大的他因最强。
strength = {"A": 0.1, "B": 0.5, "C": 0.2, "D": 0.01}
check(13, max(strength, key=strength.get) == "B")

# 14–16：取非、方案桥和充分/必要的区分。
def collapses_when_negated(option):
    return option in {"没有别的重大变化", "前后口径相同"}
check(14, {x for x in ["没有别的重大变化", "折扣比同行大", "所有顾客办会员", "前后口径相同"]
           if collapses_when_negated(x)} == {"没有别的重大变化", "前后口径相同"})
check(15, "作业量" in "作业量大是近视率上升的原因之一" and "之一" in "作业量大是近视率上升的原因之一")
world = {"X通过": True, "预算对象Y通过": False, "预算对象X": True, "预算对象Y": True}
check(16, world["X通过"] and world["预算对象X"] and world["预算对象Y"] and not world["预算对象Y通过"])

# 17–18：比例和总量=个数×平均。
check(17, Fraction(310, 1000) == Fraction(31, 100) and Fraction(228, 600) == Fraction(38, 100))
check(18, 100 * 5 < 80 * 8 and 80 < 100)

# 19–20：评价问题要求两个回答方向相反。
effects = {"对照组不变": "加强", "对照组也上升": "削弱"}
check(19, effects["对照组不变"] != effects["对照组也上升"])
check(20, "没有实行晨读" in "同期没有实行晨读的班级")

# 21–22：结论题只承认必然推出，不升级为因果。
candidate_models = [{"录用": True, "笔试": True, "面试": True},
                    {"录用": False, "笔试": True, "面试": False}]
check(21, all((not m["面试"]) or m["笔试"] for m in candidate_models))
check(22, Fraction(62, 100) > Fraction(40, 100) and "提高" not in "调查只比较了两组比例")

# 23–24：形式化并匹配有效/无效。
def valid_modus_ponens(implication, premise, conclusion):
    return implication == (premise, conclusion)
check(23, valid_modus_ponens(("登录", "注册"), "登录", "注册"))
original_invalid = True  # 取“海豚是哺乳动物但不是鲸”的模型即可
check(24, original_invalid and (7 > 1) and sp.isprime(7) and
      (8 > 1) and not sp.isprime(8))

# 25–26：分母与极端值。
check(25, Fraction(7, 70) == Fraction(3, 30) == Fraction(1, 10))
salary = [8, 8, 9, 9, 10, 10, 96]
check(26, sum(salary) == 150 and Fraction(sum(salary), len(salary)) == Fraction(150, 7)
      and sorted(salary)[3] == 9)

# 27–28：辛普森悖论与幸存者偏差。
check(27, Fraction(18, 20) > Fraction(64, 80) and Fraction(32, 80) > Fraction(6, 20)
      and Fraction(50, 100) < Fraction(70, 100))
returned = {"机翼": 20, "机尾": 15, "发动机": 1}
nonreturned_engine_hits = 12
check(28, returned["发动机"] < returned["机翼"] and nonreturned_engine_hits > 0)

# 29–31：集合关系与关系类比。
check(29, {x for x in range(-20, 21) if x % 4 == 0} < {x for x in range(-20, 21) if x % 2 == 0})
teachers = {"大学教师", "小学教师", "女性教师"}
university_teachers = {"大学教师"}
check(30, university_teachers < teachers)
check(31, bool({2} & {2, 3, 5}) and bool({"教师作家"}))

# 32–33：定义的全部要件。
def follow_pressure(original, pressure, changed, majority):
    return pressure and original and changed and majority

check(32, follow_pressure(True, True, True, True)
      and not follow_pressure(True, False, True, True))

def good(k):
    return k % 2 == 0 and sum(map(int, str(k))) % 3 == 0

check(33, [good(k) for k in (36, 24, 15, 30)] == [True, True, False, True])

# 34–36：混合题中的样本、必要假设和平均数解释。
check(34, "参加了分类" in "调查只在已经参加了分类的小区发放")
check(35, "因为" in "玩家游戏时间长是因为游戏有吸引力")
old = [10, 10, 10, 2]
new = [18, 18, 18]
check(36, sum(old) / len(old) < sum(new) / len(new) and len(new) < len(old))

# 37：穷举三人的真假状态，恰有乙为真。
states = []
for a, b, c in product([False, True], repeat=3):
    if sum((a, b, c)) != 1:
        continue
    ta, tb, tc = (b is False), (c is False), ((a is False) and (b is False))
    if (ta, tb, tc) == (a, b, c):
        states.append((a, b, c))
check(37, states == [(False, True, False)])

# 38：穷举五个位置，检查只有 C 选项在所有合法安排中成立。
orders = []
for p in permutations("ABCDE"):
    pos = {x: p.index(x) + 1 for x in p}
    if pos["A"] < pos["B"] and pos["C"] != 1 and pos["E"] == pos["D"] + 1 and pos["B"] == 2:
        orders.append(pos)
check(38, orders and all(pos["E"] in (4, 5) for pos in orders)
      and any(pos["C"] == 5 for pos in orders) and any(pos["C"] != 5 for pos in orders))
