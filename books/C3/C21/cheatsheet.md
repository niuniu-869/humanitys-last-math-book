## C.21 · 多元复合函数与隐函数的求导（速记）

| 提示 | 内容 |
|---|---|
| 全导数 | $z=f(x,y)$，$x=x(t)$，$y=y(t)$：$\dfrac{\mathrm dz}{\mathrm dt}=f_xx'+f_yy'$；条件是 $f$ 可微，只有偏导存在不够（反例 $\dfrac{x^2y}{x^2+y^2}$，$x=y=t$） |
| 项数 | 一条路径一项；项数等于从 $z$ 到该自变量的路径数；每个中间变量都有一条到该自变量的路径时，才等于中间变量个数 |
| 树形图 | $z\to$ 中间变量 $\to$ 自变量，路径上的偏导相乘，同一自变量下的路径相加；只依赖一个自变量的边写 $\mathrm d$，否则写 $\partial$ |
| 抽象函数记号 | $f'_1$、$f'_2$ 是对第一、第二个位置求导，取值点是 $f$ 的变量所在的点；$f''_{12}=f''_{21}$（二阶偏导连续） |
| 既当中间变量又当自变量 | $z=f(x,xy)$：$z_x=f'_1+y\,f'_2$，不能直接把 $z_x$ 当成 $f'_1$（只有 $y f'_2=0$ 时两者才相等），两条路径都要走 |
| 全微分形式不变性 | $\mathrm dz=f'_1\mathrm du+f'_2\mathrm dv$ 对中间变量也成立；展开 $\mathrm du,\mathrm dv$ 后读 $\mathrm dx$、$\mathrm dy$ 的系数得 $z_x,z_y$ |
| 二阶偏导 | $f'_i$ 本身还是复合函数，要再用一次链式法则：$z=f(xy,x+y)$ 时 $z_{xy}=f'_1+xy\,f''_{11}+(x+y)f''_{12}+f''_{22}$ |
| 一个中间变量 | $z=f(x^2+y^2)$：$z_{xx}=2f'+4x^2f''$，$z_{xx}+z_{yy}=4(f'+sf'')$，$s=x^2+y^2$ |
| 隐函数存在 | $F(x_0,y_0)=0$，$F$ 偏导连续，$F_y(x_0,y_0)\ne0$ $\Rightarrow$ 局部有唯一 $y(x)$；$F_y=0$ 时不一定无解（$(y-x)^3=0$） |
| 隐函数求导 | $\dfrac{\mathrm dy}{\mathrm dx}=-\dfrac{F_x}{F_y}$（来自 $F(x,y(x))\equiv0$ 求导）；二阶：对 $y'$ 再求导，遇到 $y'$ 就代回 |
| 三变量隐函数 | $z_x=-\dfrac{F_x}{F_z}$，$z_y=-\dfrac{F_y}{F_z}$；要二阶偏导时直接对方程求偏导更稳 |
| 偏导不能约分 | $F$ 偏导连续、点满足 $F=0$、$F_xF_yF_z\ne0$ 时 $\dfrac{\partial x}{\partial y}\dfrac{\partial y}{\partial z}\dfrac{\partial z}{\partial x}=-1$（每个偏导固定的变量不同） |
| 含抽象 $F$ 的证明 | 对 $F(u,v)=0$ 取全微分，再展开 $\mathrm du,\mathrm dv$，分别令 $\mathrm dx,\mathrm dy$ 的系数为 0 |
| 方程组 | 几个方程确定几个函数；两边对自变量求导得一次方程组，系数行列式 $J=\dfrac{\partial(F,G)}{\partial(u,v)}\ne0$ 才能解 |
