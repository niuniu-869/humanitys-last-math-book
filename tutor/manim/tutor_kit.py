"""
答疑画图用的 Manim 小工具，模型写的场景会自动 `from tutor_kit import *`。

- 中文：Text 默认用思源宋体；Tex / MathTex 的模板带 CJKutf8，公式里可以直接写中文（与 LaTeX 数学字体同为衬线，混排协调）。
- zh(...)：一句话里中文和 $公式$ 混排（统一用 LaTeX 排，同样的字号得到同样大的字）。
- flow(...)：流程图，按依赖自动分层排版，跨层的连线绕到外侧，fit 进画面；reveal_flow(...) 逐层出现。
- fit(...)：把一组对象缩放进画面。
- self.say(...)：写一步说明，显示在图下方；动画播到这一步时高亮。
"""
from __future__ import annotations

from manim import *

CJK_FONT = "Noto Serif CJK SC"

CJK_TEX = TexTemplate()
CJK_TEX.add_to_preamble(r"\usepackage{CJKutf8}\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}\AtEndDocument{\end{CJK}}")
config.tex_template = CJK_TEX
Text.set_default(font=CJK_FONT)
MarkupText.set_default(font=CJK_FONT)
# 图在对话里只有约 560 像素宽：函数曲线和点比 Manim 默认（为全屏视频设计）粗一些、大一些
ParametricFunction.set_default(stroke_width=5)
Dot.set_default(radius=0.1)

FRAME_W = config.frame_width
FRAME_H = config.frame_height

# 分步说明：(开始时刻, 文字)。在要说明的那段 play 之前调用 self.say(...)，时刻就是这一步开始的时间。
STEPS: list = []


def _say(self: Scene, text: str) -> None:
    STEPS.append((round(float(self.renderer.time), 1), str(text).strip()))


Scene.say = _say


def zh(text: str, font_size: float = 40, **kwargs) -> Mobject:
    """中文与 $公式$ 混排，用 LaTeX 排版（模板已支持中文）。
    同字号下 Text 的中文比 Tex 大约三分之一，混用会大小不一，所以这里一律用 Tex。"""
    return Tex(text, font_size=font_size, **kwargs)


def fit(mobject: Mobject, width: float = FRAME_W - 1.0, height: float = FRAME_H - 1.0) -> Mobject:
    """只缩小不放大，把对象放进 width × height 的范围里，并居中。"""
    scale = min(1.0, width / max(mobject.width, 1e-6), height / max(mobject.height, 1e-6))
    return mobject.scale(scale).move_to(ORIGIN)


def _wrap(text: str, per_line: int) -> str:
    """不含公式的中文按字数折行；含 $ 的不折，免得把公式拆开。"""
    if "$" in text or "\n" in text or len(text) <= per_line:
        return text
    return "\n".join(text[i:i + per_line] for i in range(0, len(text), per_line))


def _layers(names: list[str], edges: list[tuple]) -> list[list[str]]:
    """按最长路径分层；有环时环上的点留在已到达的最深一层。"""
    depth = {n: 0 for n in names}
    for _ in range(len(names)):
        changed = False
        for e in edges:
            a, b = e[0], e[1]
            if a in depth and b in depth and depth[b] < depth[a] + 1 and depth[a] + 1 < len(names):
                depth[b] = depth[a] + 1
                changed = True
        if not changed:
            break
    layers: list[list[str]] = [[] for _ in range(max(depth.values(), default=0) + 1)]
    for n in names:
        layers[depth[n]].append(n)
    return [layer for layer in layers if layer]


ARROW_STYLE = dict(stroke_width=3, color=GREY_B)


def _straight(a: Mobject, b: Mobject, vertical: bool) -> Arrow:
    """相邻两层之间的连线：从 a 朝 b 的那一边出发。"""
    delta = b.get_center() - a.get_center()
    if vertical and abs(delta[1]) > 0.1:
        start, end = (a.get_bottom(), b.get_top()) if delta[1] < 0 else (a.get_top(), b.get_bottom())
    elif not vertical and abs(delta[0]) > 0.1:
        start, end = (a.get_right(), b.get_left()) if delta[0] > 0 else (a.get_left(), b.get_right())
    else:
        start, end = (a.get_right(), b.get_left()) if delta[0] > 0 else (a.get_left(), b.get_right())
    return Arrow(start, end, buff=0.08, max_tip_length_to_length_ratio=0.15, **ARROW_STYLE)


def _detour(a: Mobject, b: Mobject, between: list, siblings: list, vertical: bool):
    """跨层的连线：绕到外侧走，最后从侧面进入 b，不穿过中间层的节点。
    a 在本层最外侧时从侧面直接出发；否则先走到层间空隙再拐出去，免得穿过同层的节点。
    返回 (连线, 放标签的位置, 标签朝哪边)。"""
    m, c = (1, 0) if vertical else (0, 1)  # m：层与层之间的方向；c：同一层里节点排开的方向
    step = np.sign(b.get_center()[m] - a.get_center()[m])
    nodes = [*between, a, b]
    side = 1 if b.get_center()[c] >= np.mean([x.get_center()[c] for x in nodes]) else -1
    reach = [x.get_center()[c] + side * x.length_over_dim(c) / 2 for x in nodes]
    route = (max(reach) if side > 0 else min(reach)) + side * 0.45
    outermost = all(side * x.get_center()[c] < side * a.get_center()[c] for x in siblings if x is not a)
    start = a.get_center().copy()
    if outermost:
        start[c] += side * a.length_over_dim(c) / 2
        p1 = start
    else:
        start[m] += step * a.length_over_dim(m) / 2
        p1 = start.copy()
        p1[m] += step * 0.45
    p2 = p1.copy()
    p2[c] = route
    p3 = p2.copy()
    p3[m] = b.get_center()[m]
    end = b.get_center().copy()
    end[c] += side * b.length_over_dim(c) / 2
    path = VMobject(**ARROW_STYLE).set_points_as_corners([start, *([p1] if p1 is not start else []), p2, p3])
    tip = Arrow(p3, end, buff=0.08, max_tip_length_to_length_ratio=0.35, **ARROW_STYLE)
    out = np.zeros(3)
    out[c] = side
    return VGroup(path, tip), (p2 + p3) / 2, out


class Flow(VGroup):
    """flow() 的结果：box[名字] 是节点，arrow[(起, 止)] 是连线，layers 是逐层的节点名。"""

    box: dict
    arrow: dict
    layers: list


def flow(nodes: dict, edges: list, direction=DOWN, font_size: float = 40, per_line: int = 10,
         node_color=BLUE_C, decision_color=YELLOW_C) -> Flow:
    """
    流程图。
    nodes: {名字: 文字}，文字可含 $公式$；以「？」或「?」结尾的节点算判断，用黄色描边。
    edges: [(起, 止)] 或 [(起, 止, 标签)]。
    direction: DOWN（自上而下）或 RIGHT（自左而右）。
    """
    names = list(nodes)
    g = Flow()
    g.box, g.arrow = {}, {}
    for name, text in nodes.items():
        label = zh(_wrap(str(text), per_line), font_size=font_size)
        decision = str(text).rstrip().endswith(("？", "?"))
        frame = RoundedRectangle(
            corner_radius=0.15, width=label.width + 0.5, height=label.height + 0.4,
            stroke_color=decision_color if decision else node_color, stroke_width=2.5,
            fill_color=BLACK, fill_opacity=0.85,
        )
        g.box[name] = VGroup(frame, label.move_to(frame))

    g.layers = _layers(names, edges)
    layer_of = {n: i for i, layer in enumerate(g.layers) for n in layer}
    vertical = np.allclose(direction, DOWN) or np.allclose(direction, UP)
    across = RIGHT if vertical else DOWN
    rows = []
    for layer in g.layers:
        row = VGroup(*[g.box[n] for n in layer]).arrange(across, buff=0.6)
        rows.append(row)
    VGroup(*rows).arrange(direction, buff=1.1)
    g.add(*[g.box[n] for n in names])

    for e in edges:
        a, b = g.box[e[0]], g.box[e[1]]
        la, lb = layer_of[e[0]], layer_of[e[1]]
        if abs(lb - la) > 1:
            between = [g.box[n] for layer in g.layers[min(la, lb) + 1:max(la, lb)] for n in layer]
            arrow, mid, out = _detour(a, b, between, [g.box[n] for n in g.layers[la]], vertical)
        else:
            arrow = _straight(a, b, vertical)
            d = arrow.get_unit_vector()
            out = np.array([-d[1], d[0], 0]) * (1 if -d[1] >= 0 else -1)  # 垂直于箭头、偏右的一侧
            mid = arrow.point_from_proportion(0.5)
        g.arrow[(e[0], e[1])] = arrow
        g.add(arrow)
        if len(e) > 2 and e[2]:
            tag = zh(str(e[2]), font_size=font_size * 0.85, color=GREY_A)
            tag.add_background_rectangle(color=BLACK, opacity=0.9, buff=0.05)
            tag.next_to(mid, out, buff=0.1)
            g.add(tag)
            arrow.tag = tag
    fit(g)
    return g


def reveal_flow(scene: Scene, g: Flow, run_time: float = 0.8) -> None:
    """按层逐步画出流程图：先出现这一层的节点，再长出指向它们的连线。"""
    shown: set = set()
    for layer in g.layers:
        scene.play(*[FadeIn(g.box[n], shift=0.2 * DOWN) for n in layer], run_time=run_time)
        shown.update(layer)
        arrows = [a for (s, t), a in g.arrow.items() if t in shown and s in shown and a not in scene.mobjects]
        anims = [GrowArrow(a) if isinstance(a, Arrow) else Create(a) for a in arrows] + [FadeIn(a.tag) for a in arrows if hasattr(a, "tag")]
        if anims:
            scene.play(*anims, run_time=run_time * 0.7)
