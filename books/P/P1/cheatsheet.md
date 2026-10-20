## P.1 · 随机事件与概率（速记）

| 提示 | 内容 |
|---|---|
| 样本空间与事件 | 试验的所有可能结果组成 $\Omega$，事件是 $\Omega$ 的子集；「$A$ 发生」= 结果落进 $A$；$\Omega$ 有 $n$ 个点时共有 $2^n$ 个事件 |
| 写样本空间 | 记录要不重不漏；要用「机会均等」，拿不准就记最细（两颗骰子用 36 个有序对，不用 11 个和） |
| 或、且、非 | $A\cup B$ 至少一个发生；$AB$ 同时发生；$\overline A$ 不发生；$A-B=A\overline B$ |
| 德摩根律 | $\overline{A\cup B}=\overline A\,\overline B$，$\overline{AB}=\overline A\cup\overline B$；「至少一个」先算反面「一个也没有」 |
| 互斥与对立 | 互斥：$AB=\varnothing$；对立：互斥且 $A\cup B=\Omega$；对立必互斥，反之不然 |
| 完备事件组 | $B_1,\dots,B_n$ 两两互斥、并为 $\Omega$；任意 $A=AB_1\cup\cdots\cup AB_n$（互斥的几块） |
| 三条公理 | $P(A)\ge0$；$P(\Omega)=1$；两两互斥的 $A_i$ 有 $P(\bigcup A_i)=\sum P(A_i)$。读作：不为负、总量 1、分开的块可以相加 |
| 基本性质 | $P(\varnothing)=0$；$P(\overline A)=1-P(A)$；$B\subset A\Rightarrow P(B)\le P(A)$；$P(A-B)=P(A)-P(AB)$ |
| 加法公式 | $P(A\cup B)=P(A)+P(B)-P(AB)$；三个事件：单项和减两两交加三交；互斥时直接相加，不互斥而直接相加会多算公共部分 |
| 四格 | $AB,\ A\overline B,\ \overline AB,\ \overline A\,\overline B$ 四块两两互斥、并为 $\Omega$，概率之和为 1；知道 $P(AB)$（或 $P(A),P(B),P(A\cup B)$ 三个数）就能填满 |
| 古典概型 | $P(A)=\#A/\#\Omega$；先确认机会均等；分子分母用同一种数法（都计次序或都不计）；「至少」先想反面 |
| 有放回与无放回 | 有放回：总数 $N^k$，每次候选不变；无放回：每次候选减少；抽签与先后无关 |
| 老朋友① | $P(S=s)=\dfrac{6-|s-7|}{36}$；$P(S\ge10)=\tfrac16$；$P(\text{至少一个 }6)=\tfrac{11}{36}$；较大点数 $P(M=m)=\tfrac{2m-1}{36}$ |
| 几何概型 | $P(A)=m(A)/m(\Omega)$（长度、面积、体积）；画区域、写不等式、求面积之比；单点概率为 0，但概率为 0 的事件不一定不可能 |
| 易错 | 把 11 个和当作机会均等是错的，要用 36 个有序对；「均匀」要说清对哪个量均匀（弦的悖论 $\tfrac13,\tfrac12,\tfrac14$）；若 $P(AB)=0$，则 $P(ABC)\le P(AB)=0$，三事件容斥时不要把 $P(ABC)$ 当未知数 |
