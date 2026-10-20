import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch, Rectangle

fig, ax = new_fig(18, 9)
nodes = {
 'root': (5.0, 6.8), 'L': (2.4, 5.2), 'R': (7.6, 5.2),
 'LL': (1.0, 3.6), 'LR': (3.8, 3.6), 'RL': (6.2, 3.6), 'RR': (9.0, 3.6),
 'LR1': (3.15, 1.7), 'LR2': (4.45, 1.7), 'RR1': (8.35, 1.7), 'RR2': (9.65, 1.7),
}
leaf_text = {'LL':'a<b<c', 'RL':'b<a<c'}
texts = {'root':'a<b？','L':'b<c？','R':'a<c？','LR':'a<c？','RR':'b<c？',
         'LR1':'a<c<b','LR2':'c<a<b','RR1':'b<c<a','RR2':'c<b<a', **leaf_text}
edges = [('root','L','是'),('root','R','否'),('L','LL','是'),('L','LR','否'),
         ('R','RL','是'),('R','RR','否'),('LR','LR1','是'),('LR','LR2','否'),
         ('RR','RR1','是'),('RR','RR2','否')]
for p,c,t in edges:
    x1,y1=nodes[p]; x2,y2=nodes[c]
    ax.plot([x1,x2],[y1-.23,y2+.25], color=C.INK, lw=1.0)
    label(ax,t,((x1+x2)/2,(y1+y2)/2+.08),ha='center',va='center',fontsize=8)
for k,(x,y) in nodes.items():
    if k in texts and k not in ('root','L','R'):
        ax.add_patch(Rectangle((x-.58,y-.25),1.16,.5,facecolor=C.PAPER,edgecolor=C.INK,lw=1.0))
    elif k in texts:
        ax.add_patch(FancyBboxPatch((x-.6,y-.25),1.2,.5,boxstyle='round,pad=.08',facecolor=C.PAPER,edgecolor=C.INK,lw=1.0))
    if k in texts: label(ax,texts[k],(x,y),ha='center',va='center',fontsize=9)
for depth,y in [(0,6.8),(1,5.2),(2,3.6),(3,1.7)]: label(ax,f'层 {depth}',(10.8,y),ha='left',va='center',fontsize=9)
label(ax,'共 6 个叶子，最深第 3 层',(5.1,.55),ha='center',fontsize=10)
ax.set(xlim=(-.5,12.0),ylim=(.15,7.45)); ax.axis('off')
save(fig, 'K32-n5')
