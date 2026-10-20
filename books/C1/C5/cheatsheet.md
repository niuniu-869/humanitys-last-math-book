## C.5 · 微分与求导技巧（速记）

| 提示 | 内容 |
|---|---|
| 微分的定义 | $\Delta y=A\Delta x+o(\Delta x)$ 即可微；一元时可微 $\iff$ 可导，$A=f'(x_0)$；$\mathrm{d}y=f'(x)\,\mathrm{d}x$，$\mathrm{d}x=\Delta x$ 但 $\mathrm{d}y$ 一般不等于 $\Delta y$ |
| 线性近似 | $f(x_0+\Delta x)\approx f(x_0)+f'(x_0)\Delta x$；$\sqrt{4.1}\approx2.025$，$e^{0.1}\approx1.1$，$\ln1.1\approx0.1$；角要先换成弧度；$e^x$ 偏小（切线在下），$\sqrt x$ 偏大 |
| 误差传播 | $\frac{\Delta y}{y}\approx\frac{xf'(x)}{f(x)}\cdot\frac{\Delta x}x$；$y=x^n$ 时相对误差放大 $n$ 倍（圆面积 2 倍，球体积 3 倍） |
| 微分运算 | $\mathrm{d}(uv)=v\,\mathrm{d}u+u\,\mathrm{d}v$，$\mathrm{d}(u/v)=\frac{v\,\mathrm{d}u-u\,\mathrm{d}v}{v^2}$ |
| 形式不变性 | $y=f(u)$，$u=g(x)$：$\mathrm{d}y=f'(u)\,\mathrm{d}u$，$u$ 是自变量还是中间变量都一样；但 $u$ 是中间变量时 $\mathrm{d}u=g'(x)\mathrm{d}x$，一般不等于 $\Delta u$ |
| 凑进 $\mathrm{d}$ | $x\,\mathrm{d}x=\mathrm{d}\frac{x^2}2$，$\cos x\,\mathrm{d}x=\mathrm{d}\sin x$，$\frac{\mathrm{d}x}x=\mathrm{d}\ln\lvert x\rvert$，$\frac{\mathrm{d}x}{1+x^2}=\mathrm{d}\arctan x$ |
| 隐函数求导 | 两边对 $x$ 求导，遇到 $y$ 多乘 $y'$；求某点的值，$x$、$y$ 都要代入；二阶导把 $y'$ 的表达式再求导，再代回 $y'$；$x^2+y^2=25$：$y'=-\frac xy$，$y''=-\frac{25}{y^3}$ |
| 对数求导 | 幂指函数、连乘连除：$\ln y$ 求导得 $\frac{y'}y$，再乘 $y$；$(u^v)'=vu^{v-1}u'+u^v\ln u\cdot v'$（两条腿相加）；$(x^x)'=x^x(\ln x+1)$ |
| 相对变化率与弹性 | $\frac{y'}y=(\ln y)'$；$E=\frac{xy'}y$；$\frac{q'}q=\frac{G'}G-\frac{N'}N$（$q=G/N$）（人均增长率 $\approx$ 总量增长率 $-$ 人口增长率） |
| 参数方程 | $\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}$；$\frac{\mathrm{d}^2y}{\mathrm{d}x^2}=\frac{\mathrm{d}}{\mathrm{d}t}\bigl(\frac{y'}{x'}\bigr)\Big/x'(t)$，最后别忘除以 $x'(t)$，也不是 $\frac{y''}{x''}$ |
| 极坐标 | $x=r\cos\theta$，$y=r\sin\theta$，$r^2=x^2+y^2$；心形线、双纽线、阿基米德螺线、三叶玫瑰线；切线 $\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{r'\sin\theta+r\cos\theta}{r'\cos\theta-r\sin\theta}$，斜率不是 $r'$ |
| 相关变化率 | 先写每一刻都成立的关系，两边对 $t$ 求导，**最后**才代入这一刻的数值 |
| 莱布尼茨公式 | $(uv)^{(n)}=\sum_{k=0}^n\binom nk u^{(k)}v^{(n-k)}$；让多项式的因子做 $u$，只剩前几项 |
| 谁推出谁 | 可导 $\Rightarrow$ 连续（反向不成立，反例 $\lvert x\rvert$）；一元：可导 $\iff$ 可微 |
