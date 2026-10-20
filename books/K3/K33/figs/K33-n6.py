import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

clauses = [(-1,2),(-1,3),(-2,-3),(1,4),(-4,5),(2,-5)]
def propagate(assignment, variable, clause_index):
    clause = clauses[clause_index]
    unknown = [v for v in clause if abs(v) not in assignment]
    assert len(unknown) == 1 and abs(unknown[0]) == variable
    assert all(assignment[abs(v)] != (v>0) for v in clause if abs(v) in assignment)
    assignment[variable] = unknown[0] > 0
left = {1:True}
propagate(left,2,0)
propagate(left,3,1)
assert all(left[abs(v)] != (v>0) for v in clauses[2])
right = {1:False}
for v,i in [(4,3),(5,4),(2,5),(3,2)]:
    propagate(right,v,i)
assert all(any(right[abs(v)] == (v>0) for v in clause) for clause in clauses)
fig, ax = new_fig(18, 13)
label(ax,"开始",(5,8),ha="center",va="center")
left_text = [r"传播：$x_2$=真"+"\n"+r"$(\neg x_1\vee x_2)$",
             r"传播：$x_3$=真"+"\n"+r"$(\neg x_1\vee x_3)$",
             r"冲突：$\neg x_2\vee\neg x_3$ 全假"]
right_text = [r"传播：$x_4$=真"+"\n"+r"$(x_1\vee x_4)$",
              r"$x_5$=真"+"\n"+r"$(\neg x_4\vee x_5)$",
              r"$x_2$=真"+"\n"+r"$(x_2\vee\neg x_5)$",
              r"$x_3$=假"+"\n"+r"$(\neg x_2\vee\neg x_3)$", "全部子句满足"]
for x, texts, truth in [(2.3,left_text,"真"),(7.7,right_text,"假")]:
    arrow(ax,(5,7.7),(x-5,-.9),color=C.INK,lw=1.2)
    label(ax,r"猜 $x_1$="+truth,((5+x)/2+(-.3 if x<5 else .3),7.55),ha="center",fontsize=10)
    for i,text in enumerate(texts):
        y = 6.25-i*1.4
        ax.add_patch(Rectangle((x-2.05,y-.47),4.1,.94,facecolor=C.PAPER,edgecolor=C.INK,lw=1))
        label(ax,text,(x,y),ha="center",va="center",fontsize=10)
        if i:
            arrow(ax,(x,y+.93),(0,-.43),color=C.INK,lw=1)
        if text == "全部子句满足":
            ax.add_patch(Rectangle((x-2.14,y-.55),4.28,1.1,fill=False,edgecolor=C.INK,lw=1))
    if x<5:
        label(ax,r"$\times$",(x+2.36,y),ha="center",va="center",fontsize=17)
ax.set(xlim=(-.2,10.4),ylim=(-.25,8.5))
ax.axis("off")
save(fig, "K33-n6")
