## C.25 · 二重积分（答案）

### A 基础

**C25-01**
**答案：** (B)。在 $D$ 上令 $r=\sqrt{x^2+y^2}$，则 $0\le r\le1$，所以 $r^2\le r$，积分后得 $I\le K$；除边界和原点外不等号严格成立，故 $I<K$。 (A) 把不等号方向看反；(C) 把点上不等误当成积分相等；(D) 忽略了区域给出的 $r$ 范围。

区分点：要先在给定区域上比较 $r^2$ 与 $r$，不能只看两个函数的形式。

**C25-02**
**答案：** $3$。被积函数连续，圆盘半径趋于 0 时平均值趋于中心 $(1,-2)$ 处的函数值：
$$1^2+1(-2)+(-2)^2=3.$$

区分点：平均值前的面积因子已经除掉，极限取的是中心处函数值，不是积分本身。

**C25-03**
**答案：** $1$。矩形上是乘积，故
$$\iint x\sin y\,\mathrm d\sigma=\left(\int_0^1x\,\mathrm dx\right)\left(\int_0^\pi\sin y\,\mathrm dy\right)=\frac12\cdot2=1.$$

区分点：里层积分时把另一个变量当常数，或直接识别乘积结构，都不能漏掉另一层的因子。

**C25-04**
**答案：** $\displaystyle\frac73$。竖直线穿过三角形时 $0\le x\le1$，下限 $y=x$，上限 $y=2-x$。里层积分为
$$x(2-2x)+\big[(2-x)^2-x^2\big]=4-2x-2x^2,$$
所以
$$\int_0^1(4-2x-2x^2)\,\mathrm dx=4-1-\frac23=\frac73.$$

区分点：先画出交点 $(0,0),(0,2),(1,1)$，再写上下限；里层的 $2y$ 积分不能把边界代入时漏掉平方。

### B 进阶

**C25-05**
**答案：** (B)。原区域满足 $0\le x\le1,\ x^2\le y\le2-x$，所以 $0\le y\le2$。水平线穿过区域时，右端同时受 $x\le\sqrt y$ 和 $x\le2-y$ 限制；两条边界在 $(1,1)$ 相交。

当 $0\le y\le1$ 时，$0\le x\le\sqrt y$；当 $1\le y\le2$ 时，$0\le x\le2-y$，因此两块积分相加，得到 (B)。(A) 漏掉 $y>1$ 的部分；(C) 把 $y=x^2$ 反解成了 $x=y^2$；(D) 漏掉 $y<1$ 的部分。

区分点：交换的是穿线方向，必须从不等式重新画区域，不能把上下限符号直接对调。

**C25-06**
**答案：** (A)。区域关于 $(1,1)$ 中心对称：把 $(x,y)$ 换成 $(2-x,2-y)$，仍有 $0\le x\le2$ 和 $|y-x|\le1$。这对点的 $x+y-2$ 互为相反数，面积不变，所以 (A) 的积分为 $0$。

(B) 的 $x$ 虽对 $x$ 是奇函数，区域却不关于 $y$ 轴对称，且内部 $x>0$，积分为正。(C) 的 $xy$ 虽分别对 $x,y$ 为奇函数，也不能消掉：
$$\int_0^2x\,\mathrm dx\int_{x-1}^{x+1}y\,\mathrm dy=\int_0^2 2x^2\,\mathrm dx=\frac{16}3.$$
(D) 的 $x^2$ 在内部为正，积分也不为零。

区分点：对称中心不在原点时，要检查成对位置的函数值，不能看见奇函数就判积分为零。

**C25-07**
**答案：** (C)。$1\le r^2\le9$ 给出 $1\le r\le3$；$y\ge|x|$ 是两条射线 $y=x$、$y=-x$ 之间的上方区域，所以 $\pi/4\le\theta\le3\pi/4$。被积函数为 $r$，面积元再乘 $r$，合为 $r^2\,\mathrm dr\,\mathrm d\theta$。(A) 把内半径改成 $0$，填上了原来挖去的部分；(B) 把半径平方的上界 $9$ 当成半径；(D) 把角度范围扩大成了整个上半平面。

区分点：上限、角度范围、面积元三处都要由图和 $r\,\mathrm dr\,\mathrm d\theta$ 一起确定。

**C25-08**
**答案：** $J=-\frac13$，积分为 $\frac13$。由 $v=x-y$ 得 $y=x-v$，代入 $u=2x+y$，反解为 $x=(u+v)/3,\ y=(u-2v)/3$，所以
$$J=\begin{vmatrix}1/3&1/3\\1/3&-2/3\end{vmatrix}=-\frac13.$$
新区域是 $0\le u\le2,\ 0\le v\le1$，被积函数变成 $uv$，面积元乘 $|J|=1/3$。因此
$$\iint_D(2x+y)(x-y)\,\mathrm d\sigma=\frac13\int_0^2u\,\mathrm du\int_0^1v\,\mathrm dv=\frac13\cdot2\cdot\frac12=\frac13.$$

区分点：换元必须同时改被积函数、区域和面积元，三者少一项都会改变结果。

**C25-09**
**答案：** 当且仅当 $p>1$ 时收敛，$I(p)=\pi/(p-1)$，特别地 $I(3/2)=2\pi$；$p\le1$ 时积分趋于 $+\infty$。

先截到外半径 $R>1$。面积元带入因子 $r$，因此
$$I_R(p)=2\pi\int_1^Rr^{1-2p}\,\mathrm dr=
\begin{cases}\displaystyle\frac{\pi}{1-p}(R^{2-2p}-1),&p\ne1,\\2\pi\ln R,&p=1.\end{cases}$$
$p>1$ 时，$R^{2-2p}\to0$；$p<1$ 时，幂次为正且 $\pi/(1-p)>0$，所以趋于 $+\infty$；$p=1$ 时则对数发散。

区分点：收敛条件由乘上面积元后的幂次决定，还要单独检查不能代入幂函数原函数的 $p=1$。

**C25-10**
**答案：** $\Phi'(1)=\mathrm e+1$；只对被积函数求导会漏掉上限移动产生的 $\mathrm e^{t^2}$，在 $t=1$ 处少算 $\mathrm e$。

取 $1/2\le t\le3/2,\ 0\le x\le3/2$，被积函数 $\mathrm e^{tx}$ 及其对 $t$ 的偏导数 $x\mathrm e^{tx}$ 都连续，上下限 $t,0$ 也可导，因而可以用三项公式：
$$\Phi'(t)=\int_0^t x\mathrm e^{tx}\,\mathrm dx+\mathrm e^{t^2}.$$
下限固定，第三项为 $0$。在 $t=1$ 时，用分部积分补出第一项：
$$\int_0^1x\mathrm e^x\,\mathrm dx=[x\mathrm e^x]_0^1-\int_0^1\mathrm e^x\,\mathrm dx=\mathrm e-(\mathrm e-1)=1.$$
加上上限项得 $\Phi'(1)=1+\mathrm e$。

区分点：不能只对被积函数求偏导，还要加上限处函数值乘上限导数。

**C25-11**
**答案：** 恒等式成立。原式对应三角形 $0\le y\le x\le a$。交换穿线方向后，固定 $y$ 时 $y\le x\le a$，且 $0\le y\le a$，故
$$\int_0^a\mathrm dx\int_0^x f(y)\,\mathrm dy
=\int_0^a\mathrm dy\int_y^a f(y)\,\mathrm dx
=\int_0^a(a-y)f(y)\,\mathrm dy.$$

区分点：证明的关键是把积分限还原成区域；只写“由交换次序”而不说明新区域，论证是不完整的。

### C 提高

**C25-12**
**答案：** $\displaystyle\frac23-\frac\pi8$，在 $\theta=\pi/4$ 处分段。

区域在第一象限，射线先从圆 $r=1$ 进入，再从正方形的边离开。$0\le\theta\le\pi/4$ 时先碰到 $x=1$，所以 $1\le r\le1/\cos\theta$；$\pi/4\le\theta\le\pi/2$ 时先碰到 $y=1$，所以 $1\le r\le1/\sin\theta$。两条外边界在 $(1,1)$ 相交，对应分界角 $\pi/4$。

被积函数乘上面积元后是 $r^3$，故
$$I=\int_0^{\pi/4}\mathrm d\theta\int_1^{1/\cos\theta}r^3\,\mathrm dr+\int_{\pi/4}^{\pi/2}\mathrm d\theta\int_1^{1/\sin\theta}r^3\,\mathrm dr.$$
第二项用 $\theta=\pi/2-\alpha$ 换元，与第一项相等，于是
$$I=\frac12\int_0^{\pi/4}\left(\frac1{\cos^4\theta}-1\right)\mathrm d\theta.$$
令 $w=\tan\theta$，则 $\mathrm dw=\mathrm d\theta/\cos^2\theta$ 且 $1/\cos^2\theta=1+w^2$，所以
$$\int_0^{\pi/4}\frac{\mathrm d\theta}{\cos^4\theta}=\int_0^1(1+w^2)\,\mathrm dw=\frac43,$$
从而 $I=\frac12(\frac43-\frac\pi4)=\frac23-\frac\pi8$。

区分点：原点不在区域内，径向下限为 $1$；射线离开时碰到的边改变，还必须按角度分块。

### 章末混合练习

**C25-13**
**答案：** 最大值为 $\sqrt2$，最小值为 $-\sqrt2$，并且
$$\pi(3-\sqrt2)\le I\le\pi(3+\sqrt2).$$
由前面章节的极值结论，$x+y$ 在单位圆盘边界上的极值点沿方向 $(1,1)$ 和 $(-1,-1)$，函数值分别为 $\pm\sqrt2$；圆盘面积为 $\pi$，再用方法 1 的估值性质即可。

区分点：先求区域上的真实最大、最小值，再乘面积夹住积分；把 $x,y$ 的范围分别相加只能给出较松的界，不能替代所求的极值。

**C25-14**
**答案：** $1$。函数在 $(0,0)$ 处的定义使它连续，因为 $\sin u/u\to1$。由方法 2，小圆盘平均值趋于中心处函数值 $f(0,0)=1$。

区分点：要先确认可去间断已经补成连续函数，才能使用平均值极限。

**C25-15**
**答案：** $\displaystyle\frac{\pi}{2}$。底面投影是单位圆盘 $D:x^2+y^2\le1$，曲面高度为 $1-x^2-y^2$，所以
$$V=\iint_D(1-x^2-y^2)\,\mathrm d\sigma
=\int_0^{2\pi}\mathrm d\theta\int_0^1(1-r^2)r\,\mathrm dr
=2\pi\left(\frac12-\frac14\right)=\frac\pi2.$$
（方法 7；底面和体积的思想用到前面章节的截面法。）

区分点：先确定投影区域和高度的非负范围，再把立体体积写成二重积分；不能把曲面公式直接当成体积。

