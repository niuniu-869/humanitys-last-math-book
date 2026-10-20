"""Independent numerical checks for K2.2 problems."""
import numpy as np
import sympy as sp
from itertools import combinations, product
from collections import Counter


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
        for v in sorted(adj[u]):
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


def is_graphical(seq):
    seq = sorted(seq, reverse=True)
    while seq:
        d = seq.pop(0)
        if d < 0 or d > len(seq):
            return False
        for i in range(d):
            seq[i] -= 1
            if seq[i] < 0:
                return False
        seq.sort(reverse=True)
    return True


def check(qid, condition):
    print(f"PASS {qid}" if condition else f"FAIL {qid}")
    return condition


def edge_set(adj):
    return {(u, v) for u in adj for v in adj[u] if u < v}


def bipartite(adj):
    marks = {}
    for root in adj:
        if root in marks:
            continue
        marks[root] = 0
        queue = [root]
        for u in queue:
            for v in adj[u]:
                if v in marks and marks[v] == marks[u]:
                    return False
                if v not in marks:
                    marks[v] = 1 - marks[u]
                    queue.append(v)
    return True


def equivalent(relation, points):
    return (all((a, a) in relation for a in points)
            and all((b, a) in relation for a, b in relation)
            and all((a, c) in relation for a, b in relation
                    for b2, c in relation if b == b2))


ok = True

degrees = [1, 2, 3, 2, 4, 2]
ok &= check("K22-01", is_graphical(degrees) and sum(degrees) // 2 == 7 and sum(d % 2 for d in degrees) == 2)

g = graph(7, [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 7)])
expected = {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
for label, edge in zip("ABCD", [(1, 4), (2, 3), (4, 5), (4, 7)]):
    possible = bfs(graph(7, list(edge_set(g)) + [edge]), 1) == expected
    ok &= check(f"K22-02-{label}", possible == (label != "A"))

g = graph(4, [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])
deg = [len(g[i]) for i in g]
odd = sum(x % 2 for x in deg)
circuit = len(components(g)) == 1 and odd == 0
trail = len(components(g)) == 1 and odd in (0, 2)
for label, value, expected_value in zip("ABCD", [circuit, trail and not circuit, not trail and odd == 2, odd == 4], [False, True, False, False]):
    ok &= check(f"K22-03-{label}", value == expected_value)

A = np.ones((3, 3), dtype=int) - np.eye(3, dtype=int)
walks = [(1, j, 1) for j in range(1, 4) if A[0, j-1] and A[j-1, 0]]
ok &= check("K22-04", int((A @ A)[0, 0]) == len(walks) == 2 and walks == [(1, 2, 1), (1, 3, 1)])

# Enumerate attainable leaf counts by exact height, including one-child roots.
leaf_counts = [{1}]
for height in range(1, 5):
    shorter = set().union(*leaf_counts)
    leaf_counts.append(leaf_counts[-1] | {a + b for a in leaf_counts[-1] for b in shorter})
ok &= check("K22-05", (min(leaf_counts[4]), max(leaf_counts[4])) == (1, 16))

sequences = {
    "A": [5, 5, 0, 0, 0, 0],
    "B": [5, 1, 1, 1, 1, 1],
    "C": [2, 2, 2, 2, 2, 2],
    "D": [3, 3, 2, 2, 1, 1],
}
for label, seq in sequences.items():
    ok &= check(f"K22-06-{label}", is_graphical(seq) == (label != "A"))
g6 = graph(6, [(1, 3), (1, 4), (1, 6), (2, 3), (2, 4), (2, 5)])
ok &= check("K22-06-D-construction", [len(g6[i]) for i in g6] == sequences["D"])

g = graph(8, [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8)])
d = bfs(g, 1)
ok &= check("K22-07", [d[i] for i in range(1, 9)] == [0, 1, 1, 2, 2, 3, 3, 4] and len(d) == 8)
for edge, distance in [((4, 8), 3), ((2, 8), 2)]:
    changed = bfs(graph(8, list(edge_set(g)) + [edge]), 1)
    ok &= check(f"K22-07-add{edge[0]}{edge[1]}", {v for v in d if d[v] != changed[v]} == {8} and changed[8] == distance)

g = graph(8, [(1, 2), (2, 3), (3, 1), (4, 5), (4, 6), (4, 7), (4, 8)])
stroke_count = 0
for block in components(g):
    odd = sum(len(g[v]) % 2 for v in block)
    stroke_count += max(1, odd // 2)
strokes = [[1, 2, 3, 1], [5, 4, 6], [7, 4, 8]]
used = Counter(tuple(sorted((a, b))) for route in strokes for a, b in zip(route, route[1:]))
ok &= check("K22-08", len(components(g)) == 2 and stroke_count == 3 and used == Counter(edge_set(g)))

internal = 17
leaves = internal + 1
total = internal + leaves
min_height = int(sp.ceiling(sp.log(leaves, 2)))
ok &= check("K22-09", (leaves, total, min_height) == (18, 35, 5))
tree_edges = [(i // 2, i) for i in range(2, 32)] + [(16, 32), (16, 33), (17, 34), (17, 35)]
tree = graph(35, tree_edges)
children = Counter(a for a, b in tree_edges)
ok &= check("K22-09-construction", max(bfs(tree, 1).values()) == 5 and len(children) == 17 and all(c == 2 for c in children.values()) and len(tree) - len(children) == 18)

S = range(1, 5)
R = {(a, a) for a in S} | {(1, 2), (2, 1), (2, 3), (3, 2)}
missing = set(product(S, repeat=2)) - R
solutions = []
for size in range(len(missing) + 1):
    solutions = [set(extra) for extra in combinations(sorted(missing), size) if equivalent(R | set(extra), S)]
    if solutions:
        break
completed = R | {(1, 3), (3, 1)}
classes = {frozenset(b for b in S if (a, b) in completed) for a in S}
ok &= check("K22-10", solutions == [{(1, 3), (3, 1)}] and classes == {frozenset({1, 2, 3}), frozenset({4})})

M = np.array([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]], dtype=int)
routes = [(1,) + middle + (4,) for middle in product(range(1, 5), repeat=3)
          if all(M[a-1, b-1] for a, b in zip((1,) + middle, middle + (4,)))]
ok &= check("K22-11", len(routes) == int(np.linalg.matrix_power(M, 4)[0, 3]) == 4
            and routes == [(1, 2, 1, 3, 4), (1, 3, 1, 3, 4), (1, 3, 2, 3, 4), (1, 3, 4, 3, 4)]
            and sum(len(set(route)) == len(route) for route in routes) == 0)

M = np.array([[1, 1], [1, 0]], dtype=int)
counts = [sum(bits[0] == bits[-1] and all((a, b) != (1, 1) for a, b in zip(bits, bits[1:]))
              for bits in product((0, 1), repeat=n)) for n in range(1, 9)]
ok &= check("K22-12", counts[:6] == [2, 1, 3, 4, 7, 11]
            and counts == [int(np.trace(np.linalg.matrix_power(M, n-1))) for n in range(1, 9)]
            and np.array_equal(M @ M, M + np.eye(2, dtype=int))
            and all(counts[i] == counts[i-1] + counts[i-2] for i in range(2, len(counts))))

print("MANUAL K22-13")
path = [(i, i+1) for i in range(1, 6)]
allowed = [edge for edge in combinations(range(1, 7), 2) if edge not in path and bipartite(graph(6, path + [edge]))]
ok &= check("K22-13-concrete", allowed == [(1, 4), (1, 6), (2, 5), (3, 6)])

g = graph(9, [(1, 2), (2, 3), (3, 4), (4, 1), (5, 6), (6, 7), (7, 8), (8, 9)])
connected = len(components(g)) == 1
ok &= check("K22-14-counterexample", sum(map(len, g.values())) // 2 == 8 and len(g) == 9 and not connected and bipartite(g))
ok &= check("K22-14-delete-cycle-edge", len(components(graph(9, edge_set(g) - {(1, 2)}))) == len(components(g)))
print("MANUAL K22-14")

raise SystemExit(0 if ok else 1)

