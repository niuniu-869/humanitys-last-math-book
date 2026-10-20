## Z.1 · 条件句：把中文翻译成逻辑式（速记）

| 提示 | 内容 |
|---|---|
| 命题 | 能判断真假的陈述句，真值记 1、0；问句、请求、含未给定变量的「$x+1=3$」都不是命题 |
| 四个联结词 | $\neg p$ 取反；$p\wedge q$ 两个都真才真（「但是」也译成 $\wedge$）；$p\vee q$ 至少一个真就真，两个都真也算；$p\oplus q$ 恰好一个真 |
| 真值表 | $n$ 个字母 $2^n$ 行；从里往外逐列算；$\neg$ 只管紧跟的字母或括号，$\neg p\wedge q$ 是 $(\neg p)\wedge q$ |
| 蕴含 $p\to q$ | 只在 $p=1,q=0$（违约行）为假；前件为假时一律为真；只看真值，不要求因果 |
| 四种命题 | 原命题 $\equiv$ 逆否命题 $\neg q\to\neg p$（违约行都是 $p=1,q=0$）；逆命题 $q\to p\equiv$ 否命题 $\neg p\to\neg q$（违约行都是 $p=0,q=1$） |
| 充分、必要 | $p\to q$ 时 $p$ 是 $q$ 的充分条件（小圈），$q$ 是 $p$ 的必要条件（大圈）；少不了的那一件放在箭头终点 |
| 方法 3：翻译 | 问「什么局面算违反」，写成「$X$ 发生而 $Y$ 没发生」，译成 $X\to Y$；字母只代表不带否定词的说法 |
| 必要条件的说法 | 「只有 $A$ 才 $B$」「$A$ 是 $B$ 的前提」「没有 $A$ 就没有 $B$」都是 $B\to A$ |
| 除非……否则 | 「除非 $A$，否则 $B$」$=\neg A\to B\equiv A\vee B$；它不包含「$A$ 就不 $B$」 |
| 双条件 | $p\leftrightarrow q\equiv(p\to q)\wedge(q\to p)$，同真同假时为真；$p\oplus q\equiv\neg(p\leftrightarrow q)$ |
| 德摩根律 | $\neg(p\wedge q)\equiv\neg p\vee\neg q$，$\neg(p\vee q)\equiv\neg p\wedge\neg q$：且、或互换，每项取反 |
| 条件句的否定 | $\neg(p\to q)\equiv p\wedge\neg q$，结果是「且」；写成「如果 $p$ 则 $\neg q$」是错的 |
| 或与如果 | $p\vee q\equiv\neg p\to q\equiv\neg q\to p$；$p\to q\equiv\neg p\vee q$ |
| 等价与矛盾 | 等价：为假的行完全相同；矛盾：每行一真一假；不能同真却能同假（「都去」与「都不去」）不是矛盾 |
| 易错 | $x>2$ 的否定是 $x\le2$；没说明的「或者」按相容处理；逆命题、否命题不能代替原命题 |
