## K1.1 · 逻辑的代数：等值演算、范式与归结（速记）

| 提示 | 内容 |
|---|---|
| 替换规则 | 把式子里的一部分换成与它等价的式子，整个式子的真值不变（固定一行赋值后，整体真值只是这一部分真值的函数）；规律表里的字母可代入任意式子 |
| 常用等价式 | $p\to q\equiv\neg p\vee q\equiv\neg q\to\neg p$；德摩根 $\neg(p\wedge q)\equiv\neg p\vee\neg q$；$p\leftrightarrow q\equiv(p\wedge q)\vee(\neg p\wedge\neg q)$ |
| 两条分配律 | $p\wedge(q\vee r)\equiv(p\wedge q)\vee(p\wedge r)$，$p\vee(q\wedge r)\equiv(p\vee q)\wedge(p\vee r)$；后一条在算术里没有对应（取 $a=b=c=1$ 算术上左 2 右 4） |
| 吸收与互补 | $p\vee(p\wedge q)\equiv p$，$p\wedge(p\vee q)\equiv p$；$p\vee\neg p\equiv1$，$p\wedge\neg p\equiv0$ |
| 方法 1：等值演算 | 先消 $\to,\leftrightarrow$，再把否定推到字母前，然后分配、吸收、互补，每步写依据 |
| 三类式子 | 重言式每行为真；矛盾式每行为假；可满足式至少一行为真（重言式也可满足） |
| 推理有效的三种说法 | 前提全真时结论不假 $\iff$ $(A_1\wedge\cdots\wedge A_n)\to B$ 是重言式 $\iff$ $A_1\wedge\cdots\wedge A_n\wedge\neg B$ 是矛盾式 |
| 方法 2：找假行 | 设整个式子为假，从最外层往里定各字母；推出矛盾是重言式，否则读出反例 |
| 主析取范式 | 取真值表为真的行，字母取 1 写它、取 0 写它的否定，合取后用 $\vee$ 连起来；行号为 $i$ 的极小项记作 $m_i$ |
| 主合取范式 | 取为假的行，字母取 0 写它、取 1 写它的否定，析取后用 $\wedge$ 连起来；两个范式项数之和为 $2^n$ |
| 范式的用处 | 在同一组字母下，两式等价 $\iff$ 主析取范式相同；一个简单析取式含 $p$ 和 $\neg p$ 才是重言式，一个简单合取式含 $p$ 和 $\neg p$ 才是矛盾式 |
| 完备集 | $\{\neg,\wedge,\vee\}$、$\{\neg,\wedge\}$、$\{\neg,\to\}$、$\{\uparrow\}$ 完备；$\{\wedge,\vee\}$、$\{\wedge,\to\}$ 不完备（不含常量时，全取 1 恒为 1） |
| 与非 | $\neg p\equiv p\uparrow p$，$p\wedge q\equiv(p\uparrow q)\uparrow(p\uparrow q)$ |
| 归结规则 | 从 $A\vee p$ 和 $B\vee\neg p$ 得 $A\vee B$；空子句 $\square$ 恒假 |
| 方法 5：归结反驳 | 前提加结论的否定，化成子句，每次只消一个字母；得 $\square$ 则推理有效，归结停住则无效 |
| 易错 | 一次不能同时消两个字母；$p\vee q$ 与 $\neg p\vee\neg q$ 可满足；$\neg(p\wedge q)\not\equiv\neg p\wedge\neg q$，$p\to q\not\equiv q\to p$ |
