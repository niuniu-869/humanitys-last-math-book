## C.28 · 曲面积分、高斯公式与斯托克斯公式

3D 打印软件拿到一个零件，常用许多小三角形表示它的封闭表面。只要表面围成一个立体、各片朝向一致，就能根据面片的位置和朝向计算体积，不必先把内部填成小块。天气模型也会把空间切成小格子；没有内部增减来源时，一格中空气质量的变化由各面的净流入决定。这些计算都把内部的累积与边界上的累积联系起来，但必须选对各自累积的量。本章会给出它们之间的精确公式。

这个想法前面已经出现过：一元的牛顿–莱布尼茨公式把内部的变化加起来，最后只剩两个端点；平面上的格林公式把区域内部的积分与边界曲线上的积分联系起来。到了空间里，区域是立体，边界是一张曲面。曲面弯曲、分片，逐片去算很麻烦，立体内部的规律却往往简单得多。19 世纪初，高斯给出过若干特例，奥斯特罗格拉茨基给出了一般形式，这就是本章的高斯公式。另一个问题出在空间里的闭曲线：它未必围得住一块平面区域，却可以像铁丝圈一样围住一张曲面，沿曲线的积分能不能换成这张曲面上的积分？这个公式后来以斯托克斯命名。

第 1、2 节定义累加数量和累加流量的两种曲面积分，第 3、4 节讲高斯公式和散度（开头的体积和空气两个问题在这里算出来），第 5、6 节讲斯托克斯公式、旋度和路径无关，第 7 节算质心。

### 1. 在一张弯曲的曲面上累加一个量，怎么算？

一个半球形的薄壳屋顶，涂料刷得不均匀：位置 $(x,y,z)$ 处每平方米有 $\mu(x,y,z)$ 千克。整个屋顶共有多少千克涂料？

涂料均匀、每平方米 $\mu_0$ 千克时，答案就是 $\mu_0$ 乘屋顶的面积（C.26.5）。难处在于 $\mu$ 随位置变化。

先考虑有界、由有限片光滑曲面拼成的 $\Sigma$，允许各片沿边界相接，并设 $f$ 是曲面上的有界函数（涂料的面密度 $\mu$ 就是这样的函数）。$\mu$ 随位置变化时，照二重积分的老办法：把曲面 $\Sigma$ 切成 $n$ 小块，第 $i$ 块面积为 $\Delta S_i$，任取一点 $(\xi_i,\eta_i,\zeta_i)$，这一块的涂料约为 $\mu(\xi_i,\eta_i,\zeta_i)\Delta S_i$。把各块加起来，再让最大的小块直径 $\lambda$ 趋于 $0$：

$$\iint_\Sigma f(x,y,z)\,\mathrm{d}S=\lim_{\lambda\to0}\sum_{i=1}^n f(\xi_i,\eta_i,\zeta_i)\,\Delta S_i .$$

如果无论怎样细分、怎样在每块中取点，这个和式都趋于同一个有限数，就称 $f$ 在 $\Sigma$ 上可积，这个数叫 $f$ 在 $\Sigma$ 上的**第一类曲面积分**（对面积的曲面积分）。$f$ 连续时，在上述曲面上可积；下面的积分性质都以相关积分存在为前提。$\mathrm{d}S$ 是面积元，代表一小块曲面的面积，永远为正。$\Sigma$ 是闭曲面时，积分号写成 $\oiint_\Sigma$。

取 $f\equiv1$ 就是曲面面积（C.26.5）。性质和二重积分一样，对称性也照 C.25.7 用：$\Sigma$ 关于 $xOy$ 面对称、$f$ 对 $z$ 为奇函数时，积分为 $0$。

要算出来，得换成平面上的二重积分。设 $\Sigma$ 是 $z=z(x,y)$，在 $xOy$ 面上的投影区域是 $D$。先设 $z(x,y)$ 在投影区域上有连续的一阶偏导数；边界处出现竖直切面的情况，要另作极限处理，例 1 会遇到它。

一小块曲面近似是一小片平面，法向量是 $(-z_x,-z_y,1)$（C.23.2），和 $z$ 轴的夹角记作 $\gamma$。两平面的夹角等于法向量的夹角，所以这小片平面与 $xOy$ 面的夹角也是 $\gamma$，投到 $xOy$ 面上，面积缩小到 $|\cos\gamma|$ 倍（面积不为负，所以取绝对值），即 $\mathrm{d}\sigma=|\cos\gamma|\,\mathrm{d}S$（见下图）。用法向量算出 $|\cos\gamma|$ 再倒过来：

$$|\cos\gamma|=\frac{1}{\sqrt{1+z_x^2+z_y^2}},\qquad\text{所以}\qquad\mathrm{d}S=\sqrt{1+z_x^2+z_y^2}\,\mathrm{d}\sigma .$$

曲面越陡，$\mathrm{d}S$ 比 $\mathrm{d}\sigma$ 大得越多。直接写 $\iint_Df\,\mathrm{d}\sigma$ 会把倾斜曲面的面积算小，只有曲面水平（$z_x=z_y=0$）时两者才相等。

![小块 $\Delta S$ 近似是斜放的小平面，法向 $\boldsymbol n$ 与 $z$ 轴夹角为 $\gamma$，投影 $\Delta\sigma\approx|\cos\gamma|\,\Delta S$](fig/C28-n1.pdf){width=62%}

再看被积函数。曲面积分里的点始终在 $\Sigma$ 上，所以 $z$ 必须换成 $z(x,y)$，曲面方程也可以随时代入被积函数里化简。三重积分不能这样做，那里的点在立体内部，不满足边界曲面的方程。

**方法 1（第一类曲面积分的投影计算）**

1. 选投影面：$z=z(x,y)$ 投到 $xOy$ 面；投影重叠时先分片。
2. 写出投影区域 $D$，算伸缩因子 $\sqrt{1+z_x^2+z_y^2}$。
3. 把曲面方程代进 $f$，能用对称性就先用。
4. 算 $D$ 上的二重积分，圆形区域换极坐标：

$$\iint_\Sigma f\,\mathrm{d}S=\iint_D f\bigl(x,y,z(x,y)\bigr)\sqrt{1+z_x^2+z_y^2}\,\mathrm{d}\sigma .$$

本章所有表示球面或半球面半径的字母 $a$，均约定 $a>0$。

**例 1**　计算 $\iint_\Sigma z\,\mathrm{d}S$，其中 $\Sigma$ 是上半球面 $z=\sqrt{a^2-x^2-y^2}$（$a>0$）。曲面就是 C.26.5 里求过面积的半球面，这次被积函数从 $1$ 换成 $z$，要学的新一步是把 $\mathrm{d}S$ 换成 $\mathrm{d}\sigma$。

投影区域是圆盘 $D:x^2+y^2\le a^2$。导数先在 $z>0$ 处计算；赤道上 $z=0$，曲面竖直，$z_x$ 不存在，留到最后处理。

先算伸缩因子。$z_x=-\dfrac{x}{z}$，$z_y=-\dfrac{y}{z}$，再用曲面方程 $x^2+y^2+z^2=a^2$：

$$1+z_x^2+z_y^2=\frac{z^2+x^2+y^2}{z^2}=\frac{a^2}{z^2},\qquad\mathrm{d}S=\frac{a}{z}\,\mathrm{d}\sigma .$$

为避开赤道，先只算 $z\ge\varepsilon$ 的球面片（$0<\varepsilon<a$）。它的投影是 $x^2+y^2\le a^2-\varepsilon^2$，在这片上可以约去 $z$：

$$\iint_{\Sigma,\ z\ge\varepsilon}z\,\mathrm{d}S=\iint_{x^2+y^2\le a^2-\varepsilon^2}z\cdot\frac{a}{z}\,\mathrm{d}\sigma=a\pi(a^2-\varepsilon^2) .$$

剩下的窄带 $0\le z<\varepsilon$ 上，被积函数不超过 $\varepsilon$，面积不超过整个半球面的面积 $2\pi a^2$，贡献不超过 $2\pi a^2\varepsilon$，随 $\varepsilon\to0$ 趋于 $0$。令 $\varepsilon\to0$，得 $\iint_\Sigma z\,\mathrm{d}S=\pi a^3$。结果也容易看：$z\,\mathrm{d}S=a\,\mathrm{d}\sigma$，积分就是 $a$ 乘投影圆盘的面积 $\pi a^2$。

> 计算 $\iint_\Sigma z\,\mathrm{d}S$，$\Sigma$ 是平面 $x+y+z=1$ 在第一卦限的部分。
>
> 答案：$z=1-x-y$，$z_x=z_y=-1$，$\mathrm{d}S=\sqrt3\,\mathrm{d}\sigma$，投影是三角形 $x,y\ge0$、$x+y\le1$，$\iint_D(1-x-y)\,\mathrm{d}\sigma=\frac16$，结果 $\frac{\sqrt3}6$。

**例 2**　计算 $\oiint_\Sigma(x^2+z)\,\mathrm{d}S$，$\Sigma$ 是球面 $x^2+y^2+z^2=a^2$。

例 1 的半球面这次补成整个球面，被积函数换成 $x^2+z$。整个球面要拆成上下两半才能投影，先看对称性能省多少。

$z$ 这一项：球面关于 $xOy$ 面对称，$z$ 是奇函数，积分为 $0$。

$x^2$ 这一项：球面的方程把 $x,y,z$ 轮换后不变，每一小块搬到轮换后的位置面积不变（把 $(x,y,z)$ 换成 $(y,z,x)$ 是绕一条轴旋转 $120^\circ$，不改变面积），所以 $\oiint x^2\,\mathrm{d}S=\oiint y^2\,\mathrm{d}S=\oiint z^2\,\mathrm{d}S$。三者相加，代入曲面方程：

$$3\oiint_\Sigma x^2\,\mathrm{d}S=\oiint_\Sigma(x^2+y^2+z^2)\,\mathrm{d}S=a^2\oiint_\Sigma\mathrm{d}S=a^2\cdot4\pi a^2 .$$

所以原积分等于 $\dfrac{4\pi a^4}{3}$。

$\mathrm{d}S$ 永远为正，累加的只是数量，分不出方向。可是水流穿过一张网，从这一面穿过去和从那一面穿过来是相反的两件事，下一节要把方向放进积分里。

合上书，说出 $\mathrm{d}S$ 与 $\mathrm{d}\sigma$ 的因子从哪里来，以及为什么能代入曲面方程。

### 2. 每秒有多少水穿过一张斜放的网？

上一节的 $\mathrm{d}S$ 不分方向。现在要数水流穿过一张网的量，方向就是关键。水渠里的水在流，每一点画一个箭头 $\boldsymbol v$，方向是水流向哪里，长度 $\lVert\boldsymbol v\rVert$ 是水每秒走多少米。设处处 $\boldsymbol v$ 相同，渠里放一张面积为 $A$ 的平面网。网面和水流垂直时，一秒钟里穿过网的水填满一个以网为底、高为 $\lVert\boldsymbol v\rVert$ 的柱体。

把网斜过来，记 $\boldsymbol n$ 为网面的单位法向量，它和 $\boldsymbol v$ 的夹角为 $\theta$。这时一秒钟里的水填满一个斜柱体，底面积还是 $A$，高变成 $\lVert\boldsymbol v\rVert\cos\theta$（$\theta$ 为锐角时）。由数量积的定义（C.19.4），

$$\text{每秒穿过的水量}=\lVert\boldsymbol v\rVert\cos\theta\cdot A=(\boldsymbol v\cdot\boldsymbol n)\,A .$$

![一秒钟里穿过网的水填满沿 $\boldsymbol v$ 斜伸出去的柱体，高是 $\boldsymbol v$ 在 $\boldsymbol n$ 上的投影 $\lVert\boldsymbol v\rVert\cos\theta$](fig/C28-n2.pdf){width=60%}

$\theta$ 超过直角时 $\boldsymbol v\cdot\boldsymbol n<0$，水从另一面穿过来，所以要约定 $\boldsymbol n$ 指向的一面为正。本章计算第二类曲面积分时，只考虑能连续选定一侧的曲面：在光滑处，所选单位法向量随点连续变化。图形曲面 $z=z(x,y)$ 可分上侧、下侧，围成立体的闭曲面按内侧、外侧区分。选定一侧，就是在每一点选定指向这一侧的单位法向量 $\boldsymbol n=(\cos\alpha,\cos\beta,\cos\gamma)$，这样的曲面叫**有向曲面**。对 $z=z(x,y)$，上侧是 $\cos\gamma>0$，下侧是 $\cos\gamma<0$。

网是弯的、各处水流不同时，照例切成近似平的小块，穿过它的水量约为 $(\boldsymbol v\cdot\boldsymbol n)\Delta S$，加起来取极限。把水流换成一般的向量场 $\boldsymbol F=(P,Q,R)$，就得到**第二类曲面积分**，也叫对坐标的曲面积分，或 $\boldsymbol F$ 穿过 $\Sigma$ 的通量：

$$\iint_\Sigma\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S=\iint_\Sigma(P\cos\alpha+Q\cos\beta+R\cos\gamma)\,\mathrm{d}S .$$

习惯上把 $\cos\alpha\,\mathrm{d}S$、$\cos\beta\,\mathrm{d}S$、$\cos\gamma\,\mathrm{d}S$（它们分别是小块在 $yOz$、$zOx$、$xOy$ 面上的带符号投影面积）分别记成 $\mathrm{d}y\mathrm{d}z$、$\mathrm{d}z\mathrm{d}x$、$\mathrm{d}x\mathrm{d}y$，于是上式写成

$$\iint_\Sigma P\,\mathrm{d}y\mathrm{d}z+Q\,\mathrm{d}z\mathrm{d}x+R\,\mathrm{d}x\mathrm{d}y .$$

$\gamma$ 是 $\boldsymbol n$ 与 $z$ 轴的夹角，所以 $\mathrm{d}x\mathrm{d}y=\cos\gamma\,\mathrm{d}S$ 是小块在 $xOy$ 面上的有向投影：大小是投影面积，上侧为正，下侧为负。三个记号各管一个坐标面，符号各看法向量的一个分量：

| 记号 | 等于 | 投到哪个面 | 为正的一侧 |
|---|---|---|---|
| $\mathrm{d}y\mathrm{d}z$ | $\cos\alpha\,\mathrm{d}S$ | $yOz$ 面 | $\boldsymbol n$ 指向 $+x$ 方向（$\cos\alpha>0$） |
| $\mathrm{d}z\mathrm{d}x$ | $\cos\beta\,\mathrm{d}S$ | $zOx$ 面 | $\boldsymbol n$ 指向 $+y$ 方向（$\cos\beta>0$） |
| $\mathrm{d}x\mathrm{d}y$ | $\cos\gamma\,\mathrm{d}S$ | $xOy$ 面 | $\boldsymbol n$ 指向 $+z$ 方向（$\cos\gamma>0$） |

它们和永远为正的 $\mathrm{d}\sigma$ 不是一回事。

把两类积分并排看：第一类不选侧，面积元 $\mathrm{d}S$ 永远为正；第二类要先选侧，换到另一侧时整个积分变号。

怎样算？先看 $\iint_\Sigma R\,\mathrm{d}x\mathrm{d}y$。由第 1 节的图，$\mathrm{d}\sigma=|\cos\gamma|\,\mathrm{d}S$，所以上侧 $\cos\gamma\,\mathrm{d}S=\mathrm{d}\sigma$，下侧 $\cos\gamma\,\mathrm{d}S=-\mathrm{d}\sigma$：

$$\iint_\Sigma R\,\mathrm{d}x\mathrm{d}y=\pm\iint_D R\bigl(x,y,z(x,y)\bigr)\,\mathrm{d}\sigma\qquad(\text{上侧取}+,\ \text{下侧取}-).$$

另外两项照样投到 $yOz$、$zOx$ 面。竖直的柱面投到 $xOy$ 面只剩一条曲线，所以它上面的 $\iint R\,\mathrm{d}x\mathrm{d}y=0$。

三项分别投影很累。$\Sigma$ 是 $z=z(x,y)$ 时有捷径：上侧的单位法向量是 $(-z_x,-z_y,1)$ 除以长度，再乘 $\mathrm{d}S=\sqrt{1+z_x^2+z_y^2}\,\mathrm{d}\sigma$，根号约掉：

$$\boldsymbol n\,\mathrm{d}S=(-z_x,-z_y,1)\,\mathrm{d}\sigma\qquad(\text{上侧}).$$

于是三项可以一次投影到 $xOy$ 面（合一投影）：

$$\iint_\Sigma P\,\mathrm{d}y\mathrm{d}z+Q\,\mathrm{d}z\mathrm{d}x+R\,\mathrm{d}x\mathrm{d}y=\pm\iint_D\bigl(-Pz_x-Qz_y+R\bigr)\,\mathrm{d}\sigma ,$$

上侧取正号，下侧取负号，$P,Q,R$ 里的 $z$ 都换成 $z(x,y)$。

**方法 2（第二类曲面积分的投影计算）**

1. 定侧：上侧还是下侧、外侧还是内侧，写下 $\cos\gamma$ 的符号。
2. 选路线：只有一项或曲面平行于坐标面，就分项投影；$z=z(x,y)$ 且三项都有，就合一投影。
3. 把曲面方程代入被积函数，写出 $D$，按侧定正负号，算二重积分。

**例 3**　计算 $\iint_\Sigma(z+1)\,\mathrm{d}x\mathrm{d}y$，$\Sigma$ 是抛物面 $z=x^2+y^2$（$x^2+y^2\le1$）的下侧。

例 1 的 $\mathrm{d}S$ 不分方向，这里换成第二类积分，被积函数只有 $R$ 一项，新的一步是定侧：下侧要取负号。这个抛物面例 4 还会用到。

第一步，定号。下侧取负号，$D:x^2+y^2\le1$，把 $z$ 换成 $x^2+y^2$：

$$\iint_\Sigma(z+1)\,\mathrm{d}x\mathrm{d}y=-\iint_D(x^2+y^2+1)\,\mathrm{d}\sigma .$$

第二步，换极坐标，面积元要带 $r$：

$$-\int_0^{2\pi}\!\mathrm{d}\theta\int_0^1(r^2+1)\,r\,\mathrm{d}r .$$

第三步，里层 $\int_0^1(r^3+r)\,\mathrm{d}r=\frac14+\frac12=\frac34$，再乘 $-2\pi$：

$$\iint_\Sigma(z+1)\,\mathrm{d}x\mathrm{d}y=-\frac{3\pi}{2}.$$

> 计算 $\iint_\Sigma z\,\mathrm{d}x\mathrm{d}y$，$\Sigma$ 是上半球面 $z=\sqrt{a^2-x^2-y^2}$ 的上侧。
>
> 答案：上侧取正号，$\iint_D\sqrt{a^2-r^2}\,\mathrm{d}\sigma=2\pi\int_0^a\sqrt{a^2-r^2}\,r\,\mathrm{d}r=\frac{2\pi a^3}3$。

**例 4**　求 $\boldsymbol F=(x,y,z)$ 穿过抛物面 $\Sigma:z=x^2+y^2$（$0\le z\le1$）的通量，$\Sigma$ 取下侧。

曲面和侧都沿用例 3，被积函数从 $(z+1)\,\mathrm{d}x\mathrm{d}y$ 换成 $\boldsymbol F=(x,y,z)$ 的三项，所以改用合一投影。$z_x=2x$，$z_y=2y$，$R=z$ 换成 $x^2+y^2$：

$$-Pz_x-Qz_y+R=-2x^2-2y^2+(x^2+y^2)=-(x^2+y^2).$$

下侧取负号，换极坐标：

$$\iint_\Sigma\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S=-\iint_D\bigl(-(x^2+y^2)\bigr)\,\mathrm{d}\sigma=\int_0^{2\pi}\!\mathrm{d}\theta\int_0^1r^3\,\mathrm{d}r=\frac{\pi}{2}.$$

例 4 的曲面只有一张，投影一次就够。球面或立方体表面这样的闭曲面要分成好几片，每片的投影和正负号都得单独处理，下一节找一条捷径。

合上书，从斜柱体推出 $(\boldsymbol v\cdot\boldsymbol n)A$，再写出上侧的 $\boldsymbol n\,\mathrm{d}S$。

### 3. 闭曲面上往外流的总量，能不能换成内部的积分？

闭曲面由好几片拼成，逐片投影很累。先在一个最简单的闭曲面上看看有没有捷径：取 $\boldsymbol F=(x,y,z)$，立方体 $[0,1]^3$ 的表面取外侧：面 $x=1$ 上 $\boldsymbol F\cdot\boldsymbol n=1$，面 $x=0$ 上为 $0$，其余四个面同理，合计 $3$，恰好是 $P_x+Q_y+R_z=3$ 乘体积 $1$。

**高斯公式**　设空间有界闭区域 $\Omega$ 的边界 $\Sigma$ 由分片光滑的曲面组成，取外侧；$P,Q,R$ 在包含 $\Omega$ 及其边界的开区域内有连续的一阶偏导数，则

$$\oiint_\Sigma P\,\mathrm{d}y\mathrm{d}z+Q\,\mathrm{d}z\mathrm{d}x+R\,\mathrm{d}x\mathrm{d}y=\iiint_\Omega\Bigl(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}+\frac{\partial R}{\partial z}\Bigr)\mathrm{d}V .$$

场的光滑条件是充分条件；若场在立体内部有一点没有定义，公式可能失效，第 4 节末尾有例子。立方体里的计算说明公式在一个简单情形成立，下面说明一般情形的原因。

思路：三项各自成立。只证 $R$ 那一项，用的是牛顿–莱布尼茨公式。

第一步，设 $\Omega$ 是「上下各一张曲面」的形状，$z_1(x,y)\le z\le z_2(x,y)$，$(x,y)\in D$。右边用先一后二（C.26.2），对 $z$ 积分：

$$\iiint_\Omega\frac{\partial R}{\partial z}\,\mathrm{d}V=\iint_D\Bigl[R\bigl(x,y,z_2(x,y)\bigr)-R\bigl(x,y,z_1(x,y)\bigr)\Bigr]\mathrm{d}\sigma .$$

第二步，算左边的 $\iint_\Sigma R\,\mathrm{d}x\mathrm{d}y$：拆成三块，逐块用第 2 节的投影公式。

- 顶面的外侧是上侧，得 $\iint_DR(x,y,z_2)\,\mathrm{d}\sigma$；
- 底面的外侧是下侧，得 $-\iint_DR(x,y,z_1)\,\mathrm{d}\sigma$；
- 竖直的侧面，法向量的 $z$ 分量为零，贡献 $0$。

三块相加，正是第一步的结果。

第三步，若区域在 $x$ 方向由两张曲面 $x=x_1(y,z)$、$x=x_2(y,z)$ 夹住，就对 $x$ 使用牛顿–莱布尼茨公式，得到 $P$ 项的等式：右边是 $\iint\bigl[P(x_2,y,z)-P(x_1,y,z)\bigr]\mathrm{d}y\mathrm{d}z$，左边把 $\Sigma$ 按左右两片投影到 $yOz$ 面：$x_2$ 片的外法向朝 $+x$ 方向，$\cos\alpha>0$，取 $+\iint P(x_2,y,z)\,\mathrm{d}y\mathrm{d}z$；$x_1$ 片的外法向朝 $-x$ 方向，取 $-\iint P(x_1,y,z)\,\mathrm{d}y\mathrm{d}z$；侧面法向的 $x$ 分量为零，贡献 $0$。相加就是右边，和第二步一样。若区域在 $y$ 方向由前后两张曲面夹住，同样得到 $Q$ 项的等式。三个方向要分别检查形状，不能由一个方向的条件推出另外两个方向的条件。

第四步，对能分成有限个上述小区域的情形，逐块相加。每个切口在相邻两块上的外法向量相反，同一个场的通量一正一负，恰好抵消，只剩原来的外边界。

更一般的分片光滑边界，用越来越细的小面片近似，内部公共面的抵消仍然保留，让近似误差趋于零就得到公式。这里只说明公式的来源，不断言任意曲面都能有限分块。

曲面本身不闭合时怎么办？可补上一张或几张曲面，使它们围成一个立体；边界在平面内时常选平面片。先统一按该立体的外侧计算，再减去补面的通量。

**方法 3（高斯公式与补面）**

1. 检查 $\Sigma$ 是否闭合、是否取外侧；给的是内侧，最后整体变号。
2. 检查场在立体及其边界附近是否有连续的一阶偏导数。若只有内部个别点不满足，可先挖去完全位于内部、包住这些点的小球，再检查剩余区域能否使用公式，小球面上的通量也必须计入（第 4 节）；挖球只对内部的孤立点有效：无定义的点落在 $\Sigma$ 上时，$\Sigma$ 上的通量本身没有定义；无定义的是一整条线时，小球包不住它，要改挖包住整条线的细管。
3. 不闭就补面。缺口不止一处时，每个开口各补一张（例如第一卦限里的一块斜面，要补三张坐标平面上的三角形），每张补面的侧都要使它和原曲面合起来是 $\Omega$ 的外侧。
4. 算 $P_x+Q_y+R_z$ 的三重积分，减去补面上的积分。

**例 5**　曲面还是例 2 的球面，取外侧，积分换成第二类。计算 $\oiint_\Sigma x^3\,\mathrm{d}y\mathrm{d}z+y^3\,\mathrm{d}z\mathrm{d}x+z^3\,\mathrm{d}x\mathrm{d}y$，$\Sigma$ 是球面 $x^2+y^2+z^2=a^2$ 的外侧。

逐片投影要分上下两半球面和三个方向，很繁。这里 $P_x+Q_y+R_z=3(x^2+y^2+z^2)=3\rho^2$。球坐标中 $\mathrm{d}V=\rho^2\sin\varphi\,\mathrm{d}\rho\,\mathrm{d}\varphi\,\mathrm{d}\theta$，与 $3\rho^2$ 相乘得 $3\rho^4\sin\varphi$，范围是 $0\le\rho\le a$、$0\le\varphi\le\pi$、$0\le\theta\le2\pi$：

$$\iiint_\Omega3\rho^2\,\mathrm{d}V=3\int_0^{2\pi}\mathrm{d}\theta\int_0^\pi\sin\varphi\,\mathrm{d}\varphi\int_0^a\rho^4\,\mathrm{d}\rho=\frac{12\pi a^5}{5} .$$

> 计算 $\oiint_\Sigma x\,\mathrm{d}y\mathrm{d}z+y\,\mathrm{d}z\mathrm{d}x+z\,\mathrm{d}x\mathrm{d}y$，$\Sigma$ 是同一个球面的外侧。
>
> 答案：$P_x+Q_y+R_z=3$，积分化为 $3$ 乘球的体积 $\frac43\pi a^3$，结果 $4\pi a^3$。

**例 6**　用高斯公式重算例 4。例 4 的曲面不闭合，所以要补面。

在碗口补一张圆盘 $\Sigma_1:z=1$（$x^2+y^2\le1$）。$\Sigma$ 取下侧，对碗围成的立体 $\Omega$ 朝外；$\Sigma_1$ 也要朝外，取上侧。

三重积分：$P_x+Q_y+R_z=3$，体积用柱面坐标算，

$$\iiint_\Omega3\,\mathrm{d}V=3\int_0^{2\pi}\!\mathrm{d}\theta\int_0^1(1-r^2)\,r\,\mathrm{d}r=3\cdot2\pi\cdot\frac14=\frac{3\pi}{2}.$$

补面：$\Sigma_1$ 是水平的，在 $yOz$、$zOx$ 面上投影面积为 $0$，只剩 $\iint_{\Sigma_1}z\,\mathrm{d}x\mathrm{d}y$，上侧取正号、$z=1$，得 $\pi$。

所以 $\iint_\Sigma=\frac{3\pi}{2}-\pi=\frac{\pi}{2}$，和例 4 一致。

回到开头的体积问题。取 $\boldsymbol F=(x,y,z)$，$\operatorname{div}\boldsymbol F=3$，高斯公式给出 $V=\frac13\oiint_\Sigma x\,\mathrm{d}y\mathrm{d}z+y\,\mathrm{d}z\mathrm{d}x+z\,\mathrm{d}x\mathrm{d}y$。三角网格的每一片是平面片。在这片上取一个固定点 $\boldsymbol c$，再把片上任意点的位置向量记作 $\boldsymbol x$，则 $\boldsymbol x-\boldsymbol c$ 在平面内、垂直于 $\boldsymbol n$，于是 $\boldsymbol F\cdot\boldsymbol n=\boldsymbol c\cdot\boldsymbol n=h$ 是常数，$h$ 是原点到这片所在平面的带符号距离。这一片的通量是 $hA$（$A$ 为面积），所以 $V=\frac13\sum hA$，每项正是以原点为顶、这一片为底的锥体体积 $\frac13\times$ 底面积 $\times$ 高；原点在立体外时有些 $h$ 为负，多算的部分会抵消。单位立方体有三个面过原点（$h=0$），另三个面 $h=1$、$A=1$，得 $V=\frac13\cdot3=1$。

高斯公式只管闭曲面上的流量，而散度这个被积函数本身代表什么，还没有说清。

合上书，用「上下两张曲面」推一遍 $R$ 那一项的高斯公式。

### 4. 一点处「往外冒」的强度有多大？

第 3 节开头的例子里，$\boldsymbol F=(x,y,z)$ 穿出单位立方体的总量是 $3$，体积是 $1$。换成边长 $\ell$ 的小立方体，穿出总量是 $3\ell^3$，体积是 $\ell^3$，每单位体积冒出的量仍是 $3$，正好等于 $P_x+Q_y+R_z$。一般的场也是这样吗？

把高斯公式右边的被积函数记作

$$\operatorname{div}\boldsymbol F=\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}+\frac{\partial R}{\partial z},$$

叫做 $\boldsymbol F$ 的**散度**。

它衡量什么？在点 $M$ 周围取一个很小的球 $\Omega_\varepsilon$，体积为 $\Delta V$，球面 $S_\varepsilon$ 取外侧。由高斯公式和三重积分的中值定理（C.26.1），球里有一点 $M^*$ 使

$$\oiint_{S_\varepsilon}\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S=\iiint_{\Omega_\varepsilon}\operatorname{div}\boldsymbol F\,\mathrm{d}V=\operatorname{div}\boldsymbol F(M^*)\,\Delta V .$$

两边除以 $\Delta V$，让小球缩到 $M$，右边趋于 $\operatorname{div}\boldsymbol F(M)$（这里用到 $\operatorname{div}\boldsymbol F$ 连续：$M^*\to M$ 时 $\operatorname{div}\boldsymbol F(M^*)\to\operatorname{div}\boldsymbol F(M)$）。所以散度是小球净流出量除以体积、再把球缩到 $M$ 所得的极限，也就是 $M$ 附近单位体积的净流出量。拿水流来想，散度为正的点像泉眼，在往外冒水；为负的点像下水口，在往里吸水；散度为零则没有这种局部的流出或流入趋势。

在一个点散度为零，不保证包住它的每个小球都恰好进出相等，极限只在球缩到该点时才成立。若立体内部处处散度为零，且满足高斯公式的条件，它的闭边界总通量就等于零。

高斯公式是一句记账的话：边界流出的总量，等于内部各点冒出量之和。

回到开头的小格子。设 $\boldsymbol F$ 是空气的质量流（密度乘速度），格子内部没有来源时，质量每秒的增加量等于净流入，即 $-\oiint\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S\approx-\operatorname{div}\boldsymbol F\cdot\Delta V$。除以体积，密度每秒的变化率就是 $-\operatorname{div}\boldsymbol F$：哪里散度为正，哪里的空气就在变稀。

散度处处为零，穿过闭曲面的通量就一定是零吗？看 $\frac{(x,y,z)}{r^3}$（$r$ 是到原点的距离）：原点以外散度为 $0$，原点处没有定义。若场只在区域内部的一个孤立点无定义，而在其余位置满足高斯公式的条件，可以先挖去包住该点、完全位于内部的小球，在球面与 $\Sigma$ 之间的夹层里用公式。

先猜一猜：以原点为心的小球面，半径 $\varepsilon$ 越小，面积越小，通量会不会也越小？

先算小球。取以原点为心、半径 $\varepsilon$ 的小球面，外侧单位法向量是 $\boldsymbol n=(x,y,z)/\varepsilon$，$\boldsymbol F\cdot\boldsymbol n=\frac1{\varepsilon^2}$，球面面积 $4\pi\varepsilon^2$，所以通量是 $\frac1{\varepsilon^2}\cdot4\pi\varepsilon^2=4\pi$，与 $\varepsilon$ 无关：面积缩小到 $\varepsilon^2$ 倍，场强正好放大到 $\frac1{\varepsilon^2}$ 倍。

再对夹层用公式。设 $\Sigma$ 是任意包住原点的闭曲面（取外侧），在 $\Sigma$ 和小球面之间的夹层里 $\operatorname{div}\boldsymbol F=0$，由高斯公式，夹层边界的总通量为 $0$。夹层的内边界是小球面，它相对夹层的外侧指向球心，通量是 $-4\pi$，所以

$$\iint_\Sigma\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S-4\pi=0,\qquad\text{即}\qquad\iint_\Sigma\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S=4\pi .$$

所以包住原点的任何闭曲面，通量都是 $4\pi$，而不是散度积分给出的 $0$。这是去掉「场在整个立体内有连续偏导数」条件会出错的例子：仅仅一个点没有定义，公式就失效。

散度只管闭曲面上的流量。许多量是沿一圈铁丝走一遍累加出来的，那是曲线积分，需要另一个公式。

合上书，从「小球上的高斯公式除以体积」推出散度的意义。

### 5. 空间里沿闭曲线绕一圈的积分，能不能换成曲面积分？

格林公式（C.27.3）把平面闭曲线上的积分换成所围区域上的二重积分。先看最简单的情形：$\Gamma$ 在 $xOy$ 面上逆时针走一圈，这时 $\mathrm{d}z=0$，积分只剩 $\oint P\,\mathrm{d}x+Q\,\mathrm{d}y$，等于 $\iint(Q_x-P_y)\,\mathrm{d}x\mathrm{d}y$。曲线一旦离开这个平面，$R$ 这一项和 $z$ 的变化都要参与进来。现在考虑空间中的闭曲线 $\Gamma$。有些曲线仍在同一个平面内，例如球面与斜平面的交线，可以选它围成的平面圆盘来算；另一些曲线不在任何一个平面内，需要选一张以它为边界的弯曲曲面，像肥皂膜蒙在弯曲的铁丝圈上。斯托克斯公式把这两种情形放在同一个公式里。

**斯托克斯公式**　设 $\Sigma$ 是有界的分片光滑有向曲面，边界 $\Gamma$ 由有限条分段光滑的闭曲线组成。$P,Q,R$ 在包含整张曲面的开区域内有连续的一阶偏导数；曲面的侧与每条边界的走向按下面的规则配对。那么

$$\oint_\Gamma P\,\mathrm{d}x+Q\,\mathrm{d}y+R\,\mathrm{d}z=\iint_\Sigma\Bigl(\frac{\partial R}{\partial y}-\frac{\partial Q}{\partial z}\Bigr)\mathrm{d}y\mathrm{d}z+\Bigl(\frac{\partial P}{\partial z}-\frac{\partial R}{\partial x}\Bigr)\mathrm{d}z\mathrm{d}x+\Bigl(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\Bigr)\mathrm{d}x\mathrm{d}y .$$

公式右边的三个括号各是一个坐标面上的有向投影的系数，它们合起来是旋度（第 6 节），这里先把它们逐个写出。

定向规则：右手四指顺着边界的走向弯曲，拇指指向所选法向；等价地说，沿边界前进、头朝所选法向时，曲面在左手边。对弯曲曲面，在每一点附近把曲面看成它的切平面，用同样的办法判断。

![碗形曲面 $\Sigma$ 取上侧（箭头 $\boldsymbol n$），边界 $\Gamma$ 从上往下看逆时针走；沿 $\Gamma$ 走、头朝 $\boldsymbol n$，曲面在左手边](fig/C28-n3.pdf){width=58%}

核对一下：$\Sigma$ 是 $xOy$ 面上的区域、取上侧（法向朝上）时，$\Gamma$ 逆时针走，$\mathrm{d}z=0$，$\mathrm{d}y\mathrm{d}z$、$\mathrm{d}z\mathrm{d}x$ 为 $0$，只剩最后一项，正是格林公式。

为什么对？先看上侧的图形曲面 $z=h(x,y)$，并设 $h$ 的二阶偏导数连续。沿曲面上的曲线有 $\mathrm{d}z=h_x\,\mathrm{d}x+h_y\,\mathrm{d}y$，边界积分便化为投影平面内的

$$\oint_{\partial D}(P+Rh_x)\,\mathrm{d}x+(Q+Rh_y)\,\mathrm{d}y .$$

$\partial D$ 表示投影区域的边界，这里 $P,Q,R$ 都先把 $z$ 换成 $h(x,y)$。对它用格林公式，需要 $\frac{\partial}{\partial x}(Q+Rh_y)-\frac{\partial}{\partial y}(P+Rh_x)$。求导时 $P,Q,R$ 里的 $z=h(x,y)$ 也在变，按复合函数求导：

$$\frac{\partial}{\partial x}(Q+Rh_y)=Q_x+Q_zh_x+(R_x+R_zh_x)h_y+Rh_{yx},$$

$$\frac{\partial}{\partial y}(P+Rh_x)=P_y+P_zh_y+(R_y+R_zh_y)h_x+Rh_{xy} .$$

两式相减，$R_zh_xh_y$ 和 $R_zh_yh_x$ 相消，$Rh_{yx}$ 与 $Rh_{xy}$ 也相消（$h$ 的二阶偏导连续，混合偏导相等），得到

$$-(R_y-Q_z)h_x-(P_z-R_x)h_y+(Q_x-P_y) .$$

这正是公式右边的三个系数与上侧的向量面积元 $(-h_x,-h_y,1)\,\mathrm{d}\sigma$ 作数量积所得的式子。

对能分成这种曲面片的曲面，逐片应用再相加：抵消的是原曲面上同一条公共边的两个反向积分，它们严格相等、符号相反，最后只剩外边界 $\Gamma$。需要近似处理的分片光滑曲面，让近似误差趋于零，仍保留同一个公式。

**方法 4（斯托克斯公式）**

1. 找一张以 $\Gamma$ 为边界、便于计算的有向曲面 $\Sigma$，并检查场在整张曲面附近是否满足公式条件；交线问题常取其中的平面片。
2. 按边界走向定侧。选的是平面片，或能向相应坐标面单值投影的曲面片时，从该坐标轴正向看为逆时针，对应法向在这根轴上的分量为正；投影重叠时，不能只凭整体看起来的顺、逆时针判断。
3. 算三个括号，再算曲面积分。$\Sigma$ 是平面时，用单位法向量化成第一类积分，常常是常数乘面积；面积不好求就用第 2 节的合一投影。

**例 7**　$\Gamma$ 是例 2 的球面被一张过球心的平面截出的大圆，它的参数方程很难写，改在它围成的平面圆盘上算。计算 $\oint_\Gamma y\,\mathrm{d}x+z\,\mathrm{d}y+x\,\mathrm{d}z$，$\Gamma$ 是球面 $x^2+y^2+z^2=a^2$ 与平面 $x+y+z=0$ 的交线，从 $x$ 轴正向看去为逆时针。

平面过球心，$\Gamma$ 围住平面上一块半径为 $a$ 的圆盘，取它为 $\Sigma$。从 $x$ 轴正向看去逆时针，法向指向 $x$ 增大的一边，取 $\boldsymbol n=\frac{1}{\sqrt3}(1,1,1)$。

算偏导数：$P=y$，$Q=z$，$R=x$，

$$R_y-Q_z=0-1=-1,\qquad P_z-R_x=0-1=-1,\qquad Q_x-P_y=0-1=-1 .$$

被积函数是常数：

$$\oint_\Gamma y\,\mathrm{d}x+z\,\mathrm{d}y+x\,\mathrm{d}z=\iint_\Sigma\frac{-1-1-1}{\sqrt3}\,\mathrm{d}S=-\sqrt3\cdot\pi a^2 .$$

> 计算 $\oint_\Gamma z\,\mathrm{d}x+x\,\mathrm{d}y+y\,\mathrm{d}z$，$\Gamma$ 是平面 $x+y+z=1$ 与三个坐标平面的交线围成的三角形边界，从 $z$ 轴正向看为逆时针。
>
> 答案：三个偏导差 $R_y-Q_z$、$P_z-R_x$、$Q_x-P_y$ 分别为 $1,1,1$。取上侧单位法向 $\boldsymbol n=(1,1,1)/\sqrt3$，数量积为 $\sqrt3$；三角形面积为 $\frac{\sqrt3}2$，所以积分为 $\frac32$。

斯托克斯公式右边那三个括号反复出现，该给它们一个名字，也该问问它们在一点处代表什么，就像散度那样。

合上书，用右手法则给一张曲面和它的边界配一次方向，再说出怎样退化成格林公式。

### 6. 一点处「打转」的强度有多大？

先看一个会打转的场 $\boldsymbol F_1=(-y,x,0)$，箭头绕 $z$ 轴逆时针转圈。沿 $xOy$ 面上的单位圆逆时针走一圈，$\boldsymbol r=(\cos t,\sin t,0)$，$\boldsymbol F_1\cdot\mathrm{d}\boldsymbol r=(\sin^2t+\cos^2t)\,\mathrm{d}t=\mathrm{d}t$，一圈的积分是 $2\pi$。圆盘面积是 $\pi$，单位面积的环流是 $2$，恰好是 $Q_x-P_y=1-(-1)$。

斯托克斯公式右边的三个括号排成的向量，叫 $\boldsymbol F$ 的**旋度**。它可以借三阶行列式（C.19.6）记：按第一行展开，把「$\frac{\partial}{\partial y}$ 乘 $R$」理解成求偏导 $\frac{\partial R}{\partial y}$，

$$\operatorname{rot}\boldsymbol F=\begin{vmatrix}\boldsymbol i&\boldsymbol j&\boldsymbol k\\[2pt]\dfrac{\partial}{\partial x}&\dfrac{\partial}{\partial y}&\dfrac{\partial}{\partial z}\\[6pt]P&Q&R\end{vmatrix}=\bigl(R_y-Q_z,\ P_z-R_x,\ Q_x-P_y\bigr).$$

把 $P\,\mathrm{d}x+Q\,\mathrm{d}y+R\,\mathrm{d}z$ 简写成 $\boldsymbol F\cdot\mathrm{d}\boldsymbol r$（C.27.2），斯托克斯公式就是

$$\oint_\Gamma\boldsymbol F\cdot\mathrm{d}\boldsymbol r=\iint_\Sigma\operatorname{rot}\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S .$$

左边叫环流量：沿闭曲线，把场在前进方向上的分量乘相应的小段长度，再加起来；顺着走的贡献为正，逆着走的贡献为负。

在点 $M$ 处，以单位向量 $\boldsymbol n$ 为法向取一个小圆盘 $D_\varepsilon$，面积为 $\Delta S$，边界按对应的正向走。由斯托克斯公式，右边除以面积就是 $\operatorname{rot}\boldsymbol F\cdot\boldsymbol n$ 在圆盘上的平均值；再由旋度的连续性，圆盘缩小时这个平均值趋于该点的值：

$$\lim_{\varepsilon\to0}\frac{1}{\Delta S}\oint_{\partial D_\varepsilon}\boldsymbol F\cdot\mathrm{d}\boldsymbol r=\operatorname{rot}\boldsymbol F(M)\cdot\boldsymbol n .$$

这里 $\partial D_\varepsilon$ 表示小圆盘的边界。右边衡量沿这个法向观察时，单位面积环流的局部大小和正负。旋度非零时，$\boldsymbol n$ 与旋度同向，这个数值最大。

**例 8**　沿用上面的 $\boldsymbol F_1=(-y,x,0)$，再和 $\boldsymbol F_2=(x,y,0)$ 对照，求两者的散度和旋度。

$\boldsymbol F_1$ 的 $P=-y$，$Q=x$，$R=0$。散度 $\operatorname{div}\boldsymbol F_1=0+0+0=0$；旋度的三个偏导差是 $R_y-Q_z=0$，$P_z-R_x=0$，$Q_x-P_y=1-(-1)=2$，所以 $\operatorname{rot}\boldsymbol F_1=(0,0,2)$。箭头绕 $z$ 轴转圈，只打转不往外冒。

$\boldsymbol F_2$ 的 $P=x$，$Q=y$，$R=0$。散度 $1+1+0=2$，三个偏导差全为 $0$，旋度 $\boldsymbol 0$。箭头向外辐射，只往外冒不打转。

旋度的重要性质是**梯度场的旋度为零**。若 $\boldsymbol F=\nabla u=(u_x,u_y,u_z)$，$u$ 的二阶偏导数连续，则旋度的第一个分量 $R_y-Q_z=u_{zy}-u_{yz}=0$，因为混合偏导数与求导次序无关（C.20.8）；另外两个分量也是一对混合偏导数相减。

反过来，旋度为零能不能保证积分与路径无关？这要看区域。设开区域 $G$ **曲面单连通**，即 $G$ 内任何分段光滑的闭曲线都能张出一张完全落在 $G$ 内、以它为边界的分片光滑有向曲面（整个空间、开球都是；挖掉一条直线的空间不是：绕这条直线转一圈的闭曲线，任何以它为边界的曲面都必须穿过这条直线，从而跑出 $G$），$P,Q,R$ 在 $G$ 内有连续的一阶偏导数。那么下面四条等价：

1. 沿 $G$ 内任意闭曲线的积分为 $0$；
2. 积分只与起点、终点有关；
3. $P\,\mathrm{d}x+Q\,\mathrm{d}y+R\,\mathrm{d}z$ 是某个函数 $u$ 的全微分；
4. 在 $G$ 内处处 $\operatorname{rot}\boldsymbol F=\boldsymbol 0$。

四条按 $1\Rightarrow2\Rightarrow3\Rightarrow4\Rightarrow1$ 绕一圈推回来（顺序同 C.27.4），曲面单连通只在最后一步 $4\Rightarrow1$ 用到：

- $1\Rightarrow2$：两条路一正一反拼成闭曲线；
- $2\Rightarrow3$：取 $u$ 为从固定起点出发的积分，它的三个偏导就是 $P,Q,R$（见下面单独的说明）；
- $3\Rightarrow4$：梯度场的旋度为零，上面刚证过（由 $u_x=P,u_y=Q,u_z=R$ 和 $P,Q,R$ 的一阶偏导连续，$u$ 的二阶偏导连续，所以可以交换混合偏导的次序）；
- $4\Rightarrow1$：闭曲线能张出 $G$ 内的曲面（这就是曲面单连通），由斯托克斯公式，积分等于旋度的面积分，为 $0$。

曲面单连通不能去掉。取 $\boldsymbol F=\dfrac{(-y,x,0)}{x^2+y^2}$，在挖掉 $z$ 轴的空间里 $\operatorname{rot}\boldsymbol F=\boldsymbol0$，但沿单位圆逆时针走一圈，$\boldsymbol F\cdot\mathrm{d}\boldsymbol r=\mathrm{d}t$，积分是 $2\pi$，不是 $0$。

$2\Rightarrow3$ 的细节：固定起点，把到 $(x,y,z)$ 的积分记为 $u(x,y,z)$，路径无关保证这个定义不随路线改变。因为 $G$ 是开区域，对足够小的 $h$，可把到 $(x+h,y,z)$ 的路径取成：先沿原来到 $(x,y,z)$ 的路，再沿平行于 $x$ 轴的直线段走到 $(x+h,y,z)$，这一小段仍在 $G$ 内。由路径无关，$u(x+h,y,z)$ 就等于这两段积分之和。于是

$$u(x+h,y,z)-u(x,y,z)=\int_x^{x+h}P(t,y,z)\,\mathrm{d}t .$$

两边除以 $h$，由 $P$ 连续，令 $h\to0$ 得 $u_x=P$。沿另两个坐标方向同样得到 $u_y=Q$，$u_z=R$，所以所给式子就是 $\mathrm{d}u$。

**方法 5（空间曲线积分与路径无关）**

1. 算 $\operatorname{rot}\boldsymbol F$，检查区域是否曲面单连通。
2. 旋度为零且区域条件满足时，固定起点，在区域内选一条通向 $(x,y,z)$ 的路径，沿它积分得到 $u$。整个空间内可以选坐标折线 $(x_0,y_0,z_0)\to(x,y_0,z_0)\to(x,y,z_0)\to(x,y,z)$。在其他区域内，先检查三段是否都留在区域里。球体等凸区域保证两点之间的直线段留在区域内，可以改走直线段；它们并不保证上面的坐标折线留在区域内。
3. 从 $A$ 到 $B$ 的积分等于 $u(B)-u(A)$。

**例 9**　例 8 的 $\boldsymbol F_1$ 旋度不为零，不可能是梯度场；这一道检验旋度为零的情形，并把 $u$ 找回来。判断 $(2xy+z^3)\,\mathrm{d}x+x^2\,\mathrm{d}y+3xz^2\,\mathrm{d}z$ 是不是某个函数 $u$ 的全微分；如果是，求出 $u$，并求从 $(0,0,0)$ 到 $(1,1,1)$ 的积分。

先算旋度：

$$R_y-Q_z=0-0=0,\qquad P_z-R_x=3z^2-3z^2=0,\qquad Q_x-P_y=2x-2x=0 .$$

整个空间是曲面单连通的，所以它是全微分。

再求 $u$。沿折线 $(0,0,0)\to(x,0,0)\to(x,y,0)\to(x,y,z)$ 走，每段只有一个坐标在变：第一段被积的是 $P(t,0,0)=0$，第二段是 $Q(x,t,0)=x^2$，第三段是 $R(x,y,t)=3xt^2$。于是

$$u(x,y,z)=\int_0^x0\,\mathrm{d}t+\int_0^yx^2\,\mathrm{d}t+\int_0^z3xt^2\,\mathrm{d}t=x^2y+xz^3 .$$

所求积分为 $u(1,1,1)-u(0,0,0)=2$。

> 判断 $yz\,\mathrm{d}x+xz\,\mathrm{d}y+xy\,\mathrm{d}z$ 是不是全微分；如果是，求 $u$ 和从 $(0,0,0)$ 到 $(1,2,3)$ 的积分。
>
> 答案：三个偏导差 $x-x$、$y-y$、$z-z$ 都是 $0$。沿折线三段，被积分别是 $0$、$0$、$xy$，得 $u=xyz$，积分为 $u(1,2,3)=6$。

到这里，两种积分和两个公式都有了。最后看曲面积分还能算出什么。

合上书，用混合偏导数相等证一次「梯度场的旋度为零」。

### 7. 曲面积分能算出哪些量？

第 1 节刷涂料的屋顶就是一块薄壳。薄壳 $\Sigma$ 每平方米的质量是 $\mu(x,y,z)$（面密度），总质量 $M=\iint_\Sigma\mu\,\mathrm{d}S$。其中密度 $\mu\ge0$，并假设总质量 $M>0$；均匀薄壳指 $\mu$ 是一个正的常数。质心是各点坐标按质量的加权平均（C.26.6）：

$$\bar x=\frac1M\iint_\Sigma x\mu\,\mathrm{d}S,$$

$\bar y$、$\bar z$ 把 $x$ 换成 $y$、$z$ 即可。

**例 10**　求均匀半球面 $z=\sqrt{a^2-x^2-y^2}$ 的质心。

$\mu$ 约掉。半球面关于 $yOz$ 面和 $zOx$ 面对称，所以 $\bar x=\bar y=0$。$\bar z$ 的分子就是例 1 的 $\pi a^3$，分母是半球面面积 $2\pi a^2$：

$$\bar z=\frac{\pi a^3}{2\pi a^2}=\frac a2 .$$

合上书，写出薄壳的质心公式。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（第一类曲面积分的投影计算） | 对面积积分、质心 | C28-01、C28-02 |
| 方法 2（第二类曲面积分的投影计算） | 有向曲面的通量 | C28-01、C28-07、C28-08 |
| 方法 3（高斯公式与补面） | 闭曲面、补面、挖球 | C28-06、C28-07 |
| 方法 4（斯托克斯公式） | 空间闭曲线 | C28-03、C28-08 |
| 方法 5（空间曲线积分与路径无关） | 验旋度、折线求 $u$ | C28-04、C28-05 |

本章在主线上的位置：这是第三、四次见到「内部的总和等于边界上的累积」。本章新增的等价关系：空间里 $\operatorname{rot}\boldsymbol F=\boldsymbol 0$（曲面单连通）⇔ 闭曲线积分为 0 ⇔ 与路径无关 ⇔ $\boldsymbol F$ 是梯度场。四个公式是同一个想法在不同维数上的样子。
