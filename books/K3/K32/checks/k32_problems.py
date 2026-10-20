"""独立验算 K3.2 题目；数值由程序重新计算，再与 answers.md 的文字比对。"""
from pathlib import Path
import math
import re
from itertools import permutations, product, combinations
from collections import deque
from functools import lru_cache

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")


def block(pid):
    m = re.search(rf"^\*\*{pid}\*\*(.*?)(?=^\*\*K32-\d+\*\*|\Z)", ANS, re.M | re.S)
    assert m, f"missing answer block {pid}"
    return re.sub(r"\s+", "", m.group(1))


def check(pid, ok):
    print(f"{'PASS' if ok else 'FAIL'} {pid}")


def inv(a):
    return sum(bool(a[i] > a[j]) for i in range(len(a)) for j in range(i + 1, len(a)))


def merge(left, right):
    i = j = comparisons = 0
    out = []
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out, comparisons


def partition(a, trace=None):
    a = list(a)
    x = a[-1]
    i = -1
    for j in range(len(a) - 1):
        if a[j] <= x:
            i += 1
            a[i], a[j] = a[j], a[i]
            if trace is not None:
                trace.append(a[:])
    a[i + 1], a[-1] = a[-1], a[i + 1]
    return a, i + 1


def sift_down(a, end):
    i = 0
    while 2 * i + 1 < end:
        c = 2 * i + 1
        if c + 1 < end and a[c + 1] > a[c]:
            c += 1
        if a[i] >= a[c]:
            break
        a[i], a[c] = a[c], a[i]
        i = c


def heap_two_extracts(a):
    a = list(a)
    states = []
    for end in (len(a) - 1, len(a) - 2):
        a[0], a[end] = a[end], a[0]
        sift_down(a, end)
        states.append(list(a))
    return states


def stable_count(records, key, k):
    counts = [0] * (k + 1)
    for r in records:
        counts[key(r)] += 1
    for v in range(1, k + 1):
        counts[v] += counts[v - 1]
    out = [None] * len(records)
    for r in reversed(records):
        v = key(r)
        counts[v] -= 1
        out[counts[v]] = r
    return out



def contains(pid, *tokens):
    return all(re.sub(r"\s+", "", token) in block(pid) for token in tokens)


def choice_check(pid, truths):
    selected = re.search(r"答案：\*\*\(([A-D])\)", block(pid))
    for letter, actual in zip("ABCD", truths):
        check(f"{pid}-{letter}", bool(actual) == (selected is not None and selected[1] == letter))
    check(f"{pid}-unique", sum(map(bool, truths)) == 1)


def insertion_trace(a):
    a = list(a)
    states, comps = [], 0
    for j in range(1, len(a)):
        key = a[j]
        i = j - 1
        moved = []
        while i >= 0:
            comps += 1
            if a[i] <= key:
                break
            moved.append(a[i])
            a[i + 1] = a[i]
            i -= 1
        a[i + 1] = key
        states.append((key, moved, a[:]))
    return states, comps


def counting_trace(records, key, k, reverse=True):
    c = [0] * (k + 1)
    for r in records:
        c[key(r)] += 1
    for v in range(1, k + 1):
        c[v] += c[v - 1]
    cumulative = c[:]
    out, placements = [None] * len(records), []
    for r in (reversed(records) if reverse else records):
        v = key(r)
        placements.append((r, c[v]))
        c[v] -= 1
        out[c[v]] = r
    return out, cumulative, placements


states, comps = insertion_trace([7, 4, 6, 2, 5])
expected = [(4, [7], [4,7,6,2,5]), (6, [7], [4,6,7,2,5]),
            (2, [7,6,4], [2,4,6,7,5]), (5, [7,6], [2,4,5,6,7])]
for j, (actual, wanted) in enumerate(zip(states, expected), 2):
    check(f"K32-01-round{j}", actual == wanted and contains("K32-01", str(wanted[2]), rf"\mathrm{{key}}={wanted[0]}"))
check("K32-01-total", sum(len(s[1]) for s in states) == inv([7,4,6,2,5]) == 7)

samples = [sp.Rational(0), sp.Rational(2), sp.Rational(7,2), sp.Rational(5)]
counts = [sum(len(s[1]) for s in insertion_trace([3,x,1,4])[0]) for x in samples]
check("K32-02-intervals", counts == [2,3,2,3] and contains("K32-02", r"(1,3)\cup(4,+\infty)", "|逆序对数|2|3|2|3|"))
x = sp.Symbol("x", real=True)
condition = sp.Union(sp.Interval.open(1,3), sp.Interval.open(4,sp.oo))
check("K32-02-range", all(bool(condition.contains(x)) == (inv([3,x,1,4]) == 3)
                         for x in [sp.Rational(i,2) for i in range(-10,21)] if x not in (1,3,4)))

out, comps = merge([1,6,10], [2,4,9,11])
check("K32-03", out == [1,2,4,6,9,10,11] and comps == 6 and contains("K32-03", str(out), "$6$次"))

for x in [sp.Rational(i,2) for i in range(-5,15)]:
    if x in (1,2,3,4):
        continue
    out, pos = partition([4,1,x,2,3])
    assert (pos + 1 == 3) == (x > 3)
    if x > 3:
        assert out == [1,2,3,4,x]
        trace = []
        partition([4,1,x,2,3], trace)
        assert trace == [[1,4,x,2,3], [1,2,x,4,3]]
check("K32-04", contains("K32-04", r"x>3", r"x\ne4", "[1,2,3,4,x]", "[1,4,x,2,3]", "[1,2,x,4,3]"))

records = [(1,"a"), (3,"c"), (1,"b")]
normal, cumulative, _ = counting_trace(records, lambda r:r[0], 3)
forward, _, _ = counting_trace(records, lambda r:r[0], 3, False)
missing, cmissing, _ = counting_trace([(1,"a"), (3,"b")], lambda r:r[0], 3)
# A: a noninteger counterexample; B: actually reverse equal-key identities.
# C: compare cumulative counts with ranks, including an absent key.
c_valid = all(cumulative[v] == sum(r[0] <= v for r in records)
              and (v not in [r[0] for r in records]
                   or cumulative[v] == max(i+1 for i,r in enumerate(normal) if r[0] == v))
              for v in range(1,4))
# D: the actual allocated output and count arrays grow with n and k.
spaces = [len(counting_trace([(1,i) for i in range(n)], lambda r:r[0], n)[0]) + n for n in (2,4,8)]
choice_check("K32-05", [sp.Rational(1,2).is_integer, forward == normal, c_valid, len(set(spaces)) == 1])
check("K32-05-missing", cmissing[2] == 1 and all(r[0] != 2 for r in missing) and contains("K32-05", "C[2]=1", "[1,3]"))

weak = [2,3,1]
check("K32-06-counterexample", weak[:2] == sorted(weak[:2]) and weak != sorted(weak))
print("MANUAL K32-06-proof")

def min_swaps(start, adjacent):
    start = tuple(start)
    target = tuple(sorted(start))
    queue, seen = deque([(start,0)]), {start}
    while queue:
        a, depth = queue.popleft()
        if a == target:
            return depth
        pairs = [(i,i+1) for i in range(len(a)-1)] if adjacent else combinations(range(len(a)), 2)
        for i,j in pairs:
            b = list(a)
            b[i],b[j] = b[j],b[i]
            b = tuple(b)
            if b not in seen:
                seen.add(b)
                queue.append((b,depth+1))

adj, arbitrary = min_swaps([3,2,1], True), min_swaps([3,2,1], False)
choice_check("K32-07", [adj == 3 and arbitrary == 1,
                      inv([1,2,3]) == inv([3,2,1])-1,
                      arbitrary >= 3,
                      all(inv(a) == 3 for a in permutations([1,2,3]))])

@lru_cache(None)
def work(n):
    if n <= 2:
        return 1
    m = n // 3
    return work(m) + work(n-m) + n*n

check("K32-08-integer-bounds", all(n*n <= work(n) and 8*work(n) <= 25*n*n+8*n
                                  and 25*((n//3)**2+(n-n//3)**2) <= 17*n*n
                                  for n in range(3,2001)))
def level_costs(n):
    level, costs = [n], []
    while level:
        costs.append(sum(v*v for v in level if v > 2))
        level = [child for v in level if v > 2 for child in (v//3, v-v//3)]
    return costs
check("K32-08-levels", all(all(25*b <= 17*a for a,b in zip(level_costs(n), level_costs(n)[1:]))
                          for n in range(3,201)) and contains("K32-08", r"T(n)=\Theta(n^2)"))
print("MANUAL K32-08-proof")

realkeys = [sp.Rational(1,10), sp.sqrt(2), sp.Rational(1,5), sp.pi]
valid = lambda a,k: all(v.is_integer is True and 1 <= v <= k for v in a)
choice_check("K32-09", [valid(realkeys,4), all(v.is_integer is True and v>0 for v in realkeys),
                       not valid(realkeys,4), valid(list(reversed(realkeys)),4)])
check("K32-09-ranking", sorted(range(4),key=lambda i:realkeys[i]) == [0,2,1,3])

a = [10,7,9,4,8,3,6]
bad_edges = [(i//2, i) for i in range(2,len(a)+1) if a[i//2-1] < a[i-1]]
# Repair the offending subtree by the same down operation on its child indices.
def down_at(a, i, end):
    while 2*i+1 < end:
        c = 2*i+1
        if c+1 < end and a[c+1] > a[c]:
            c += 1
        if a[i] >= a[c]:
            break
        a[i],a[c] = a[c],a[i]
        i = c
down_at(a,1,len(a))
check("K32-10-repair", bad_edges == [(2,5)] and a == [10,8,9,4,7,3,6] and contains("K32-10",str(a)))
a[0],a[-1] = a[-1],a[0]
check("K32-10-exchange", a == [6,8,9,4,7,3,10] and contains("K32-10", r"[6,8,9,4,7,3\mid10]"))
down_at(a,0,len(a)-1)
check("K32-10-extract", a == [9,8,6,4,7,3,10] and contains("K32-10",r"[9,8,6,4,7,3\mid10]"))

def merge_sort(a):
    if len(a) < 2:
        return list(a),0
    mid = (len(a)+1)//2
    left,c1 = merge_sort(a[:mid])
    right,c2 = merge_sort(a[mid:])
    out,c3 = merge(left,right)
    return out,c1+c2+c3

bound = (math.factorial(8)-1).bit_length()
worst = max(merge_sort(a)[1] for a in permutations(range(8)))
possible = range(bound,worst+1)
# These are implications from the two stated bounds, not claims that every
# abstract candidate has an existing sorting algorithm.
choice_check("K32-11", [all(v==16 for v in possible),
                       min(possible)>=16 and len(possible)>1,
                       all(v>=17 for v in possible),
                       insertion_trace(list(range(8)))[1] >= 16])
check("K32-11-data", (bound,worst) == (16,17) and contains("K32-11","40320"))

records = [(2,7,"a"),(1,5,"b"),(2,5,"c"),(1,7,"d"),(2,6,"e")]
first = stable_count(records,lambda r:r[0],2)
wrong = stable_count(first,lambda r:r[1],7)
target = stable_count(stable_count(records,lambda r:r[1],7),lambda r:r[0],2)
ids = lambda a: ",".join(r[2] for r in a)
ranks = {r[2]:i+1 for i,r in enumerate(target)}
positions = [ranks[r[2]] for r in wrong]
check("K32-12-orders", ids(first)=="b,d,a,c,e" and ids(wrong)=="b,c,e,d,a" and ids(target)=="b,d,c,e,a"
      and contains("K32-12", ids(first),ids(wrong),ids(target),str(positions)))
check("K32-12-minimum", inv(positions)==min_swaps(positions,True)==2)
for i, expected in [(3,"b,c,d,e,a"),(2,"b,d,c,e,a")]:
    wrong[i],wrong[i-1] = wrong[i-1],wrong[i]
    check(f"K32-12-swap{i}",ids(wrong)==expected and contains("K32-12",expected))

interleavings = list(combinations(range(1,6),2))
costs = [merge([v for v in range(1,6) if v not in r], list(r))[1] for r in interleavings]
check("K32-13-numeric", len(interleavings)==10 and (len(interleavings)-1).bit_length()==4
      and max(costs)==4 and merge([1,3,5],[2,4])[1]==4
      and contains("K32-13", r"\binom52=10", "[1,3,5]", "[2,4]"))
print("MANUAL K32-13-proof")

def merge_inversions(a, trace=None):
    if len(a)<=1:
        return list(a),0
    mid=(len(a)+1)//2
    left,lc=merge_inversions(a[:mid], trace)
    right,rc=merge_inversions(a[mid:], trace)
    i=j=cross=0
    out=[]
    while i<len(left) and j<len(right):
        if left[i]<=right[j]:
            out.append(left[i])
            i+=1
        else:
            cross+=len(left)-i
            if trace is not None:
                trace.append((len(a),right[j],len(left)-i))
            out.append(right[j])
            j+=1
    return out+left[i:]+right[j:],lc+rc+cross

cases = [list(p) for n in range(7) for p in product(range(3),repeat=n)]
cases += [list(p) for p in permutations(range(7))]
check("K32-14-algorithm", all(merge_inversions(a)==(sorted(a),inv(a)) for a in cases))
a=[7,2,6,3,5,1,4]
trace = []
merge_inversions(a, trace)
check("K32-14-values", merge_inversions(a)[1]==14 and merge_inversions(a[:4])[1]==4
      and merge_inversions(a[4:])[1]==2
      and [entry[1:] for entry in trace if entry[0]==7] == [(1,4),(4,2),(5,2)]
      and contains("K32-14","逆序对数为$14$",r"\Theta(n\log n)","p-i+1"))
print("MANUAL K32-14-proof")

problems = (ROOT/"problems.md").read_text(encoding="utf-8")
lesson = (ROOT/"lesson.md").read_text(encoding="utf-8")
pids = re.findall(r"^\*\*(K32-\d+)\*\*",problems,re.M)
aids = re.findall(r"^\*\*(K32-\d+)\*\*",ANS,re.M)
tableids = re.findall(r"^\| (K32-\d+) \|",problems,re.M)
lessonids = set(re.findall(r"K32-\d+",lesson.split("### 本章小结")[1]))
check("indices",len(pids)==len(set(pids))==14 and set(pids)==set(aids)==lessonids and tableids==pids)
check("tiers", [len(re.findall(rf"\*\*〔{tier}",problems)) for tier in "ABC"]==[5,6,3])
for row in re.findall(r"^\| 方法 \d.*$",lesson,re.M):
    method = re.search(r"方法 (\d)",row)[1]
    for pid in re.findall(r"K32-\d+",row):
        pb = re.search(rf"^\*\*{pid}\*\*(.*?)(?=^\*\*K32-|\Z)",problems,re.M|re.S)[1]
        check(f"index-{pid}-method{method}", f"方法 {method}" in pb or f"方法{method}" in block(pid))

for pid in ("K32-12","K32-13","K32-14"):
    line = next(line for line in problems.splitlines() if line.startswith(f"**{pid}**"))
    check(f"{pid}-mixed", "方法" not in line)
