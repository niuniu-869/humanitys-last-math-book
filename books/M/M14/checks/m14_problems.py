import math
import numpy as np


def softmax(z, t=1.0):
    z = np.asarray(z, dtype=float) / t
    z = z - np.max(z)
    e = np.exp(z)
    return e / e.sum()


def top_k(p, k):
    p = np.asarray(p, dtype=float)
    idx = np.argsort(-p, kind="stable")[:k]
    q = np.zeros(len(p), dtype=float)
    q[idx] = p[idx]
    return q / q.sum()


def top_p(p, threshold):
    p = np.asarray(p, dtype=float)
    order = np.argsort(-p, kind="stable")
    c = np.cumsum(p[order])
    m = int(np.searchsorted(c, threshold, side="left")) + 1
    q = np.zeros(len(p), dtype=float)
    q[order[:m]] = p[order[:m]]
    return q / q.sum(), order[:m]


def check(name, condition):
    print(("PASS " if condition else "FAIL ") + name)


p = np.array([0.18, 0.47, 0.35])
c = np.cumsum(p)
draws = [int(np.searchsorted(c, u, side="right")) + 1 for u in (0.17, 0.65, 0.99)]
check("M14-01", draws == [1, 3, 3] and math.isclose(c[0], 0.18) and math.isclose(c[1], 0.65))

p1 = np.array([16, 4, 1]) / 21
p2 = softmax(np.log(p1), 2)
h2 = float(-(p2 * np.log(p2)).sum())
h1 = float(-(p1 * np.log(p1)).sum())
check("M14-02", np.allclose(p2, np.array([4, 2, 1]) / 7) and h2 > h1 and abs(h2 - 0.9557) < 0.00005 and abs(h1 - 0.6680) < 0.00005)

q3 = top_k([0.4, 0.3, 0.2, 0.1], 2)
opt3 = {
    "A": np.isclose(q3.sum(), 0.7),
    "B": np.allclose(q3, [4 / 7, 3 / 7, 0, 0]),
    "C": np.allclose(q3, [0.5, 0.5, 0, 0]),
    "D": np.allclose(q3, [0.4, 0.3, 0.2, 0.1]),
}
check("M14-03", opt3["B"] and not any(opt3[k] for k in ("A", "C", "D")))

s4 = 0.42 / 0.6
p4 = [0.42, 0.4 * s4, 0.18, 0.07, 0.05]
q4, keep4 = top_p(p4, 0.70)
sizes4 = [len(top_p(p4, t)[1]) for t in (0.42, 0.420001, 0.70, 0.700001)]
check("M14-04", math.isclose(s4, 0.7) and math.isclose(p4[1], 0.28) and sizes4 == [1, 2, 2, 3] and np.array_equal(keep4, [0, 1]) and np.allclose(q4, [0.6, 0.4, 0, 0, 0]))

temps5 = np.array([0.25, 0.5, 1, 1.001, 2, 10])
two5 = np.array([len(top_p(top_k(softmax(np.log([4, 2, 1]), t), 2), 2 / 3)[1]) == 2 for t in temps5])
opt5 = {
    "A": np.array_equal(two5, temps5 < 1),
    "B": np.array_equal(two5, temps5 > 1),
    "C": np.array_equal(two5, temps5 >= 1),
    "D": bool(np.all(two5)),
}
check("M14-05", opt5["B"] and not any(opt5[k] for k in ("A", "C", "D")))

q6 = top_k([0.12, 0.33, 0.27, 0.18, 0.10], 3)
c6 = np.cumsum(q6)
draw6 = [int(np.searchsorted(c6, u, side="right")) + 1 for u in (0.10, 0.50, 0.79)]
check("M14-06", np.allclose(q6, [0, 0.4230769231, 0.3461538462, 0.2307692308, 0]) and draw6 == [2, 3, 4])

t7 = 4 / math.log(9)
p7, cold7 = softmax([2, 0, -2], t7), softmax([2, 0, -2], t7 / 2)
check("M14-07", math.isclose(p7[0] / p7[2], 9) and np.allclose(p7, np.array([9, 3, 1]) / 13) and np.allclose(cold7, np.array([81, 9, 1]) / 91) and len(top_p(p7, 0.8)[1]) == 2 and len(top_p(cold7, 0.8)[1]) == 1 and -(p7 * np.log(p7)).sum() > -(cold7 * np.log(cold7)).sum())

p8 = [np.array([0.72, 0.12, 0.08, 0.05, 0.03]), np.array([0.28, 0.24, 0.20, 0.16, 0.12])]
mass8k = [p[top_k(p, 2) > 0].sum() for p in p8]
keep8p = [top_p(p, 0.8)[1] for p in p8]
mass8p = [p[keep].sum() for p, keep in zip(p8, keep8p)]
sizes8p = [len(keep) for keep in keep8p]
opt8 = {
    "A": np.allclose(mass8k, [0.8, 0.8]),
    "B": np.allclose(mass8k, [0.84, 0.52]) and sizes8p == [2, 4] and np.allclose(mass8p, [0.84, 0.88]),
    "C": np.allclose(mass8p, [0.8, 0.8]),
    "D": sizes8p == [2, 2],
}
check("M14-08", opt8["B"] and not any(opt8[k] for k in ("A", "C", "D")))

print("MANUAL M14-09")

q10 = top_k([0.5, 0.3, 0.2], 2)
bad_c10 = np.cumsum([0.5, 0.3, 0])
check("M14-10", np.allclose(q10, [0.625, 0.375, 0]) and all(np.searchsorted(bad_c10, u, side="right") == 3 for u in (0.8, 0.9, 0.999)))

tree11 = {
    "": {"x": 0.55, "y": 0.45},
    "x": {"a": 0.60, "b": 0.40}, "y": {"c": 0.95, "d": 0.05},
    "xa": {"e": 0.5, "f": 0.5}, "xb": {"g": 0.99, "h": 0.01},
    "yc": {"i": 0.5, "j": 0.5}, "yd": {"k": 0.9, "l": 0.1},
}


def beam(width):
    candidates = [("", 1.0)]
    history = []
    for _ in range(3):
        expanded = [(prefix + token, prob * cond) for prefix, prob in candidates for token, cond in tree11[prefix].items()]
        candidates = sorted(expanded, key=lambda pair: (-pair[1], pair[0]))[:width]
        history.append(candidates)
    return history


b1, b2, exhaustive = beam(1), beam(2), beam(8)
expected11 = {"xae": 0.165, "xaf": 0.165, "xbg": 0.2178, "xbh": 0.0022, "yci": 0.21375, "ycj": 0.21375, "ydk": 0.02025, "ydl": 0.00225}
check("M14-11", [[s for s, _ in step] for step in b1] == [["x"], ["xa"], ["xae"]] and [[s for s, _ in step] for step in b2] == [["x", "y"], ["yc", "xa"], ["yci", "ycj"]] and all(math.isclose(p, expected11[s]) for s, p in exhaustive[-1]) and exhaustive[-1][0][0] == "xbg" and math.isclose(sum(p for _, p in exhaustive[-1]), 1))

print("MANUAL M14-12")

t0 = 2 / math.log(3)
p_t0 = math.exp(2 / t0) / (1 + math.exp(2 / t0))
check("M14-13", math.isclose(t0, 1.8204784532536746) and math.isclose(p_t0, 0.75))

per14 = 2 * 24 * 16 * 64 * 8 * 2
n14, remainder14 = divmod(2**30, per14)
check("M14-14", n14 == 1365 and remainder14 == 262144 and n14 * per14 == 1073479680 and (n14 + 1) * per14 == 1074266112 and n14 * per14 <= 2**30 < (n14 + 1) * per14 and per14 == 2 * 24 * 8 * 128 * 8 * 2)

q15 = softmax([2, 1])
q15b = softmax([2, 1, 0])
draw15 = int(np.searchsorted(np.cumsum(q15), 0.70, side="right")) + 1
draw15b = int(np.searchsorted(np.cumsum(q15b), 0.70, side="right")) + 1
check("M14-15", draw15 == 1 and draw15b == 2)

p16 = softmax([2, 1, 1, 0])
q16a, keep16a = top_p(top_k(p16, 2), 0.8)
threshold16 = np.sort(p16)[-2]
p16b = np.where(p16 >= threshold16, p16, 0)
q16b, keep16b = top_p(p16b / p16b.sum(), 0.8)
draw16 = [int(np.searchsorted(np.cumsum(q), 0.90, side="right")) + 1 for q in (q16a, q16b)]
check("M14-16", np.allclose(q16a, [math.e / (math.e + 1), 1 / (math.e + 1), 0, 0]) and np.allclose(q16b, np.array([math.e, 1, 1, 0]) / (math.e + 2)) and list(keep16a) == [0, 1] and list(keep16b) == [0, 1, 2] and draw16 == [2, 3])

p17 = np.array([[0.9, 0.9, 0.1], [0.6, 0.6, 0.6]])
means17 = p17.mean(axis=1)
losses17 = -np.log(p17).mean(axis=1)
wrong17 = -np.log(means17)
check("M14-17", means17[0] > means17[1] and losses17[0] > losses17[1] and wrong17[0] < wrong17[1] and np.allclose(means17, [1.9 / 3, 0.6]) and np.allclose(losses17, [0.8378, 0.5108], atol=0.00005) and np.allclose(wrong17, [0.4568, 0.5108], atol=0.00005))

widths18 = range(64, 4097, 64)
counts18 = {w: 24 * (4 * 512**2 + 2 * 512 * w) for w in widths18}
max18 = max(w for w, count in counts18.items() if count <= 80000000)
cache18 = 2 * 24 * 8 * 64 * 1024 * 2
batch18 = (64 * 2**20) // cache18
check("M14-18", max18 == 2176 and counts18[max18] == 78643200 and counts18[max18 + 64] == 80216064 and counts18[max18] <= 80000000 < counts18[max18 + 64] and cache18 == 50331648 and batch18 == 1 and batch18 * cache18 <= 64 * 2**20 < (batch18 + 1) * cache18)
