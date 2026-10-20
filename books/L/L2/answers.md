## L.2 · 点积、长度、夹角与投影（答案）

### A 基础

**L2-01**
**答案：** (D)。

$\boldsymbol{a}\cdot\boldsymbol{b}=k+2>0$，即 $k>-2$；还要排除同向：$(k,1)=\lambda(1,2)$ 且 $\lambda>0$ 时 $\lambda=\frac12$，$k=\frac12$，夹角为 0，所以选 (D)。(A) 漏掉了同向的 $k=\frac12$；(B) 把 $k=-2$ 也算进来，这时点积为 0，是直角；(C) 把共线条件交叉相乘写反了（$1\cdot k-2\cdot1=0$），排除的 $k=2$ 并不同向，$(2,1)$ 与 $(1,2)$ 的余弦是 $\frac45$，是锐角。

区分点：巩固「点积为正只说明 $0\le\theta<\frac{\pi}{2}$，锐角还要排除同向」，共线条件要列对。

**L2-02**
**答案：** $k=-1$。

$\cos\frac{2\pi}{3}=\frac{k}{\sqrt{k^2+1}\cdot\sqrt2}=-\frac12$，分子 $k$ 必须为负。两边平方：$\frac{k^2}{2(k^2+1)}=\frac14$，$k^2=1$，$k=\pm1$。$k=1$ 时余弦是 $+\frac12$，夹角是 $\frac{\pi}{3}$，是平方时混进来的根，舍去；$k=-1$ 时余弦 $\frac{-1}{\sqrt2\cdot\sqrt2}=-\frac12$，符合。

区分点：平方会把余弦为 $+\frac12$ 的根一起带进来，要先记下 $k<0$，或把两个根逐个代回。

**L2-03**
**答案：** $x=1$，$\boldsymbol{e}=(-1,0,1)^{\mathsf T}$；2 是 $\boldsymbol{b}$ 三个分量的平均数。

由投影系数 $t=\frac{x+2+3}{3}=2$ 得 $x=1$，于是 $\boldsymbol{e}=(1,2,3)^{\mathsf T}-(2,2,2)^{\mathsf T}=(-1,0,1)^{\mathsf T}$，验算 $\boldsymbol{e}\cdot(1,1,1)^{\mathsf T}=0$。投影到全 1 方向的系数是「分量之和 ÷ 个数」，即平均数。

区分点：巩固投影系数 $t=\frac{\boldsymbol{a}\cdot\boldsymbol{b}}{\boldsymbol{a}\cdot\boldsymbol{a}}$，以及「投影到全 1 方向 = 平均数」。

**L2-04**
**答案：** (D)。

新系数 $\frac{(-2\boldsymbol{a})\cdot\boldsymbol{b}}{4\,\boldsymbol{a}\cdot\boldsymbol{a}}=-\frac t2$；投影 $-\frac t2(-2\boldsymbol{a})=\boldsymbol{p}$，残差也不变，(D) 对，(A)(B) 错。带符号长度 $\frac{-2\,\boldsymbol{a}\cdot\boldsymbol{b}}{2\lVert\boldsymbol{a}\rVert}=-\ell$ 变了号，(C) 错；换成 $2\boldsymbol{a}$ 时它才不变。

区分点：投影只取决于直线；$t$ 随 $\boldsymbol{a}$ 的长度和方向变，带符号长度随方向变号。

**L2-05**
**答案：** (1) $\frac{6}{\sqrt{46}}\approx0.885$；(2) 去均值后是零向量，余弦没有定义。

(1) $\boldsymbol{q}\cdot\boldsymbol{u}=4\times12=48$，$\lVert\boldsymbol{q}\rVert=8$，余弦 $\frac{48}{8\sqrt{46}}=\frac{6}{\sqrt{46}}$。(2) $\boldsymbol{q}-4\cdot\boldsymbol{1}=\boldsymbol{0}$，分母为 0：$\boldsymbol{q}=4\cdot\boldsymbol{1}$ 在 $\boldsymbol{1}$ 上的投影就是它自己，残差为零。

区分点：巩固「余弦只对非零向量有定义」，直接余弦里含沿 $\boldsymbol{1}$ 的整体水平。

### B 进阶

**L2-06**
**答案：** (1) $6$，$\sqrt{13}$，$\frac{\pi}{3}$；(2) $t=-\frac38$，最小值 $\frac{3\sqrt3}{2}$，此时 $\boldsymbol{a}+t\boldsymbol{b}\perp\boldsymbol{b}$。

方法 2：$37=\lVert\boldsymbol{a}+\boldsymbol{b}\rVert^2=9+2\,\boldsymbol{a}\cdot\boldsymbol{b}+16$，得 $\boldsymbol{a}\cdot\boldsymbol{b}=6$；$\lVert\boldsymbol{a}-\boldsymbol{b}\rVert^2=9-12+16=13$；$\cos\theta=\frac{6}{12}=\frac12$。

(2) $\lVert\boldsymbol{a}+t\boldsymbol{b}\rVert^2=16t^2+12t+9=16(t+\frac38)^2+\frac{27}{4}$，$t=-\frac38$ 时最小，最小值 $\frac{3\sqrt3}{2}$，这时 $\boldsymbol{b}\cdot(\boldsymbol{a}+t\boldsymbol{b})=6+16t=0$。用方法 4 看，$\frac{\boldsymbol{a}\cdot\boldsymbol{b}}{\boldsymbol{b}\cdot\boldsymbol{b}}=\frac38$，$\boldsymbol{a}-\frac38\boldsymbol{b}$ 正是 $\boldsymbol{a}$ 在 $\boldsymbol{b}$ 上的残差，由勾股定理其长度平方为 $9-\frac{36}{16}=\frac{27}{4}$。

区分点：没有分量时长度要先平方再展开；(2) 要认出最短的 $\boldsymbol{a}+t\boldsymbol{b}$ 就是残差，它与 $\boldsymbol{b}$ 正交。

**L2-07**
**答案：** 最大值 $6$，在 $(2,0)$ 取到；最小值 $3-2\sqrt3$，在 $(1,\frac{\sqrt3}{2})$ 取到。

令 $\boldsymbol{z}=(x,2y)^{\mathsf T}$，则 $\lVert\boldsymbol{z}\rVert=2$，且 $3x-4y=(3,-2)\cdot\boldsymbol{z}$。柯西–施瓦茨给出 $|3x-4y|\le2\sqrt{13}$。等号要求 $\boldsymbol{z}$ 与 $(3,-2)^{\mathsf T}$ 同向或反向；同向时 $y<0$，反向时 $x<0$，两个等号点都不满足题设条件，所以要检查可行弧的端点。

参数化 $x=2\cos\theta$、$y=\sin\theta$。条件 $x\ge1$ 给出 $0\le\theta\le\frac{\pi}{3}$，而 $y\ge0$ 已包含在这个区间内。于是

$$3x-4y=6\cos\theta-4\sin\theta.$$

其导数为 $-6\sin\theta-4\cos\theta<0$，所以函数在可行区间递减。两端分别给出

$$f(0)=6,\qquad f\left(\frac{\pi}{3}\right)=3-2\sqrt3.$$

区分点：柯西–施瓦茨给出的界只有在等号点可行时才能取到；等号点被条件排除后，要把可行弧的端点完整检查一遍。

**L2-08**
**答案：** (C)。

$\lVert\boldsymbol{a}+\boldsymbol{b}\rVert^2-\lVert\boldsymbol{a}-\boldsymbol{b}\rVert^2=4\,\boldsymbol{a}\cdot\boldsymbol{b}$，两长度相等即 $\boldsymbol{a}\cdot\boldsymbol{b}=0$，(C) 对。
(A) 误以为垂直可以传递：$\boldsymbol{a}=\boldsymbol{c}=(1,0)^{\mathsf T}$，$\boldsymbol{b}=(0,1)^{\mathsf T}$，$\boldsymbol{a}\perp\boldsymbol{b}$，$\boldsymbol{b}\perp\boldsymbol{c}$，但 $\boldsymbol{a}\cdot\boldsymbol{c}=1$。
(B) 把正交当成共线：等式只说明 $\boldsymbol{a}\perp(\boldsymbol{b}-\boldsymbol{c})$。如 $\boldsymbol{a}=(1,0)^{\mathsf T}$，$\boldsymbol{b}=(0,1)^{\mathsf T}$，$\boldsymbol{c}=(0,5)^{\mathsf T}$，$\boldsymbol{b}-\boldsymbol{c}=(0,-4)^{\mathsf T}$ 与 $\boldsymbol{a}$ 不共线。
(D) 漏掉了反向：$\boldsymbol{b}=-2\boldsymbol{a}$ 时等号成立（两边都是 $2\lVert\boldsymbol{a}\rVert^2$），但两者反向。

区分点：(C) 要把两个长度平方后展开相减；(A)(B)(D) 是「垂直可传递」「正交当成共线」「共线只想到同向」三种误解，会的人各能举出反例。

**L2-09**
**答案：** (1) 小何；(2) 小孙，与小何的余弦为 0；(3) 见下。

(1) 点积 52、64，$\lVert\boldsymbol{r}\rVert=\lVert\boldsymbol{h}\rVert=\sqrt{66}$，$\lVert\boldsymbol{s}\rVert=\sqrt{46}$，余弦为 $\frac{52}{\sqrt{3036}}\approx0.944$、$\frac{64}{66}\approx0.970$。

(2) 平均分依次为 4、3、4，残差 $\boldsymbol{r}'=(0,-1,0,1)^{\mathsf T}$，$\boldsymbol{s}'=(-1,-2,1,2)^{\mathsf T}$，$\boldsymbol{h}'=(1,0,-1,0)^{\mathsf T}$，余弦为 $\frac{4}{\sqrt{20}}\approx0.894$ 和 0：小冯和小孙都偏爱文艺、不喜欢动作。

(3) 设每个向量都写成“平均分 $\times\boldsymbol{1}$ + 残差”。残差与 $\boldsymbol{1}$ 正交，所以交叉项为 0。

点积部分：

$$\boldsymbol{r}\cdot\boldsymbol{h}=4\cdot4\cdot4+\boldsymbol{r}'\cdot\boldsymbol{h}'=64+0=64,$$
$$\boldsymbol{r}\cdot\boldsymbol{s}=4\cdot3\cdot4+\boldsymbol{r}'\cdot\boldsymbol{s}'=48+4=52.$$

长度平方部分：

$$\lVert\boldsymbol{r}\rVert^2=4^2\cdot4+\lVert\boldsymbol{r}'\rVert^2=64+2,$$
$$\lVert\boldsymbol{h}\rVert^2=64+2,\qquad \lVert\boldsymbol{s}\rVert^2=3^2\cdot4+10=36+10.$$

因此，小冯和小何的整体打分水平都贡献了平方长度中的 $64/66$，余弦接近 1；小孙的残差平方长度为 10，且与小冯的残差点积只有 4，所以余弦更低。

区分点：要看出直接余弦里整体打分水平占大头，并用正交分解把点积和长度都拆成两份，解释排序为什么反转。

### C 提高

**L2-10**
**答案：** (1) 同侧；(2) $P^*=(1,-2,1)$；(3) 最小值 $\sqrt{30}$，在 $(\frac12,\frac12,2)$ 取到。

(1) 法向量 $\boldsymbol{n}=(1,1,1)^{\mathsf T}$，$\boldsymbol{n}\cdot P-3=3>0$，$\boldsymbol{n}\cdot R-3=3>0$，两点都在 $\boldsymbol{n}$ 所指的一侧。

(2) 方法 5：$t=\frac{6-3}{3}=1$，垂足 $F=(3,0,3)-(1,1,1)=(2,-1,2)$，代回 $2-1+2=3$。$F$ 是中点，$P^*=2F-P=(1,-2,1)$，$\boldsymbol{n}\cdot P^*-3=-3$，在另一侧。对 $\pi$ 上任一点 $\boldsymbol{x}$：

1. $\boldsymbol{n}\cdot(\boldsymbol{x}-F)=3-3=0$，而 $F-P=-\boldsymbol{n}$，所以 $\boldsymbol{x}-F\perp F-P$。
2. $\boldsymbol{x}-P=(\boldsymbol{x}-F)+(F-P)$，$\boldsymbol{x}-P^*=(\boldsymbol{x}-F)-(F-P)$。
3. 由勾股定理，两者长度的平方都是 $\lVert\boldsymbol{x}-F\rVert^2+\lVert F-P\rVert^2$，所以 $\lVert\boldsymbol{x}-P\rVert=\lVert\boldsymbol{x}-P^*\rVert$。

(3) 对 $\pi$ 上的 $\boldsymbol{x}$，由 (2) 和三角不等式，
$$\lVert\boldsymbol{x}-P\rVert+\lVert\boldsymbol{x}-R\rVert=\lVert\boldsymbol{x}-P^*\rVert+\lVert R-\boldsymbol{x}\rVert\ge\lVert R-P^*\rVert=\lVert(-1,5,2)^{\mathsf T}\rVert=\sqrt{30}.$$
等号当且仅当 $\boldsymbol{x}-P^*$ 与 $R-\boldsymbol{x}$ 同向，即其中一个向量是另一个向量的非负倍数，且 $\boldsymbol{x}$ 在线段 $P^*R$ 上。$P^*$、$R$ 在 $\pi$ 两侧（$-3$ 和 $3$），线段 $P^*+s(R-P^*)=(1-s,-2+5s,1+2s)$ 代入平面方程得 $6s=3$，$s=\frac12$，交点 $(\frac12,\frac12,2)$ 取到下界，最小值 $\sqrt{30}$。

区分点：$R-P=(-3,3,0)$ 与 $\boldsymbol{n}$ 正交，直线 $PR$ 和 $\pi$ 平行，直接连线找交点走不通；要先把 $P$ 反射到另一侧，再用三角不等式的等号条件定点。

**L2-11**
**答案：** (1) $\boldsymbol{d}_3>\boldsymbol{d}_2>\boldsymbol{d}_1$；(2) 见下；(3) 只单位化文档时一致，都不单位化时不一致。

(1) 与三篇的点积依次为 4、2、6，$\lVert\boldsymbol{q}\rVert=\sqrt2$，余弦依次为 $\frac{4}{4\sqrt2}\approx0.707$、$\frac{2}{\sqrt2\sqrt3}\approx0.816$、$\frac{6}{\sqrt2\cdot3\sqrt2}=1$。按点积 $\boldsymbol{d}_1$ 会排在 $\boldsymbol{d}_2$ 前，只因为它长。

(2) 展开长度平方：

$$\lVert\boldsymbol{q}-\boldsymbol{d}\rVert^2=\lVert\boldsymbol{q}\rVert^2-2\boldsymbol{q}\cdot\boldsymbol{d}+\lVert\boldsymbol{d}\rVert^2.$$ 

再用夹角定义 $\boldsymbol{q}\cdot\boldsymbol{d}=\lVert\boldsymbol{q}\rVert\lVert\boldsymbol{d}\rVert\cos\theta$，得到题中的等式。

(3) 若所有文档长度都是同一个 $L$，则

$$\lVert\boldsymbol{q}-\boldsymbol{d}\rVert^2=\lVert\boldsymbol{q}\rVert^2+L^2-2\lVert\boldsymbol{q}\rVert L\cos\theta.$$ 

对固定的非零查询向量，前两项和正的系数都相同，所以余弦越大，距离平方越小；查询向量是否单位化只会同时改变这些公共量，不改变排序。

本题只把文档单位化时，三篇文档长度都为 1，距离平方依次为 $1$、$3-\frac{4}{\sqrt3}\approx0.691$、$3-2\sqrt2\approx0.172$，排序为 $\boldsymbol{d}_3,\boldsymbol{d}_2,\boldsymbol{d}_1$，与余弦排序一致。三篇文档都不单位化时，距离平方依次为 $10$、$1$、$8$，排序为 $\boldsymbol{d}_2,\boldsymbol{d}_3,\boldsymbol{d}_1$，与余弦排序不一致。

区分点：要从 (2) 看出距离排序只差在 $\lVert\boldsymbol{d}\rVert$ 上，文档长度相同就和余弦一致，与查询长度无关；不单位化时要能用本题数据举出反例。

### 章末混合练习

**L2-12**
**答案：** 方法 3 里的柯西–施瓦茨、方法 4，L.1 第 4 节的凸组合；等号都在各分量相等时取到；(2) 的差是离差平方和；(3) 没有用到非负。

(1) $(b_1+\cdots+b_n)^2=(\boldsymbol{1}\cdot\boldsymbol{b})^2\le\lVert\boldsymbol{1}\rVert^2\lVert\boldsymbol{b}\rVert^2=n(b_1^2+\cdots+b_n^2)$。$\boldsymbol{1}\ne\boldsymbol{0}$，等号当且仅当 $\boldsymbol{b}$ 是 $\boldsymbol{1}$ 的倍数，即 $b_1=\cdots=b_n$。

(2) $t=\frac{\boldsymbol{1}\cdot\boldsymbol{b}}{n}=\bar b$，残差 $\boldsymbol{e}=\boldsymbol{b}-\bar b\,\boldsymbol{1}\perp\boldsymbol{1}$，由勾股定理 $\lVert\boldsymbol{b}\rVert^2=n\bar b^2+\lVert\boldsymbol{e}\rVert^2\ge n\bar b^2$，乘以 $n$ 就是 (1)。差 $\lVert\boldsymbol{e}\rVert^2=\sum(b_i-\bar b)^2$ 是离差平方和，为 0 当且仅当各分量相等。

(3) 对 $(c_1,\dots,c_n)^{\mathsf T}$ 用 (1)：$1\le n(c_1^2+\cdots+c_n^2)$，所以平方和 $\ge\frac1n$，等号要各 $c_i$ 相等，即都等于 $\frac1n$。只用了和为 1：$(2,-1)$ 的平方和 5 也不小于 $\frac12$。

区分点：等号条件要写成「各分量相等，即与 $\boldsymbol{1}$ 共线」，只写「共线」不够；要认出两种证法是同一件事，差值就是离差平方和；(3) 要看出只用到和为 1。

**L2-13**
**答案：** L.1 例 3，方法 1、5；(2) 不能；(3) $\boldsymbol{n}=(1,1,-1)^{\mathsf T}$，平面 $x+y-z=0$，$(2,3,4)^{\mathsf T}$ 不属于这个张成。

(1) 张成里的向量都是 $\alpha\boldsymbol{a}_1+\beta\boldsymbol{a}_2$，由分配律它与 $\boldsymbol{b}$ 的点积为 $\alpha(\boldsymbol{b}\cdot\boldsymbol{a}_1)+\beta(\boldsymbol{b}\cdot\boldsymbol{a}_2)=0$。若 $\boldsymbol{b}$ 也在张成里，就和自己正交：$\boldsymbol{b}\cdot\boldsymbol{b}=0$，长度为 0 的只有零向量，$\boldsymbol{b}=\boldsymbol{0}$。

(2) 取 $\boldsymbol{b}=(1,-1,0)^{\mathsf T}$，它与 $\boldsymbol{a}_1+\boldsymbol{a}_2=(1,1,2)^{\mathsf T}$ 正交，但 $\boldsymbol{b}\cdot\boldsymbol{a}_1=1$。

(3) 由 $x+z=0$、$y+z=0$ 取 $\boldsymbol{n}=(1,1,-1)^{\mathsf T}$。方程 $x+y-z=0$ 的解 $z=x+y$ 可写成 $x\boldsymbol{a}_1+y\boldsymbol{a}_2$，解集正是这个张成，也就是 L.1 例 3 解方程组得到的 $z=x+y$。$(2,3,4)$ 代入得 $2+3-4=1\ne0$，不属于，与 L.1 例 3 一致。

区分点：(1) 后一问要想到让 $\boldsymbol{b}$ 和自己做点积；(2) 与一个组合正交推不出与每个向量正交；(3) 要把张成写成超平面，用一个方程代替解方程组。

**L2-14**
**答案：** L.1 方法 4（凸组合），方法 5，第 4 节的勾股论证；(1) $x+y=50$；(2) $s=\frac12$，距离 $10\sqrt2$；(3) $s=0$（即 $\boldsymbol{p}_1$），距离 $5\sqrt{10}$。

(1) $\boldsymbol{p}_2-\boldsymbol{p}_1=(-30,30)^{\mathsf T}$ 与 $\boldsymbol{a}=(1,1)^{\mathsf T}$ 正交，$\boldsymbol{a}\cdot\boldsymbol{p}_1=50$，直线是 $x+y=50$。

(2) $\boldsymbol{a}\cdot\boldsymbol{g}-50=20$，$t=10$，垂足 $(35,35)-10(1,1)=(25,25)$。由 $40-30s=25$ 得 $s=\frac12\in[0,1]$，垂足在线段上，就是最近点，距离 $\frac{20}{\sqrt2}=10\sqrt2$。

(3) 同样 $\boldsymbol{a}\cdot\boldsymbol{g}-50=20$，垂足 $F=(45,5)$，由 $40-30s=45$ 得 $s=-\frac16<0$，垂足不在线段上。对直线上任一点 $\boldsymbol{x}$，$\boldsymbol{g}-F$ 沿法向量，$F-\boldsymbol{x}$ 沿直线，由勾股定理
$$\lVert\boldsymbol{g}-\boldsymbol{x}\rVert^2=\lVert\boldsymbol{g}-F\rVert^2+\lVert F-\boldsymbol{x}\rVert^2=200+\lVert F-\boldsymbol{x}\rVert^2 .$$
线段上的点 $s\in[0,1]$ 满足 $\lVert F-\boldsymbol{x}\rVert=\left(s+\frac16\right)\cdot30\sqrt2$，$s=0$ 时最小，即 $\boldsymbol{x}=\boldsymbol{p}_1=(40,10)$。距离 $\sqrt{15^2+5^2}=\sqrt{250}=5\sqrt{10}$，与 $200+50=250$ 一致。

区分点：垂足不一定在可行的线段上；要用勾股定理把距离拆成「到直线的距离」加「沿直线离垂足多远」，再在线段上取离垂足最近的点。
