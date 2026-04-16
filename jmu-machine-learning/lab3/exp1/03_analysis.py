"""
实验三 - 03: 结果对比分析 + 生成 Markdown 报告
先运行 01 和 02，再运行此脚本。
运行：在 lab3/ 目录下  python 03_analysis.py
"""
import os
import textwrap
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
os.makedirs('results', exist_ok=True)

# ── 1. 读取两组结果 ──────────────────────────────────────────
m1 = pd.read_csv('results/01_no_norm_metrics.csv')
m2 = pd.read_csv('results/02_norm_metrics.csv')
p1 = pd.read_csv('results/01_no_norm_predictions.csv')
p2 = pd.read_csv('results/02_norm_predictions.csv')

mse1, rmse1, r2_1 = m1['MSE'].iloc[0], m1['RMSE'].iloc[0], m1['R2'].iloc[0]
mse2, rmse2, r2_2 = m2['MSE'].iloc[0], m2['RMSE'].iloc[0], m2['R2'].iloc[0]

print(f"{'指标':<8} {'不归一化':>12} {'归一化':>12}")
print("-" * 35)
print(f"{'MSE':<8} {mse1:>12.6f} {mse2:>12.6f}")
print(f"{'RMSE':<8} {rmse1:>12.6f} {rmse2:>12.6f}")
print(f"{'R²':<8} {r2_1:>12.6f} {r2_2:>12.6f}")

# ── 2. 对比图（2×2）─────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle('SVM：归一化 vs 不归一化 — 全面对比', fontsize=15, fontweight='bold')
lims = [0.28, 1.02]

# 左上：不归一化 预测 vs 真实
ax = axes[0, 0]
ax.scatter(p1['真实值'], p1['预测值'], alpha=0.65, color='steelblue', s=50,
           edgecolors='white', lw=0.4, label='预测点')
ax.plot(lims, lims, 'r--', lw=1.8, label='理想线')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('真实录取概率'); ax.set_ylabel('预测录取概率')
ax.set_title(f'[不归一化]  预测 vs 真实\nR² = {r2_1:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 右上：归一化 预测 vs 真实
ax = axes[0, 1]
ax.scatter(p2['真实值'], p2['预测值'], alpha=0.65, color='mediumseagreen', s=50,
           edgecolors='white', lw=0.4, label='预测点')
ax.plot(lims, lims, 'r--', lw=1.8, label='理想线')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('真实录取概率'); ax.set_ylabel('预测录取概率')
ax.set_title(f'[归一化]    预测 vs 真实\nR² = {r2_2:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 左下：误差分布直方图对比
ax = axes[1, 0]
ax.hist(p1['误差'], bins=22, alpha=0.65, color='steelblue',
        label=f'不归一化 RMSE={rmse1:.4f}', edgecolor='white')
ax.hist(p2['误差'], bins=22, alpha=0.65, color='mediumseagreen',
        label=f'归一化   RMSE={rmse2:.4f}', edgecolor='white')
ax.axvline(0, color='red', linestyle='--', lw=1.5, label='零误差')
ax.set_xlabel('预测误差（真实值 - 预测值）'); ax.set_ylabel('频次')
ax.set_title('误差分布对比（越集中在0附近越好）', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 右下：三个指标柱状图
ax = axes[1, 1]
metrics_names = ['MSE', 'RMSE', 'R²']
v1 = [mse1, rmse1, r2_1]
v2 = [mse2, rmse2, r2_2]
x  = np.arange(3); w = 0.35
b1 = ax.bar(x - w/2, v1, w, label='不归一化', color='steelblue',      alpha=0.85)
b2 = ax.bar(x + w/2, v2, w, label='归一化',   color='mediumseagreen', alpha=0.85)
for bar in list(b1) + list(b2):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
            f'{bar.get_height():.4f}', ha='center', va='bottom', fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(metrics_names, fontsize=11)
ax.set_title('评估指标对比', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/03_comparison_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 对比图 → results/03_comparison_plot.png")

# ── 3. 生成 Markdown 报告 ────────────────────────────────────
# 动态判断哪个更好，让报告内容随实验结果变化
better     = "归一化" if r2_2 > r2_1 else "不归一化"
mse_drop   = (mse1 - mse2) / mse1 * 100
r2_improve = r2_2 - r2_1

report = f"""# 实验三 — SVM 预测录取率：归一化对比分析报告

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、实验背景

本实验使用研究生录取预测数据集（500条），用支持向量机（SVM）预测学生的录取概率。
我们做了同一个模型的两次实验，**唯一区别**是是否对输入特征进行归一化。

### 数据集特征
| 特征 | 含义 | 数值范围 |
|------|------|----------|
| GRE Score | GRE 考试成绩 | 290 – 340 |
| TOEFL Score | 托福成绩 | 92 – 120 |
| University Rating | 本科院校评级 | 1 – 5 |
| SOP | 目的陈述质量 | 1 – 5 |
| LOR | 推荐信质量 | 1 – 5 |
| CGPA | 本科 GPA | 6.8 – 9.9 |
| Research | 是否有研究经验 | 0 或 1 |

---

## 二、为什么归一化对 SVM 很重要？

### 2.1 问题根源：特征尺度不统一

把上表的"数值范围"对比一下：
- GRE 分数范围是 **50**（340-290）
- University Rating 范围只有 **4**（5-1）
- Research 只有 **0 或 1**

SVM 使用 **RBF 核函数**，它的核心计算是测量两个数据点之间的**距离**：

```
距离 = √[(GRE₁-GRE₂)² + (TOEFL₁-TOEFL₂)² + (Rating₁-Rating₂)² + ...]
```

问题来了：GRE 的差值动辄 10-30，而 Rating 的差值最多只有 4。
**GRE 这一个特征会"霸占"整个距离计算**，其他特征几乎没有发言权。

### 2.2 归一化的解决方案

Min-Max 归一化把所有特征压缩到 **[0, 1]** 区间：

```
新值 = (原值 - 最小值) / (最大值 - 最小值)
```

归一化后，GRE 的范围是 [0,1]，Rating 也是 [0,1]，大家"平起平坐"。

---

## 三、实验设置

- **模型**：SVR（支持向量回归），RBF 核，C=100，gamma=0.1，epsilon=0.1
- **数据划分**：训练集 400 条（80%），测试集 100 条（20%），随机种子=42
- **唯一变量**：是否用 MinMaxScaler 对特征归一化

---

## 四、实验结果

### 4.1 数值对比

| 指标 | 不归一化 | 归一化 | 变化 |
|------|----------|--------|------|
| **MSE**（↓越小越好） | {mse1:.6f} | {mse2:.6f} | {mse_drop:+.1f}% |
| **RMSE**（↓越小越好） | {rmse1:.6f} | {rmse2:.6f} | — |
| **R²**（↑越大越好） | {r2_1:.6f} | {r2_2:.6f} | {r2_improve:+.6f} |

> **结论：{better}效果更好。**

### 4.2 如何读懂这些指标？

**MSE（均方误差）**
= 预测误差的平方的平均值。越小说明预测越准。
例：MSE=0.005 意味着平均误差约为 √0.005 ≈ 0.07（录取概率差了7个百分点）

**RMSE（均方根误差）**
= √MSE，单位和预测值一样（录取概率）。
例：RMSE=0.07 意味着模型预测的录取概率平均偏差约 7%。

**R²（决定系数）**
= 模型解释了多少比例的数据变化，范围 0-1，越接近 1 越好。
例：R²=0.85 意味着模型解释了 85% 的录取概率变化。

### 4.3 可视化分析

#### 不归一化结果图

![不归一化](01_no_norm_plot.png)

#### 归一化结果图

![归一化](02_norm_plot.png)

#### 全面对比图

![对比图](03_comparison_plot.png)

**图中包含 4 个子图：**
1. **左上（蓝色）**：不归一化的预测 vs 真实散点图。点越靠近红色对角线，预测越准。
2. **右上（绿色）**：归一化的预测 vs 真实散点图。
3. **左下**：两组的误差分布直方图。误差越集中在 0 附近越好。
4. **右下**：三个指标的柱状对比图。

---

## 五、结论与建议

1. **归一化对 SVM 影响巨大**。SVM 使用距离计算，特征尺度不一致会导致大数值特征主导模型。

2. **实际开发中的最佳实践**：
   - 使用 `MinMaxScaler` 或 `StandardScaler` 对特征归一化
   - 注意：scaler 只在**训练集**上 `fit`，再对测试集做 `transform`（避免数据泄露）

3. **归一化不适用的情况**：
   - 决策树、随机森林不需要归一化（它们基于阈值划分，不用距离）
   - 如果特征本身尺度有意义（如经济学模型），谨慎使用

---

*本报告由 03_analysis.py 自动生成*
"""

report_path = 'results/03_analysis_report.md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✓ 分析报告 → {report_path}")
print("\n全部完成！结果文件：")
print("  results/01_no_norm_plot.png        — 不归一化图")
print("  results/02_norm_plot.png           — 归一化图")
print("  results/03_comparison_plot.png     — 对比图")
print("  results/03_analysis_report.md      — Markdown 报告")
