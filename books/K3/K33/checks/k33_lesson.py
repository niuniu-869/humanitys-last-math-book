"""Recompute all 22 worked examples; shared algorithms have no answer constants."""

from collections import deque
from itertools import combinations, permutations, product
from pathlib import Path
import sys

import numpy as np
import sympy as sp


def binary(values, target):
    lo, hi, trace = 1, len(values), []
    while lo <= hi:
        mid = (lo + hi) // 2
        trace.append((lo, hi, mid))
        if values[mid - 1] == target:
            return mid, trace, (lo, hi)
        if values[mid - 1] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return 0, trace, (lo, hi)


def lower_bound(values, target, broken=False):
    lo, hi, trace = 1, len(values) + 1, []
    while lo < hi:
        mid = (lo + hi) // 2
        trace.append((lo, hi, mid))
        if values[mid - 1] < target:
            lo = mid + 1
        else:
            hi = mid - 1 if broken else mid
    return lo, trace


def insert(tree, value):
    if tree is None:
        return [value, None, None]
    side = 1 if value < tree[0] else 2
    tree[side] = insert(tree[side], value)
    return tree


def build(values):
    tree = None
    for value in values:
        tree = insert(tree, value)
    return tree


def search(tree, value):
    path = []
    while tree:
        path.append(tree[0])
        if tree[0] == value:
            return path, True
        tree = tree[1 if value < tree[0] else 2]
    return path, False


def delete(tree, value):
    if tree is None:
        return None
    if value != tree[0]:
        side = 1 if value < tree[0] else 2
        tree[side] = delete(tree[side], value)
    elif tree[1] is None:
        return tree[2]
    elif tree[2] is None:
        return tree[1]
    else:
        successor = tree[2]
        while successor[1]:
            successor = successor[1]
        tree[0] = successor[0]
        tree[2] = delete(tree[2], successor[0])
    return tree


def depths(tree, depth=1):
    if tree is None:
        return {}
    return {tree[0]: depth, **depths(tree[1], depth + 1),
            **depths(tree[2], depth + 1)}


def inorder(tree):
    return [] if tree is None else inorder(tree[1]) + [tree[0]] + inorder(tree[2])


def graph(vertices, edges, directed=False):
    adjacency = {v: [] for v in vertices}
    for u, v in edges:
        adjacency[u].append(v)
        if not directed:
            adjacency[v].append(u)
    return {u: sorted(vs) for u, vs in adjacency.items()}


def bfs(adjacency, source):
    queue = deque([source])
    distance, parent, order, queues = {source: 0}, {}, [], []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adjacency[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                parent[v] = u
                queue.append(v)
        queues.append(list(queue))
    return order, distance, parent, queues


def dfs(adjacency, roots):
    visited, entry, finish, starts, non_tree = set(), [], [], [], []

    def visit(u, parent=None):
        visited.add(u)
        entry.append(u)
        for v in adjacency[u]:
            if v not in visited:
                visit(v, u)
            elif v != parent:
                non_tree.append((u, v))
        finish.append(u)

    for root in roots:
        if root not in visited:
            starts.append(root)
            visit(root)
    return entry, finish, starts, non_tree


def restore(parent, source, target):
    path = [target]
    while path[-1] != source:
        path.append(parent[path[-1]])
    return path[::-1]


def topo(vertices, edges):
    adjacency = graph(vertices, edges, True)
    degree = {v: 0 for v in vertices}
    for _, v in edges:
        degree[v] += 1
    initial = degree.copy()
    queue = deque(v for v in vertices if degree[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        # Use the given vertex order, as in the lesson's input-order convention.
        for v in vertices:
            if v in adjacency[u]:
                degree[v] -= 1
                if degree[v] == 0:
                    queue.append(v)
    return order, initial, degree


def topo_orders(vertices, edges):
    return [p for p in permutations(vertices)
            if all(p.index(u) < p.index(v) for u, v in edges)]


def weighted(vertices, edges, directed=False):
    adjacency = {v: [] for v in vertices}
    for u, v, weight in edges:
        adjacency[u].append((v, weight))
        if not directed:
            adjacency[v].append((u, weight))
    return adjacency


def simple_paths(adjacency, source, target):
    found = []

    def walk(u, path, length):
        if u == target:
            found.append((tuple(path), sp.expand(length)))
            return
        for v, weight in adjacency[u]:
            if v not in path:
                walk(v, path + [v], length + weight)

    walk(source, [source], sp.Integer(0))
    return found


def dijkstra(adjacency, source):
    distance = {v: sp.oo for v in adjacency}
    distance[source] = 0
    done, order, parent, snapshots = set(), [], {}, []
    while len(done) < len(adjacency):
        u = min((v for v in adjacency if v not in done),
                key=lambda v: (distance[v], v))
        done.add(u)
        order.append(u)
        for v, weight in adjacency[u]:
            if v not in done and distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                parent[v] = u
        snapshots.append(distance.copy())
    return order, distance, parent, snapshots


def formula(clauses, n):
    symbols = sp.symbols(f"x1:{n + 1}")
    return sp.And(*(sp.Or(*(symbols[abs(lit) - 1] if lit > 0
                            else sp.Not(symbols[-lit - 1]) for lit in clause))
                    for clause in clauses)), symbols


def models(clauses, n):
    expression, symbols = formula(clauses, n)
    return {values for values in product((False, True), repeat=n)
            if expression.subs(dict(zip(symbols, values))) == sp.true}


def propagate(clauses, initial=None):
    assignment = dict(initial or {})
    trail = []
    while True:
        changed = False
        for clause in clauses:
            if any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0)
                   for lit in clause):
                continue
            undecided = [lit for lit in clause if abs(lit) not in assignment]
            if not undecided:
                return assignment, True, trail
            if len(undecided) == 1:
                lit = undecided[0]
                assignment[abs(lit)] = lit > 0
                trail.append(lit)
                changed = True
        if not changed:
            return assignment, False, trail


def stack_orders(n):
    results = set()

    def walk(next_value, stack, output):
        if len(output) == n:
            results.add(tuple(output))
        if next_value <= n:
            walk(next_value + 1, stack + [next_value], output)
        if stack:
            walk(next_value, stack[:-1], output + [stack[-1]])

    walk(1, [], [])
    return results


def brackets(text):
    stack, pairs = [], {')': '(', ']': '[', '}': '{'}
    for char in text:
        if char in pairs.values():
            stack.append(char)
        elif not stack or stack.pop() != pairs[char]:
            return False
    return not stack


def queens(n):
    counts, solutions = [0] * (n + 1), []

    def place(prefix):
        counts[len(prefix)] += 1
        if len(prefix) == n:
            solutions.append(tuple(prefix))
            return
        for col in range(1, n + 1):
            if all(col != old and abs(col - old) != len(prefix) - row
                   for row, old in enumerate(prefix)):
                place(prefix + [col])

    place([])
    return solutions, counts


def check(label, actual, expected):
    ok = actual == expected
    print(f"{'PASS' if ok else 'FAIL'} {label}" +
          ("" if ok else f" computed={actual!r}; expected={expected!r}"))
    return int(not ok)


def lesson_checks():
    failures = 0
    text = (Path(__file__).resolve().parents[1] / 'lesson.md').read_text()

    def verify(number, actual, expected):
        nonlocal failures
        if f'**例 {number}**' not in text:
            failures += check(f'例{number}', 'missing example', 'present')
        else:
            label = f'例{number}'
            if number == 1:
                label += ' 数值吻合；并核对「没找到不一定多一轮」的反例'
            failures += check(label, actual, expected)

    array = [1, 2, 3, 5, 8, 9]
    # Verify the worked trace and expose, rather than endorse, its overgeneralization.
    verify(1, (binary(array, 4), binary(array, 1)[:2], binary(array, 8)[:2],
               len(binary(array, 0)[1]), len(binary(array, 5)[1])),
           ((0, [(1, 6, 3), (4, 6, 5), (4, 4, 4)], (4, 3)),
            (1, [(1, 6, 3), (1, 2, 1)]), (5, [(1, 6, 3), (4, 6, 5)]), 2, 3))
    values = [1, 2, 2, 2, 5, 7, 7, 9]
    verify(2, (lower_bound(values, 7), lower_bound(values, 6)[0],
               lower_bound(values, 3)[0] - lower_bound(values, 2)[0]),
           ((6, [(1, 9, 5), (6, 9, 7), (6, 7, 6)]), 6, 3))
    values = [5, 2, 8, 1, 9, 3]
    tree = build(values)
    mean = sp.Rational(sum(depths(tree).values()), len(values))
    modified = delete(build(values), 5)
    verify(3, (modified, mean, len(search(insert(tree, 4), 4)[0])),
           ([8, [2, [1, None, None], [3, None, None]], [9, None, None]],
            sp.Rational(14, 6), 4))
    chain_depths = list(depths(build(sorted(values))).values())
    min_sum = min(sum(depths(build(p)).values()) for p in permutations(values))
    verify(4, (chain_depths, sp.Rational(sum(chain_depths), 6), min_sum),
           ([1, 2, 3, 4, 5, 6], sp.Rational(7, 2), 14))
    verify(5, [brackets(s) for s in ('{[()]}', '([)]', '(()')], [True, False, False])
    verify(6, (stack_orders(3), len(stack_orders(4))),
           ({(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 2, 1)}, 14))
    queue = deque([('A', 3), ('B', 1), ('C', 2)])
    completed, states, time = [], [], 0
    while queue:
        name, remaining = queue.popleft()
        remaining -= 1
        time += 1
        if remaining:
            queue.append((name, remaining))
        else:
            completed.append((name, time))
        states.append(list(queue))
    verify(7, (completed, states),
           ([('B', 2), ('C', 5), ('A', 6)],
            [[('B', 1), ('C', 2), ('A', 2)], [('C', 2), ('A', 2)],
             [('A', 2), ('C', 1)], [('C', 1), ('A', 1)], [('A', 1)], []]))
    edges = [('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1), ('B', 'D', 5),
             ('C', 'D', 8), ('C', 'E', 10), ('D', 'E', 2), ('D', 'F', 6),
             ('E', 'F', 3)]
    adjacency = graph('ABCDEF', [(u, v) for u, v, _ in edges])
    order, distance, parent, queues = bfs(adjacency, 'E')
    verify(8, (order, [distance[v] for v in 'ABCDEF'], parent['B'], queues),
           (list('ECDFAB'), [2, 2, 1, 1, 0, 1], 'C',
            [list('CDF'), list('DFAB'), list('FAB'), list('AB'), ['B'], []]))
    paths = simple_paths(weighted('ABCDEF', [(u, v, 1) for u, v, _ in edges]), 'E', 'B')
    verify(9, (restore(parent, 'E', 'B'), min(length for _, length in paths)),
           (list('ECB'), 2))
    maze = ['S.#....', '..#.##.', '..#..#.', '....#.E']
    cells = [(r, c) for r in range(4) for c in range(7) if maze[r][c] != '#']
    cell_set = set(cells)
    maze_graph = {u: sorted(v for v in cell_set
                           if abs(u[0] - v[0]) + abs(u[1] - v[1]) == 1) for u in cells}
    distance = bfs(maze_graph, (0, 0))[1]
    observed = np.array([[distance.get((r, c), -1) for c in range(7)] for r in range(4)])
    expected = np.array([[0, 1, -1, 9, 10, 11, 12], [1, 2, -1, 8, -1, -1, 13],
                         [2, 3, -1, 7, 8, -1, 14], [3, 4, 5, 6, -1, 16, 15]])
    verify(10, bool(np.array_equal(observed, expected)), True)
    jug = {}
    for a, b in product(range(4), range(6)):
        ab, ba = min(a, 5 - b), min(b, 3 - a)
        jug[a, b] = sorted({(3, b), (a, 5), (0, b), (a, 0),
                            (a - ab, b + ab), (a + ba, b - ba)} - {(a, b)})
    distance = bfs(jug, (0, 0))[1]
    route = [(0, 0), (0, 5), (3, 2), (0, 2), (2, 0), (2, 5), (3, 4)]
    verify(11, (min(d for state, d in distance.items() if 4 in state),
                all(v in jug[u] for u, v in zip(route, route[1:]))), (6, True))
    entry, finish, _, non_tree = dfs(adjacency, ['E'])
    verify(12, (entry, finish), (list('ECABDF'), list('FDBACE')))
    land = np.array([[1, 1, 0, 0, 0], [1, 1, 0, 1, 1],
                     [0, 0, 1, 0, 0], [0, 0, 0, 1, 1]])
    cells = sorted(map(tuple, np.argwhere(land)))
    land_graph = {u: [v for v in cells if sum(abs(a - b) for a, b in zip(u, v)) == 1]
                  for u in cells}
    entry, _, starts, _ = dfs(land_graph, cells)
    component_sizes = [len(bfs(land_graph, s)[0]) for s in starts]
    verify(13, (len(starts), component_sizes), (4, [4, 2, 1, 2]))
    cycle = list('CABC')
    verify(14, (non_tree[0], all(v in adjacency[u] for u, v in zip(cycle, cycle[1:]))),
           (('B', 'C'), True))
    leaves, node_counts = [], [0] * 4

    def permute(prefix):
        node_counts[len(prefix)] += 1
        if len(prefix) == 3:
            leaves.append(''.join(prefix))
        for x in 'abc':
            if x not in prefix:
                permute(prefix + [x])

    permute([])
    verify(15, (leaves, node_counts[-1]), (['abc', 'acb', 'bac', 'bca', 'cab', 'cba'], 6))
    solutions4, counts4 = queens(4)
    solutions8, counts8 = queens(8)
    verify(16, (solutions4, counts4, sum(counts4), 4 ** 4,
                len(solutions8), sum(counts8), 8 ** 8),
           ([(2, 4, 1, 3), (3, 1, 4, 2)], [1, 4, 6, 4, 2], 17, 256,
            92, 2057, 16777216))
    clauses = [(-1, 2), (-1, 3), (-2, -3), (1, 4), (-4, 5), (2, -5)]
    verify(17, (models(clauses, 5), propagate(clauses, {1: True})[1],
                propagate(clauses, {1: False})[:2]),
           ({(False, True, False, True, True)}, True,
            ({1: False, 4: True, 5: True, 2: True, 3: False}, False)))
    path_clauses = [(1, 2), (-1, -2), (2, 3), (-2, -3)]
    triangle = path_clauses + [(1, 3), (-1, -3)]
    seating_clauses = []
    for line in ([3 * r + c + 1 for c in range(3)] for r in range(3)):
        seating_clauses.append(tuple(line))
        seating_clauses.extend(tuple(-v for v in pair) for pair in combinations(line, 2))
    for line in ([3 * r + c + 1 for r in range(3)] for c in range(3)):
        seating_clauses.append(tuple(line))
        seating_clauses.extend(tuple(-v for v in pair) for pair in combinations(line, 2))
    verify(18, (models(path_clauses, 3), models(triangle, 3), len(seating_clauses),
                len(models(seating_clauses, 9)),
                [propagate(triangle, {1: b})[1] for b in (True, False)]),
           ({(True, False, True), (False, True, False)}, set(), 24, 6, [True, True]))
    vertices = list('PDMGOB')
    directed_edges = [('P', 'D'), ('D', 'G'), ('M', 'G'), ('D', 'O'), ('D', 'B')]
    result = topo(vertices, directed_edges)
    verify(19, (result[0], [result[1][v] for v in vertices],
                tuple(vertices) in topo_orders(vertices, directed_edges)),
           (list('PMDGOB'), [0, 1, 0, 2, 1, 1], True))
    result = topo(vertices, directed_edges + [('G', 'D')])
    verify(20, (result[0], [v for v in vertices if v not in result[0]],
                len(topo_orders(vertices, directed_edges + [('G', 'D')]))),
           (list('PM'), list('DGOB'), 0))
    wg = weighted('ABCDEF', edges)
    order, distance, parent, snapshots = dijkstra(wg, 'A')
    exhaustive = {v: min(length for _, length in simple_paths(wg, 'A', v)) for v in wg}
    verify(21, (order, [distance[v] for v in 'ABCDEF'], distance == exhaustive,
                restore(parent, 'A', 'F'), [[row[v] for v in 'ABCDEF'] for row in snapshots]),
           (list('ACBDEF'), [0, 3, 2, 8, 10, 13], True, list('ACBDEF'),
            [[0, 4, 2, sp.oo, sp.oo, sp.oo], [0, 3, 2, 10, 12, sp.oo],
             [0, 3, 2, 8, 12, sp.oo], [0, 3, 2, 8, 10, 14],
             [0, 3, 2, 8, 10, 13], [0, 3, 2, 8, 10, 13]]))
    negative = weighted('sab', [('s', 'a', 2), ('s', 'b', 3), ('b', 'a', -2)], True)
    verify(22, (dijkstra(negative, 's')[1]['a'],
                min(length for _, length in simple_paths(negative, 's', 'a'))), (2, 1))
    return failures


if __name__ == '__main__':
    sys.exit(bool(lesson_checks()))
