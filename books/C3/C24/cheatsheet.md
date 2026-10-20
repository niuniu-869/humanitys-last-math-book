| 提示 | 内容 |
|---|---|
| 驻点 | $f_x=f_y=0$（$\nabla f=\boldsymbol0$）；可微的极值点一定是驻点，驻点不一定是极值点（鞍点 $x^2-y^2$）；偏导数不存在的点也要查（圆锥顶点） |
| 二元二阶泰勒 | $f(x_0+h,y_0+k)=f+f_xh+f_yk+\frac12(f_{xx}h^2+2f_{xy}hk+f_{yy}k^2)+o(\rho^2)$，$\rho=\sqrt{h^2+k^2}$；证明：令 $\varphi(t)=f(x_0+th,y_0+tk)$，用一元泰勒加链式法则 |
| 黑塞矩阵 | $H=\begin{pmatrix}f_{xx}&f_{xy}\\f_{yx}&f_{yy}\end{pmatrix}$，二阶偏导数连续时对称 |
| 极值判别 | 驻点处 $A=f_{xx}$，$B=f_{xy}$，$C=f_{yy}$，$\Delta=AC-B^2$：$\Delta>0$ 且 $A>0$ 极小，$\Delta>0$ 且 $A<0$ 极大，$\Delta<0$ 鞍点，$\Delta=0$ 失效 |
| $\Delta=0$ | 回到函数本身比较：$x^4+y^4$ 极小，$-x^4-y^4$ 极大，$x^4-y^4$ 鞍点，$(x+y)^2$ 平底极小；符号不同即可排除，要证明极值需代数变形 |
| 闭区域最值 | 有界闭区域上连续函数必有最值；内部驻点（不必判别）加边界（化成一元）加角点，比较全部函数值 |
| 最小二乘 | 最小化 $S=\sum(ax_i+b-y_i)^2$；正规方程 $\sum x_i^2\,a+\sum x_i\,b=\sum x_iy_i$，$\sum x_i\,a+nb=\sum y_i$；$S$ 是二次函数，驻点就是整体最小点 |
| 条件极值 | 约束 $g=c$ 下求 $f$ 的最值；能解出变量就代入消元，解不出就用乘数法；最值点处等高线与约束曲线相切 |
| 拉格朗日乘数法 | $L=f-\lambda(g-c)$，解 $L_x=L_y=0$、$g=c$；等价于 $\nabla f=\lambda\nabla g$ 加约束；多个约束各配一个乘子：$\nabla f=\lambda\nabla g_1+\mu\nabla g_2$ |
| 解方程提醒 | 消去因子（如除以 $x$）前先单独检查它等于 0 的情形；候选点处必须满足 $\nabla g\ne\boldsymbol0$；比较全部候选点的函数值；约束集不是有界闭集时，先用不等式等数学办法说明最值存在 |
| 乘数法的证明骨架 | 设 $g_y\ne0$：隐函数 $y=y(x)$，$y'=-g_x/g_y$；令 $\psi(x)=f(x,y(x))$；$\psi'(x_0)=0$ 即 $f_x+f_yy'=0$；取 $\lambda=f_y/g_y$；得 $\nabla f=\lambda\nabla g$ |
| 建模五步 | 设变量（注明范围）、写目标、写约束、求解、检验（先说明最值存在；存在且候选点唯一时它就是答案） |
| 乘子的含义 | 约束 $g=c$ 放宽一个单位，最优值大约增加 $\lambda$：$\frac{\mathrm df^*}{\mathrm dc}=\lambda$（对应 $L=f-\lambda(g-c)$） |
