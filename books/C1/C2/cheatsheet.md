## C.2 · 函数的极限（速记）

| 提示 | 内容 |
|---|---|
| $x\to x_0$ 的定义 | $\forall\varepsilon>0\ \exists\delta>0\ \forall x\ (0<\lvert x-x_0\rvert<\delta\Rightarrow\lvert f(x)-A\rvert<\varepsilon)$；只看去心邻域，与 $f(x_0)$ 是否有定义无关；对方给 $\varepsilon$，你回 $\delta$ |
| 用定义证明 | 化简成 $\lvert x-x_0\rvert\cdot\lvert g(x)\rvert$；限制 $\lvert x-x_0\rvert<1$ 给 $g$ 找上界 $K$；取 $\delta=\min\{1,\varepsilon/K\}$；因子在分母上就找下界 |
| 左右极限 | 极限存在 $\iff$ 左、右极限都存在且相等；分段函数的分界点、含绝对值的式子在零点处要分开算 |
| $x\to\infty$ | $\forall\varepsilon\ \exists X\ (\lvert x\rvert>X\Rightarrow\lvert f-A\rvert<\varepsilon)$；$x\to\infty$ 极限存在 $\iff$ $\pm\infty$ 两侧都存在且相等；$x\to\pm\infty$ 的极限给出水平渐近线 |
| 基本事实 | $\frac1{x^p}\to0$（$x\to+\infty$，$p>0$）；$e^x\to+\infty$（$x\to+\infty$），$e^x\to0$（$x\to-\infty$）；$x\to\pm\infty$ 时 $\arctan x\to\pm\frac\pi2$ |
| 归结原理 | $\lim_{x\to x_0}f=A\iff$ 每个 $x_n\to x_0$（$x_n\ne x_0$）都有 $f(x_n)\to A$；$x_n\ne x_0$ 不能去掉；两个数列给出不同的值，或其中一个数列上函数值没有极限，则函数极限不存在（$\sin\frac1x$，狄利克雷函数） |
| 局部性质 | 极限唯一；局部有界；局部保号（后两条只在去心邻域内成立） |
| 运算法则与代换 | 和、积、商（分母极限 $\ne0$）；$\frac00$ 先约分，$\frac\infty\infty$ 同除最高次，根式乘共轭；变量代换要求 $x\ne x_0$ 时 $g(x)\ne u_0$ |
| 第一个重要极限 | $\lim_{x\to0}\frac{\sin x}x=1$（单位圆三块面积夹出 $\cos x<\frac{\sin x}x<1$）；凑出同一个方框 $\frac{\sin u}u$，$u\to0$；不能用洛必达证它（循环论证） |
| 第二个重要极限 | $\lim_{x\to\infty}(1+\frac1x)^x=e$，$\lim_{y\to0}(1+y)^{1/y}=e$；$1^\infty$ 型写成 $(1+u)^v=[(1+u)^{1/u}]^{uv}$，结果 $e^{\lim uv}$；连续复利 $Pe^{rt}$ |
| 无穷小与有界 | $f\to A\iff f=A+\alpha$；有限个无穷小之和是无穷小；有界乘无穷小是无穷小，无界则不行（$x\cdot\frac1{x^2}$）；$x\to0$ 时 $x\sin\frac1x\to0$，$x\to\infty$ 时 $\frac{\sin x}x\to0$ |
| 无穷大与无界 | 无穷大：一个 $\delta$ 内每个 $x$ 都超过 $M$；无界：有些点超过 $M$；无穷大必无界，反之不然（$\frac1x\sin\frac1x$）；无穷大的倒数是无穷小 |
| 无穷小的比较 | $\alpha=o(\beta)$：比值 $\to0$；同阶：比值 $\to c\ne0$；等价 $\sim$：比值 $\to1$；$k$ 阶：$\alpha/x^k\to c\ne0$；$o(x)=x^2$ 不成立，$x^2=o(x)$ 成立 |
| 常用等价（$x\to0$） | $\sin x\sim x$，$\tan x\sim x$，$1-\cos x\sim\frac{x^2}2$，$\sqrt{1+x}-1\sim\frac x2$；$\tan x-\sin x\sim\frac{x^3}2$；另有 $\arcsin x\sim x$，$\arctan x\sim x$，$e^x-1\sim x$，$\ln(1+x)\sim x$，$(1+x)^\alpha-1\sim\alpha x$（$\alpha\ne0$；证明用连续性，见 C.3.4） |
| 等价替换的条件 | 乘除时可整体替换；加减时看主项：$\alpha=o(\beta)$ 则 $\alpha+\beta\sim\beta$，主项相消（$c=-1$）不能换，先有理化或提公因式（$\frac{\tan x-\sin x}{x^3}\to\frac12$，换成 $x-x$ 会错成 $0$） |
