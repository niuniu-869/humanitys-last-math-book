#!/usr/bin/env python3
"""跑全部章节的验算：python tools/verify_all.py [册号 ...]

每章的 verify.py 会依次运行本章 checks/ 下的脚本，用 sympy/numpy 独立算出讲义例题和题目的数值答案。
输出每章的 PASS / FAIL / MANUAL 计数；MANUAL 是证明题等只能人工核对的项。有任何 FAIL 时退出码为 1。
依赖：pip install sympy numpy scipy
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER = ["Z", "C1", "C2", "C3", "L", "P", "M", "K1", "K2", "K3", "K4"]


def chapters(books):
    for b in books:
        units = sorted((ROOT / "books" / b).glob("*/verify.py"), key=lambda p: int(re.sub(r"\D", "", p.parent.name)))
        yield from (p.parent for p in units)


def main() -> None:
    books = sys.argv[1:] or ORDER
    total = {"PASS": 0, "FAIL": 0, "MANUAL": 0}
    bad = []
    for d in chapters(books):
        r = subprocess.run([sys.executable, "verify.py"], cwd=d, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        m = re.search(r"PASS (\d+)，FAIL (\d+)，MANUAL (\d+)", r.stdout)
        if not m:
            bad.append(d.name)
            print(f"{d.relative_to(ROOT)}  脚本出错：{(r.stderr or r.stdout)[-300:]}")
            continue
        n = dict(zip(total, map(int, m.groups())))
        for k in total:
            total[k] += n[k]
        if n["FAIL"]:
            bad.append(d.name)
        print(f"{d.relative_to(ROOT)}  PASS {n['PASS']}  FAIL {n['FAIL']}  MANUAL {n['MANUAL']}")
    print(f"\n合计：PASS {total['PASS']}，FAIL {total['FAIL']}，MANUAL {total['MANUAL']}"
          + (f"；有问题的章：{'、'.join(bad)}" if bad else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
