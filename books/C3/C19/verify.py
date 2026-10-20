"""验算：依次运行 checks/ 下各写作任务的验算脚本，汇总结果。用法：python verify.py"""
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
count = {"PASS": 0, "FAIL": 0, "MANUAL": 0}
for p in sorted((here / "checks").glob("*.py")):
    r = subprocess.run([sys.executable, p.name], cwd=p.parent, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in (r.stdout + r.stderr).splitlines():
        head = line.split(" ", 1)[0]
        if head in count:
            count[head] += 1
            print(f"[{p.stem}] {line}")
    if r.returncode:
        count["FAIL"] += 1
        print(f"[{p.stem}] FAIL 脚本出错：{r.stderr[-300:]}")
print(f"汇总：PASS {count['PASS']}，FAIL {count['FAIL']}，MANUAL {count['MANUAL']}")
sys.exit(1 if count["FAIL"] else 0)
