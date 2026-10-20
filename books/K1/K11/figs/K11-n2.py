import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, C, new_fig, save, dot, label
from matplotlib.patches import Rectangle

fig, (ax, tabax) = new_fig(15, 8.5, nrows=2, gridspec_kw={'height_ratios': [3.1, 1.25]})

W, H = 1.1, 0.72          # gate size
Y1, Y2, Y3, Y4 = 2.0, 3.4, 0.6, 2.0
X1, X23, X4 = 2.6, 5.5, 8.4
DY = H / 6.0              # inputs sit at 1/3 and 2/3 of the gate height


def gate(x, y, name):
    ax.add_patch(Rectangle((x - W / 2, y - H / 2), W, H, facecolor=C.PAPER,
                           edgecolor=C.INK, lw=1.4, zorder=3))
    label(ax, '与非', (x, y), ha='center', va='center', fontsize=9)
    label(ax, name, (x, y - H / 2 - 0.06), ha='center', va='top', fontsize=8)


def wire(points):
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=C.INK, lw=1.4, solid_capstyle='round',
            solid_joinstyle='miter', zorder=2)


# G1 left middle, G2 upper right, G3 lower right, G4 far right middle.
gate(X1, Y1, 'G1'); gate(X23, Y2, 'G2')
gate(X23, Y3, 'G3'); gate(X4, Y4, 'G4')

# p enters and splits before G1: one branch to G1's upper input,
# the other along the very top to G2's upper input.
wire([(0.55, 2.45), (1.2, 2.45)])
wire([(1.2, 2.45), (1.2, Y1 + DY), (X1 - W / 2, Y1 + DY)])
wire([(1.2, 2.45), (1.2, Y2 + DY), (X23 - W / 2, Y2 + DY)])
dot(ax, (1.2, 2.45), size=22)

# q enters and splits before G1: one branch to G1's lower input,
# the other along the very bottom to G3's lower input.
wire([(0.55, 1.55), (1.5, 1.55)])
wire([(1.5, 1.55), (1.5, Y1 - DY), (X1 - W / 2, Y1 - DY)])
wire([(1.5, 1.55), (1.5, Y3 - DY), (X23 - W / 2, Y3 - DY)])
dot(ax, (1.5, 1.55), size=22)

# G1 output: short run, then split (solid dot) up to G2's lower input
# and down to G3's upper input.  t labels the run before the split.
wire([(X1 + W / 2, Y1), (3.65, Y1)])
wire([(3.65, Y1), (3.65, Y2 - DY), (X23 - W / 2, Y2 - DY)])
wire([(3.65, Y1), (3.65, Y3 + DY), (X23 - W / 2, Y3 + DY)])
dot(ax, (3.65, Y1), size=22)
label(ax, '$t$', (3.40, Y1), offset=(0, 4), ha='center', va='bottom')

# G2/G3 outputs enter G4's upper/lower inputs.
wire([(X23 + W / 2, Y2), (7.45, Y2), (7.45, Y4 + DY), (X4 - W / 2, Y4 + DY)])
wire([(X23 + W / 2, Y3), (7.45, Y3), (7.45, Y4 - DY), (X4 - W / 2, Y4 - DY)])

# G4 output.
wire([(X4 + W / 2, Y4), (9.75, Y4)])
label(ax, r'$p\oplus q$', (9.85, Y4), ha='left', va='center')

label(ax, '$p$', (0.48, 2.45), ha='right', va='center')
label(ax, '$q$', (0.48, 1.55), ha='right', va='center')

ax.set(xlim=(0.1, 10.45), ylim=(-0.12, 4.02)); ax.axis('off')

tabax.axis('off')
columns = [r'$p,q$', r'$t$', 'G2', 'G3', r'$p\oplus q$']
rows = [[r'$(1,1)$', r'$0$', r'$1$', r'$1$', r'$0$'],
        [r'$(1,0)$', r'$1$', r'$0$', r'$1$', r'$1$'],
        [r'$(0,1)$', r'$1$', r'$1$', r'$0$', r'$1$'],
        [r'$(0,0)$', r'$1$', r'$1$', r'$1$', r'$0$']]
table = tabax.table(cellText=rows, colLabels=columns, cellLoc='center',
                    colLoc='center', bbox=[0.12, 0.02, 0.76, 0.9])
table.auto_set_font_size(False); table.set_fontsize(9)
for cell in table.get_celld().values():
    cell.set_edgecolor(C.GRAY); cell.set_linewidth(0.8)
save(fig, 'K11-n2')
