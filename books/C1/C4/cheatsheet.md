## C.4 · 导数（速记）

| 提示 | 内容 |
|---|---|
| 导数的定义 | $f'(x_0)=\lim\limits_{h\to0}\frac{f(x_0+h)-f(x_0)}h=\lim\limits_{x\to x_0}\frac{f(x)-f(x_0)}{x-x_0}$：差商（平均变化率）的极限；单位是 $y$ 的单位除以 $x$ 的单位 |
| 读出导数的极限 | 差商里两点与分母要一致：$\lim\limits_{h\to0}\frac{f(x_0+ah)-f(x_0-bh)}h=(a+b)f'(x_0)$ |
| 切线与法线 | 切线 $y-f(x_0)=f'(x_0)(x-x_0)$；法线斜率 $-\frac1{f'(x_0)}$（$f'(x_0)=0$ 时法线为 $x=x_0$）；切点未知就设 $(t,f(t))$ 列方程 |
| 可导与连续 | 可导 $\Rightarrow$ 连续 $\Rightarrow$ 极限存在，反向都不成立（$\lvert x\rvert$；可去间断点） |
| 左右导数 | 可导 $\iff f'_-=f'_+$；分段点先查连续（不连续一定不可导，两段导函数相同也不行），再用定义算左右导数，不要直接把两段的导函数代入 |
| 绝对值乘连续函数 | $\varphi$ 在 $x_0$ 连续：$\lvert x-x_0\rvert\varphi(x)$ 在 $x_0$ 可导 $\iff\varphi(x_0)=0$ |
| 反例 | $x\sin\frac1x$（$f(0)=0$）连续不可导；$x^2\sin\frac1x$ 在 0 可导，导函数在 0 不连续；ReLU 在 0 左导数 0、右导数 1 |
| 基本导数表（一） | $(x^\alpha)'=\alpha x^{\alpha-1}$，$(a^x)'=a^x\ln a$，$(e^x)'=e^x$，$(\ln\lvert x\rvert)'=\frac1x$，$(\log_ax)'=\frac1{x\ln a}$ |
| 基本导数表（二） | $(\sin x)'=\cos x$，$(\cos x)'=-\sin x$，$(\tan x)'=\sec^2x$，$(\cot x)'=-\csc^2x$，$(\sec x)'=\sec x\tan x$，$(\csc x)'=-\csc x\cot x$ |
| 基本导数表（三） | $(\arcsin x)'=\frac1{\sqrt{1-x^2}}$，$(\arccos x)'=-\frac1{\sqrt{1-x^2}}$，$(\arctan x)'=\frac1{1+x^2}$；每一步法则的条件在该点成立才能用，$\lvert x\rvert$ 在 0 处回到定义 |
| 四则运算 | $(u\pm v)'=u'\pm v'$；$(uv)'=u'v+uv'$（不是 $u'v'$）；$\big(\frac uv\big)'=\frac{u'v-uv'}{v^2}$；$\big(\frac1v\big)'=-\frac{v'}{v^2}$ |
| 链式法则 | $[f(g(x))]'=f'(g(x))\,g'(x)$：变化率逐层相乘，外层的导数在 $g(x)$ 处取；漏乘里层的导数是最常见的错 |
| 反函数求导 | $g'(y_0)=\frac1{f'(x_0)}$（$f'(x_0)\ne0$）；图像关于 $y=x$ 对称，斜率互为倒数 |
| sigmoid | $\sigma'(z)=\sigma(z)\big(1-\sigma(z)\big)$ |
| $n$ 阶导数 | $(e^{ax})^{(n)}=a^ne^{ax}$；$(\sin(ax+b))^{(n)}=a^n\sin(ax+b+\frac{n\pi}2)$；$(\ln(1+x))^{(n)}=\frac{(-1)^{n-1}(n-1)!}{(1+x)^n}$；$(uv)^{(n)}=\sum\binom nku^{(k)}v^{(n-k)}$ |
