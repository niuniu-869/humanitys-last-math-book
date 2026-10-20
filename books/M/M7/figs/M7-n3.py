import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

x, w, b = 3., 0.5, -1.
u = w*x; z = u+b; p = 1/(1+np.exp(-z)); loss = -np.log(p)
gp = -1/p; gz = p-1; gw = gz*x
assert np.allclose([u,z,p,loss,gp,gz,gw], [1.5,.5,.6225,.4741,-1.6065,-.3775,-1.1326], atol=5e-5)
fig, ax = new_fig(18, 8)
ax.set(xlim=(-1, 12.8), ylim=(-2.8, 3.0))
ax.axis('off')
def txt(text, xy, size=10):
    label(ax, text, xy, ha='center', va='center', fontsize=size)
def node(name, xy, val, grad=None):
    a,b = xy
    ax.add_patch(Rectangle((a-.4,b-.28), .8,.56, facecolor=C.PAPER, edgecolor=C.INK))
    txt(name, xy)
    txt(val, (a+.63 if name == '$ z$' else a,b+.64 if name == '$ z$' else b+.53), 9)
    if grad: txt(grad, (a,b-.72), 9)
def edge(a,b,back=False):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=C.INK, lw=1.1, linestyle='--' if back else '-', shrinkA=0, shrinkB=0))
node('$x$', (0,1.8), '$3$')
node('$w$', (0,0), '$0.5$', rf'$\bar w={gw:.4f}$')
for pos, name, value, grad in [
    (3,'u',u,gz), (6,'z',z,gz), (9,'p',p,gp), (12,r'\ell',loss,1)]:
    fmt = '.1f' if name in ('u','z') else '.4f'
    node(f'$ {name}$', (pos,0), f'$ {value:{fmt}}$', rf'$\bar{{{name}}}={grad:.4f}$' if name != r'\ell' else r'$\bar\ell=1$')
node('$b$', (6,1.8), '$-1$', None)
txt(rf'$\bar b={gz:.4f}$', (7.2,1.08), 9)
edge((.4,1.8),(2.6,.20))
edge((.4,.14),(2.6,.14))
for left in [3,6,9]:
    edge((left+.4,.14),(left+2.6,.14))
    edge((left+2.6,-.14),(left+.4,-.14),True)
edge((6,1.52),(6,.28))
edge((6.2,.28),(6.2,1.52),True)
edge((2.6,-.14),(.4,-.14),True)
for a, op in [(1.5,r'$\times$'),(4.5,'$+$'),(7.5,r'$\sigma$'),(10.5,r'$-\ln$')]:
    txt(op,(a,.48))
txt('局部导数 $x=3$', (1.5,-1.55), 9)
txt('局部导数 $p(1-p)=0.2350$', (7.5,-1.55), 9)
edge((2.8,2.7),(4.1,2.7)); txt('前向值',(4.9,2.7),9)
edge((8.5,2.7),(7.2,2.7),True); txt('反向梯度',(9.5,2.7),9)
save(fig, "M7-n3")
