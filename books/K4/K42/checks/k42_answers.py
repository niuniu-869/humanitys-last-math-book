"""Enforce this task's length bounds, format, vocabulary and coverage locally."""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
problems = (root / "problems.md").read_text()
answers = (root / "answers.md").read_text()
tiers = dict(re.findall(r"^\*\*(K42-\d+)\*\*〔([ABC])", problems, re.M))
bounds = {"A": 400, "B": 900, "C": 1400}
chunks = re.split(r"(?m)^(?=\*\*K42-\d+\*\*)", answers)[1:]
seen = []
for chunk in chunks:
    pid = re.match(r"\*\*(K42-\d+)\*\*", chunk)[1]
    seen.append(pid)
    tier = tiers[pid]
    hi = bounds[tier]
    body = re.split(r"(?m)^### ",chunk)[0].strip()
    assert len(body) <= hi, (pid,tier,len(body))
    lines = body.splitlines()
    assert lines[0] == f"**{pid}**" and lines[1].startswith("**答案：**"),pid
    assert lines[-1].startswith("区分点："),pid
    if int(pid[-2:]) in list(range(1,11))+list(range(18,28))+list(range(35,41))+list(range(52,58)):
        assert all(f"({option})" in body for option in "ABCD"),pid
    assert body.count("$$") % 2 == 0,pid
    print(f"PASS {pid}-格式字数 {tier} {len(body)}..{len(chunk)}")
expected = [f"K42-{i:02d}" for i in range(1,69)]
assert seen == expected and set(tiers) == set(expected)
for name,text in [("题目",problems),("答案",answers)]:
    forbidden = re.search(r"高中|初中|中学(?!到|会|习|得)|备考|考研|数学一|真题|考纲|应试|常考|考试要求",text)
    assert forbidden is None,(name,forbidden.group() if forbidden else None)
    print(f"PASS {name}-口径")
for tier,hi in bounds.items():
    values=[len(re.split(r"(?m)^### ",c)[0].strip()) for c in chunks
            if tiers[re.match(r"\*\*(K42-\d+)\*\*",c)[1]]==tier]
    print(f"PASS {tier}档范围 {min(values)}..{max(values)}，上限{hi}，不设下限")

lesson = (root / "lesson.md").read_text()
summary = lesson.split("### 本章小结", 1)[1]
assert set(re.findall(r"K42-\d+", summary)) <= set(expected)
table = problems.split("### 综合测验一", 1)[0]
ranges = re.findall(r"K42-(\d+) 至 K42-(\d+)", table)
assert [(int(a), int(b)) for a,b in ranges] == [(1,17),(18,34),(35,51),(52,68)]
sections = re.split(r"(?m)^### 综合测验[一二三四]\s*$", problems)[1:]
for section, (start, end) in zip(sections, ranges):
    ids = re.findall(r"(?m)^\*\*(K42-\d+)\*\*", section)
    assert ids == [f"K42-{i:02d}" for i in range(int(start),int(end)+1)]
    assert sum(map(int, re.findall(r"^\*\*K42-\d+\*\*[^\n]*?（(\d+) 分）", section,re.M))) == 100
print("PASS 题号表-讲义小结-答案覆盖及各卷100分")
