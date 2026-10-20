"""Independent checks for the numerical conclusions in lesson.md."""
import math
import numpy as np
import sympy as sp
from collections import Counter
from itertools import combinations, product


def graph(n, edges):
    adj = {i: set() for i in range(1, n + 1)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def bfs(adj, start):
    dist = {start: 0}
    q = [start]
    for u in q:
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def components(adj):
    unseen = set(adj)
    out = []
    while unseen:
        s = min(unseen)
        block = set(bfs(adj, s))
        out.append(block)
        unseen -= block
    return out


def bipartite(adj):
    color = {}
    for root in adj:
        if root in color:
            continue
        color[root] = 0
        q = [root]
        for u in q:
            for v in adj[u]:
                if v in color and color[v] == color[u]:
                    return False
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
    return True


def pass_example(k, cond):
    print(f"PASS 例{k}" if cond else f"FAIL 例{k}")
    return cond


ok = True

old = graph(6, [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6)])
ds = [len(old[i]) for i in range(1, 7)]
ok &= pass_example(1, ds == [2, 3, 4, 4, 3, 2] and sum(ds) == 18 and sum(d % 2 for d in ds) == 2)

ok &= pass_example(2, (7 * 3) % 2 == 1 and (8 * 3) // 2 == 12)

g3 = graph(6, [(a, b) for a in range(1, 4) for b in range(4, 7)] + [(1, 2)])
ok &= pass_example(3, 20 // 3 == len(g3) == 6 and sum(map(len, g3.values())) // 2 == 10 and min(map(len, g3.values())) >= 3)

d = bfs(old, 5)
ok &= pass_example(4, d == {5: 0, 3: 1, 4: 1, 6: 1, 1: 2, 2: 2})

g5 = graph(8, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (7, 8)])
ok &= pass_example(5, len(components(g5)) == 3)

ok &= pass_example(6, 16 > (7 - 1) * (7 - 2) // 2)

bridges = [(1, 2), (1, 2), (1, 3), (1, 3), (2, 4), (3, 4), (1, 4)]
bridge_degrees = Counter(v for edge in bridges for v in edge)
ok &= pass_example(7, len(bridges) == 7 and list(bridge_degrees[v] for v in range(1, 5)) == [5, 3, 3, 3] and sum(d % 2 for d in bridge_degrees.values()) == 4)
old_edges = {(u, v) for u in old for v in old[u] if u < v}
route = [2, 1, 3, 2, 4, 3, 5, 4, 6, 5]
used = Counter(tuple(sorted(edge)) for edge in zip(route, route[1:]))
ok &= pass_example(8, used == Counter(old_edges) and len(components(old)) == 1 and {v for v in old if len(old[v]) % 2} == {2, 5})

grid_edges = [(3*r+c+1, 3*r+c+2) for r in range(3) for c in range(2)] + [(3*r+c+1, 3*(r+1)+c+1) for r in range(2) for c in range(3)]
grid = graph(9, grid_edges)
odd = [v for v in grid if len(grid[v]) % 2]
augmented = graph(9, grid_edges + [(2, 8)])
ok &= pass_example(9, len(grid_edges) == 12 and Counter(map(len, grid.values())) == {2: 4, 3: 4, 4: 1} and len(odd) // 2 == 2 and len(components(augmented)) == 1 and sum(len(ns) % 2 for ns in augmented.values()) == 2)

ok &= pass_example(10, 10 - 7 == 3)

leaf = sp.symbols("leaf", integer=True)
solutions = sp.solve(sp.Eq(2 * 3 + 2 + leaf, 2 * (3 + leaf - 1)), leaf)
ok &= pass_example(11, solutions == [4] and 3 + solutions[0] == 7)

counter = graph(4, [(1, 2), (2, 3), (3, 1)])
ok &= pass_example(12, len(counter) == 4 and len(components(counter)) == 2)

ok &= pass_example(13, 2**6 < 100 <= 2**7)
ok &= pass_example(14, 2**2 < 6 <= 2**3)
ok &= pass_example(15, 32 - 1 == 31)

A = np.array([
    [0, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1],
    [0, 0, 0, 1, 1, 0],
], dtype=int)
A2 = A @ A
A3 = A2 @ A
ok &= pass_example(16, A2[0].tolist() == [2, 1, 1, 2, 1, 0] and A3[0].tolist() == [2, 5, 6, 3, 3, 3])
triangles = [triple for triple in combinations(range(1, 7), 3) if all(b in old[a] for a, b in combinations(triple, 2))]
ok &= pass_example(17, np.diag(A3).tolist() == [2, 4, 6, 6, 4, 2] and int(np.trace(A3)) == 24 and triangles == [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)])

M = np.array([[1, 1], [1, 0]], dtype=int)
ok &= pass_example(18, int(np.linalg.matrix_power(M, 5).sum()) == 21)

old_has_triangle = all(v in old[u] for u, v in [(1, 2), (2, 3), (3, 1)])
ok &= pass_example(19, old_has_triangle)
cycle7 = graph(7, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)])
path7 = graph(7, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])
ok &= pass_example(20, not bipartite(cycle7) and bipartite(path7))

ok &= pass_example(21, 26 > (10 * 10) // 4)

R22 = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}
S22 = {1, 2, 3, 4}
refl = all((x, x) in R22 for x in S22)
sym = all((b, a) in R22 for a, b in R22)
trans = all((a, c) in R22 for a, b in R22 for b2, c in R22 if b == b2)
ok &= pass_example(22, not refl and sym and trans)

partitions = {frozenset(frozenset(i+1 for i, label in enumerate(labels) if label == block)
                        for block in set(labels)) for labels in product(range(4), repeat=4)}
sizes = Counter(tuple(sorted(map(len, partition), reverse=True)) for partition in partitions)
ok &= pass_example(23, len(partitions) == 15 and sizes == {(4,): 1, (3, 1): 4, (2, 2): 3, (2, 1, 1): 6, (1, 1, 1, 1): 1})

ok &= pass_example(24, math.gcd(2, 2) != 1 and math.gcd(2, 3) == 1 and math.gcd(3, 4) == 1 and math.gcd(2, 4) != 1)

g = graph(5, [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
ok &= pass_example("随堂-度", [len(g[i]) for i in g] == [2, 2, 3, 2, 1] and sum(map(len, g.values())) == 10)
ok &= pass_example("随堂-分层", bfs(old, 1) == {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3})
minus_bd = graph(6, old_edges - {(2, 4)})
ok &= pass_example("随堂-欧拉", len(components(minus_bd)) == 1 and [len(minus_bd[i]) for i in minus_bd] == [2, 2, 4, 3, 3, 2])
ok &= pass_example("随堂-森林", sp.solve(sp.Eq(11, 15 - leaf), leaf) == [4])
chosen = [(1, 3), (2, 3), (2, 4), (4, 5), (5, 6)]
deleted = [(1, 2), (3, 4), (3, 5), (4, 6)]
ok &= pass_example("随堂-生成树", len(components(graph(6, chosen))) == 1 and len(chosen) == 5 and set(chosen) | set(deleted) == old_edges and len(deleted) == 4)
koenig = [(0, 1), (0, 1), (0, 2), (0, 2), (0, 3), (1, 3), (2, 3)]
kd = Counter(v for e in koenig for v in e)
kd2 = kd.copy(); kd2[1] += 1; kd2[2] += 1
ok &= pass_example("随堂-柯尼斯堡加桥", sorted(kd.values()) == [3, 3, 3, 5] and sum(1 for v in kd2.values() if v % 2) == 2)
Mx = np.array([[1 if j in old[i] else 0 for j in range(1, 7)] for i in range(1, 7)])
ok &= pass_example("随堂-B到E两步", (Mx @ Mx)[1][4] == 2)
sym = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1), (2, 3), (3, 2)}
cls = lambda R, a: frozenset(x for x in range(1, 4) if (x, a) in R)
ok &= pass_example("等价类缺条件", cls({(1, 1), (2, 2), (1, 2), (2, 1)}, 3) == frozenset()
                   and cls({(1, 1), (2, 2), (3, 3), (1, 2)}, 1) == {1} and cls({(1, 1), (2, 2), (3, 3), (1, 2)}, 2) == {1, 2}
                   and cls(sym, 1) == {1, 2} and cls(sym, 2) == {1, 2, 3})
for name, route in [("路径", [1, 2, 3, 4, 5, 6]), ("圈", [1, 2, 4, 6, 5, 3, 1])]:
    ok &= pass_example("哈密顿-" + name, len(set(route[:6])) == 6 and all(b in old[a] for a, b in zip(route, route[1:])))
children = {4: (2, 6), 2: (1, 3), 6: (5, 7)}


def traverse(root, mode):
    if root not in children:
        return [root]
    left, right = (traverse(child, mode) for child in children[root])
    return {"pre": [root] + left + right, "in": left + [root] + right, "post": left + right + [root]}[mode]


for mode, expected in [("pre", [4, 2, 1, 3, 6, 5, 7]), ("in", list(range(1, 8))), ("post", [1, 3, 2, 5, 7, 6, 4])]:
    ok &= pass_example("遍历-" + mode, traverse(4, mode) == expected)
points = {1, 2, 3, 4, 6, 12}
covers = {(a, b) for a in points for b in points if a != b and b % a == 0 and not any(c != a and c != b and c % a == 0 and b % c == 0 for c in points)}
ok &= pass_example("哈斯图", covers == {(1, 2), (1, 3), (2, 4), (2, 6), (3, 6), (4, 12), (6, 12)})
closed = [(1, a, b, 1) for a, b in product(range(1, 7), repeat=2) if a in old[1] and b in old[a] and 1 in old[b]]
ok &= pass_example("随堂-三步", closed == [(1, 2, 3, 1), (1, 3, 2, 1)])
ok &= pass_example("随堂-猜数", math.ceil(math.log2(50)) == 6)
ok &= pass_example("随堂-六边圈", bipartite(graph(6, [(i, i+1) for i in range(1, 6)] + [(6, 1)])))
relation = {(1, 1), (2, 2), (3, 3), (1, 2)}
ok &= pass_example("随堂-偏序", all((a, a) in relation for a in range(1, 4)) and not all((b, a) in relation for a, b in relation)
                   and all(a == b for a, b in relation if (b, a) in relation)
                   and all((a, c) in relation for a, b in relation for b2, c in relation if b == b2))

raise SystemExit(0 if ok else 1)

