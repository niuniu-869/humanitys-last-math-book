## C.25 · 二重积分（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| C25-01 | A | 方法 1 |
| C25-02 | A | 方法 2 |
| C25-03 | A | 方法 3 |
| C25-04 | A | 方法 4 |
| C25-05 | B | 方法 5 |
| C25-06 | B | 方法 6 |
| C25-07 | B | 方法 7 |
| C25-08 | B | 方法 9 |
| C25-09 | B | 方法 8 |
| C25-10 | B | 方法 10 |
| C25-11 | B | 方法 5 |
| C25-12 | C | 方法 7 |
| C25-13 | B | 章末混合 |
| C25-14 | B | 章末混合 |
| C25-15 | C | 章末混合 |

### A 基础

**C25-01**〔A｜方法 1 · 考查：在同一块区域上比较被积函数〕设
$$D=\{(x,y):x^2+y^2\le1\},\quad I=\iint_D(x^2+y^2)\,\mathrm d\sigma,\quad K=\iint_D\sqrt{x^2+y^2}\,\mathrm d\sigma.$$
下列说法正确的是（　）。

(A) $I>K$　(B) $I<K$　(C) $I=K$　(D) 仅由题目条件不能判断 $I,K$ 的大小

**C25-02**〔A｜方法 2 · 考查：把小圆盘平均值极限换成中心处的函数值〕求
$$\lim_{r\to0^+}\frac1{\pi r^2}\iint_{(x-1)^2+(y+2)^2\le r^2}(x^2+xy+y^2)\,\mathrm d\sigma.$$

**C25-03**〔A｜方法 3 · 考查：矩形区域上的累次积分与乘积结构〕计算
$$\iint_{[0,1]\times[0,\pi]}x\sin y\,\mathrm d\sigma.$$

**C25-04**〔A｜方法 4 · 考查：画出区域后正确确定穿线的上下限〕设 $D$ 由三条直线 $x=0$、$y=x$、$y=2-x$ 围成，计算
$$\iint_D(x+2y)\,\mathrm d\sigma.$$

### B 进阶

**C25-05**〔B｜方法 5 · 考查：换序后在边界改变处把区域分块〕设 $f$ 在 $D=\{(x,y):0\le x\le1,\ x^2\le y\le2-x\}$ 上连续，则对任意这样的 $f$，
$$\int_0^1\mathrm dx\int_{x^2}^{2-x}f(x,y)\,\mathrm dy$$
交换积分次序后等于（　）。

(A) $\displaystyle\int_0^1\mathrm dy\int_0^{\sqrt y}f(x,y)\,\mathrm dx$

(B) $\displaystyle\int_0^1\mathrm dy\int_0^{\sqrt y}f(x,y)\,\mathrm dx+\int_1^2\mathrm dy\int_0^{2-y}f(x,y)\,\mathrm dx$

(C) $\displaystyle\int_0^1\mathrm dy\int_0^{y^2}f(x,y)\,\mathrm dx+\int_1^2\mathrm dy\int_0^{2-y}f(x,y)\,\mathrm dx$

(D) $\displaystyle\int_1^2\mathrm dy\int_0^{2-y}f(x,y)\,\mathrm dx$

**C25-06**〔B｜方法 6 · 考查：同时检查区域对称性和被积函数奇偶性〕设
$$D=\{(x,y):0\le x\le2,\ x-1\le y\le x+1\}.$$
下列积分一定等于 $0$ 的是（　）。

(A) $\displaystyle\iint_D(x+y-2)\,\mathrm d\sigma$

(B) $\displaystyle\iint_Dx\,\mathrm d\sigma$

(C) $\displaystyle\iint_Dxy\,\mathrm d\sigma$

(D) $\displaystyle\iint_Dx^2\,\mathrm d\sigma$

**C25-07**〔B｜方法 7 · 考查：同时确定扇环的内外半径、角度范围和面积元〕设 $D=\{(x,y):1\le x^2+y^2\le9,\ y\ge|x|\}$，则
$$\iint_D\sqrt{x^2+y^2}\,\mathrm d\sigma$$
的正确极坐标表达式是（　）。

(A) $\displaystyle\int_{\pi/4}^{3\pi/4}\mathrm d\theta\int_0^3 r^2\,\mathrm dr$

(B) $\displaystyle\int_{\pi/4}^{3\pi/4}\mathrm d\theta\int_1^9 r^2\,\mathrm dr$

(C) $\displaystyle\int_{\pi/4}^{3\pi/4}\mathrm d\theta\int_1^3 r^2\,\mathrm dr$

(D) $\displaystyle\int_0^\pi\mathrm d\theta\int_1^3 r^2\,\mathrm dr$

**C25-08**〔B｜方法 9 · 考查：换元时同时变换区域、被积函数和面积元〕设平行四边形
$$D=\{(x,y):0\le2x+y\le2,\ 0\le x-y\le1\}.$$
令 $u=2x+y,\ v=x-y$，求 $J=\dfrac{\partial(x,y)}{\partial(u,v)}$，并计算
$$\iint_D(2x+y)(x-y)\,\mathrm d\sigma.$$

**C25-09**〔B｜方法 8 · 考查：参数如何影响无界区域上的积分收敛性〕设 $p$ 为实数，判断
$$I(p)=\iint_{x^2+y^2\ge1}\frac1{(x^2+y^2)^p}\,\mathrm d\sigma$$
在什么条件下收敛；收敛时求 $I(p)$，并算出 $I(3/2)$。发散时说明积分趋于什么。

**C25-10**〔B｜方法 10 · 考查：积分限含参数时的三项求导公式〕设
$$\Phi(t)=\int_0^t\mathrm e^{tx}\,\mathrm dx,$$
求 $\Phi'(1)$，说明求导公式所需的连续性条件在 $t=1$ 附近为何成立，并指出只对被积函数求导会漏掉哪一项。

**C25-11**〔B｜方法 5 · 考查：用区域互换证明一个累次积分恒等式〕设 $f$ 在 $[0,a]$ 上连续，且 $a>0$。证明
$$\int_0^a\mathrm dx\int_0^x f(y)\,\mathrm dy=\int_0^a(a-y)f(y)\,\mathrm dy.$$

### C 提高

**C25-12**〔C｜方法 7 · 考查：极坐标中径向上限随角度分段改变〕用极坐标计算
$$\iint_D(x^2+y^2)\,\mathrm d\sigma,\qquad D=\{(x,y):0\le x\le1,\ 0\le y\le1,\ x^2+y^2\ge1\},$$
并说明角度的分段位置以及每段的径向上下限。

拆法：先做 C25-05、C25-07

### 章末混合练习

**C25-13**〔B〕设 $D=\{(x,y):x^2+y^2\le1\}$。利用前面章节的极值结论，先求 $x+y$ 在 $D$ 上的最大值和最小值，再给出
$$I=\iint_D(3+x+y)\,\mathrm d\sigma$$
的上下界。

**C25-14**〔B〕设
$$f(x,y)=\begin{cases}\dfrac{\sin(xy)}{xy},&xy\ne0,\\1,&xy=0.\end{cases}$$
求
$$\lim_{r\to0^+}\frac1{\pi r^2}\iint_{x^2+y^2\le r^2}f(x,y)\,\mathrm d\sigma.$$

**C25-15**〔C〕求曲面 $z=1-x^2-y^2$ 与 $z=0$ 围成的立体体积（取有界部分），并说明所用的二重积分区域和被积函数分别是什么。

拆法：先做 C25-04、C25-07
