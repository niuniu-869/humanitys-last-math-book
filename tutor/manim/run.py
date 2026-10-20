"""
在沙箱里渲染模型写的 Manim 场景，并做自查。由宿主在 bwrap 里调用：python run.py <工作目录>。

工作目录里有 scene.py（模型写的代码）和 job.json（{"animate", "width", "height", "fps", "maxSeconds"}）；
结束时写 report.json：
- 成功：{"ok": true, "animate", "width", "height", "duration", "issues": [{"t", "msg"}], "manifest": [...], "files": {...}}
- 失败：{"ok": false, "error": "..."}，error 只保留模型改代码用得上的部分（场景代码的出错行、LaTeX 报错）。

自查分两部分：每段 play / wait 结束时检查文字出界、互相重叠、压在线条上、字号过小（规则写在 check_frame 里）；
最后列出画面里各元素在坐标系中的实际坐标（图元清单），供模型逐项核对数学是否画对。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import traceback
from pathlib import Path

WORK = Path(sys.argv[1])
JOB = json.loads((WORK / "job.json").read_text())
ANIMATE = bool(JOB["animate"])
MAX_SECONDS = float(JOB["maxSeconds"])


def finish(report: dict) -> None:
    (WORK / "report.json").write_text(json.dumps(report, ensure_ascii=False))
    sys.exit(0)


def user_error(exc: BaseException) -> str:
    """场景代码里的出错行 + 异常本身；LaTeX 报错时附上日志里以 ! 开头的几行。"""
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == "scene.py"]
    lines = [f"scene.py 第 {f.lineno} 行：{f.line}" for f in frames[-3:]]
    message = f"{type(exc).__name__}: {exc}"
    log = re.search(r"log file:\s*(\S+\.log)", str(exc))
    if log and Path(log.group(1)).exists():
        text = Path(log.group(1)).read_text(errors="replace").splitlines()
        bad = [i for i, l in enumerate(text) if l.startswith("!")]
        tex = "\n".join("\n".join(text[i:i + 3]) for i in bad[:3])
        message = f"LaTeX 编译失败：\n{tex}" if tex else message
    return "\n".join([*lines, message])


try:
    from manim import *  # noqa: F403
    from manim import config
    import numpy as np
    from PIL import Image

    config.media_dir = str(WORK / "media")
    config.disable_caching = True
    config.verbosity = "ERROR"
    config.progress_bar = "none"
    config.pixel_width, config.pixel_height = int(JOB["width"]), int(JOB["height"])
    config.frame_rate = int(JOB["fps"])
    config.output_file = "out"
    config.write_to_movie = ANIMATE
    config.save_last_frame = False
    config.skip_animations = not ANIMATE
    config.format = "mp4"
    import tutor_kit  # 设定中文字体和 LaTeX 模板；场景里 self.say(...) 的分步说明也记在这里
except Exception as exc:  # 环境问题，不是模型的错
    finish({"ok": False, "internal": True, "error": f"渲染环境出错：{exc}"})

TEXTY = (Text, MarkupText, Paragraph, MathTex, Tex, SingleStringMathTex, DecimalNumber, Integer)
FW, FH = config.frame_width / 2, config.frame_height / 2
# 图在对话里只有约 560 像素宽（手机上更窄），字号低于这个就看不清了。
# 同字号下 LaTeX 排的字（公式、zh()、坐标轴数字）比 Text 小约四分之一，下限相应高一些。
MIN_FONT_TEXT = 28
MIN_FONT_TEX = 32
LATEX = (MathTex, Tex, SingleStringMathTex, DecimalNumber, Integer)


def name_of(m) -> str:
    raw = getattr(m, "text", None) or getattr(m, "tex_string", None)
    if raw is None and hasattr(m, "number"):
        raw = f"{m.number:g}"
    raw = re.sub(r"\s+", " ", str(raw if raw is not None else type(m).__name__)).strip()
    return raw if len(raw) <= 24 else raw[:23] + "…"


def opacity(m) -> float:
    best = 0.0
    for s in m.family_members_with_points():
        try:
            best = max(best, float(s.get_fill_opacity()))
            if s.get_stroke_width() > 0:
                best = max(best, float(s.get_stroke_opacity()))
        except Exception:
            pass
    return best


def box(m) -> tuple[float, float, float, float]:
    return (m.get_left()[0], m.get_bottom()[1], m.get_right()[0], m.get_top()[1])


def texts(mobjects) -> list:
    """画面里看得见的文字对象（文字对象内部不再往下拆）。"""
    out = []

    def walk(m):
        if isinstance(m, TEXTY):
            if m.has_points() or m.family_members_with_points():
                if opacity(m) > 0.3:
                    out.append(m)
            return
        for s in m.submobjects:
            walk(s)

    for m in mobjects:
        walk(m)
    return out


def strokes(mobjects) -> list:
    """画面里看得见的线条（曲线、线段、箭头、多边形的边，以及坐标轴本身）；网格、刻度和文字不算。"""
    out = []

    def walk(m):
        if isinstance(m, CoordinateSystem):
            out.extend(a for a in m.get_axes() if opacity(a) > 0.3)
            return
        if isinstance(m, (*TEXTY, BackgroundRectangle)):
            return
        if isinstance(m, VMobject) and m.has_points():
            try:
                if m.get_stroke_width() > 0.5 and float(m.get_stroke_opacity()) > 0.3:
                    out.append(m)
            except Exception:
                pass
        for s in m.submobjects:
            walk(s)

    for m in mobjects:
        walk(m)
    return out


BEZIER_T = np.linspace(0, 1, 9)


def samples(m) -> np.ndarray:
    """线条上的采样点：每段三次贝塞尔曲线取 9 个点。"""
    pts = m.points[: len(m.points) // 4 * 4].reshape(-1, 4, 3)
    t = BEZIER_T[None, :, None]
    return ((1 - t) ** 3 * pts[:, None, 0] + 3 * (1 - t) ** 2 * t * pts[:, None, 1]
            + 3 * (1 - t) * t ** 2 * pts[:, None, 2] + t ** 3 * pts[:, None, 3]).reshape(-1, 3)


def has_backdrop(m) -> bool:
    return any(isinstance(s, BackgroundRectangle) for s in m.submobjects)


def check_frame(scene, issues: dict, t: float) -> None:
    ts = texts(scene.mobjects)
    lines = [(s, samples(s)) for s in strokes(scene.mobjects)]
    # 坐标轴自带的数字由 Manim 排好位置，不查压线；字号太小时合并成一条
    axis_owned = {id(x) for m in scene.mobjects for c in m.get_family() if isinstance(c, CoordinateSystem) for x in c.get_family()}
    for m in ts:
        if has_backdrop(m) or id(m) in axis_owned:
            continue
        x0, y0, x1, y1 = box(m)
        dx, dy = (x1 - x0) * 0.06, (y1 - y0) * 0.1
        for s, pts in lines:
            inside = (pts[:, 0] > x0 + dx) & (pts[:, 0] < x1 - dx) & (pts[:, 1] > y0 + dy) & (pts[:, 1] < y1 - dy)
            if inside.sum() >= 2:
                issues.setdefault(f"文字「{name_of(m)}」压在{kind_of(s)}上，看不清（挪开，或 add_background_rectangle()）", t)
                break
    for m in ts:
        x0, y0, x1, y1 = box(m)
        side = [n for n, bad in (("左", x0 < -FW + 0.05), ("右", x1 > FW - 0.05), ("下", y0 < -FH + 0.05), ("上", y1 > FH - 0.05)) if bad]
        if side:
            issues.setdefault(f"文字「{name_of(m)}」超出画面（{'、'.join(side)}边）", t)
        size = getattr(m, "font_size", None)
        least = MIN_FONT_TEX if isinstance(m, LATEX) else MIN_FONT_TEXT
        if (size is not None and size < least - 0.5) or (size is None and m.height < 0.14 and m.width < 0.6):
            if id(m) in axis_owned and size is not None:
                issues.setdefault(f"坐标轴数字太小（字号 {size:.0f}），在对话里看不清，axis_config 的 font_size 至少 {least}", t)
            elif size is not None:
                issues.setdefault(f"文字「{name_of(m)}」太小（字号 {size:.0f}），在对话里看不清，{type(m).__name__} 的字号至少 {least}", t)
            else:
                issues.setdefault(f"文字「{name_of(m)}」太小，在对话里看不清", t)
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            a, b = box(ts[i]), box(ts[j])
            w = min(a[2], b[2]) - max(a[0], b[0])
            h = min(a[3], b[3]) - max(a[1], b[1])
            if w <= 0 or h <= 0:
                continue
            small = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
            if small > 0 and w * h / small > 0.2:
                issues.setdefault(f"文字「{name_of(ts[i])}」和「{name_of(ts[j])}」重叠", t)
    for m in scene.mobjects:
        if not m.family_members_with_points() or opacity(m) < 0.05:
            continue
        x0, y0, x1, y1 = box(m)
        if x1 < -FW or x0 > FW or y1 < -FH or y0 > FH:
            issues.setdefault(f"{type(m).__name__}「{name_of(m)}」完全在画面外", t)


KINDS = ((NumberLine, "坐标轴"), (Arrow, "箭头"), (Line, "线段"), (Circle, "圆"), (Polygram, "多边形"), (ParametricFunction, "曲线"))


def kind_of(m) -> str:
    return next((name for cls, name in KINDS if isinstance(m, cls)), "线条")


def axis_aligned(axes) -> bool:
    """坐标系的 x 轴还朝右、y 轴还朝上（没有被 ApplyMatrix、旋转之类变换过）。"""
    try:
        ux, uy = axes.x_axis.get_unit_vector(), axes.y_axis.get_unit_vector()
        return abs(ux[1]) < 0.01 and abs(uy[0]) < 0.01 and ux[0] > 0 and uy[1] > 0
    except Exception:
        return True


def sample_xs(x0: float, x1: float) -> list[float]:
    """函数采样点：两个端点，中间取三个落在整齐刻度（1、2、5 × 10^k 的倍数）上的点，方便和题目对照。"""
    lo, hi = min(x0, x1), max(x0, x1)
    span = hi - lo
    if span <= 0:
        return [x0]
    step = min((k * 10.0 ** e for e in range(-3, 4) for k in (1, 2, 5)), key=lambda v: abs(v - span / 4))
    inner = sorted({round(round(x / step) * step, 6) for x in np.linspace(lo, hi, 5)[1:-1]} - {lo, hi})
    return [lo, *[x for x in inner if lo < x < hi], hi]


def fmt(v: float) -> str:
    v = float(v)
    return "0" if abs(v) < 5e-4 else f"{v:.3g}"


def manifest(scene) -> list[str]:
    """最终画面的图元清单：有坐标系时用坐标系里的坐标，否则用场景坐标。"""
    axes = next((m for m in scene.mobjects if isinstance(m, CoordinateSystem)), None)
    if axes is None:
        for m in scene.mobjects:
            axes = next((s for s in m.get_family() if isinstance(s, CoordinateSystem)), None)
            if axes is not None:
                break
    warped = axes is not None and not axis_aligned(axes)
    if warped:
        axes = None

    def c(p) -> str:
        q = axes.p2c(p) if axes is not None else p[:2]
        return f"({fmt(q[0])}, {fmt(q[1])})"

    skip = set(map(id, axes.get_family())) if axes is not None else set()
    lines: list[str] = []
    head = (f"坐标系 x∈[{fmt(axes.x_range[0])}, {fmt(axes.x_range[1])}], y∈[{fmt(axes.y_range[0])}, {fmt(axes.y_range[1])}]" if axes is not None
            else f"坐标系被变换过（不再横平竖直），以下用画面坐标（画面 x∈[{fmt(-FW)}, {fmt(FW)}]，y∈[{fmt(-FH)}, {fmt(FH)}]）" if warped
            else f"画面坐标（画面 x∈[{fmt(-FW)}, {fmt(FW)}]，y∈[{fmt(-FH)}, {fmt(FH)}]）")
    lines.append(head)

    def walk(m, depth=0):
        if id(m) in skip or len(lines) > 40 or opacity(m) < 0.05 or isinstance(m, BackgroundRectangle):
            return
        kinds = {type(s) for s in m.submobjects}
        if isinstance(m, TEXTY):
            lines.append(f"文字「{name_of(m)}」在 {c(m.get_center())}")
        elif isinstance(m, Dot):
            lines.append(f"点 {c(m.get_center())}")
        elif isinstance(m, Arrow):
            lines.append(f"箭头 {c(m.get_start())} → {c(m.get_end())}")
        elif isinstance(m, Line):
            lines.append(f"线段 {c(m.get_start())} — {c(m.get_end())}")
        elif isinstance(m, DashedVMobject):
            lines.append(f"虚线 范围 {c(m.get_corner(DL))} 到 {c(m.get_corner(UR))}")
        elif isinstance(m, Circle):
            r = m.width / 2
            if axes is not None:
                r = abs(axes.p2c(m.get_center() + RIGHT * r)[0] - axes.p2c(m.get_center())[0])
            lines.append(f"圆 圆心 {c(m.get_center())} 半径 {fmt(r)}")
        elif isinstance(m, Polygram):
            vs = m.get_vertices()[:8]
            lines.append(f"多边形 顶点 {' '.join(c(v) for v in vs)}")
        elif isinstance(m, ParametricFunction):
            f = getattr(m, "underlying_function", None)
            if axes is not None and f is not None:
                x0, x1 = axes.p2c(m.get_start())[0], axes.p2c(m.get_end())[0]
                pts = ", ".join(f"f({fmt(x)})={fmt(f(x))}" for x in sample_xs(x0, x1))
                lines.append(f"函数图像 x∈[{fmt(x0)}, {fmt(x1)}]：{pts}")
            else:
                lines.append(f"曲线 {c(m.get_start())} 到 {c(m.get_end())}")
        elif len(m.submobjects) > 6 and len(kinds) == 1 and not issubclass(next(iter(kinds)), TEXTY):
            lines.append(f"{len(m.submobjects)} 个{kind_of(m.submobjects[0])}，整体范围 {c(m.get_corner(DL))} 到 {c(m.get_corner(UR))}")
        elif m.submobjects and depth < 4:
            for s in m.submobjects:
                walk(s, depth + 1)
        elif m.has_points():
            lines.append(f"{type(m).__name__} 范围 {c(m.get_corner(DL))} 到 {c(m.get_corner(UR))}")

    for m in scene.mobjects:
        walk(m)
    return lines[:41]


def frame_image(scene) -> Image.Image:
    return Image.fromarray(np.array(scene.renderer.get_frame())).convert("RGB")


try:
    namespace: dict = {"__name__": "scene"}
    exec("from manim import *\nfrom tutor_kit import *", namespace)
    exec(compile((WORK / "scene.py").read_text(), "scene.py", "exec"), namespace)
    scenes = [v for v in namespace.values() if isinstance(v, type) and issubclass(v, Scene) and v.__module__ == "scene"]
    base = namespace.get("Main") if isinstance(namespace.get("Main"), type) else (scenes[-1] if scenes else None)
    if base is None:
        raise ValueError("没有找到场景：请定义 class Main(Scene)，在 construct 里画图")

    issues: dict = {}
    keyframes: list = []

    class Checked(base):  # type: ignore[valid-type, misc]
        def _after(self):
            t = round(float(self.renderer.time), 1)
            if t > MAX_SECONDS:
                raise RuntimeError(f"动画总时长超过 {MAX_SECONDS:g} 秒，请精简步骤或缩短 run_time")
            check_frame(self, issues, t)
            if ANIMATE and not (keyframes and keyframes[-1][0] == t):
                # 帧缓冲里是这段动画渲染的最后一帧（差一点没播完），先按结束状态重画一帧再截
                self.renderer.update_frame(self, ignore_skipping=True)
                img = frame_image(self)
                img.thumbnail((480, 270))
                # 和上一帧一样（wait 之类）就不收，拼图里每格都该有变化。重画同一画面时抗锯齿会有轻微差异（实测单像素差 < 64），
                # 多了一个小标签则有上百个像素变化超过 96，所以按「明显变化的像素数」判断
                if not keyframes or (np.abs(np.asarray(img, dtype=np.int16) - np.asarray(keyframes[-1][1], dtype=np.int16)).max(axis=2) > 80).sum() > 30:
                    keyframes.append((t, img))

        # wait 内部也走 play，只挂 play 就能覆盖两者
        def play(self, *args, **kwargs):
            super().play(*args, **kwargs)
            self._after()

    Checked.__name__ = base.__name__
    scene = Checked()
    scene.render()
except SystemExit:
    raise
except BaseException as exc:  # noqa: BLE001  模型的代码可能抛任何异常
    finish({"ok": False, "error": user_error(exc)})

try:
    check_frame(scene, issues, round(float(scene.renderer.time), 1))
    if not any(m.family_members_with_points() for m in scene.mobjects):
        finish({"ok": False, "error": "画面是空的：场景结束时没有任何可见的对象（静态图请用 self.add 加上对象）"})
    scene.renderer.update_frame(scene, ignore_skipping=True)
    final = frame_image(scene)
    final.save(WORK / "final.png", optimize=True)
    files = {"final": "final.png"}
    if ANIMATE:
        movies = [p for p in (WORK / "media").rglob("out.mp4") if "partial_movie_files" not in p.parts]
        if not movies:
            finish({"ok": False, "internal": True, "error": "视频没有生成"})
        # moov 放到文件开头，浏览器边下边放
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(movies[0]), "-c", "copy", "-movflags", "+faststart",
                        str(WORK / "out.mp4")], check=True)
        files["video"] = "out.mp4"
        picks = keyframes if len(keyframes) <= 8 else [keyframes[round(i * (len(keyframes) - 1) / 7)] for i in range(8)]
        cols = 2 if len(picks) <= 4 else 3 if len(picks) <= 6 else 4
        rows = (len(picks) + cols - 1) // cols
        gap = 8  # 灰色分隔，免得相邻两帧的内容连在一起
        sheet = Image.new("RGB", (cols * 480 + (cols - 1) * gap, rows * 270 + (rows - 1) * gap), (90, 90, 90))
        for i, (_, img) in enumerate(picks):
            sheet.paste(img, ((i % cols) * (480 + gap), (i // cols) * (270 + gap)))
        sheet.save(WORK / "sheet.png", optimize=True)
        files["sheet"] = "sheet.png"
        files["sheetTimes"] = [t for t, _ in picks]
    finish({
        "ok": True, "animate": ANIMATE, "width": config.pixel_width, "height": config.pixel_height,
        "duration": round(float(scene.renderer.time), 1),
        "steps": [{"t": t, "text": text} for t, text in tutor_kit.STEPS if text],
        "issues": [{"t": t, "msg": msg} for msg, t in issues.items()],
        "manifest": manifest(scene), "files": files,
    })
except SystemExit:
    raise
except BaseException as exc:  # noqa: BLE001
    finish({"ok": False, "internal": True, "error": f"渲染后处理出错：{type(exc).__name__}: {exc}"})
