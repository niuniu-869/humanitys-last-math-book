| 提示 | 内容 |
|---|---|
| 定义 | $\iint_Df\,\mathrm d\sigma=\lim\sum f(\xi_i,\eta_i)\Delta\sigma_i$：分割、近似、求和、取极限；$f\ge0$ 时是曲顶柱体体积，$f\equiv1$ 时是面积 $\sigma$；边界分段光滑的有界闭区域上连续则可积 |
| 性质 | 线性；对区域可加；比较 $f\le g\Rightarrow\iint f\le\iint g$；估值 $m\sigma\le\iint f\le M\sigma$；$\lvert\iint f\rvert\le\iint\lvert f\rvert$ |
| 平均值与中值定理 | $\bar f=\frac1\sigma\iint_Df\,\mathrm d\sigma$；$f$ 在连通有界闭区域上连续，则有 $(\xi,\eta)\in D$ 使 $\iint f=f(\xi,\eta)\sigma$（最值定理、估值、介值定理三步；区域不连通则不成立）；$\frac1{\pi r^2}\iint_{\text{小圆盘}}f\to f(\text{圆心})$ |
| 累次积分 | $\iint_D=\int_a^b\mathrm dx\int_c^df\,\mathrm dy$（截面面积再积分）；矩形上两个次序相等；$\alpha(x)\beta(y)$ 型在矩形上等于两个积分的乘积 |
| 穿线法 | X 型：$a\le x\le b$，$\varphi_1(x)\le y\le\varphi_2(x)$；Y 型同理；先画图，穿线时进入处是下限，离开处是上限；进出曲线变了就分块 |
| 选次序 | 里层原函数积不出（$\frac{\sin y}y$、$\mathrm e^{-y^2}$、$\sqrt{1+y^3}$）就换次序；能不分块的次序优先 |
| 交换次序 | 先由积分限写出区域不等式并画图，再按另一方向穿线重写上下限；被积函数照抄 |
| 对称性 | 区域关于 $y$ 轴对称且 $f$ 对 $x$ 为奇：积分为 0；为偶：$2\iint_{x\ge0}$；区域关于 $y=x$ 对称：$\iint f(x,y)=\iint f(y,x)$；关于点 $(a,b)$ 中心对称且 $f(2a-x,2b-y)=-f(x,y)$：积分为 0；两个条件必须同时检查 |
| 极坐标 | $x=r\cos\theta$，$y=r\sin\theta$，$\mathrm d\sigma=r\,\mathrm dr\,\mathrm d\theta$（扇环面积 $\approx r\Delta r\Delta\theta$）；圆盘 $0\le r\le R$；圆 $x^2+y^2=2x$ 即 $r=2\cos\theta$；不要漏 $r$ |
| 无界区域与高斯积分 | 非负函数（去掉非负，极限可能不存在，如 $\sin(x^2+y^2)$）：圆盘上积分后让半径趋于无穷；$\int_{-\infty}^{+\infty}\mathrm e^{-x^2}\,\mathrm dx=\sqrt\pi$（平方、正方形夹在两圆盘之间、极坐标）；$\int\mathrm e^{-t^2/2}\,\mathrm dt=\sqrt{2\pi}$ |
| 雅可比换元 | $\mathrm dx\,\mathrm dy=\lvert J\rvert\,\mathrm du\,\mathrm dv$，$J=\frac{\partial(x,y)}{\partial(u,v)}=x_uy_v-x_vy_u$；反解不便时 $J=1\big/\frac{\partial(u,v)}{\partial(x,y)}$；被积函数、区域、面积元一起换；极坐标 $J=r$ |
| 积分号下求导 | $\varphi(t)=\int_a^bf(x,t)\mathrm dx$，$f,f_t$ 在有界闭矩形上连续：$\varphi'=\int_a^bf_t\,\mathrm dx$（证明：交换次序再求导）；限含参数：$\Phi'=\int_u^vf_t\mathrm dx+f(v,t)v'-f(u,t)u'$ |
