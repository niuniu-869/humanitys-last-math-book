## C.22 · 方向导数与梯度（速记）

| 提示 | 内容 |
|---|---|
| 方向导数定义 | $\boldsymbol l=(\cos\alpha,\cos\beta)$ 是单位向量：$\dfrac{\partial f}{\partial\boldsymbol l}=\lim\limits_{t\to0^+}\dfrac{f(P_0+t\boldsymbol l)-f(P_0)}{t}$，几何上是竖直截线的切线斜率；只取 $t\to0^+$，$-\boldsymbol l$ 是另一个方向 |
| 与偏导数的关系 | $f_x$ 存在时，沿 $(1,0)$ 是 $f_x$，沿 $(-1,0)$ 是 $-f_x$；方向导数都存在不要求偏导存在（圆锥面 $\sqrt{x^2+y^2}$ 在原点处处为 1，$f_x(0,0)$ 不存在） |
| 计算公式 | $f$ 可微时 $\dfrac{\partial f}{\partial\boldsymbol l}=f_x\cos\alpha+f_y\cos\beta(+f_z\cos\gamma)$；条件不能少（$\dfrac{x^2y}{x^2+y^2}$ 在原点沿 $(a,b)$ 是 $a^2b$，公式给 0） |
| 先单位化 | 给的方向向量 $\boldsymbol v$ 要除以 $\lVert\boldsymbol v\rVert$；「从 $P$ 指向 $Q$」取 $\overrightarrow{PQ}$ |
| 梯度 | $\nabla f=(f_x,f_y,f_z)$；可微时 $\dfrac{\partial f}{\partial\boldsymbol l}=\nabla f\cdot\boldsymbol l=\lVert\nabla f\rVert\cos\theta$，$\theta$ 是 $\boldsymbol l$ 与 $\nabla f$ 的夹角 |
| 最快与最慢 | 沿 $\nabla f$ 上升最快，变化率 $\lVert\nabla f\rVert$；沿 $-\nabla f$ 下降最快，变化率 $-\lVert\nabla f\rVert$；垂直于 $\nabla f$ 的方向变化率为 0；$\nabla f=\boldsymbol0$ 时没有最陡方向 |
| 梯度垂直等高线 | 等高线 $f=c$ 上的曲线 $\boldsymbol r(t)$ 满足 $\nabla f\cdot\boldsymbol r'=0$；$f_y\ne0$ 时切向量取 $(1,-f_x/f_y)$，它与梯度的数量积为 0；$f_y=0$ 时切线竖直（要求 $f$ 可微、$\nabla f\ne\boldsymbol0$；偏导连续是可微的充分条件，也保证等高线光滑）；梯度指向函数变大的一侧 |
| 等高线的疏密 | 沿梯度方向量，相邻等高线（高度差 $\Delta c$ 足够小）间距 $h\approx\Delta c/\lVert\nabla f\rVert$：梯度大，等高线密 |
| 等高线的切线与法线 | 法线方向取 $\nabla f(P_0)$，切线是过 $P_0$ 垂直于 $\nabla f$ 的直线（先约去公因子） |
| 谁推出谁（新增） | 可微 $\Rightarrow$ 所有方向导数存在；反过来不成立。方向导数都存在 $\not\Rightarrow$ 连续（$\dfrac{x^2y}{x^4+y^2}$）、$\not\Rightarrow$ 偏导存在（圆锥面）；偏导存在 $\not\Rightarrow$ 方向导数存在（$\dfrac{xy}{x^2+y^2}$） |
| 梯度下降一步 | $\boldsymbol x_{k+1}=\boldsymbol x_k-\eta\nabla f(\boldsymbol x_k)$；$\eta$ 小时 $f$ 约减少 $\eta\lVert\nabla f\rVert^2$ |
| 二次函数上的步长 | $f=x^2+4y^2$：$x_{k+1}=(1-2\eta)x_k$，$y_{k+1}=(1-8\eta)y_k$，从 $(4,1)$ 出发收敛当且仅当 $0<\eta<\frac14$；$\eta=0.2$ 时两个因子绝对值相等，最快；上限由最陡的方向决定 |
| 驻点 | $\nabla f=\boldsymbol0$ 的点；梯度下降停在驻点，不一定是最小值点（判别见 C.24） |
