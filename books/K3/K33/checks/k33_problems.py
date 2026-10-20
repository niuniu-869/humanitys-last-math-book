"""Check computed results against answers, including every choice alternative.

Expected values below transcribe answers.md; actual values come from simulation,
exhaustive enumeration, or symbolic calculation, never from those constants.
Text anchors prevent an edited answer from silently retaining an obsolete PASS.
"""

from collections import Counter, deque
from itertools import combinations, permutations, product
from pathlib import Path
import re
import sys

import sympy as sp

from k33_lesson import (bfs, binary, build, check, depths, dfs, dijkstra,
                        formula, graph, insert, lower_bound, models, propagate,
                        restore, search, simple_paths, topo, topo_orders, weighted)


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / 'answers.md').read_text(encoding='utf-8')
PROBLEMS = (ROOT / 'problems.md').read_text(encoding='utf-8')


def blocks(text):
    return {match[1]: match[2] for match in re.finditer(
        r'^\*\*(K33-\d+)\*\*(.*?)(?=^\*\*K33-\d+\*\*|\Z)', text, re.M | re.S)}


ANSWER = blocks(ANSWERS)
PROBLEM = blocks(PROBLEMS)


def equal(actual, expected):
    assert actual == expected, f'computed={actual!r}; answer={expected!r}'


def anchors(pid, *snippets):
    compact = re.sub(r'\s+', '', ANSWER[pid])
    for snippet in snippets:
        assert re.sub(r'\s+', '', snippet) in compact, f'answer text changed: {snippet}'


def choice(pid, truth):
    answer = re.search(r'\*\*答案：\*\*\s*\(([A-D])\)', ANSWER[pid])[1]
    failures = 0
    for letter, value in zip('ABCD', truth):
        failures += check(f'{pid}({letter})', bool(value), letter == answer)
    equal(failures, 0)


def problem_01():
    position, trace, _ = binary([-3, 0, 4, 7, 9, 12, 18], 12)
    equal((position, trace), (6, [(1, 7, 4), (5, 7, 6)]))
    anchors('K33-01', '返回位置 6，共比较 2 次', '(1,7,4)', '(5,7,6)')


def problem_02():
    tree = build([6, 2, 10, 4])
    before = search(tree, 5)
    after = search(insert(tree, 5), 5)
    equal((before, after), (([6, 2, 4], False), ([6, 2, 4, 5], True)))
    anchors('K33-02', '$6,2,4$，比较 3 次', '$6,2,4,5$，比较 4 次', '父结点为 4')


def problem_03():
    stack, queue, stack_out, queue_out = [], deque(), [], []
    for action in (1, 2, None, 3, None, None):
        if action is None:
            stack_out.append(stack.pop())
            queue_out.append(queue.popleft())
        else:
            stack.append(action)
            queue.append(action)
    alternatives = re.findall(r'\([A-D]\) 栈为 \$([\d,]+)\$，队列为 \$([\d,]+)\$',
                              PROBLEM['K33-03'])
    equal(len(alternatives), 4)
    truth = [(stack_out, queue_out) == ([int(x) for x in s.split(',')],
                                       [int(x) for x in q.split(',')])
             for s, q in alternatives]
    choice('K33-03', truth)
    anchors('K33-03', '栈依次取出 $2,3,1$', '队列依次取出 $1,2,3$')


def problem_04():
    adjacency = graph('ABCDE', ['AB', 'AC', 'BD', 'CE'])
    order, distance, parent, _ = bfs(adjacency, 'A')
    entry = dfs(adjacency, ['A'])[0]
    truth = [distance['D'] == 3, parent['D'] == 'C', entry == list('ABCDE'),
             order == list('ABCDE') and entry == list('ABDCE')]
    choice('K33-04', truth)
    equal((distance['D'], parent['D']), (2, 'B'))
    anchors('K33-04', '只有 2 条边', '处理 $B$ 时发现')


def problem_05():
    clauses = [(1,), (-1, 2), (-2, 3), (3, 4)]
    assignment, conflict, trail = propagate(clauses)
    found = models(clauses, 4)
    truth = [assignment == {1: True},
             all(assignment.get(i) == value for i, value in [(1, True), (2, True), (3, False)]),
             assignment == dict.fromkeys(range(1, 5), True),
             assignment == {1: True, 2: True, 3: True}
             and {v[3] for v in found} == {False, True}]
    choice('K33-05', truth)
    equal((conflict, trail, found),
          (False, [1, 2, 3], {(True, True, True, False), (True, True, True, True)}))
    anchors('K33-05', '$p,q,r$ 为真', '$s$ 可以为真或假')


def problem_06():
    values = [1, 3, 5, 5, 9]
    equal(lower_bound(values, 5, broken=True), (2, [(1, 6, 3), (1, 2, 1)]))
    equal(lower_bound(values, 5), (3, [(1, 6, 3), (1, 3, 2)]))
    equal(lower_bound(values, 10), (6, [(1, 6, 3), (4, 6, 5)]))
    # Compare the corrected method to a linear definition, including sentinels.
    for target in range(-1, 12):
        expected = next((i for i, v in enumerate(values, 1) if v >= target), len(values) + 1)
        equal(lower_bound(values, target)[0], expected)
    anchors('K33-06', '错误程序返回 2', r'$hi\leftarrow mid$',
            '$x=5$ 返回 3', '$x=10$ 返回 6', '(1,6,3)', '(1,2,1)', '(1,3,2)', '(4,6,5)')


def problem_07():
    values = (1, 2, 3, 4, 6)
    target = [4, [2, [1, None, None], [3, None, None]], [6, None, None]]
    orders = [p for p in permutations(values) if build(p) == target]
    distribution = Counter(p.index(6) for p in orders)
    average = sp.Rational(sum(depths(target).values()), len(values))
    chain_average = sp.Rational(sum(depths(build(values)).values()), len(values))
    equal((len(orders), dict(distribution), average, chain_average),
          (8, {1: 2, 2: 2, 3: 2, 4: 2}, sp.Rational(11, 5), 3))
    anchors('K33-07', '有 8 种', '$11/5$', '$2,1,3$', '$2,3,1$', '4 个位置', '/5=3')


def problem_08():
    adjacency = graph('ABCDEFG', ['AB', 'AC', 'BD', 'CD', 'DE', 'FG'])
    entry, finish, starts, non_tree = dfs(adjacency, 'ABCDEFG')
    equal((entry, finish, len(starts), non_tree[0]),
          (list('ABDCEFG'), list('CEDBAGF'), 2, ('C', 'A')))
    cycle = 'ABDCA'
    equal(all(v in adjacency[u] for u, v in zip(cycle, cycle[1:])), True)
    reduced = graph('ABCDEFG', ['AB', 'AC', 'BD', 'DE', 'FG'])
    reduced_dfs = dfs(reduced, 'ABCDEFG')
    equal((len(reduced_dfs[2]), reduced_dfs[3]), (2, []))
    # Independently check the forest equation in each connected component.
    for root in reduced_dfs[2]:
        component = bfs(reduced, root)[0]
        equal(sum(len(reduced[u]) for u in component) // 2, len(component) - 1)
    anchors('K33-08', '$A,B,D,C,E,F,G$', '$C,E,D,B,A,G,F$', '2 个连通块',
            r'$C\to A$', '$A-B-D-C-A$', '删除 $CD$ 后没有环')


def problem_09():
    vertices = 'ABCDE'
    edges = [('A', 'C'), ('B', 'C'), ('C', 'D'), ('C', 'E')]
    orders = [''.join(p) for p in topo_orders(vertices, edges)]
    equal(orders, ['ABCDE', 'ABCED', 'BACDE', 'BACED'])
    added = edges + [('D', 'C')]
    output, initial, _ = topo(vertices, added)
    equal((output, [initial[v] for v in vertices], topo_orders(vertices, added)),
          (['A', 'B'], [0, 0, 3, 1, 1], []))
    adjacency = graph(vertices, added, directed=True)
    # Find all vertices on directed cycles by actual reachability.
    on_cycles = {u for u in vertices if any(u in bfs(adjacency, v)[1] for v in adjacency[u])}
    equal(on_cycles, {'C', 'D'})
    anchors('K33-09', '4 个拓扑顺序', '$ABCDE,ABCED,BACDE,BACED$', '(0,0,3,1,1)',
            '只输出 $A,B$', '未输出的是 $C,D,E$', 'E 不属于任何有向环')


def problem_10():
    w = sp.Symbol('w', nonnegative=True)
    edges = [('s', 'a', 1), ('a', 't', 8), ('s', 'b', 4),
             ('b', 'c', 1), ('c', 't', 1), ('a', 'c', w)]
    adjacency = graph('sabct', [(u, v) for u, v, _ in edges], True)
    parent = bfs(adjacency, 's')[2]
    equal(restore(parent, 's', 't'), list('sat'))
    wg = weighted('sabct', edges, True)
    routes = dict(simple_paths(wg, 's', 't'))
    equal(routes, {tuple('sat'): 9, tuple('sact'): w + 2, tuple('sbct'): 6})
    numeric = weighted('sabct', [(u, v, sp.sympify(d).subs(w, 2)) for u, v, d in edges], True)
    order, distance, parent, _ = dijkstra(numeric, 's')
    equal((order, [distance[v] for v in order]), (list('sacbt'), [0, 1, 3, 4, 4]))
    for v in numeric:
        equal(distance[v], min(length for _, length in simple_paths(numeric, 's', v)))
    equal(sp.solve(sp.Eq(routes[tuple('sact')], routes[tuple('sbct')]), w), [4])
    equal(sp.reduce_inequalities([w >= 0, w + 2 < 6], w), (w < 4))
    equal(sp.simplify(sp.Equivalent(
        sp.reduce_inequalities([w >= 0, 6 < w + 2], w), w > 4)), sp.true)
    for value, expected in [(0, {'sact'}), (2, {'sact'}), (4, {'sact', 'sbct'}), (9, {'sbct'})]:
        lengths = {p: length.subs(w, value) for p, length in routes.items()}
        shortest = min(lengths.values())
        equal({''.join(p) for p, length in lengths.items() if length == shortest}, expected)
    anchors('K33-10', r'$s\to a\to t$，长 9', '$s,a,c,b,t$', '(0,1,3,4,4)',
            r'$\min\{w+2,6\}$', '$w=4$', '$w>4$')


def problem_11():
    clauses = [(1, 2), (-1, 3), (-2, 3), (-3, 4), (-1, -2)]
    solutions = models(clauses, 4)
    equal(solutions, {(True, False, True, True), (False, True, True, True)})
    for guess in (True, False):
        assignment, conflict, _ = propagate(clauses, {1: guess})
        equal(conflict, False)
        equal({tuple(assignment[i] for i in range(1, 5))}, {v for v in solutions if v[0] == guess})
    expanded = models(clauses[:-1], 4)
    equal(expanded - solutions, {(True, True, True, True)})
    equal([(all(v[2] for v in group), all(v[0] for v in group))
           for group in (solutions, expanded)], [(True, False), (True, False)])
    anchors('K33-11', '(真,假,真,真)', '(假,真,真,真)', 'F 能推出 r，不能推出 p',
            '只增加 $(真,真,真,真)$', '两个判断均不变')


def problem_12():
    adjacency = graph('ABCDEF', ['AB', 'AC', 'BD', 'CD', 'CE', 'DF', 'EF'])
    labels = {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 3}
    equal(all(abs(labels[u] - labels[v]) <= 1
              for u in adjacency for v in adjacency[u]), True)
    equal({v for v in labels if v != 'A' and
           any(labels[u] == labels[v] - 1 for u in adjacency[v])}, set('BCDEF'))
    order, distance, _, _ = bfs(adjacency, 'A')
    equal((order, [distance[v] for v in 'ABCDEF']),
          (list('ABCDEF'), [0, 1, 1, 2, 2, 3]))
    altered = dict(labels, F=2)
    equal(all(abs(altered[u] - altered[v]) <= 1
              for u in adjacency for v in adjacency[u]), True)
    equal(any(altered[u] == altered['F'] - 1 for u in adjacency['F']), False)
    equal(distance['F'], 3)
    anchors('K33-12', '标号相差不超过 1', '任何到达 $v$ 的路径至少有 $h(v)$ 条边',
            'A-B-D-F', 'A-C-E-F', '改标为 2', '最短距离仍为 3')


def problem_13():
    universe, target = tuple(range(1, 7)), 14
    exhaustive = {p for p in combinations(universe, 4) if sum(p) == target}

    def bounds(prefix):
        remaining = 4 - len(prefix)
        last = prefix[-1] if prefix else 0
        available = [v for v in universe if v > last]
        if len(available) < remaining:
            return None
        low = sum(prefix) + sum(available[:remaining])
        high = sum(prefix) + sum(available[-remaining:]) if remaining else sum(prefix)
        return low, high

    levels, rejected, solutions = [[] for _ in range(5)], [], []

    def walk(prefix):
        limits = bounds(prefix)
        if limits is None or not limits[0] <= target <= limits[1]:
            rejected.append(prefix)
            return
        levels[len(prefix)].append(prefix)
        if len(prefix) == 4:
            solutions.append(prefix)
            return
        for v in universe:
            if not prefix or v > prefix[-1]:
                walk(prefix + (v,))

    walk(())
    equal(set(solutions), exhaustive)
    equal(solutions, [(1, 2, 5, 6), (1, 3, 4, 6), (2, 3, 4, 5)])
    equal([len(level) for level in levels], [1, 2, 3, 3, 3])
    equal(sum(map(len, levels)), 12)
    equal(levels[1:4], [[(1,), (2,)], [(1, 2), (1, 3), (2, 3)],
                       [(1, 2, 5), (1, 3, 4), (2, 3, 4)]])
    equal([bounds(p) for p in [(1, 2), (1, 5), (3,)]], [(10, 14), None, (18, 18)])
    # Check all possible prefixes, not just those visited by the pruned tree.
    for r in range(5):
        for prefix in combinations(universe, r):
            m, k, t = (prefix[-1] if prefix else 0), 4 - r, sum(prefix)
            suffixes = list(combinations([v for v in universe if v > m], k))
            if suffixes:
                totals = [t + sum(suffix) for suffix in suffixes]
                equal(bounds(prefix), (min(totals), max(totals)))
                equal(bounds(prefix), (t + sum(range(m + 1, m + k + 1)),
                                       t + sum(range(7 - k, 7))))
            else:
                equal(bounds(prefix), None)
    equal(any(solution[:len(prefix)] == prefix for prefix in rejected for solution in exhaustive), False)
    anchors('K33-13', '(1,2,5,6)', '(1,3,4,6)', '(2,3,4,5)', '(1,2,3,3,3)',
            '共 12 个', '$L=10,U=14$', '$6-m<k$', '$L>14$', '$U<14$')


def problem_14():
    clauses = [(-1, -2, -3), (1, 2), (1, 3), (2, 3), (-4, 1), (-4, 2), (-1, -2, 4)]
    solutions = models(clauses, 4)
    direct = {values for values in product((False, True), repeat=4)
              if sum(values[:3]) == 2 and values[3] == (values[0] and values[1])}
    equal(solutions, direct)
    equal(solutions, {(True, True, False, True), (True, False, True, False),
                      (False, True, True, False)})
    equal((len({abs(lit) for clause in clauses for lit in clause}), len(clauses)), (4, 7))
    true_assignment, conflict, _ = propagate(clauses, {4: True})
    equal((true_assignment, conflict), ({4: True, 1: True, 2: True, 3: False}, False))
    for p in (True, False):
        assignment, conflict, _ = propagate(clauses, {4: False, 1: p})
        equal(conflict, False)
        equal({tuple(assignment[i] for i in range(1, 5))},
              {v for v in solutions if not v[3] and v[0] == p})
    equal(models(clauses + [(4, 3)], 4), solutions)
    # Bind all seven clauses to the displayed CNF, in addition to the answers.
    for clause in (r'(\neg p\lor\neg q\lor\neg r)', r'(p\lor q)', r'(p\lor r)',
                   r'(q\lor r)', r'(\neg s\lor p)', r'(\neg s\lor q)',
                   r'(\neg p\lor\neg q\lor s)'):
        anchors('K33-14', clause)
    anchors('K33-14', '4 个变量、7 个子句', '(真,真,假,真)', '(真,假,真,假)',
            '(假,真,真,假)', '解不减少')


def main():
    failures = 0
    equal(set(ANSWER), {f'K33-{i:02}' for i in range(1, 15)})
    equal(set(PROBLEM), set(ANSWER))
    for number in range(1, 15):
        pid = f'K33-{number:02}'
        try:
            block = ANSWER[pid].split('\n### ')[0].strip()
            assert any(line.startswith('**答案：**') for line in block.splitlines()[:5]), f'{pid}: missing answer prefix'
            assert block.splitlines()[-1].startswith('区分点：'), f'{pid}: missing distinction'
            tier = re.match(r'〔([ABC])', PROBLEM[pid])[1]
            assert len(block) <= {'A': 400, 'B': 900, 'C': 1400}[tier], 'answer too long'
            globals()[f'problem_{number:02}']()
            print(f'PASS {pid}')
            if number == 12:
                assert '（证明）' in PROBLEM[pid]
                print(f'MANUAL {pid} proof: check lower bound and attainable path argument')
        except Exception as error:
            failures += 1
            print(f'FAIL {pid} {type(error).__name__}: {error}')
    return failures


if __name__ == '__main__':
    sys.exit(bool(main()))
