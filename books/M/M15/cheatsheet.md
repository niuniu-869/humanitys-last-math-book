## M.15 · 强化学习与 RLHF：价值、策略梯度、奖励模型与 KL 约束（速记）

| 提示 | 内容 |
|---|---|
| MDP 与回报 | 状态、动作、转移 $P(s'\mid s,a)$、奖励、策略 $\pi(a\mid s)$；折扣回报 $G=\sum_t\gamma^tr_{t+1}$，目标 $\max E[G]$；固定 $\pi$ 得马尔可夫链 $P_\pi(s'\mid s)=\sum_a\pi(a\mid s)P(s'\mid s,a)$ |
| 语言模型是 MDP | 状态 = 提示加已写的词，动作 = 下一个词，转移 = 接在后面，奖励在整段写完才给；策略就是语言模型 |
| 贝尔曼方程 | $V^\pi(s)=\sum_a\pi\sum_{s'}P\,[r+\gamma V^\pi(s')]$，由 $G_t=r_{t+1}+\gamma G_{t+1}$ 和全期望公式推出；$V=r_\pi+\gamma P_\pi V$；$V(s)=\sum_a\pi(a\mid s)Q(s,a)$ |
| 价值迭代 | $V_{k+1}(s)=\max_a\sum P[r+\gamma V_k(s')]$；每遍最大误差缩小到 $\gamma$ 倍，收敛到 $V^*$ |
| Q 学习 | $Q\leftarrow Q+\alpha[r+\gamma\max_{a'}Q(s',a')-Q]$：用单次样本代替期望，不需要知道 $P$ |
| 策略梯度 | $\nabla J=E[R\,\nabla\ln P_\theta(\tau)]$（$\nabla P=P\nabla\ln P$）；$\nabla\ln P_\theta=\sum_t\nabla\ln\pi_\theta(a_t\mid s_t)$，转移概率不含 $\theta$；形式上像「按奖励加权的最大似然」 |
| softmax 策略的梯度 | $\nabla_z\ln\pi_a=\mathbf e_a-\pi$；老虎机 $\partial J/\partial\theta_k=\pi_k(r_k-J)$，老朋友⑤在 $\theta=0$ 为 $\pm0.05$ |
| 基线 | $E[b\nabla\ln\pi]=b\nabla\sum\pi=0$，所以 $E[(R-b)\nabla\ln\pi]$ 不变、$b$ 选得合适时方差变小；$b$ 不能依赖当前动作；优势 $A=Q-V$，按 $\pi$ 平均为 0；组内归一化 $(R_i-\bar R)/\mathrm{std}$ |
| PPO | $\rho=\pi_\theta/\pi_{\text{old}}$，$\min(\rho A,\operatorname{clip}(\rho,1-\varepsilon,1+\varepsilon)A)$；$A>0$ 时 $\rho>1+\varepsilon$ 无梯度，$A<0$ 时 $\rho<1-\varepsilon$ 无梯度 |
| Bradley–Terry | $P(i\succ j)=\sigma(r_i-r_j)$；损失 $-\ln\sigma(r_w-r_l)$，对分差的导数 $-(1-\sigma(\Delta))$；只有分差有意义；胜率 $q$ 对应分差 $\ln\frac q{1-q}$ |
| KL 约束的最优策略 | $\max E_\pi[r]-\beta\mathrm{KL}(\pi\Vert\pi_{\text{ref}})$ 的解 $\pi^*=\pi_{\text{ref}}e^{r/\beta}/Z$，最大值 $\beta\ln Z$；$\beta\to0$ 取最大奖励，$\beta\to\infty$ 回到 $\pi_{\text{ref}}$ |
| 老朋友⑤ | $r=(1,0)$，$\pi_{\text{ref}}$ 均匀，$\beta=0.5$：$\pi^*=(0.8808,0.1192)$；偏好概率 $\sigma(1)=0.7311$ |
| DPO | 由 $r=\beta\ln(\pi^*/\pi_{\text{ref}})+\beta\ln Z$ 代入 Bradley–Terry，$Z$ 抵消：$-\ln\sigma(\beta[\ln\frac{\pi_\theta(y_w)}{\pi_{\text{ref}}(y_w)}-\ln\frac{\pi_\theta(y_l)}{\pi_{\text{ref}}(y_l)}])$ |
| 易错 | 基线依赖动作则期望变；RLHF 的 KL 是 $\mathrm{KL}(\pi\Vert\pi_{\text{ref}})$（对 $\pi$ 取期望）；终点之后 $V=0$；策略梯度做的是上升不是下降 |
