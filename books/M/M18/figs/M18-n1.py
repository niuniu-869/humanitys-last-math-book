import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(21, 23)
ax.set(xlim=(-1.1, 12.6), ylim=(-1.4, 15.6))
ax.axis('off')
w, h = 3.8, 0.85

def box(x, y, text, shape=r'$n\times512$'):
    ax.add_patch(Rectangle((x-w/2, y-h/2), w, h,
                           facecolor=C.PAPER, edgecolor=C.INK, lw=1))
    label(ax, text, (x, y), ha='center', va='center', fontsize=9)
    label(ax, shape, (x+w/2+0.12, y), va='center', fontsize=9)

def up(x, a, b):
    arrow(ax, (x, a+h/2), (0, b-a-h), color=C.INK, lw=1.2)

def residual(x, sub, norm):
    # Tap the sublayer input, then enter the normalization box from the left.
    y = sub-0.70
    side = x-w/2-0.35
    ax.plot([x, side, side], [y, y, norm], color=C.INK, ls='--', lw=1)
    ax.annotate('', xy=(x-w/2, norm), xytext=(side, norm),
                arrowprops=dict(arrowstyle='-|>', color=C.INK, ls='--', lw=1))

xl, xr = 1.8, 8.5
enc = [(0, '输入嵌入 + 位置编码\n（M.9.3、M.12.4）'),
       (1.8, '多头自注意力（M.12.1）'),
       (3.6, '加 & 层归一化\n（M.8.5、M.12.3）'),
       (5.4, '前馈层（M.12.2）'),
       (7.2, '加 & 层归一化（M.12.3）')]
dec = [(0, '输出嵌入（右移一位）\n+ 位置编码（M.9.3、M.12.4）'),
       (1.8, '带掩码的多头自注意力\n（M.11.5）'),
       (3.6, '加 & 层归一化（M.12.3）'),
       (5.4, '交叉注意力（M.11.6）'),
       (7.2, '加 & 层归一化（M.12.3）'),
       (9.0, '前馈层（M.12.2）'),
       (10.8, '加 & 层归一化（M.12.3）'),
       (13.6, '线性层 + softmax（M.12.7）')]
for x, rows in [(xl, enc), (xr, dec)]:
    for y, text in rows:
        box(x, y, text, r'$n\times$词表大小' if y == 13.6 else r'$n\times512$')
    for (a, _), (b, _) in zip(rows, rows[1:]):
        up(x, a, b)
for x, pairs in [(xl, [(1.8, 3.6), (5.4, 7.2)]),
                 (xr, [(1.8, 3.6), (5.4, 7.2), (9.0, 10.8)])]:
    for sub, norm in pairs:
        residual(x, sub, norm)

# Dotted outlines delimit only the layers repeated six times.
for x, top in [(xl, 7.95), (xr, 11.55)]:
    ax.add_patch(Rectangle((x-2.45, 0.85), 5.6, top-0.85,
                          fill=False, edgecolor=C.GRAY, ls=':', lw=1))
label(ax, '编码器的一层（× 6）', (xl+0.3, 9.8), ha='center', fontsize=11)
label(ax, '解码器的一层（× 6）', (xr+0.3, 14.8), ha='center', fontsize=11)
ax.plot([xl, xl, 5.5, 5.5], [7.625, 9.25, 9.25, 5.4],
        color=C.INK, lw=2.1, ls='-')
arrow(ax, (5.5, 5.4), (xr-w/2-5.5, 0), color=C.INK, lw=2.1)
label(ax, r'$K,V$', (4.55, 10.05), ha='center', va='center', fontsize=11)
label(ax, r'$Q$', (xr, 4.55), offset=(8, 0), fontsize=11)
label(ax, '本书写法（M.12.6）：层归一化放在子层之前，没有编码器一列。',
      (-0.65, -1.1), fontsize=9)
fig.tight_layout(pad=0.5)
save(fig, "M18-n1")
