"""独立核对 lesson.md 中例 1--17 的数值和结论。"""
from pathlib import Path
import math
import re

LESSON = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")


def example(k):
    m = re.search(rf"\*\*例 {k}\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON, re.S)
    assert m, f"missing 例{k}"
    return re.sub(r"\s+", "", m.group(1))


def check(k, ok):
    print(f"{'PASS' if ok else 'FAIL'} 例{k}")


def inv(a):
    return sum(a[i] > a[j] for i in range(len(a)) for j in range(i + 1, len(a)))


def insertion(a):
    a = list(a)
    shifts = 0
    for j in range(1, len(a)):
        key = a[j]
        i = j - 1
        while i >= 0 and a[i] > key:
            a[i + 1] = a[i]
            i -= 1
            shifts += 1
        a[i + 1] = key
    return a, shifts


def selection(a):
    a = list(a)
    for k in range(len(a) - 1):
        p = min(range(k, len(a)), key=a.__getitem__)
        a[k], a[p] = a[p], a[k]
    return a


def bubble(a):
    a = list(a)
    swaps = 0
    while True:
        changed = False
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swaps += 1
                changed = True
        if not changed:
            return a, swaps


def merge(left, right):
    i = j = c = 0
    out = []
    while i < len(left) and j < len(right):
        c += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out, c


def merge_sort(a):
    if len(a) <= 1:
        return list(a), 0
    # lesson.md uses 1-based mid=floor((lo+hi)/2), so the left half
    # gets the extra item when the length is odd.
    m = (len(a) + 1) // 2
    l, c1 = merge_sort(a[:m])
    r, c2 = merge_sort(a[m:])
    out, c3 = merge(l, r)
    return out, c1 + c2 + c3


def partition(a):
    a = list(a)
    x = a[-1]
    i = -1
    for j in range(len(a) - 1):
        if a[j] <= x:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[-1] = a[-1], a[i + 1]
    return a, i + 1


def quick_comps(a):
    if len(a) <= 1:
        return 0
    b, q = partition(a)
    return len(a) - 1 + quick_comps(b[:q]) + quick_comps(b[q + 1:])


def heapify(a):
    a = list(a)
    def down(i, n):
        while 2 * i + 1 < n:
            c = 2 * i + 1
            if c + 1 < n and a[c + 1] > a[c]:
                c += 1
            if a[i] >= a[c]:
                break
            a[i], a[c] = a[c], a[i]
            i = c
    for i in range((len(a) - 2) // 2, -1, -1):
        down(i, len(a))
    return a


def counting(a, k):
    c = [0] * (k + 1)
    for x in a:
        c[x] += 1
    for v in range(2, k + 1):
        c[v] += c[v - 1]
    b = [None] * len(a)
    for x in reversed(a):
        c[x] -= 1
        b[c[x]] = x
    return b, c


e = example(1)
sorted_a, shifts = insertion([5, 2, 8, 1, 9, 3])
check(1, sorted_a == [1, 2, 3, 5, 8, 9] and shifts == 7 and "7" in e)

e = example(2)
check(2, insertion([5, 2, 8, 1, 9, 3])[0] == [1, 2, 3, 5, 8, 9]
      and insertion([5, 2, 8, 1, 9, 3])[1] == 7)
print("MANUAL 例2-proof")

e = example(3)
check(3, selection([5, 2, 8, 1, 9, 3]) == [1, 2, 3, 5, 8, 9]
      and "15" in e and "最小的$k-1$个数" in e)
print("MANUAL 例3-proof")

e = example(4)
check(4, inv([6, 4, 7, 2, 5, 1]) == 11 and "11" in e)

e = example(5)
check(5, bubble([5, 2, 8, 1, 9, 3])[1] == 7 and "3+2+2+0=7" in e)

e = example(6)
check(6, inv([2, 1, 4, 3, 6, 5]) == 3 * 1
      and "5\\times10^5" in e and "1.5\\times10^6" in e
      and "2.5\\times10^{11}" in e)

e = example(7)
out, c = merge([2, 5, 8], [1, 3, 9])
check(7, out == [1, 2, 3, 5, 8, 9] and c == 5 and "5次" in e)
print("MANUAL 例7-proof")

e = example(8)
out, c = merge_sort([5, 2, 8, 1, 9, 3])
check(8, out == [1, 2, 3, 5, 8, 9] and c == 11 and "11" in e)

e = example(9)
scores = [0.31, 0.82, 0.47, 0.91, 0.15, 0.66, 0.78, 0.52]
order = sorted(range(8), key=lambda i: scores[i], reverse=True)
check(9, order[:3] == [3, 1, 6] and "17次" in e and "文档4、2、7" in e)

e = example(10)
out, pos = partition([5, 2, 8, 1, 9, 3])
check(10, out == [2, 1, 3, 5, 9, 8] and pos == 2 and "比较了5次" in e)

e = example(11)
check(11, quick_comps([1, 2, 3, 5, 8, 9]) == 15 and "15" in e)

e = example(12)
check(12, heapify([5, 2, 8, 1, 9, 3]) == [9, 5, 8, 1, 2, 3]
      and "[1,2,3,5,8,9]" in e)

e = example(13)
expected = [math.ceil(math.log2(math.factorial(n))) for n in (3, 4, 5, 8, 1000)]
check(13, expected == [3, 5, 7, 16, 8530]
      and all(str(v) in e for v in expected))

e = example(14)
check(14, 5 * 1000 < math.ceil(math.log2(math.factorial(1000)))
      and "5000<8530" in e)

e = example(15)
out, c = counting([5, 2, 8, 1, 9, 3], 9)
cumulative = [0] * 10
for value in [5, 2, 8, 1, 9, 3]:
    cumulative[value] += 1
for value in range(2, 10):
    cumulative[value] += cumulative[value - 1]
check(15, out == [1, 2, 3, 5, 8, 9]
      and cumulative[1:] == [1, 2, 3, 3, 4, 4, 4, 5, 6]
      and "[1,2,3,5,8,9]" in e)

e = example(16)
records = [(3, "a"), (1, "b"), (3, "c"), (2, "d"), (1, "e")]
counts = {v: sum(r[0] == v for r in records) for v in (1, 2, 3)}
def counting_records(records, k):
    counts = [0] * (k + 1)
    for key, label in records:
        counts[key] += 1
    for v in range(1, k + 1):
        counts[v] += counts[v - 1]
    output = [None] * len(records)
    placements = []
    for record in reversed(records):
        key = record[0]
        placements.append((record, counts[key]))
        counts[key] -= 1
        output[counts[key]] = record
    return output, placements

stable, placements = counting_records(records, 3)
check(16, stable == sorted(records, key=lambda r: r[0])
      and placements == [((1,"e"),2),((2,"d"),3),((3,"c"),5),((1,"b"),1),((3,"a"),4)])

e = example(17)
def down(a, i, end, key=lambda x: x):
    while 2*i+1 < end:
        c = 2*i+1
        if c+1 < end and key(a[c+1]) > key(a[c]):
            c += 1
        if key(a[i]) >= key(a[c]):
            break
        a[i], a[c] = a[c], a[i]
        i = c


def heap_trace(a, key=lambda x: x):
    a = list(a)
    for i in range(len(a)//2-1, -1, -1):
        down(a, i, len(a), key)
    states = []
    for end in range(len(a)-1, 0, -1):
        a[0], a[end] = a[end], a[0]
        swapped = a[:]
        down(a, 0, end, key)
        states.append((swapped, a[:]))
    return states


tagged = [(2,"a"),(2,"b"),(1,"c")]
selected = tagged[:]
for k in range(len(selected)-1):
    p = min(range(k,len(selected)),key=lambda i:selected[i][0])
    selected[k], selected[p] = selected[p], selected[k]
quick = tagged[:]
i = -1
for j in range(len(quick)-1):
    if quick[j][0] <= quick[-1][0]:
        i += 1
        quick[i], quick[j] = quick[j], quick[i]
quick[i+1], quick[-1] = quick[-1], quick[i+1]
heaps = heap_trace(tagged,lambda r:r[0])
reversed_equals = [(1,"c"),(2,"b"),(2,"a")]
check("17-selection", selected == reversed_equals)
check("17-quick", quick == reversed_equals)
check("17-heap", heaps[0][1] == [(2,"b"),(1,"c"),(2,"a")]
      and heaps[-1][1] == reversed_equals)
print("MANUAL 例17-stability-proof")

# Recompute all submerges, not just the final sum.
def merge_trace(a, descending=False):
    if len(a) < 2:
        return list(a), []
    mid = (len(a)+1)//2
    left, lt = merge_trace(a[:mid], descending)
    right, rt = merge_trace(a[mid:], descending)
    if descending:
        neg, c = merge([-v for v in left], [-v for v in right])
        out = [-v for v in neg]
    else:
        out, c = merge(left, right)
    return out, lt + rt + [(len(left),len(right),out,c)]


out, trace = merge_trace([5,2,8,1,9,3])
check("8-submerges", [(p,q,c) for p,q,_,c in trace]
      == [(1,1,1),(2,1,2),(1,1,1),(2,1,2),(3,3,5)]
      and trace[1][2] == [2,5,8]
      and all(c <= p+q-1 for p,q,_,c in trace))
out, trace = merge_trace(scores, True)
check("9-comparisons", out == sorted(scores, reverse=True)
      and sum(c for _,_,_,c in trace) == 17)

states = heap_trace([5,2,8,1,9,3])
expected_states = [
    ([3,5,8,1,2,9],[8,5,3,1,2,9]),
    ([2,5,3,1,8,9],[5,2,3,1,8,9]),
    ([1,2,3,5,8,9],[3,2,1,5,8,9]),
    ([1,2,3,5,8,9],[2,1,3,5,8,9]),
    ([1,2,3,5,8,9],[1,2,3,5,8,9]),
]
for step,(actual,wanted) in enumerate(zip(states,expected_states),1):
    check(f"12-extract{step}", actual == wanted)
