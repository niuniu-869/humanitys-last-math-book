## C.13 · 定积分的应用（速记）

| 提示 | 内容 |
|---|---|
| 微元法 | 取 $[x,x+\mathrm{d}x]$，写 $\mathrm{d}U=f(x)\,\mathrm{d}x$（只保留同阶项），$U=\int_a^bf\,\mathrm{d}x$；先检验与真实值只差高阶无穷小 |
| 两曲线间的面积 | 竖条 $\int(\text{上}-\text{下})\,\mathrm{d}x$，横条 $\int(\text{右}-\text{左})\,\mathrm{d}y$；选边不换的方向，上下对调处分段 |
| 参数方程的面积 | $A=\int y\,\mathrm{d}x=\int y(t)x'(t)\,\mathrm{d}t$，换元要换限，顺序跟着 $x$ 的方向 |
| 极坐标的面积 | $A=\frac12\int r^2\,\mathrm{d}\theta$；两曲线所围部分取靠里的那条；$\theta$ 范围让曲线恰好画一遍 |
| 截面法 | $V=\int A(x)\,\mathrm{d}x$；旋转体：条垂直于轴用 $\pi(\text{外}^2-\text{内}^2)$，条平行于轴用 $2\pi\cdot(\text{到轴的距离})\cdot(\text{高})\,\mathrm{d}x$ |
| 圆筒公式 | 绕 $y$ 轴：$V=2\pi\int_a^bx\,f(x)\,\mathrm{d}x$（$0\le a<b$）；轴不是坐标轴时半径换成到轴的距离 |
| 弧长 | $\mathrm{d}s=\sqrt{1+y'^2}\,\mathrm{d}x=\sqrt{x'^2+y'^2}\,\mathrm{d}t=\sqrt{r^2+r'^2}\,\mathrm{d}\theta$；参数、极坐标要带绝对值并让曲线只走一遍 |
| 旋转曲面面积 | $S=2\pi\int(\text{半径})\,\mathrm{d}s$；易错：把 $\mathrm{d}s$ 写成 $\mathrm{d}x$（球面会得到 $\pi^2R^2$）；圆台侧面积 $\pi(r_1+r_2)l$ |
| 常用结果 | 球体积 $\frac43\pi R^3$，球面 $4\pi R^2$；椭圆 $\pi ab$；摆线一拱 $3\pi a^2$；心形线 $\frac{3\pi a^2}2$，周长 $8a$；星形线周长 $6$（$a=1$） |
| 平均值与折算 | $\bar f=\frac1{b-a}\int_a^bf\,\mathrm{d}x$；连续收入流 $R$、连续复利利率 $i$：$PV=\int_0^TRe^{-it}\mathrm{d}t$，$T\to\infty$ 时 $=\frac Ri$ |
| 变力做功 | $\mathrm{d}W=(\text{这一块受到的力})\times(\text{要移动的距离})$，抽水时力是这一块的重量；水 $\rho=1000$ kg/m³，$g\approx9.8$ N/kg |
| 液体压力 | 深度 $x$ 处压强 $\rho gx$；$F=\rho g\int x\,w(x)\,\mathrm{d}x$，$w$ 是该深度的宽度 |
| 引力 | 质点间 $F=G\frac{m_1m_2}{r^2}$；小段先分解成分量再积分，对称的分量抵消 |
| 形心 | $\bar x=\frac1A\int x(g-h)\,\mathrm{d}x$，$\bar y=\frac1{2A}\int(g^2-h^2)\,\mathrm{d}x$；有对称轴则形心在轴上；半圆盘 $\bar y=\frac{4R}{3\pi}$ |
