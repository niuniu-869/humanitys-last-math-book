## C.26 · 三重积分与重积分的应用

医院的 CT 把人体切成几百层图像，软件把每一层里器官的面积乘上层厚，再把各层加起来，就得到器官的体积。3D 打印软件面对一个零件，要算体积（用多少耗材），还要算重心在哪里：物体能否平稳放置，要看重心的竖直投影是否落在支撑范围内。零件各处的材料可能不同，要算的量随位置变化，这些数都是把「每一小块的贡献」在整个立体上加起来，也就是三重积分。

难处不在定义，而在计算时换坐标。直角坐标下的边界往往太复杂，换一套坐标常能让积分限简单得多。但坐标一换，同样大小的坐标小块对应的实际体积也会变，所以积分里必须带上体积的缩放因子，一般的缩放因子用雅可比行列式计算。概率里换变量也需要处理这种缩放：同一小块所占的概率保持不变，但描述它的密度会随坐标改变。具体怎样计算，P.5、P.6 再讲。

换坐标时，体积到底要乘什么？这个倍数在欧拉、拉格朗日处理重积分换元时就已经出现，但当时还没有统一的算法；雅可比 1841 年把由偏导数排成的行列式系统化为「函数行列式」，也就是今天说的雅可比行列式，这个倍数才有了统一的算法。为什么一个行列式能表示体积的放大率？它在哪些点会失灵？

本章先把二重积分推到立体上：定义和性质（第 1 节），化成三次定积分（第 2 节）。然后换坐标：圆柱形区域用柱面坐标（第 3 节），球形区域用球面坐标，并由混合积看出一般的放大倍数（第 4 节）。最后用重积分算曲面的面积（第 5 节），以及质心、转动惯量和吸引力（第 6 节）。

### 1. 立体区域上随位置变化的量，总共有多少？

一间屋子里甲醛的浓度各处不同，靠近新家具的地方高，窗边低。浓度的单位是「每立方米多少毫克」，它是位置的函数 $c(x,y,z)$。屋里一共有多少毫克甲醛？

浓度处处相同时，总量就是浓度乘体积。浓度变化时，照二重积分（C.25.1）的四步来：

1. **分割**：把屋子 $\Omega$ 切成 $n$ 个小块，第 $i$ 块体积 $\Delta V_i$。
2. **近似**：小块里浓度差不多，任取一点 $(\xi_i,\eta_i,\zeta_i)$，这块的甲醛约为 $c(\xi_i,\eta_i,\zeta_i)\Delta V_i$。
3. **求和**：$\sum_{i=1}^nc(\xi_i,\eta_i,\zeta_i)\Delta V_i$。
4. **取极限**：最大的小块直径趋于 0 时，和的极限就是总量。

先手算一个小例子。设 $\Omega$ 是单位立方体 $[0,1]^3$，$f=x+y+z$。每条棱对半分，切成 8 个边长 $\frac12$ 的小立方体，每块体积 $\frac18$，取每块中心的值。中心的三个坐标各是 $\frac14$ 或 $\frac34$，8 个中心正好取遍所有组合，每个坐标的平均是 $\frac12$，所以 8 个函数值的平均是 $\frac32$，和式为

$$\sum f(\text{中心})\cdot\frac18=\frac32 .$$

本章所用的立体区域都由有限片光滑曲面围成。设 $\Omega$ 是这样的有界闭区域，$f$ 是 $\Omega$ 上的有界函数。不断细分区域，使最大的小块直径趋于 0；如果无论怎样分割、怎样在每块中取点，和式都趋于同一个有限数，就称 $f$ 在 $\Omega$ 上可积，这个数叫作 $f$ 在 $\Omega$ 上的**三重积分**，记作

$$\iiint_\Omega f(x,y,z)\,\mathrm{d}V ,$$

$\mathrm{d}V$ 叫体积元，在直角坐标下也写成 $\mathrm{d}x\,\mathrm{d}y\,\mathrm{d}z$。在上述区域条件下，$f$ 连续时三重积分一定存在。下面列出的性质都以涉及的函数可积为前提。从这里开始只用定义推出的性质，不再回到具体的分割。

性质和二重积分（C.25.2、C.25.3、C.25.7）逐条对应，理由也一样，都来自和式：

- 线性：常数可以提出，和的积分等于积分的和。
- 区域可加：把 $\Omega$ 分成内部不重叠的两块，积分分开算再相加。
- $\iiint_\Omega1\,\mathrm{d}V$ 等于 $\Omega$ 的体积 $V$。
- 比较：$f\le g$ 则积分也 $\le$。
- 中值：$f$ 连续、$\Omega$ 连通（连成一整块）时，有一点使 $\iiint_\Omega f\,\mathrm{d}V=f(\xi,\eta,\zeta)V$。
- 奇偶对称：$\Omega$ 关于 $xOy$ 平面对称（把 $z$ 换成 $-z$ 区域不变），$f$ 对 $z$ 是奇函数时积分为 0，是偶函数时等于上半部分的 2 倍。
- 轮换对称：$\Omega$ 的方程把 $x,y,z$ 轮换后不变（如球 $x^2+y^2+z^2\le a^2$），则 $\iiint x\,\mathrm{d}V=\iiint y\,\mathrm{d}V=\iiint z\,\mathrm{d}V$，同样 $\iiint x^2=\iiint y^2=\iiint z^2$。理由是把坐标的名字轮换一下，区域不变，一个积分就变成了另一个。

条件各有用处，去掉就会出错。两个相隔很远、体积相同的球合成的区域不连通，$f$ 在一个球上取 $1$、在另一个球上取 $-1$，积分为 0，可是 $f$ 处处不为 0，中值公式不成立。上半球上 $z$ 的积分是正数，因为区域本身不关于 $xOy$ 平面对称。长方体 $[0,1]\times[0,2]\times[0,3]$ 的方程轮换后会变，$\iiint x\,\mathrm{d}V=3$，$\iiint y\,\mathrm{d}V=6$，并不相等。

奇偶对称为什么成立？取关于 $xOy$ 平面对称的分割，把互为镜像的两小块配成一对，跨过平面的小块总体积趋于 0，可以不计。配对的两块里，点 $(x,y,z)$ 和 $(x,y,-z)$ 处 $f$ 的值互为相反数，和式里成对抵消。

定义只说明和式的极限是什么，怎样算出真值、误差有多大，它都没有回答。下一节把三重积分化成三次一元积分。

合上书，写出三重积分定义的四步，并说明 $\iiint_{x^2+y^2+z^2\le1}z^3\,\mathrm{d}V$ 为什么是 0。

### 2. 三重积分怎样化成三次定积分？

回到屋子里的甲醛。CT 的做法是把屋子切成很薄的水平层，每层的甲醛约为这一层上的二重积分乘层厚，再把各层加起来；也可以竖着切成细柱，每根细柱沿高度积分，再把细柱加起来。二重积分是先「穿线」再化成两次定积分（C.25.5），这两种切法是它在立体上的两个版本。

**先一后二（投影法）**　把 $\Omega$ 投影到 $xOy$ 平面，影子是区域 $D_{xy}$（C.19.15）。在 $D_{xy}$ 里任取一点 $(x,y)$，过它画一条竖直线，从下往上穿过 $\Omega$：从下表面 $z=z_1(x,y)$ 穿入，从上表面 $z=z_2(x,y)$ 穿出（图 C26-n1）。站在小块 $\Delta\sigma$ 上的细柱，把它沿竖直方向切成许多高 $\Delta z$ 的小段，每段体积约 $\Delta\sigma\,\Delta z$，对 $z$ 求和取极限，贡献约为 $\big(\int_{z_1}^{z_2}f\,\mathrm{d}z\big)\Delta\sigma$；再把所有细柱加起来（这里假设每条竖线和 $\Omega$ 只交一段；交成几段时，把 $\Omega$ 切成几块分别算）：

$$\iiint_\Omega f\,\mathrm{d}V=\iint_{D_{xy}}\Big(\int_{z_1(x,y)}^{z_2(x,y)}f(x,y,z)\,\mathrm{d}z\Big)\mathrm{d}\sigma .$$

![以例 1 的四面体为例：过影子 $D_{xy}$ 里的一点竖着穿线，从底面 $z=0$ 穿入、从斜面 $z=1-x-y$ 穿出，这一段就是对 $z$ 积分的上下限](fig/C26-n1.pdf){width=60%}

**方法 1（投影法：先一后二）**

1. 画出 $\Omega$，找它在 $xOy$ 平面上的投影 $D_{xy}$。
2. 在 $D_{xy}$ 里竖着穿线，穿入的曲面是下限 $z_1$，穿出的是上限 $z_2$。
3. 先对 $z$ 积分，$x,y$ 当常数；剩下的是 $D_{xy}$ 上的二重积分，照 C.25.5 定限。

**例 1**　$\Omega$ 由三个坐标平面和平面 $x+y+z=1$ 围成，求 $\iiint_\Omega x\,\mathrm{d}V$。和第 1 节的单位立方体相比，被积函数只剩 $x$，区域换成斜面截出的四面体，上限不再是常数，难点在定限。

第一步，投影。$\Omega$ 是一个四面体，影子是 $xOy$ 平面上 $x\ge0$、$y\ge0$、$x+y\le1$ 的三角形。

第二步，穿线。竖线从 $z=0$ 进，从 $z=1-x-y$ 出，所以

$$\iiint_\Omega x\,\mathrm{d}V=\int_0^1\!\!\int_0^{1-x}\!\!\int_0^{1-x-y}x\,\mathrm{d}z\,\mathrm{d}y\,\mathrm{d}x .$$

第三步，逐层算。对 $z$ 积分得 $x(1-x-y)$；再对 $y$ 积分，

$$\int_0^{1-x}x(1-x-y)\,\mathrm{d}y=x\cdot\frac{(1-x)^2}{2} ;$$

最后 $\int_0^1\frac{x(1-x)^2}2\,\mathrm{d}x=\frac12\Big(\frac12-\frac23+\frac14\Big)=\frac1{24}$。

> 求单位立方体上的 $\iiint(x+y+z)\,\mathrm{d}V$。
>
> 答案：三层上下限都是 0 到 1，$\iiint x\,\mathrm{d}V=\frac12$，三项共 $\frac32$，和上一节 8 块的近似值恰好相同，因为被积函数是一次的，中心值正好是每块上的平均值。

**先二后一（截面法）**　如果 $\Omega$ 夹在两个平面 $z=c_1$、$z=c_2$ 之间，在高度 $z$ 处横切一刀，截面是一块平面区域 $D_z$。先在截面上做二重积分，再把各层加起来：

$$\iiint_\Omega f\,\mathrm{d}V=\int_{c_1}^{c_2}\Big(\iint_{D_z}f\,\mathrm{d}\sigma\Big)\mathrm{d}z .$$

当 $f$ 只含 $z$ 时，里层的 $f(z)$ 是常数，里层积分就是 $f(z)$ 乘截面面积 $A(z)$，整个三重积分变成一次定积分 $\int_{c_1}^{c_2}f(z)A(z)\,\mathrm{d}z$。

**方法 2（截面法：先二后一）**

1. 选定高度变量 $z$，写出高度 $z$ 处的截面 $D_z$。
2. 在 $D_z$ 上先算二重积分。如果被积函数在这一层处处相同（例如只含 $z$），就可以把这一步简化成 $f(z)A(z)$，其中 $A(z)$ 是截面积。
3. 再把各层的积分结果对 $z$ 积分。

**例 2**　设 $a,b,c>0$，求椭球 $\Omega:\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}\le1$ 上的 $\iiint_\Omega z^2\,\mathrm{d}V$。和例 1 相比，被积函数只含 $z$，区域换成了边界带根号的椭球，这时改用方法 2。

高度 $z$ 处的截面是 $\frac{x^2}{a^2}+\frac{y^2}{b^2}\le1-\frac{z^2}{c^2}$，这是半轴为 $a\sqrt{1-z^2/c^2}$、$b\sqrt{1-z^2/c^2}$ 的椭圆。半轴为 $p,q$ 的椭圆是把单位圆横向拉长 $p$ 倍、纵向拉长 $q$ 倍，面积是 $\pi pq$，所以

$$A(z)=\pi ab\Big(1-\frac{z^2}{c^2}\Big) .$$

于是

$$\iiint_\Omega z^2\,\mathrm{d}V=\int_{-c}^{c}z^2\cdot\pi ab\Big(1-\frac{z^2}{c^2}\Big)\mathrm{d}z=\pi ab\Big(\frac{2c^3}3-\frac{2c^3}5\Big)=\frac{4\pi abc^3}{15} .$$

> 求 $\Omega:\ x^2+y^2\le z^2,\ 0\le z\le1$ 上的 $\iiint_\Omega z\,\mathrm{d}V$。
>
> 答案：高度 $z$ 处的截面是半径为 $z$ 的圆盘，面积 $\pi z^2$，被积函数只含 $z$，所以 $\int_0^1z\cdot\pi z^2\,\mathrm{d}z=\frac\pi4$。

两种方法并排看：例 2 若用投影法，对 $z$ 积分得到 $\frac23\big(c\sqrt{1-x^2/a^2-y^2/b^2}\big)^3$，再在椭圆上做二重积分，很难对付；截面法只需要会算椭圆面积。反过来，例 1 的被积函数含 $x$，截面法里层要在三角形上积 $x$，并不比投影法省事。选法看两样：被积函数含几个变量，截面面积好不好写。

截面法有一个容易想错的地方：只有被积函数在整个截面上处处相同，才能写成 $f(z)A(z)$。圆柱 $x^2+y^2\le1$、$0\le z\le1$ 上的 $\iiint x^2\,\mathrm{d}V$，若因为轴线上 $x^2=0$ 就把每层记成 $0\cdot\pi$，会得到 0；实际每层的 $\iint_{D_z}x^2\,\mathrm{d}\sigma=\frac\pi4$，结果是 $\frac\pi4$。

两种切法都要自己写出上下限或截面。遇到圆柱、抛物面这类绕 $z$ 轴转出来的区域，投影是圆盘，用 $x,y$ 定限很别扭，下一节换坐标。

合上书，对同一个区域分别写出投影法和截面法的积分式，说出各自先对谁积分。

### 3. 圆柱形区域上用什么坐标？

先用投影法算圆柱 $x^2+y^2\le1$、$0\le z\le2$ 的体积：竖线从 $z=0$ 穿到 $z=2$，里层得 2，外层 $\iint_D2\,\mathrm{d}\sigma$ 的 $D$ 是单位圆盘，用极坐标得 $\int_0^{2\pi}\!\int_0^12r\,\mathrm{d}r\,\mathrm{d}\theta=2\pi$。这里 $x,y$ 那一层换成了极坐标（C.25.8），高度 $z$ 保持不动，合起来就是**柱面坐标**：

$$x=r\cos\theta,\qquad y=r\sin\theta,\qquad z=z ,$$

$r\ge0$ 是点到 $z$ 轴的距离，$\theta$ 和极坐标里的一样。

体积元怎么变？在 $(r,\theta,z)$ 处让三个坐标各变一点，围出的小块底面是极坐标的小扇环，面积约 $r\,\Delta r\,\Delta\theta$（C.25.8）；高是 $\Delta z$。所以

$$\mathrm{d}V=r\,\mathrm{d}r\,\mathrm{d}\theta\,\mathrm{d}z .$$

**方法 3（柱面坐标）**

1. 投影是圆盘、扇形，或被积函数、边界含 $x^2+y^2$ 时用它。
2. 按投影法先定 $z$ 的上下限，把其中的 $x$、$y$ 换成 $r\cos\theta$、$r\sin\theta$；上下限一般可以同时含 $r$ 和 $\theta$。再在投影上按极坐标定 $r$、$\theta$ 的范围。
3. 被积函数换成 $r,\theta,z$，别忘了多乘一个 $r$。

**例 3**　$\Omega$ 由旋转抛物面 $z=x^2+y^2$ 和平面 $z=4$ 围成，求 $\iiint_\Omega z\,\mathrm{d}V$。穿线的做法和例 1 完全一样，区别是投影变成圆盘，投影那一层要用极坐标。

第一步，投影。两个曲面的交线是 $x^2+y^2=4$、$z=4$，投影是圆盘 $r\le2$。

第二步，穿线。竖线从抛物面 $z=r^2$ 进，从平面 $z=4$ 出。

第三步，积分。先对 $z$：$\int_{r^2}^4z\,\mathrm{d}z=\frac{16-r^4}2$。再乘 $r$，对 $r$、$\theta$ 积分：

$$\iiint_\Omega z\,\mathrm{d}V=\int_0^{2\pi}\!\!\int_0^2\frac{16-r^4}2\,r\,\mathrm{d}r\,\mathrm{d}\theta=2\pi\cdot\frac12\Big(32-\frac{64}6\Big)=\frac{64\pi}3 ,$$

其中 $\int_0^2(16r-r^5)\,\mathrm{d}r=\Big(8r^2-\frac{r^6}6\Big)\Big|_0^2=32-\frac{64}6$。

> 求圆柱 $x^2+y^2\le1$、$0\le z\le2$ 上的 $\iiint\sqrt{x^2+y^2}\,\mathrm{d}V$。
>
> 答案：被积函数是 $r$，再乘体积元里的 $r$，得 $\int_0^{2\pi}\!\int_0^1\!\int_0^2r^2\,\mathrm{d}z\,\mathrm{d}r\,\mathrm{d}\theta=2\pi\cdot\frac13\cdot2=\frac{4\pi}3$。

柱面坐标只改了底面。球 $x^2+y^2+z^2\le a^2$ 在柱面坐标下，$z$ 的上下限是 $\pm\sqrt{a^2-r^2}$，带根号；球面与圆锥面围成的区域，$z$ 的上下限里仍会出现这个根号。下一节换一套以原点为中心的坐标。

合上书，用「底面是扇环、高是 $\Delta z$」说出 $\mathrm{d}V=r\,\mathrm{d}r\,\mathrm{d}\theta\,\mathrm{d}z$ 的来历。

### 4. 球形、锥形区域上用什么坐标？

我们要一套坐标，让球面变成「某个坐标等于常数」。

**球面坐标**用三个量确定点 $P$：

- $\rho$：$P$ 到原点的距离，$\rho\ge0$；
- $\varphi$：线段 $OP$ 与 $z$ 轴正方向的夹角，$0\le\varphi\le\pi$；
- $\theta$：$P$ 投影到 $xOy$ 平面后的极角，和柱面坐标的一样。

$OP$ 在 $xOy$ 平面上的投影长是 $\rho\sin\varphi$，它就是柱面坐标的 $r$；$P$ 的高度是 $\rho\cos\varphi$。于是

$$x=\rho\sin\varphi\cos\theta,\qquad y=\rho\sin\varphi\sin\theta,\qquad z=\rho\cos\varphi .$$

例如单位球面上的点 $(\frac12,\frac12,\frac{\sqrt2}2)$：$\rho=1$，$\cos\varphi=\frac{\sqrt2}2$，所以 $\varphi=\frac\pi4$，它的影子在第一象限的对角线上，$\theta=\frac\pi4$。代回公式，$x=\sin\frac\pi4\cos\frac\pi4=\frac12$，与原来的坐标一致。

在这套坐标下，球面 $x^2+y^2+z^2=a^2$ 是 $\rho=a$，圆锥面 $z=\sqrt{x^2+y^2}$ 是 $\varphi=\frac\pi4$。

体积元由小块的三条边得到（图 C26-n2）。让 $\rho$、$\varphi$、$\theta$ 各变一点：

1. 沿射线方向，边长 $\Delta\rho$；
2. $\varphi$ 变化时，点在半径为 $\rho$ 的圆（经线）上走，弧长 $\rho\,\Delta\varphi$；
3. $\theta$ 变化时，点在半径为 $\rho\sin\varphi$ 的水平圆（纬线）上走，弧长 $\rho\sin\varphi\,\Delta\theta$。

这三条边两两垂直。径向方向垂直于球面，经线、纬线在这一点的切向都在球面的切平面内，所以它们各自垂直于径向。经线的切向位于过 $z$ 轴的竖直平面内，纬线的切向垂直于这个平面，所以这两个切向也互相垂直。小块缩得很小时，就可以用这三条边围出的长方体近似它。于是

$$\mathrm{d}V=\rho^2\sin\varphi\,\mathrm{d}\rho\,\mathrm{d}\varphi\,\mathrm{d}\theta .$$

用它检验单位球的体积：$\int_0^{2\pi}\mathrm{d}\theta\int_0^\pi\sin\varphi\,\mathrm{d}\varphi\int_0^1\rho^2\,\mathrm{d}\rho=2\pi\cdot2\cdot\frac13=\frac{4\pi}3$。若漏掉 $\rho^2\sin\varphi$，同样的限给出 $2\pi\cdot\pi\cdot1=2\pi^2$，显然不对。

![小块的三条边：沿射线 $\Delta\rho$，沿经线 $\rho\,\Delta\varphi$，沿纬线 $\rho\sin\varphi\,\Delta\theta$；纬线圆的半径是 $\rho\sin\varphi$，所以第三条边多一个 $\sin\varphi$](fig/C26-n2.pdf){width=62%}

**方法 4（球面坐标）**

1. 区域由球面、过原点的圆锥面围成，或被积函数含 $x^2+y^2+z^2$ 时用它。
2. 一般按 $\theta$、$\varphi$、$\rho$ 的顺序定限：$\theta$ 看投影绕了多大角度，$\varphi$ 看从 $z$ 轴张开多大，$\rho$ 沿射线从原点到穿出处（原点不在区域里时，下限是射线穿入处）。射线与区域交成几段时，分段列出径向上下限，再把积分相加。
3. 别忘了乘 $\rho^2\sin\varphi$。

**例 4**　$\Omega$ 在圆锥面 $z=\sqrt{x^2+y^2}$ 之上、单位球面 $x^2+y^2+z^2=1$ 之内，求 $\iiint_\Omega z\,\mathrm{d}V$。被积函数仍是例 1、例 3 的 $x$ 或 $z$ 这类一次函数，这次区域由球和锥围成，方法 3 的上下限带根号，改用方法 4。

第一步，定限。区域绕 $z$ 轴一整圈，$0\le\theta\le2\pi$；从 $z$ 轴张开到锥面，$0\le\varphi\le\frac\pi4$；沿射线从原点到球面，$0\le\rho\le1$。

第二步，换被积函数：$z=\rho\cos\varphi$。

第三步，三个变量的上下限都是常数，被积函数又拆成三个因子的乘积，三次积分可以分开算：

$$\iiint_\Omega z\,\mathrm{d}V=\int_0^{2\pi}\mathrm{d}\theta\int_0^{\pi/4}\sin\varphi\cos\varphi\,\mathrm{d}\varphi\int_0^1\rho^3\,\mathrm{d}\rho=2\pi\cdot\frac14\cdot\frac14=\frac\pi8 .$$

> 求单位球上的 $\iiint(x^2+y^2+z^2)\,\mathrm{d}V$。
>
> 答案：被积函数是 $\rho^2$，$\int_0^{2\pi}\mathrm{d}\theta\int_0^\pi\sin\varphi\,\mathrm{d}\varphi\int_0^1\rho^4\,\mathrm{d}\rho=2\pi\cdot2\cdot\frac15=\frac{4\pi}5$。

#### 一般的换元

一般椭球 $\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}\le1$ 的边界不是 $\rho=$ 常数，球面坐标不顺手。先看最简单的伸缩 $x=2u$、$y=3v$、$z=4w$：$uvw$ 空间里 $\Delta u\times\Delta v\times\Delta w$ 的小长方体，变成 $2\Delta u\times3\Delta v\times4\Delta w$ 的长方体，体积放大 $2\cdot3\cdot4=24$ 倍。一般的变换会把小长方体变成斜的平行六面体，放大倍数要用混合积来算。

柱面、球面坐标都是换元的特例。一般地，选新变量 $x=x(u,v,w)$、$y=y(u,v,w)$、$z=z(u,v,w)$，道理和二维的雅可比行列式（C.25.10）一样。

先把点写成位置向量 $\boldsymbol{r}=(x,y,z)$，它是 $u,v,w$ 的函数。$uvw$ 空间里的小长方体，三条边变成三个位移 $\boldsymbol{r}_u\Delta u$、$\boldsymbol{r}_v\Delta v$、$\boldsymbol{r}_w\Delta w$，其中

$$\boldsymbol{r}_u=(x_u,y_u,z_u),\qquad\boldsymbol{r}_v=(x_v,y_v,z_v),\qquad\boldsymbol{r}_w=(x_w,y_w,z_w),$$

$x_u$ 表示 $x$ 对 $u$ 的偏导数 $\frac{\partial x}{\partial u}$，其余下标同理。位移是偏导数乘增量，因为只让 $u$ 变化 $\Delta u$ 时，位置的改变量约等于 $\boldsymbol{r}_u\Delta u$。

换元后的小块近似是以这三个位移为棱的平行六面体，体积是混合积的绝对值（C.19.6）。混合积对每个向量都是线性的（一条棱变成 2 倍，体积就变成 2 倍），所以三个增量可以提到外面：

$$[\boldsymbol{r}_u\Delta u,\boldsymbol{r}_v\Delta v,\boldsymbol{r}_w\Delta w]=\Delta u\Delta v\Delta w\,[\boldsymbol{r}_u,\boldsymbol{r}_v,\boldsymbol{r}_w] .$$

右边的混合积按 C.19.6 就是三阶行列式

$$J=\frac{\partial(x,y,z)}{\partial(u,v,w)}=\begin{vmatrix}x_u&x_v&x_w\\y_u&y_v&y_w\\z_u&z_v&z_w\end{vmatrix} ,$$

所以 $\mathrm{d}V=|J|\,\mathrm{d}u\,\mathrm{d}v\,\mathrm{d}w$，$|J|$ 就是新小块与 $\Delta u\,\Delta v\,\Delta w$ 的体积之比，在上面的伸缩例子里是 24。

对本章使用的换元，先在新坐标区域的内部检查：各坐标函数的偏导连续，变换一一对应，并且 $J\ne0$。这是够用的条件，不是必要条件。

边界需要单独看。柱面、球面坐标在轴、原点或角度接缝处会出现重复表示或 $J=0$。这些地方在原来的立体里不占体积，可以用总体积任意小的小块盖住，对和式的贡献趋于 0，积分限里算不算它们都一样。真正要避免的是让有体积的一整块区域被重复覆盖：柱面坐标里若取 $0\le\theta\le4\pi$，每个点被算两遍，圆柱的体积就会算成两倍。完整的换元公式是

$$\iiint_\Omega f(x,y,z)\,\mathrm dV=\iiint_E f\bigl(x(u,v,w),y(u,v,w),z(u,v,w)\bigr)\,|J|\,\mathrm du\,\mathrm dv\,\mathrm dw ,$$

这里 $E$ 是新变量的取值区域，它经过变换恰好得到 $\Omega$。换元时要一起改变区域、被积函数和体积元。

用它核对球面坐标：$\boldsymbol{r}_\rho$、$\boldsymbol{r}_\varphi$、$\boldsymbol{r}_\theta$ 正是图 C26-n2 三条边的方向，两两的数量积都是 0，长度分别是 $1$、$\rho$、$\rho\sin\varphi$。三条棱两两垂直的平行六面体是长方体，体积是三个长度之积，所以 $|J|=\rho^2\sin\varphi$。

**例 5**　设 $a,b,c>0$，求椭球 $\Omega:\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}\le1$ 的体积，以及 $\iiint_\Omega\Big(\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}\Big)\mathrm{d}V$。区域和例 2 相同，这次不用截面，直接把椭球换成单位球。

令 $x=au$、$y=bv$、$z=cw$，椭球变成单位球 $u^2+v^2+w^2\le1$。$J$ 是对角线为 $a,b,c$ 的行列式，等于 $abc$，所以 $\mathrm{d}V=abc\,\mathrm{d}u\,\mathrm{d}v\,\mathrm{d}w$。

体积等于 $abc$ 乘单位球的体积，即 $\frac43\pi abc$；用例 2 的截面积 $A(z)$ 积一次，$\int_{-c}^{c}A(z)\,\mathrm{d}z$ 也是 $\frac43\pi abc$，两条路一致。被积函数变成 $u^2+v^2+w^2$，由例 4 后面的小题，单位球上 $\iiint(u^2+v^2+w^2)\,\mathrm{d}V=\frac{4\pi}5$，所以第二个积分等于 $\frac{4\pi abc}5$。

> 求椭球 $\frac{x^2}4+\frac{y^2}9+\frac{z^2}{16}\le1$ 的体积。
>
> 答案：令 $x=2u$、$y=3v$、$z=4w$，$|J|=2\cdot3\cdot4=24$，单位球体积 $\frac43\pi$，所以体积是 $24\cdot\frac43\pi=32\pi$。

到这里算的都是体积和随位置变化的量。曲面本身的面积，例如一只碗的内壁，是二维的量，体积元帮不上忙。

合上书，画出球面坐标的小块，说出三条边的长度，再用「三条棱两两垂直」核对 $|J|$。

### 5. 一张弯曲的曲面有多大面积？

例 3 里的抛物面 $z=x^2+y^2$ 是那块立体的外壳。立体的体积用体积元累加，外壳这层「皮」有多大？先看最简单的斜面 $z=x$（$0\le x\le1$，$0\le y\le1$）：它是边长 $1$ 和 $\sqrt2$ 的长方形，面积 $\sqrt2$，而它在 $xOy$ 平面上的影子是单位正方形，面积 1。斜面比影子大，大多少与倾斜程度有关。

一般地，设 $D$ 是边界由有限段光滑曲线围成的有界闭区域，$f$ 在 $D$ 及其附近有连续的一阶偏导数。要求曲面 $z=f(x,y)$（$(x,y)\in D$）的面积，仍然从分割求和出发：把 $D$ 切成小矩形，算出每个小矩形「头顶上」那一小片曲面的面积，再加起来。

一小片曲面很难直接量，但它几乎是平的，可以用切平面上的一小片代替。两者的面积之差比 $\Delta x\Delta y$ 小得多（高阶无穷小），所有小片加起来，总误差随分割变细趋于 0，所以下面求出的极限就是曲面的面积。在 $(x,y)$ 处取边长 $\Delta x$、$\Delta y$ 的小矩形。沿 $x$ 方向走 $\Delta x$，切平面上升 $f_x\Delta x$；沿 $y$ 方向走 $\Delta y$，上升 $f_y\Delta y$（C.23.2）。所以切平面上对应的是以

$$\boldsymbol{a}=(\Delta x,\ 0,\ f_x\Delta x),\qquad \boldsymbol{b}=(0,\ \Delta y,\ f_y\Delta y)$$

为邻边的平行四边形（图 C26-n3）。它的面积是向量积的长度（C.19.5）：

$$\boldsymbol{a}\times\boldsymbol{b}=(-f_x,\ -f_y,\ 1)\,\Delta x\Delta y,\qquad \lVert\boldsymbol{a}\times\boldsymbol{b}\rVert=\sqrt{1+f_x^2+f_y^2}\,\Delta x\Delta y .$$

![小矩形 $\Delta x\Delta y$ 正上方，切平面上是以 $\boldsymbol a$、$\boldsymbol b$ 为邻边的平行四边形；它倾斜得越厉害，面积比底下的小矩形大得越多](fig/C26-n3.pdf){width=60%}

加起来取极限，得到**曲面面积公式**

$$S=\iint_D\sqrt{1+f_x^2+f_y^2}\,\mathrm{d}\sigma .$$

核对斜面 $z=x$：$f_x=1$，$f_y=0$，根号是 $\sqrt2$，在单位正方形上积分得 $\sqrt2$，与长方形的面积一致。

根号这个因子有一个几何读法。$(-f_x,-f_y,1)$ 是切平面的法向量，它和 $z$ 轴正方向的夹角 $\gamma$ 满足 $\cos\gamma=\frac1{\sqrt{1+f_x^2+f_y^2}}$。所以面积元 $\mathrm{d}S=\frac{\mathrm{d}\sigma}{\cos\gamma}$：一小片斜放的曲面，投到地上的影子要乘 $\cos\gamma$，斜得越厉害影子越小。

**方法 5（曲面面积）**

1. 把曲面写成 $z=f(x,y)$，找它在 $xOy$ 平面上的投影 $D$。
2. 算 $\sqrt{1+f_x^2+f_y^2}$。
3. 在 $D$ 上做二重积分，$D$ 是圆盘时换极坐标。

**例 6**　求旋转抛物面 $z=x^2+y^2$ 在平面 $z=1$ 以下那部分的面积。和例 3 用同一个抛物面，这次不算立体，算它在 $z=1$ 以下那层「皮」的面积。

第一步，投影是圆盘 $x^2+y^2\le1$。

第二步，$f_x=2x$，$f_y=2y$，根号是 $\sqrt{1+4(x^2+y^2)}=\sqrt{1+4r^2}$。

第三步，用极坐标。里层令 $s=1+4r^2$，则 $r\,\mathrm{d}r=\frac{\mathrm{d}s}8$，$\int\sqrt s\,\frac{\mathrm{d}s}8=\frac{s^{3/2}}{12}$：

$$S=\int_0^{2\pi}\!\!\int_0^1\sqrt{1+4r^2}\,r\,\mathrm{d}r\,\mathrm{d}\theta=2\pi\cdot\frac1{12}(1+4r^2)^{3/2}\Big|_0^1=\frac\pi6\big(5\sqrt5-1\big) .$$

> 求圆锥面 $z=\sqrt{x^2+y^2}$ 在 $z\le1$ 部分的面积。
>
> 答案：除锥顶外 $f_x^2+f_y^2=\frac{x^2+y^2}{x^2+y^2}=1$，根号是 $\sqrt2$（锥顶不可导，但只是一个点，不影响积分），$S=\sqrt2\cdot\pi$。

面积和体积只由形状决定。形状相同的两个零件，一个是实心钢，一个是泡沫，质量和转起来的难易并不相同，还差一个量：每一处有多少材料。

合上书，从小矩形上方的平行四边形出发，推出根号因子。

### 6. 物体的重心在哪里，转起来有多费劲，吸引力有多大？

物体各处的材料不同时，用**密度** $\mu(x,y,z)$ 表示「每立方米有多少千克」，它和第 1 节的甲醛浓度是同一种量，所以物体的质量是

$$M=\iiint_\Omega\mu\,\mathrm{d}V .$$

密度 $\mu\ge0$；下面讨论质心时，假定总质量 $M$ 有限且大于 0。

薄板（厚度可以不计）用面密度 $\mu(x,y)$，单位是每平方米多少千克，$M=\iint_D\mu\,\mathrm{d}\sigma$。

#### 质心

C.13.11 讲过，质心是「各处位置按质量加权的平均」。在重力大小和方向处处相同的近似下，质心与重心重合。小块 $\mathrm{d}V$ 的质量是 $\mu\,\mathrm{d}V$，它的 $x$ 坐标是 $x$，按质量加权求平均再取极限，得到三个坐标：

$$\bar x=\frac1M\iiint_\Omega x\,\mu\,\mathrm{d}V,\qquad \bar y=\frac1M\iiint_\Omega y\,\mu\,\mathrm{d}V,\qquad \bar z=\frac1M\iiint_\Omega z\,\mu\,\mathrm{d}V .$$

密度处处相同时，$\mu$ 约掉，质心只由形状决定，叫**形心**。

#### 转动惯量

同样的质量，分布在转轴附近或远离转轴，对改变物体转动快慢的影响不同。转动惯量用「质量乘离轴距离的平方」来衡量每一小块的贡献，再把这些贡献加起来。它同时取决于质量分布和所选的转轴；同一物体换一根轴，转动惯量通常也会改变。

设 $d$ 是小块到转轴的距离，这一小块的贡献是 $d^2\mu\,\mathrm{d}V$。绕 $z$ 轴时 $d^2=x^2+y^2$，所以得到下面的积分式：

$$I_z=\iiint_\Omega(x^2+y^2)\,\mu\,\mathrm{d}V .$$

#### 吸引力

两个质点互相吸引，力的大小与两个质量之积成正比，与距离的平方成反比，方向沿两点的连线（C.13.10）。设 $G$ 是一个常数，质量 $m$ 的质点对质量为 1、相距 $d$ 的质点的吸引力大小是 $Gm/d^2$。物体是连续分布时，把它切成小块，每块当质点，各块的吸引力（向量）加起来，就是积分。

**方法 6（质心、转动惯量与吸引力）**

1. 先同时检查区域和密度的对称性。例如区域关于 $x=0$ 对称，且 $\mu(-x,y,z)=\mu(x,y,z)$ 时，$x\mu$ 的积分为 0，从而 $\bar x=0$。
2. 写出 $M$ 和需要的「坐标乘密度」的积分，按区域形状选坐标系。
3. 转动惯量里的 $d^2$ 是到转轴的距离的平方，不是到原点的。
4. 求轴线上一点受到的吸引力时，如果物体形状和密度都绕这根轴对称，可以把等质量小块配对，抵消垂直于轴的分量，只累加沿轴的分量。

**例 7**　设 $a>0$，$\Omega=\{(x,y,z):x^2+y^2+z^2\le a^2,\ z\ge0\}$ 是半个球。求 $\Omega$ 的体积 $V$，以及三个坐标在 $\Omega$ 上的平均值 $\frac1V\iiint_\Omega x\,\mathrm{d}V$、$\frac1V\iiint_\Omega y\,\mathrm{d}V$、$\frac1V\iiint_\Omega z\,\mathrm{d}V$（均匀物体的形心就是这三个平均值）。积分的做法和例 4 一样，球换成半球，$\varphi$ 的范围改成 $0$ 到 $\frac\pi2$，被积函数 $z$ 没变；这次要的是平均值，所以还要除以体积。先猜一猜：半球的形心离底面比 $\frac a2$ 高还是低？

第一步，对称性。$\Omega$ 关于 $yOz$ 平面对称，被积函数 $x$ 是奇函数，所以 $\iiint x\,\mathrm{d}V=0$，$x$ 的平均值为 0；同理 $y$ 的平均值也是 0。

第二步，体积是半个球，$V=\frac23\pi a^3$。用球面坐标：

$$\iiint_\Omega z\,\mathrm{d}V=\int_0^{2\pi}\mathrm{d}\theta\int_0^{\pi/2}\sin\varphi\cos\varphi\,\mathrm{d}\varphi\int_0^a\rho^3\,\mathrm{d}\rho=2\pi\cdot\frac12\cdot\frac{a^4}4=\frac{\pi a^4}4 .$$

第三步，$z$ 的平均值是 $\frac{\pi a^4/4}{2\pi a^3/3}=\frac{3a}8$。比 $\frac a2$ 低，因为较小高度处的截面积较大，这些点在平均里占的份额更多。

> 求 $\Omega:\ x^2+y^2\le z,\ 0\le z\le1$ 上 $z$ 的平均值，即 $\frac1V\iiint_\Omega z\,\mathrm{d}V$。
>
> 答案：高度 $z$ 处的截面是半径 $\sqrt z$ 的圆盘，面积 $\pi z$。体积 $V=\int_0^1\pi z\,\mathrm{d}z=\frac\pi2$，$\iiint z\,\mathrm{d}V=\int_0^1\pi z^2\,\mathrm{d}z=\frac\pi3$，平均值是 $\frac\pi3\big/\frac\pi2=\frac23$。

**例 8**　设 $a>0$，$B$ 是球 $x^2+y^2+z^2\le a^2$。利用轮换对称性计算 $\iiint_B(x^2+y^2)\,\mathrm{d}V$。和例 7 不同的是，被积函数是 $x^2+y^2$，而且可以用轮换对称省掉一次积分。

球的方程轮换不变，所以三个平方的积分相等，记它们都等于 $K$：

$$\iiint_Bx^2\,\mathrm{d}V=\iiint_By^2\,\mathrm{d}V=\iiint_Bz^2\,\mathrm{d}V=K .$$

于是

$$\iiint_B(x^2+y^2)\,\mathrm{d}V=2K,\qquad\iiint_B(x^2+y^2+z^2)\,\mathrm{d}V=3K .$$

后一式的被积函数是 $\rho^2$，用球面坐标直接算（第 4 节小题，半径换成 $a$，$\rho^4$ 积到 $a$ 得 $\frac{a^5}5$）：

$$3K=\int_0^{2\pi}\mathrm{d}\theta\int_0^\pi\sin\varphi\,\mathrm{d}\varphi\int_0^a\rho^4\,\mathrm{d}\rho=2\pi\cdot2\cdot\frac{a^5}5=\frac{4\pi a^5}5 .$$

所求的是 $2K$，由两式的比例 $2K=\frac23\cdot3K$ 得

$$\iiint_B(x^2+y^2)\,\mathrm{d}V=\frac23\cdot\frac{4\pi a^5}5=\frac{8\pi a^5}{15} .$$

这就是均匀球绕过球心的轴的转动惯量里要算的积分：密度 $\mu=\frac M{4\pi a^3/3}$ 乘上它，得 $I_z=\frac25Ma^2$。

**例 9**　设 $a,h>0$。一块半径为 $a$、面密度为常数 $\mu$ 的薄圆盘，水平放在原点周围。求它对正上方高 $h$ 处单位质点的吸引力。前面各题把小块的数相加，这里要相加的是方向各不相同的力（向量）。先猜一猜：圆盘无限增大时，吸引力会无限增大吗？

设圆盘在 $xOy$ 平面，质点在 $(0,0,h)$。

第一步，小块的质量和距离。圆盘上一小块 $\mathrm{d}\sigma$ 在 $(x,y,0)$，记 $r=\sqrt{x^2+y^2}$，它的质量是 $\mu\,\mathrm{d}\sigma$，到质点的距离 $d=\sqrt{r^2+h^2}$。

第二步，一小块的力。吸引力的大小是 $G\mu\,\mathrm{d}\sigma/d^2$，方向从质点指向这一小块。

第三步，对称性。质点在圆盘的对称轴上，圆盘的形状和密度都绕这根轴对称，所以圆盘上相对的两小块质量相等，对质点的力的水平分量大小相等、方向相反，抵消，只剩竖直分量。

![每个小块产生的力沿斜线方向，其竖直分量（粗线）的大小等于这一个力的大小乘 $\cos\beta=h/d$。两个等质量小块的水平分量（点线）抵消，竖直分量相加](fig/C26-n4.pdf){width=55%}

第四步，竖直分量。这一小块的力与竖直线的夹角为 $\beta$，$\cos\beta=\frac hd$，所以它向下的竖直分量的大小是 $G\mu\,\mathrm{d}\sigma\cdot\frac h{d^3}$。

第五步，把所有小块加起来。用 $F$ 表示合力的大小，水平分量抵消以后，$F$ 就是所有向下竖直分量的大小之和。用极坐标，$\mathrm{d}\sigma=r\,\mathrm{d}r\,\mathrm{d}\theta$：

$$F=G\mu h\int_0^{2\pi}\!\!\int_0^a\frac{r\,\mathrm{d}r\,\mathrm{d}\theta}{(r^2+h^2)^{3/2}} .$$

里层关于 $r$ 的积分，令 $s=r^2+h^2$，则 $r\,\mathrm{d}r=\frac12\mathrm{d}s$，被积函数变成 $\frac12s^{-3/2}$，原函数是 $-s^{-1/2}$：

$$\int_0^a\frac{r\,\mathrm{d}r}{(r^2+h^2)^{3/2}}=\Big[-\frac1{\sqrt{r^2+h^2}}\Big]_0^a=\frac1h-\frac1{\sqrt{a^2+h^2}} .$$

$\theta$ 的积分给出 $2\pi$，再乘前面的 $G\mu h$：

$$F=2\pi G\mu h\Big(\frac1h-\frac1{\sqrt{a^2+h^2}}\Big)=2\pi G\mu\Big(1-\frac h{\sqrt{a^2+h^2}}\Big) ,$$

方向指向圆盘。取 $h=1$，$\frac F{2\pi G\mu}=1-\frac1{\sqrt{1+a^2}}$，$a=1,10,100$ 时约为 $0.293,0.900,0.990$，增长越来越慢。公式解释了原因：$a\to\infty$ 时 $\frac h{\sqrt{a^2+h^2}}\to0$，$F\to2\pi G\mu$，既不会无限增大，极限也与 $h$ 无关。无限大的薄板，在哪里受的吸引力都一样。远处的小块虽然多，但每块的竖直分量 $G\mu\,\mathrm{d}\sigma\,h/d^3$ 衰减得很快。

回到开头的问题。均匀的半球形零件，半径 $a=10$ 毫米，体积 $\frac23\pi a^3\approx2094$ 立方毫米，用料按这个数估计；重心在对称轴上、平面以上 $\frac{3a}8=3.75$ 毫米处。平面朝下放时，重心的竖直投影落在底面圆心，在支撑范围内，能放稳。CT 的逐层相加，则是第 2 节截面法 $\int A(z)\,\mathrm{d}z$ 的离散形式：每层面积乘层厚，再把各层加起来。

合上书，写出质心和转动惯量的积分式，说明例 7 中 $\bar x=0$ 的理由，以及例 9 为什么只算竖直分量。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（投影法：先一后二） | 竖着穿线，上下表面清楚 | C26-01、C26-06 |
| 方法 2（截面法：先二后一） | 截面容易描述；函数在每层恒定时可简化为函数值乘截面积 | C26-04 |
| 方法 3（柱面坐标） | 投影是圆盘、扇形，含 $x^2+y^2$ | C26-02、C26-04 |
| 方法 4（球面坐标；一般换元） | 球面、锥面围成，含 $x^2+y^2+z^2$；椭球类区域先伸缩成球 | C26-03、C26-05、C26-08 |
| 方法 5（曲面面积） | $\iint_D\sqrt{1+f_x^2+f_y^2}\,\mathrm{d}\sigma$ | C26-07 |
| 方法 6（质心、转动惯量、吸引力） | 同时核对区域与密度的对称性，再写加权积分 | C26-06 |
| 对称性（第 1 节） | 奇偶、轮换 | C26-06 |

本章在主线上的位置：重积分是「把区域切成小块，每块当柱体，加起来」，二重积分在平面上做过一次，这一章把它搬到立体里，并且弄清了换坐标时小块的体积被放大多少倍（本章新增：体积元 $r\,\mathrm{d}r\,\mathrm{d}\theta\,\mathrm{d}z$、$\rho^2\sin\varphi\,\mathrm{d}\rho\,\mathrm{d}\varphi\,\mathrm{d}\theta$ 和三阶雅可比行列式）。下面两章讲沿曲线、曲面累加，并把这个「切细再加」换成「边界上的累积」。
