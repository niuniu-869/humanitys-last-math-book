#!/usr/bin/env python3
"""给答疑插件生成题目索引：python tools/qa_index.py

先用 tools/build.py 排出全部分册的 PDF，再运行本脚本。产物 release/qa-index.json 和 PDF 一起发布：
  books[册号] = {title, pdf, pages, units, page_items:{页码: [条目号...]}, page_text:[每页文字...]}
  items[条目号] = {kind: problem|example, book, unit, label, md, answer?, verify?, section?, pages:{problem?, answer?, lesson?}}
  units["册号/单元号"] = {title, lesson, problems_head, cheatsheet}
pdf 是相对 qa-index.json 所在目录的文件名。题号如 L8-05，例题号如 L8·例03（单元内按出现顺序编号）。
条目号或单元号在全书里重复、某册 PDF 缺失时报错退出。
依赖：poppler-utils（pdftotext、pdfinfo）；verify.py 的依赖见 requirements.txt。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import BOOKS, NAME, ORDER, RELEASE  # noqa: E402

PIDS = r"[A-Z]{1,4}\d{0,2}[A-Z]?-(?:\d{2}|C\d)"  # 题号，如 L8-05、K31-12
PID = re.compile(rf"^\*\*({PIDS})\*\*", re.M)
PART_MARK = {"lesson": ("问题·直觉·方法·例题",), "problems": ("A基础·B进阶·C提高",), "answers": ("做完再对照",)}  # 各部分封面上的副标题


def squash(s: str) -> str:
    # 矩阵的大括号拼件（⎛⎜⎝ 等）会被 pdftotext 插进相邻行的文字里，一并去掉
    return re.sub(r"[\s⎛-⎭]+", "", s)


def split_items(md: str) -> dict[str, str]:
    """按 **题号** 切块，块一直到下一个 **题号** 或下一个二、三级标题。"""
    out, marks = {}, list(PID.finditer(md))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(md)
        h = re.search(r"^#{2,3} ", md[m.start():end], re.M)
        if h and h.start() > 0:
            end = m.start() + h.start()
        out[m.group(1)] = md[m.start():end].strip()
    return out


def lesson_items(unit: str, md: str) -> list[dict]:
    """讲义里的例题，按出现顺序；附所在小节标题。"""
    items, section = [], ""
    lines = md.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("### "):
            section = ln[4:].strip()
            continue
        m = re.match(r"^\*\*例\s*(\d+)\s*[·:：]?\s*(.*?)\*\*", ln)
        if m:
            j = i + 1  # 块延伸到下一个例题或标题
            while j < len(lines) and not re.match(r"^(#{2,3} |\*\*例\s*\d+)", lines[j]):
                j += 1
            items.append({"id": f"{unit}·例{len(items) + 1:02d}", "label": f"例 {m[1]}" + (f" · {m[2][:40]}" if m[2] else ""),
                          "section": section, "md": "\n".join(lines[i:j]).strip()})
    return items


def core(s: str) -> str:
    """只留汉字、ASCII 字母和数字：pdftotext 会把直引号印成弯引号，还会把高公式的上下限（如 ∞）插进相邻行。"""
    return re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", "", s)


def fingerprint(md: str) -> str:
    """例题的指纹：标题行第一个公式之前的文字，只留汉字和字母数字，至多 10 个字符。"""
    return core(md.split("\n", 1)[0].split("$", 1)[0])[:10]


def pdf_pages(pdf: Path) -> list[str]:
    """逐页抽取。整本一次抽取时，页面内容里会混进额外的分页符，导致页码错位。"""
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout)[1])
    one = lambda i: subprocess.run(["pdftotext", "-layout", "-f", str(i), "-l", str(i), str(pdf), "-"],  # noqa: E731
                                   capture_output=True, text=True).stdout.replace("\f", "")
    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(one, range(1, n + 1)))


def verify_lines(unit_dir: Path) -> dict[str, list[str]]:
    """跑一次本章 verify.py，按题号收集 PASS/MANUAL 行，作为「代码验算过的数值」给模型参考。"""
    r = subprocess.run([sys.executable, "verify.py"], cwd=unit_dir, capture_output=True, text=True, timeout=300)
    out: dict[str, list[str]] = {}
    for ln in r.stdout.splitlines():
        for pid in re.findall(PIDS, ln):
            out.setdefault(pid, []).append(ln.strip()[:300])
    return out


def put(table: dict, key: str, value, what: str) -> None:
    if key in table:
        raise SystemExit(f"{what} {key} 在全书里重复：答疑插件会把它挂到错误的位置")
    table[key] = value


def build_book(book: str, items: dict, units: dict, codes_seen: dict) -> dict:
    outline = json.loads((BOOKS / book / "outline.json").read_text(encoding="utf-8"))
    codes = [u["code"] for u in outline["units"]]
    pdf = RELEASE / f"{book}_{NAME}.pdf"
    if not pdf.exists():
        raise SystemExit(f"缺少 {pdf}，先运行 python tools/build.py {book}")
    mine: dict[str, dict] = {}
    for u in codes:
        d = BOOKS / book / u
        les, pro, ans, che = ((d / n).read_text(encoding="utf-8") for n in ("lesson.md", "problems.md", "answers.md", "cheatsheet.md"))
        first = PID.search(pro)
        title = (re.match(r"^#{1,2} (.*)", les) or [None, u])[1]
        put(codes_seen, u, book, "单元号")
        units[f"{book}/{u}"] = {"title": title, "lesson": les, "problems_head": pro[:first.start()].strip() if first else "",
                                "cheatsheet": che}
        answers, vl = split_items(ans), verify_lines(d)
        for pid, md in split_items(pro).items():
            tier = re.match(r"^\*\*[^*]+\*\*\s*〔([^〕]*)〕", md)
            put(mine, pid, {"kind": "problem", "book": book, "unit": u, "label": pid + (f"〔{tier[1]}〕" if tier else ""),
                            "md": md, "answer": answers.get(pid, ""), "verify": vl.get(pid, []), "pages": {}}, "条目号")
        for it in lesson_items(u, les):
            put(mine, it["id"], {"kind": "example", "book": book, "unit": u, "label": it["label"], "md": it["md"],
                                 "section": it["section"], "pages": {}}, "条目号")
    for k, v in mine.items():
        put(items, k, v, "条目号")

    pages = pdf_pages(pdf)
    sq = [squash(p) for p in pages]
    # 各部分（讲义、题目、答案）的起始页：部分封面上的副标题
    starts = {k: next((i for i, p in enumerate(sq) if any(mk in p for mk in marks)), None) for k, marks in PART_MARK.items()}
    bounds = sorted((v, k) for k, v in starts.items() if v is not None) + [(len(pages), "end")]
    part_of = {i: k for (a, k), (b, _) in zip(bounds, bounds[1:]) for i in range(a, b)}
    page_items: dict[int, list[str]] = {}

    def mark(pid: str, key: str, page: int) -> None:
        pg = mine[pid]["pages"].setdefault(key, [])
        if page not in pg:
            pg.append(page)
        if pid not in page_items.setdefault(page, []):
            page_items[page].append(pid)

    cur, lesson_pages = None, {u: [] for u in codes}
    for i, raw in enumerate(pages):
        part = part_of.get(i)
        for ln in raw.splitlines():
            s = ln.strip()
            # 章名印成 L.1、C.9、K3.1（单元 K31）。必须带点：页眉上的册名「C1 · 极限与导数」不带点，C1 又恰好是单元号
            m = re.match(r"^([A-Z]{1,4}\d?)\.(\d{1,2})\s*·\s*\S", s)
            if m and m[1] + m[2] in codes:
                cur = m[1] + m[2]
            if part == "lesson" and cur and (not lesson_pages[cur] or lesson_pages[cur][-1] != i):
                lesson_pages[cur].append(i)
            if part in ("problems", "answers"):
                # 题目部分：题号后紧跟「〔」；答案部分：题号独占一行。这样排除了开头的题号总表
                pat = rf"^({PIDS})\s*〔" if part == "problems" else rf"^({PIDS})\s*$"
                for pid in re.findall(pat, s):
                    if pid in mine:
                        mark(pid, "problem" if part == "problems" else "answer", i + 1)
    # 兜底：高公式会打乱 pdftotext 的行，「〔」可能落到别的行。只认行首题号，取最后一次出现（题号总表在前）
    missing = {k for k, x in mine.items() if x["kind"] == "problem" and not x["pages"].get("problem")}
    last: dict[str, int] = {}
    for i, raw in enumerate(pages):
        if part_of.get(i) == "problems":
            for ln in raw.splitlines():
                m = re.match(rf"^({PIDS})(?:\s|$)", ln.strip())
                if m and m[1] in missing:
                    last[m[1]] = i + 1
    for pid, pg in last.items():
        mark(pid, "problem", pg)
    # 例题：用指纹在本单元讲义页的文本里按顺序查找
    for u in codes:
        text, offs = "", []
        for i in lesson_pages[u]:
            offs.append((len(text), i))
            text += core(pages[i])
        pos = 0
        for iid in [k for k, x in mine.items() if x["unit"] == u and x["kind"] == "example"]:
            key = fingerprint(mine[iid]["md"])
            hit = text.find(key, pos) if key else -1
            if hit < 0:
                continue
            pos = hit + len(key)
            mark(iid, "lesson", max(i for o, i in offs if o <= hit) + 1)

    found = sum(1 for x in mine.values() if x["pages"])
    print(f"[{book}] {len(pages)} 页，{len(mine)} 个条目，其中 {found} 个找到页码")
    return {"title": outline["title"], "pdf": pdf.name, "pages": len(pages), "units": codes,
            "page_items": page_items, "page_text": [p.strip() for p in pages]}


def main() -> None:
    idx: dict = {"books": {}, "items": {}, "units": {}}
    codes_seen: dict = {}  # 单元号 → 册号：单元号要在全书里唯一
    for book in ORDER:
        idx["books"][book] = build_book(book, idx["items"], idx["units"], codes_seen)
    out = RELEASE / "qa-index.json"
    out.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    print(f"写入 {out}（{out.stat().st_size // 1024} KB）")


if __name__ == "__main__":
    main()
