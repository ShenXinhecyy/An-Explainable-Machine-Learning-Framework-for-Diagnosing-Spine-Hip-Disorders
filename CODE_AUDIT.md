# 原版代码审计报告（BOLD 模型 + 验证流水线）

审计方式：逐行读码 + 本地实跑（Python 3.11 + numpy/scipy）。
结论：**核心模型是对的，但有 1 处致命缺口、3 处必须修、5 处建议修。**

---

## 一、致命问题（P0，直接影响"核心结果可复现"）

### 1. `strategy_comparison.py` 没有亚阈值臂，正文的核心协同结果无法复现

**实跑该脚本的原始输出：**

| Strategy | k_ROS | RS |
|---|---|---|
| None | 0 | 0.1228 |
| ROS only | **0.5** | **0.9183** |
| AMPK only | 0 | 0.5338 |
| Stiffness only | 0 | 0.2610 |
| **ROS + AMPK** | **0.5** | **0.9183** |
| Triple | 0.5 | 0.9425 |

**问题**：脚本里 `('ROS + AMPK', {'k_ROS': 0.5, ...})` 用的是 **0.5（已超阈值 0.333）**，所以结果与 "ROS only 0.5" **完全相同（0.9183）**——**协同效应在代码里根本看不见**。

而正文的核心卖点是"**亚阈值** ROS（k=0.3）单独只有 0.31，加上 AMPK 才到 0.92"。这个臂 **在代码里不存在**。

**我补测（证明数值本身是对的，只是脚本没写）：**

```
ROS only k=0.30 -> RS = 0.3053   (正文 0.31 ✓)
ROS(0.3)+AMPK(0.35) -> 0.9183    (正文 0.92 ✓)
AMPK only 0.35 -> 0.5338          (正文 0.53 ✓)
additive 0.31+0.53-0.12 = 0.72    (正文 0.72 ✓)
```

**修复**：在 `strategies` 列表里补两个臂并打印加和期望：

```python
strategies = [
    ('None (control)',            {'k_ROS': 0.0, 'alpha_AMPK': 0.0, 'E_matrix': 0.0}),
    ('Sub-threshold ROS only',    {'k_ROS': 0.3, 'alpha_AMPK': 0.0, 'E_matrix': 0.0}),
    ('AMPK activation only',      {'k_ROS': 0.0, 'alpha_AMPK': 0.35, 'E_matrix': 0.0}),
    ('Stiffness only',            {'k_ROS': 0.0, 'alpha_AMPK': 0.0, 'E_matrix': 0.2}),
    ('Supra-threshold ROS only',  {'k_ROS': 0.5, 'alpha_AMPK': 0.0, 'E_matrix': 0.0}),
    ('Sub-threshold ROS + AMPK',  {'k_ROS': 0.3, 'alpha_AMPK': 0.35, 'E_matrix': 0.0}),
    ('Triple Push-Pull',          {'k_ROS': 0.5, 'alpha_AMPK': 0.35, 'E_matrix': 0.2}),
]
# 加和期望 = RS(ROS0.3) + RS(AMPK0.35) - RS(none)
```

**这是唯一一条会直接导致审稿人"结果不可复现"判断的问题，必须修。**

---

## 二、必须修（P1）

### 2. `bistability_test.py` 在 Windows 下直接崩溃

实跑报错：

```
UnicodeEncodeError: 'gbk' codec can't encode character '\u2713'
```

脚本里用了 `✓ ✗ ✅ ❌ —` 这些非 ASCII 字符，Windows 默认 GBK 控制台无法编码，**脚本跑到一半直接退出**。

**修复**（二选一）：
- 把 `✓/✗/✅/❌` 换成 ASCII `[OK]/[FAIL]/[YES]/[NO]`；
- 或文件头加 `sys.stdout.reconfigure(encoding='utf-8')`。

### 3. `monte_carlo_robustness.py` 文档写 100.0%，实际是 99.99%

- docstring：`qualitative prediction maintained in 100.0% of sets`
- 代码：`valid.mean()*100` → **9999/10000 = 99.99%**
- README/正文写的是 9,999/10,000（99.99%）

→ docstring 与代码/正文不一致，应改为 99.99%。

### 4. `bifurcation_scan.py` 声称"bisection"，实际不是

- 文档/README：`located by equilibrium continuation (Newton + bisection)`
- 代码实际：`fold = df.loc[df['RS_inflammatory'].notna(), 'k_ROS'].max() + 0.0025`
  —— 只是**网格最大值 + 半个步长**，没有 bisection。
- 真正的 bisection 在 `hysteresis_analysis.fold_forward()`（45 次二分，我实跑得 **0.3327**）。

→ 两个脚本应统一：要么 `bifurcation_scan` 也调用 `fold_forward`，要么在文档里明确"网格估计 ±0.0025"。

---

## 三、建议修（P2）

### 5. `regscore()` 有两套实现，容易让审稿人困惑
- `ode_model.regscore()`：**不做** min-max 归一化；
- `validation_pipelines/common.regscore()`：**做** min-max 归一化。

正文写 "X,Y,Z are min-max normalised to [0,1]"。模型里状态本身有界（自动满足），验证里必须手动归一。**建议在两个文件里加注释说明各自适用场景**，或统一成一个带 `normalise` 参数的函数。

### 6. Z 模块基因集与 M2 标志基因 3/5 重叠
```python
Z_MOUSE = ["Tfam", "Cpt1a", "Mrc1", "Arg1", "Il10"]
M2_MARKERS = ["Mrc1", "Arg1", "Il10", "Cd163"]
```
Z 模块 5 个基因里 3 个是 M2 标志 → "M2 的 Z 更高"**部分是同义反复**（正文已加说明，但代码层面更彻底的做法是去掉这 3 个基因重算）。

### 7. 正文引用的个别数值脚本不直接输出
- `sensitivity_sweeps.py` 只打印 min/max/range，不输出 "k=0.3 → 0.31"；
- `strategy_comparison.py` 不计算 "additive expectation 0.72"（手算值）。

→ 建议脚本里显式打印这些中间值，正文引用才可逐条溯源。

### 8. `simulate()` 默认 `t_eval` 只有 10 个点
`t_eval = np.linspace(0, 200, 10)`——对轨迹图太粗（终态无影响）。画图时建议显式传密集 `t_eval`。

### 9. `pathology_comparison.py` 的健康/骨质疏松/骨髓炎参数无来源注释
`alpha_X = 0.25 / 0.55 / 0.90`、`alpha_Z=0.03`、`gamma_ZX_damage=0.40` 都是手工设定，代码里没注释依据。正文已承认 "transferred without direct calibration data"，**建议在代码里也加一行注释**，避免被问"这些参数哪来的"。

---

## 四、已确认没问题的部分

- **核心 ODE 与参数**：20 参数齐全，Hill 函数、`(1−X)` 饱和项、控制输入都正确；
- **折点 0.333**：`hysteresis_analysis.fold_forward()` 实跑得 **0.3327**，与正文 0.333 一致；
- **永久性结论**：反向无折叠（down to −0.5），k_ROS=0 处再生吸引子 RS=0.918，与正文一致；
- **策略数值**：0.12 / 0.92 / 0.53 / 0.26 / 0.94 全部实跑复现；
- **验证流水线的统计约定**：已知等权 vs 加权 d、Student vs Welch t，已由 `derive_manuscript_stats.py` 复现。

---

## 五、修完后对审稿人的意义

修掉 P0（补亚阈值臂）+ P1（Windows 兼容、docstring、bisection 表述）后：

- 审稿人点开仓库 → 跑 `strategy_comparison.py` → **能直接看到 0.31 → 0.92 vs 0.72 的亚阈值协同**（现在看不到）；
- 跑 `bistability_test.py` → 不再崩溃；
- 跑 `derive_manuscript_stats.py` → 精确复现正文所有转录组数字。

这样"核心结果不可复现"的质疑基本消除。
