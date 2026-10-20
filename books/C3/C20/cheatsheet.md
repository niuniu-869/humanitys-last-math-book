## C.20 · 多元函数与偏导数（速记）

| 提示 | 内容 |
|---|---|
| 定义域 | 分母不为 0，偶次根号下 $\ge0$，对数真数 $>0$；画出区域，取交集，注意边界含不含 |
| 画图 | 截线（固定一个变量）+ 等高线 $f(x,y)=c$；碗 $z=x^2+y^2$：同心圆；鞍 $z=x^2-y^2$：双曲线，$c=0$ 是 $y=\pm x$；$z=xy$ 是转了 $45^\circ$ 的鞍；经济里的无差异曲线就是等高线 |
| 二元极限 | 对圆盘里所有点成立：$0<\rho<\delta\Rightarrow\lvert f-A\rvert<\varepsilon$；证存在用放缩（如 $\frac{x^2}{x^2+y^2}\le1$）、极坐标、化成一元重要极限；试路径只能证不存在 |
| 证极限不存在 | 沿 $y=kx$ 得 $k$ 相关的值（如 $\frac{xy}{x^2+y^2}\to\frac k{1+k^2}$）；直线都得同一个值时再试抛物线（$\frac{xy^2}{x^2+y^4}$ 沿 $x=y^2$ 得 $\frac12$） |
| 连续与最值 | 连续 $\iff$ 极限 $=$ 函数值；有界闭区域上连续函数有最值，路径连通时取遍中间值；缺有界、闭、连续任一条，最值可能不存在；间断点可以连成一条线 |
| 偏导数 | $f_x=\lim\frac{f(x_0+\Delta x,y_0)-f(x_0,y_0)}{\Delta x}$，其余变量当常数；几何：截线的切线斜率；经济：边际量；$x^y$ 对 $x$ 是幂函数、对 $y$ 是指数函数；分界点用定义 |
| 偏导数的局限 | 偏导数只沿两条坐标轴看：$h=\frac{xy}{x^2+y^2}$ 在原点 $h_x=h_y=0$，却不连续；偏导数同时为 0 不一定是极值（鞍） |
| 可微 | $\Delta z=A\Delta x+B\Delta y+o(\rho)$，$\rho=\sqrt{\Delta x^2+\Delta y^2}$；$A=f_x$，$B=f_y$；$\mathrm dz=f_x\mathrm dx+f_y\mathrm dy$ |
| 按定义判断可微 | 先求 $f_x,f_y$，再看 $\frac{\Delta z-f_x\Delta x-f_y\Delta y}{\rho}\to0$ 是否成立；沿 $\Delta y=k\Delta x$ 试；放缩用 $\lvert\Delta x\Delta y\rvert\le\frac{\rho^2}2$ |
| 切平面与近似 | $z-z_0=f_x(x-x_0)+f_y(y-y_0)$；法向量 $(f_x,f_y,-1)$；$f(x_0+\Delta x,y_0+\Delta y)\approx f(x_0,y_0)+f_x\Delta x+f_y\Delta y$ |
| 充分条件 | $f_x,f_y$ 在点的邻域存在且在该点连续 $\Rightarrow$ 可微（证明：拆成两步，各用一次拉格朗日中值定理）；偏导连续这一条不能删：$g=\frac{xy}{\sqrt{x^2+y^2}}$ 的偏导处处存在，$g$ 本身连续，但偏导在原点不连续，$g$ 也不可微；这只是充分条件，$(x^2+y^2)\sin\frac1{x^2+y^2}$ 可微而偏导不连续 |
| 谁推出谁 | 偏导连续 $\Rightarrow$ 可微 $\Rightarrow$ 连续、偏导存在；反例：$h$（偏导存在不连续）、$\sqrt{x^2+y^2}$（连续偏导不存在）、$g=\frac{xy}{\sqrt{x^2+y^2}}$（连续且偏导存在不可微）、$(x^2+y^2)\sin\frac1{x^2+y^2}$（可微但偏导不连续） |
| 高阶偏导数 | $f_{xy}=(f_x)_y$ 先 $x$ 后 $y$；混合偏导数在点邻域内连续时 $f_{xy}=f_{yx}$（只是充分条件）；反例 $\frac{xy(x^2-y^2)}{x^2+y^2}$ 在原点 $f_{xy}=-1$，$f_{yx}=1$ |
