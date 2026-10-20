## P.6 · 多维随机变量（速记）

| 提示 | 内容 |
|---|---|
| 联合分布律 | $p_{ij}=P(X=x_i,Y=y_j)\ge0$，总和为 1；事件的概率 = 圈出的格子相加，格子多时算补集 |
| 联合分布函数与矩形 | $F(x,y)=P(X\le x,Y\le y)$；$P(a<X\le b,c<Y\le d)=F(b,d)-F(a,d)-F(b,c)+F(a,c)$ |
| 联合密度 | $f\ge0$，$\iint f=1$，$P((X,Y)\in D)=\iint_Df$；密度可大于 1，点和曲线的概率为 0（$P(X=Y)=0$）；区域 $G$ 上均匀：$f=\frac1{G\text{ 的面积}}$ |
| 边缘分布 | 离散：行和、列和；连续：$f_X(x)=\int f(x,y)\,\mathrm dy$，积分限常依赖 $x$。边缘不能决定联合 |
| 条件分布 | $p_{i\cdot}>0$ 时 $P(Y=y_j\mid X=x_i)=p_{ij}/p_{i\cdot}$；$f_X(x)>0$ 时 $f_{Y\mid X}(y\mid x)=f(x,y)/f_X(x)$（切口除以切口面积，缩放到面积 1）；乘法公式 $f=f_Xf_{Y\mid X}$ |
| 独立的定义 | $F=F_XF_Y$ ⇔ 离散 $p_{ij}=p_{i\cdot}p_{\cdot j}$ 对每格成立 ⇔ 连续 $f=f_Xf_Y$（忽略点和线上的取值）⇔ 边缘为正处条件分布等于边缘 |
| 连续判独立 | 各自取值范围是区间时，先看区域是否矩形，再看 $f$ 能否写成 $g(x)h(y)$（$8xy$ 在三角形上不独立）；一般以 $f=f_Xf_Y$ 为准，各自取值可由几段区间组成。离散：一个格子为 0 而边缘乘积大于 0，就不独立 |
| 独立的推论 | $X,Y$ 独立 ⇒ $g(X),h(Y)$ 独立；$n$ 个相互独立 ⇒ 分组后各组的函数也独立；$g(X,Y)$ 与 $X$ 一般不独立 |
| 二维正态 | $(X,Y)\sim N(\mu_1,\mu_2;\sigma_1^2,\sigma_2^2;\rho)$（$\sigma_i>0$，$\lvert\rho\rvert<1$）：对指数配方 $x^2-2\rho xy+y^2=(y-\rho x)^2+(1-\rho^2)x^2$；边缘 $N(\mu_i,\sigma_i^2)$；$Y\mid X=x\sim N\bigl(\mu_2+\rho\frac{\sigma_2}{\sigma_1}(x-\mu_1),\ \sigma_2^2(1-\rho^2)\bigr)$；独立 ⇔ $\rho=0$ |
| 老朋友⑦ | $\rho=\frac12$，密度 $\frac1{2\pi\sqrt3}e^{-(x^2-xy+y^2)/3}$；$\frac{X+Y}{\sqrt2}\sim N(0,3)$ 与 $\frac{Y-X}{\sqrt2}\sim N(0,1)$ 独立；$Y\mid X=x\sim N(\frac x2,\frac32)$ |
| 二维分布函数法 | $F_Z(z)=\iint_{g(x,y)\le z}f$：画出 $\{g\le z\}$ 的区域再积分，有密度时分段求导，离散时看跳跃；比值 $X/Y$ 也这样做 |
| 和的卷积公式 | $f_{X+Y}(z)=\int f(x,z-x)\,\mathrm dx$（独立时 $\int f_X(x)f_Y(z-x)\,\mathrm dx$）；离散 $P(Z=z)=\sum_iP(X=x_i,Y=z-x_i)$；积分限要两个密度同时非零 |
| 可加性 | $X\sim P(\lambda_1),Y\sim P(\lambda_2)$ 独立 $\Rightarrow X+Y\sim P(\lambda_1+\lambda_2)$；$X\sim B(n_1,p),Y\sim B(n_2,p)$ 独立 $\Rightarrow X+Y\sim B(n_1+n_2,p)$（$p$ 必须相同）；前两条去掉独立就不成立（$X+X$ 不是泊松）；独立的 $N(\mu_1,\sigma_1^2)+N(\mu_2,\sigma_2^2)=N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$（方差相加） |
| 最大与最小 | 独立：$F_{\max}=\prod F_i$（用 $\le z$），$F_{\min}=1-\prod(1-F_i)$（用 $>z$）；同分布 $F^n$ 与 $1-(1-F)^n$；独立的 $E(\lambda_i)$ 的最小值是 $E(\sum\lambda_i)$；至少两个独立指数变量的最大值不是指数；去掉独立不成立（$Y=X$ 时 $\max=X$，不是 $F^2$） |
