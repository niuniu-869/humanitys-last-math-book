## C.27 · 曲线积分与格林公式（速记）

| 提示 | 内容 |
|---|---|
| 第一类（对弧长） | $\int_Lf\,\mathrm{d}s=\int_\alpha^\beta f(x(t),y(t))\sqrt{x'^2+y'^2}\,\mathrm{d}t$，下限 < 上限；与走向无关 |
| 曲线上可代方程 | 积分只在曲线上取值，可用曲线方程化简被积函数（圆上 $x^2+y^2=a^2$）；二重积分不行 |
| 第二类（对坐标） | $\int_LP\,\mathrm{d}x+Q\,\mathrm{d}y=\int_{t_A}^{t_B}(Px'+Qy')\,\mathrm{d}t$，$t_A$ 对应起点，可以 $t_A>t_B$ |
| 方向与两类联系 | 反向变号：$\int_{L^-}=-\int_L$；$\int_L\boldsymbol F\cdot\mathrm{d}\boldsymbol r=\int_L\boldsymbol F\cdot\boldsymbol\tau\,\mathrm{d}s$ |
| 正向 | 沿边界走时区域在左手边：外边界逆时针，洞的边界顺时针 |
| 格林公式 | $\oint_LP\,\mathrm{d}x+Q\,\mathrm{d}y=\iint_D(Q_x-P_y)\,\mathrm{d}\sigma$；$L$ 正向，$P,Q$ 在 $D$ 上偏导连续 |
| 面积公式 | $A=\frac12\oint_Lx\,\mathrm{d}y-y\,\mathrm{d}x$（$L$ 正向）；椭圆 $\pi ab$；多边形 $\frac12\sum(x_iy_{i+1}-x_{i+1}y_i)$（鞋带公式，顶点逆时针；顺时针取绝对值） |
| 补线与挖洞 | 不封闭：补线段，减去补线上的积分；内有坏点：挖小圆，内圈顺时针 |
| 经典结果 | $\oint\frac{x\,\mathrm{d}y-y\,\mathrm{d}x}{x^2+y^2}$：围住原点（正向）$=2\pi$，不围住 $=0$ |
| 路径无关四等价 | 单连通、偏导连续时：闭路积分为 0 ⇔ 与路径无关 ⇔ 是某个 $\mathrm{d}u$ ⇔ $P_y=Q_x$ |
| 单连通不能少 | 去掉原点的平面上 $\frac{x\,\mathrm{d}y-y\,\mathrm{d}x}{x^2+y^2}$ 满足 $P_y=Q_x$，但绕原点积分 $2\pi$；单连通只是 (4)⇒(1) 的充分条件，有洞时看绕每个洞的积分是否为 0 |
| 求原函数 | 折线法 $u=\int_{x_0}^xP(t,y_0)\,\mathrm{d}t+\int_{y_0}^yQ(x,s)\,\mathrm{d}s$；偏积分法 $u=\int P\,\mathrm{d}x+h(y)$ |
| 基本定理 | $\int_L\nabla u\cdot\mathrm{d}\boldsymbol r=u(B)-u(A)$；各特征的贡献加起来等于总变化（积分梯度法） |
| 全微分方程 | $P\,\mathrm{d}x+Q\,\mathrm{d}y=0$，$P_y=Q_x$（单连通或局部）⇒ 通解 $u(x,y)=C$；$Q\ne0$ 处解成 $y(x)$，$Q=0$ 而 $P\ne0$ 处解成 $x(y)$ |
| 应用 | 弧长 $\int\mathrm{d}s$；质量 $\int\mu\,\mathrm{d}s$；质心 $\bar x=\frac1M\int x\mu\,\mathrm{d}s$；功 $\int\boldsymbol F\cdot\mathrm{d}\boldsymbol r$ |
