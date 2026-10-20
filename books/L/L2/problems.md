## L.2 · 点积、长度、夹角与投影（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L2-01 | A | 方法 1（选择） |
| L2-02 | A | 方法 2 |
| L2-03 | A | 方法 4 |
| L2-04 | A | 方法 4（选择） |
| L2-05 | A | 方法 6 |
| L2-06 | B | 方法 2、4 |
| L2-07 | B | 方法 3 |
| L2-08 | B | 方法 1、2（选择） |
| L2-09 | B | 方法 6 |
| L2-10 | C | 方法 5（证明） |
| L2-11 | C | 方法 2、6（证明） |
| L2-12 | B | 混合（答案里标，证明） |
| L2-13 | B | 混合（答案里标，证明） |
| L2-14 | C | 混合（答案里标） |

### A 基础

**L2-01**〔A｜方法 1 · 考查：锐角要排除同向〕（选择）设 $\boldsymbol{a}=(1,2)^{\mathsf T}$，$\boldsymbol{b}=(k,1)^{\mathsf T}$。$\boldsymbol{a}$ 与 $\boldsymbol{b}$ 的夹角为锐角，当且仅当（　）。

(A) $k>-2$
(B) $k\ge-2$
(C) $k>-2$ 且 $k\ne2$
(D) $k>-2$ 且 $k\ne\frac12$

**L2-02**〔A｜方法 2 · 考查：由夹角反求分量〕若 $(k,0,1)^{\mathsf T}$ 与 $(1,1,0)^{\mathsf T}$ 的夹角为 $\frac{2\pi}{3}$，则 $k=$ \_\_\_\_。

**L2-03**〔A｜方法 4 · 考查：由投影反求向量〕已知 $\boldsymbol{b}=(x,2,3)^{\mathsf T}$ 在 $(1,1,1)^{\mathsf T}$ 上的投影是 $(2,2,2)^{\mathsf T}$。求 $x$ 和残差 $\boldsymbol{e}$，并说明投影里的 2 是 $\boldsymbol{b}$ 的什么量。

**L2-04**〔A｜方法 4 · 考查：投影的三个量在 $\boldsymbol{a}$ 伸缩、反向时怎么变〕（选择）对任意非零向量 $\boldsymbol{a}$ 和任意向量 $\boldsymbol{b}$，$\boldsymbol{b}$ 在 $\boldsymbol{a}$ 上的投影系数为 $t$，带符号长度为 $\ell=\frac{\boldsymbol{a}\cdot\boldsymbol{b}}{\lVert\boldsymbol{a}\rVert}$，投影为 $\boldsymbol{p}$，残差为 $\boldsymbol{e}$。把 $\boldsymbol{a}$ 换成 $-2\boldsymbol{a}$ 后，下面哪一项变换公式对任意这样的 $\boldsymbol{a},\boldsymbol{b}$ 恒成立（　）。

(A) 投影系数变成 $-2t$
(B) 投影变成 $-2\boldsymbol{p}$
(C) 带符号长度仍是 $\ell$
(D) 投影和残差都不变

**L2-05**〔A｜方法 6 · 考查：去均值后的零向量没有夹角〕设 $\boldsymbol{q}=(4,4,4,4)^{\mathsf T}$，$\boldsymbol{u}=(5,4,1,2)^{\mathsf T}$。(1) 求 $\boldsymbol{q}$ 与 $\boldsymbol{u}$ 的余弦相似度；(2) 按方法 6 先去均值再算，会遇到什么情况？用第 3 节的投影说明原因。

### B 进阶

**L2-06**〔B｜方法 2、4 · 考查：只给长度时先平方展开，最短的组合是残差〕已知 $\lVert\boldsymbol{a}\rVert=3$，$\lVert\boldsymbol{b}\rVert=4$，$\lVert\boldsymbol{a}+\boldsymbol{b}\rVert=\sqrt{37}$。(1) 求 $\boldsymbol{a}\cdot\boldsymbol{b}$、$\lVert\boldsymbol{a}-\boldsymbol{b}\rVert$ 以及 $\boldsymbol{a}$ 与 $\boldsymbol{b}$ 的夹角；(2) $t$ 取何值时 $\lVert\boldsymbol{a}+t\boldsymbol{b}\rVert$ 最小？求最小值，并说明这时 $\boldsymbol{a}+t\boldsymbol{b}$ 与 $\boldsymbol{b}$ 是什么关系。

**L2-07**〔B｜方法 3 · 考查：椭圆弧上先检查柯西等号点，再处理端点〕已知 $x^2+4y^2=4$，且 $x\ge1$，$y\ge0$。求 $3x-4y$ 的最大值和最小值，并写出取到的点。

**L2-08**〔B｜方法 1、2 · 考查：实数的哪些运算习惯不能搬到点积上〕（选择）设 $\boldsymbol{a},\boldsymbol{b},\boldsymbol{c}$ 是 $\mathbb{R}^n$ 中的非零向量。下列说法正确的是（　）。

(A) 若 $\boldsymbol{a}\perp\boldsymbol{b}$，$\boldsymbol{b}\perp\boldsymbol{c}$，则 $\boldsymbol{a}\perp\boldsymbol{c}$
(B) 若 $\boldsymbol{a}\cdot\boldsymbol{b}=\boldsymbol{a}\cdot\boldsymbol{c}$，则 $\boldsymbol{b}-\boldsymbol{c}$ 与 $\boldsymbol{a}$ 共线
(C) 若 $\lVert\boldsymbol{a}+\boldsymbol{b}\rVert=\lVert\boldsymbol{a}-\boldsymbol{b}\rVert$，则 $\boldsymbol{a}\perp\boldsymbol{b}$
(D) 若 $|\boldsymbol{a}\cdot\boldsymbol{b}|=\lVert\boldsymbol{a}\rVert\lVert\boldsymbol{b}\rVert$，则 $\boldsymbol{a}$ 与 $\boldsymbol{b}$ 同向

**L2-09**〔B｜方法 6 · 考查：直接余弦被整体打分水平主导〕网站要给新用户小冯找口味相近的用户。小冯、小孙、小何给四部电影（科幻、动作、爱情、文艺）的打分是 $\boldsymbol{r}=(4,3,4,5)^{\mathsf T}$、$\boldsymbol{s}=(2,1,4,5)^{\mathsf T}$、$\boldsymbol{h}=(5,4,3,4)^{\mathsf T}$。(1) 直接用余弦相似度，小冯和谁更像？(2) 按方法 6 先去均值，结论如何？(3) 把每个打分向量写成「平均分 $\times\boldsymbol{1}$ + 残差」，用点积的展开解释 (1) 里小何的余弦为什么更高。

### C 提高

**L2-10**〔C｜方法 5 · 考查：同侧两点到平面上一点的距离之和〕设平面 $\pi$：$x+y+z=3$，点 $P(3,0,3)$、$R(0,3,3)$。(1) 判断 $P$、$R$ 在 $\pi$ 的同侧还是异侧；(2) 求 $P$ 关于 $\pi$ 的对称点 $P^*$（$PP^*$ 的中点是 $P$ 到 $\pi$ 的垂足），并证明 $\pi$ 上任一点 $\boldsymbol{x}$ 都满足 $\lVert\boldsymbol{x}-P\rVert=\lVert\boldsymbol{x}-P^*\rVert$；(3) 求 $\pi$ 上使 $\lVert\boldsymbol{x}-P\rVert+\lVert\boldsymbol{x}-R\rVert$ 最小的点和最小值。

拆法：先做例 8 后的练习（垂足）；(2) 仿照第 4 节「垂足最近」的勾股论证；(3) 用第 2 节三角不等式的等号条件。

**L2-11**〔C｜方法 2、6 · 考查：余弦与欧氏距离两种排序的关系〕检索系统里，四个分量是四个词出现的次数。非零查询 $\boldsymbol{q}=(1,1,0,0)^{\mathsf T}$，文档 $\boldsymbol{d}_1=(4,0,0,0)^{\mathsf T}$、$\boldsymbol{d}_2=(1,1,1,0)^{\mathsf T}$、$\boldsymbol{d}_3=(3,3,0,0)^{\mathsf T}$。(1) 按余弦相似度从大到小给三篇文档排序；(2) 设 $\boldsymbol{q},\boldsymbol{d}$ 非零，夹角为 $\theta$，证明 $\lVert\boldsymbol{q}-\boldsymbol{d}\rVert^2=\lVert\boldsymbol{q}\rVert^2+\lVert\boldsymbol{d}\rVert^2-2\lVert\boldsymbol{q}\rVert\lVert\boldsymbol{d}\rVert\cos\theta$；(3) 证明：如果所有文档的长度相同，那么按欧氏距离从小到大的排序与按余弦从大到小的排序一致，而且查询向量是否单位化不影响这个结论。再说明文档长度不同时为什么可能不一致，并用本题数据给出反例。

拆法：先做 L2-02（夹角公式）、L2-06（只给长度时平方展开）、L2-09（直接余弦的偏差）。

### 章末混合练习

**L2-12**〔B〕设 $\boldsymbol{b}=(b_1,\dots,b_n)^{\mathsf T}$，平均数 $\bar b=\frac1n(b_1+\cdots+b_n)$，$\boldsymbol{1}$ 是 $n$ 维全 1 向量。(1) 证明 $(b_1+\cdots+b_n)^2\le n(b_1^2+\cdots+b_n^2)$，并写出等号成立的条件；(2) 把 $\boldsymbol{b}$ 投影到 $\boldsymbol{1}$ 上，用勾股定理再证一次，并说明差 $\lVert\boldsymbol{b}\rVert^2-n\bar b^2$ 等于什么；(3) 设 $c_1,\dots,c_n$ 是一组凸组合的权重（非负、和为 1），证明 $c_1^2+\cdots+c_n^2\ge\frac1n$，指出何时取等，并说明证明中有没有用到「非负」。

**L2-13**〔B〕设 $\boldsymbol{a}_1=(1,0,1)^{\mathsf T}$，$\boldsymbol{a}_2=(0,1,1)^{\mathsf T}$。(1) 证明：若 $\boldsymbol{b}$ 与 $\boldsymbol{a}_1$、$\boldsymbol{a}_2$ 都正交，则 $\boldsymbol{b}$ 与 $\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)$ 中每个向量都正交；若 $\boldsymbol{b}$ 还属于 $\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)$，则 $\boldsymbol{b}=\boldsymbol{0}$；(2) 若 $\boldsymbol{b}$ 只与 $\boldsymbol{a}_1+\boldsymbol{a}_2$ 正交，能否推出 $\boldsymbol{b}$ 与 $\boldsymbol{a}_1$、$\boldsymbol{a}_2$ 都正交？举例说明；(3) 求一个与 $\boldsymbol{a}_1$、$\boldsymbol{a}_2$ 都正交的非零向量 $\boldsymbol{n}$，写出平面 $\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)$ 的方程，并用它判断 $(2,3,4)^{\mathsf T}$ 是否属于这个张成。

**L2-14**〔C〕设 $\boldsymbol{p}_1=(40,10)^{\mathsf T}$，$\boldsymbol{p}_2=(10,40)^{\mathsf T}$，线段 $\boldsymbol{p}_1\boldsymbol{p}_2$ 上的点是 $\boldsymbol{p}_1+s(\boldsymbol{p}_2-\boldsymbol{p}_1)$，$0\le s\le1$，也就是 $\boldsymbol{p}_1,\boldsymbol{p}_2$ 的凸组合（L.1 第 4 节）。(1) 写出过 $\boldsymbol{p}_1$、$\boldsymbol{p}_2$ 的直线方程；(2) $\boldsymbol{g}=(35,35)^{\mathsf T}$ 时，求线段上离 $\boldsymbol{g}$ 最近的点（$s$ 的值）和距离；(3) $\boldsymbol{g}=(55,15)^{\mathsf T}$ 时，同样求最近的点和距离。

拆法：先做例 8（垂足）；(3) 仿照第 4 节「垂足最近」的勾股论证，再想想 L1-05（凸组合的系数非负）。
