## C.23 · 多元微分的几何应用：切线与切平面（速记）

| 提示 | 内容 |
|---|---|
| 参数曲线的切向量 | $x=x(t),y=y(t),z=z(t)$：$\boldsymbol T=(x'(t_0),y'(t_0),z'(t_0))\ne\boldsymbol 0$，是割线方向 $\dfrac{\Delta\boldsymbol r}{\Delta t}$ 的极限 |
| 切线与法平面 | 切线用点向式（方向数含 0 时写成参数式）；法平面以 $\boldsymbol T$ 为法向量：$x'(x-x_0)+y'(y-y_0)+z'(z-z_0)=0$ |
| $y=y(x)$，$z=z(x)$ | 把 $x$ 当参数：$\boldsymbol T=(1,y'(x_0),z'(x_0))$ |
| 切向量为零 | $\boldsymbol T=\boldsymbol 0$ 时公式不给方向，要换参数另行判断（$x=y=z=t^3$ 在 $t=0$） |
| 曲面的法向量 | 设 $F$ 偏导连续、$F(P)=0$、$\nabla F(P)\ne\boldsymbol0$：$\boldsymbol n=\nabla F(P)=(F_x,F_y,F_z)$，来自 $\nabla F\cdot\boldsymbol T=0$（曲面上任一条曲线代入 $F$ 恒为 0 再求导） |
| 切平面与法线 | 切平面 $F_x(x-x_0)+F_y(y-y_0)+F_z(z-z_0)=0$；法线方向取 $\nabla F(P)$；先验证点在曲面上，法向量可约去公因子 |
| $z=f(x,y)$ | 取 $F=f-z$，$\boldsymbol n=(f_x,f_y,-1)$，切平面还原为 $z-z_0=f_x(x-x_0)+f_y(y-y_0)$ |
| 点未知的题 | 切平面平行于已知平面：法向量成比例 $(F_x,F_y,F_z)=k\boldsymbol n_0$，通常需联立「点在曲面上」；解的个数由具体方程决定 |
| 梯度为零 | 方法 2 不能直接使用，切平面是否存在须另行判断：$z^2=0$ 有切平面，圆锥面顶点没有 |
| 交线的切向量 | $F=G=0$（偏导连续）：$\boldsymbol T=\nabla F(P)\times\nabla G(P)$，要求两个梯度非零且不平行（两曲面在 $P$ 不相切）；梯度平行时须另行判断（球面与相切平面交成一点，$z=0$ 与 $z=x^2$ 交成 $y$ 轴） |
| 求导法与向量积 | 对方程组求导得 $(1,y',z')$，它是 $\nabla F\times\nabla G$ 除以第一个分量，所以要求 $\dfrac{\partial(F,G)}{\partial(y,z)}\ne0$；第一个分量为 0 时换参数或直接用向量积 |
| 曲线与曲面对照 | 曲线算出切向量（做切线方向、法平面法向量）；曲面算出法向量（做法线方向、切平面法向量） |
