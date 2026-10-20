import itertools


def out(ok, label):
    print(("PASS " if ok else "FAIL ") + label)


# 例1
table = []
sol = []
for culprit in "甲乙丙丁":
    truth = [culprit == "乙", culprit == "丁", culprit != "丙", culprit != "丁"]
    table.append(truth)
    if sum(truth) == 1:
        sol.append(culprit)
expected_table = [[0, 0, 1, 1], [1, 0, 1, 1], [0, 0, 0, 1], [0, 1, 1, 0]]
out(table == expected_table and [sum(row) for row in table] == [2, 3, 1, 2]
    and sol == ["丙"], "例1 完整真值表")

# 例1后练习
sol = []
for thief in "甲乙丙丁":
    truth = [thief == "丁", thief != "甲", thief == "乙", thief in "甲乙"]
    if sum(truth) == 2:
        sol.append(thief)
out(sol == ["丁"], "例1后练习")

# 例2
sol = []
for passed in "甲乙丙丁":
    truth = [passed == "甲", passed != "甲", passed not in "丙丁", passed == "乙"]
    if sum(truth) == 2:
        sol.append(passed)
out(sol == ["甲"], "例2")

# 例3
sol = []
table = []
for culprit in "甲乙丙丁":
    truth = [culprit == "乙", culprit == "丁", culprit != "丙", culprit != "丁"]
    table.append(truth)
    if sum(truth) == 1:
        sol.append(culprit)
out(sol == ["丙"] and table == expected_table
    and [sum(row) for row in table] == [2, 3, 1, 2], "例3 完整真值表")

# 例4
valid = []
for passed in itertools.product([0, 1], repeat=4):
    a, b, c, d = passed
    truth = [a and b and c and d, not (a and b and c and d), not b, d]
    if sum(truth) == 1:
        valid.append(passed)
out(valid == [(0, 1, 0, 0), (0, 1, 1, 0), (1, 1, 0, 0), (1, 1, 1, 0)],
    "例4 完整解集")

# 例4后练习
sol = []
counts = []
for culprit in "甲乙丙丁":
    truth = [culprit in "丙丁", culprit not in "丙丁", culprit == "乙", culprit != "丁"]
    counts.append(sum(truth))
    if sum(truth) == 1:
        sol.append(culprit)
out(sol == ["丁"] and counts == [2, 3, 2, 1], "例4后练习")

# 例5
sol = []
for winner in "甲乙丙丁":
    truth = [winner in "甲丁", winner not in "甲乙", winner in "乙丁",
             winner == "乙", winner in "乙丙"]
    if sum(truth) == 2:
        sol.append(winner)
out(sol == ["丙"], "例5")

people = "甲乙丙丁"

# 例6
sol = []
for order in itertools.permutations(people):
    p = {x: i + 1 for i, x in enumerate(order)}
    truth = [p["乙"] == 1 or p["丙"] == 1, p["丙"] < p["甲"], p["甲"] < p["丁"],
             p["甲"] == 1, p["丁"] != 1]
    if sum(truth) == 2:
        sol.append(order)
out(sol == [("乙", "丁", "甲", "丙")], "例6")

# 例6后练习只问第4句是否仍假，不要求排列唯一。
sol = []
for order in itertools.permutations(people):
    p = {x: i + 1 for i, x in enumerate(order)}
    truth = [p["乙"] == 1 or p["丙"] == 1, p["丙"] < p["甲"], p["甲"] < p["丁"],
             p["甲"] == 1, p["乙"] != 1]
    if sum(truth) == 2:
        sol.append((order, truth[3]))
out(len(sol) == 7 and all(not fourth for order, fourth in sol), "例6后练习")

# 例7
sol = []
for order in itertools.permutations(people):
    p = {x: i + 1 for i, x in enumerate(order)}
    truth = [p["甲"] < p["乙"], p["甲"] == 4, p["甲"] < p["丁"],
             p["乙"] != 1, p["乙"] != 3]
    if sum(truth) == 1:
        sol.append(order)
out(sol == [("乙", "丁", "甲", "丙")], "例7")

# 例8
sol = []
for a, b in itertools.product([0, 1], repeat=2):
    truth = (not a) and (not b)
    if truth == bool(a):
        sol.append((a, b))
out(sol == [(0, 1)], "例8")

# 例8后练习
sol = []
for a, b in itertools.product([0, 1], repeat=2):
    if [b == 0, a == b] == [bool(a), bool(b)]:
        sol.append((a, b))
out(sol == [(1, 0)], "例8后练习")

# 例9
sol = []
for a, b, c in itertools.product([0, 1], repeat=3):
    truth = [b, not c, a != b]
    if truth == [bool(a), bool(b), bool(c)]:
        sol.append((a, b, c))
out(sol == [(1, 1, 0)], "例9")

# 例10
sol = []
for bits in itertools.product([0, 1], repeat=4):
    k = sum(bits)
    truth = [k == 3, k == 2, k == 1, k == 0]
    if truth == [bool(x) for x in bits]:
        sol.append(bits)
out(sol == [(0, 0, 1, 0)], "例10")

# 例11
sol = []
for order in itertools.permutations(people):
    p = {x: i + 1 for i, x in enumerate(order)}
    pairs = [[p["丁"] == 3, p["丙"] == 4], [p["丁"] == 1, p["丙"] == 4],
             [p["甲"] == 2, p["丙"] == 4], [p["丙"] == 2, p["乙"] == 1]]
    if all(sum(pair) == 1 for pair in pairs):
        sol.append(order)
out(sol == [("乙", "丁", "甲", "丙")], "例11")

# 例11后练习
sol = []
for order in itertools.permutations(people):
    p = {x: i + 1 for i, x in enumerate(order)}
    pairs = [[p["乙"] == 4, p["丙"] == 2], [p["乙"] == 1, p["丙"] == 2],
             [p["甲"] == 1, p["乙"] == 2], [p["丁"] == 1, p["丙"] == 2]]
    if all(sum(pair) == 1 for pair in pairs):
        sol.append((order, pairs))
out(sol == [(("甲", "丙", "乙", "丁"), [[0, 1], [0, 1], [1, 0], [0, 1]])],
    "例11后练习")
