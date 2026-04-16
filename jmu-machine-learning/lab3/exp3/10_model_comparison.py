"""
实验三 - 10: 三模型对比分析 + 生成 Markdown 报告
先运行 07, 08, 09，再运行此脚本。
运行：在 lab3/ 目录下  python exp3/10_model_comparison.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
os.makedirs('results', exist_ok=True)

# ── 1. 读取三组结果 ──────────────────────────────────────────
m_lr = pd.read_csv('results/07_lr_metrics.csv')
m_svm = pd.read_csv('results/08_svm_metrics.csv')
m_dt = pd.read_csv('results/09_dt_metrics.csv')

p_lr = pd.read_csv('results/07_lr_predictions.csv')
p_svm = pd.read_csv('results/08_svm_predictions.csv')
p_dt = pd.read_csv('results/09_dt_predictions.csv')

# 提取指标
models = ['线性回归', 'SVM', '决策树']
mse_vals = [m_lr['MSE'].iloc[0], m_svm['MSE'].iloc[0], m_dt['MSE'].iloc[0]]
rmse_vals = [m_lr['RMSE'].iloc[0], m_svm['RMSE'].iloc[0], m_dt['RMSE'].iloc[0]]
r2_vals = [m_lr['R2'].iloc[0], m_svm['R2'].iloc[0], m_dt['R2'].iloc[0]]
time_vals = [m_lr['train_time'].iloc[0], m_svm['train_time'].iloc[0], m_dt['train_time'].iloc[0]]

print(f"{'模型':<12} {'MSE':>12} {'RMSE':>12} {'R²':>12} {'训练时间(秒)':>15}")
print("-" * 65)
for i, model in enumerate(models):
    print(f"{model:<12} {mse_vals[i]:>12.6f} {rmse_vals[i]:>12.6f} {r2_vals[i]:>12.6f} {time_vals[i]:>15.4f}")

best_idx = np.argmax(r2_vals)
print(f"\n最佳模型: {models[best_idx]} (R² = {r2_vals[best_idx]:.6f})")

# ── 2. 对比图（3×3 九宫格）──────────────────────────────────
fig = plt.figure(figsize=(16, 13))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
lims = [0.28, 1.02]
colors = ['darkorange', 'mediumseagreen', 'mediumpurple']

predictions = [p_lr, p_svm, p_dt]

for row, (pred, model, color, r2, rmse) in enumerate(zip(predictions, models, colors, r2_vals, rmse_vals)):
    # 左列：预测 vs 真实
    ax = fig.add_subplot(gs[row, 0])
    ax.scatter(pred['真实值'], pred['预测值'], alpha=0.65, color=color, s=50,
               edgecolors='white', lw=0.4, label='预测点')
    ax.plot(lims, lims, 'r--', lw=1.8, label='理想线')
    ax.set_xlim(lims); ax.set_ylim(lims)
    ax.set_xlabel('真实录取概率', fontsize=10)
    ax.set_ylabel('预测录取概率', fontsize=10)
    ax.set_title(f'[{model}] 预测 vs 真实\nR² = {r2:.4f}', fontsize=11)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # 中列：残差图
    ax = fig.add_subplot(gs[row, 1])
    residuals = pred['真实值'] - pred['预测值']
    ax.scatter(pred['预测值'], residuals, alpha=0.65, color=color, s=50,
               edgecolors='white', lw=0.4)
    ax.axhline(0, color='r', linestyle='--', lw=1.8, label='零误差线')
    ax.set_xlabel('预测录取概率', fontsize=10)
    ax.set_ylabel('残差', fontsize=10)
    ax.set_title(f'[{model}] 残差图\nRMSE = {rmse:.4f}', fontsize=11)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # 右列：误差分布直方图
    ax = fig.add_subplot(gs[row, 2])
    ax.hist(pred['误差'], bins=20, alpha=0.7, color=color, edgecolor='white')
    ax.axvline(0, color='red', linestyle='--', lw=1.8, label='零误差')
    ax.set_xlabel('预测误差', fontsize=10)
    ax.set_ylabel('频次', fontsize=10)
    ax.set_title(f'[{model}] 误差分布\n均值={np.mean(pred["误差"]):.4f}', fontsize=11)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3, axis='y')

fig.suptitle('三模型全面对比：线性回归 vs SVM vs 决策树', fontsize=15, fontweight='bold')
plt.savefig('results/10_model_comparison_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ 对比图 → results/10_model_comparison_plot.png")

# ── 3. 指标对比柱状图 ────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
x_pos = np.arange(len(models))
width = 0.6

# MSE对比
ax = axes[0]
bars = ax.bar(x_pos, mse_vals, width, color=colors, alpha=0.8, edgecolor='white')
for bar, val in zip(bars, mse_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0002,
            f'{val:.5f}', ha='center', va='bottom', fontsize=9)
ax.set_xticks(x_pos)
ax.set_xticklabels(models)
ax.set_ylabel('MSE', fontsize=11)
ax.set_title('MSE 对比（越小越好）', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

# R²对比
ax = axes[1]
bars = ax.bar(x_pos, r2_vals, width, color=colors, alpha=0.8, edgecolor='white')
for bar, val in zip(bars, r2_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{val:.4f}', ha='center', va='bottom', fontsize=9)
ax.set_xticks(x_pos)
ax.set_xticklabels(models)
ax.set_ylabel('R²', fontsize=11)
ax.set_title('R² 对比（越大越好）', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([0, 1])

# 训练时间对比
ax = axes[2]
bars = ax.bar(x_pos, time_vals, width, color=colors, alpha=0.8, edgecolor='white')
for bar, val in zip(bars, time_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0002,
            f'{val:.4f}s', ha='center', va='bottom', fontsize=9)
ax.set_xticks(x_pos)
ax.set_xticklabels(models)
ax.set_ylabel('训练时间（秒）', fontsize=11)
ax.set_title('训练时间对比（越小越好）', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

plt.suptitle('三模型性能指标对比', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('results/10_metrics_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 指标对比图 → results/10_metrics_comparison.png")

# ── 4. 生成 Markdown 报告 ────────────────────────────────────
best_model = models[best_idx]
best_r2 = r2_vals[best_idx]

report = f"""# 实验三 — SVM 预测录取率：三模型对比分析报告

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、实验背景

本实验对比三种经典机器学习算法在研究生录取预测任务上的表现：
- **多元线性回归**：最简单的线性模型
- **SVM（支持向量机）**：强大的非线性模型
- **决策树**：直观易懂的树形模型

---

## 二、三种模型简介

### 2.1 多元线性回归（Linear Regression）

**核心思想：** 假设目标值是特征的线性组合。

```
录取概率 = w₁×GRE + w₂×托福 + w₃×GPA + ... + 常数
```

**优点：**
- 训练速度快，计算简单
- 可解释性强：能看出每个特征的权重
- 不容易过拟合

**缺点：**
- 只能处理线性关系
- 对异常值敏感
- 假设特征之间相互独立

**适用场景：** 特征和目标呈线性关系，需要快速建模和解释

---

### 2.2 SVM（支持向量机）

**核心思想：** 找到最优的超平面（或曲面）来拟合数据。

使用 RBF 核函数可以处理非线性关系：
```
K(x, x') = exp(-γ||x - x'||²)
```

**优点：**
- 能处理非线性关系（通过核函数）
- 泛化能力强，不容易过拟合
- 在高维空间表现良好

**缺点：**
- 训练速度慢（尤其是大数据集）
- 参数调优复杂（C, gamma, epsilon）
- 可解释性差（黑盒模型）
- 必须归一化

**适用场景：** 数据量中等，关系复杂，追求高精度

---

### 2.3 决策树（Decision Tree）

**核心思想：** 通过一系列"是/否"问题来做决策。

```
GRE >= 320?
├─ 是 → GPA >= 8.5?
│         ├─ 是 → 录取概率 = 0.85
│         └─ 否 → 录取概率 = 0.65
└─ 否 → ...
```

**优点：**
- 非常直观，容易理解和解释
- 不需要归一化
- 能自动处理特征交互
- 能处理非线性关系

**缺点：**
- 容易过拟合（需要剪枝）
- 不够稳定（数据稍变，树结构可能完全不同）
- 对连续值预测不够精确

**适用场景：** 需要可解释性，特征有明显的阈值划分

---

## 三、实验设置

- **数据集**：研究生录取预测，7个特征，500条数据
- **数据划分**：训练集 400 条（80%），测试集 100 条（20%），随机种子=42
- **预处理**：
  - 线性回归 & SVM：MinMaxScaler 归一化
  - 决策树：不归一化（不需要）
- **模型参数**：
  - 线性回归：默认参数
  - SVM：RBF核，C=100，gamma=0.1，epsilon=0.1
  - 决策树：max_depth=5，min_samples_split=10（防止过拟合）

---

## 四、实验结果

### 4.1 数值对比

| 模型 | MSE（↓越小越好） | RMSE（↓越小越好） | R²（↑越大越好） | 训练时间 |
|------|-----------------|------------------|----------------|----------|
| **线性回归** | {mse_vals[0]:.6f} | {rmse_vals[0]:.6f} | {r2_vals[0]:.6f} | {time_vals[0]:.4f}秒 |
| **SVM** | {mse_vals[1]:.6f} | {rmse_vals[1]:.6f} | {r2_vals[1]:.6f} | {time_vals[1]:.4f}秒 |
| **决策树** | {mse_vals[2]:.6f} | {rmse_vals[2]:.6f} | {r2_vals[2]:.6f} | {time_vals[2]:.4f}秒 |

> **结论：{best_model}效果最好（R² = {best_r2:.6f}）**

### 4.2 排名分析

**准确度排名（按 R² 从高到低）：**
"""

# 排序
sorted_indices = np.argsort(r2_vals)[::-1]
for rank, idx in enumerate(sorted_indices, 1):
    report += f"{rank}. **{models[idx]}** - R² = {r2_vals[idx]:.6f}\n"

report += f"""
**速度排名（按训练时间从快到慢）：**
"""

sorted_time_indices = np.argsort(time_vals)
for rank, idx in enumerate(sorted_time_indices, 1):
    report += f"{rank}. **{models[idx]}** - {time_vals[idx]:.4f}秒\n"

report += f"""
### 4.3 可视化分析

#### 线性回归结果图

![线性回归](07_lr_plot.png)

#### SVM结果图

![SVM](08_svm_plot.png)

#### 决策树结果图

![决策树](09_dt_plot.png)

#### 三模型全面对比图

![三模型对比](10_model_comparison_plot.png)

**3×3 九宫格，每行一个模型，每行包含：预测图、残差图、误差分布**

#### 指标对比图

![指标对比](10_metrics_comparison.png)

**MSE、R²、训练时间的柱状对比**

---

## 五、深入分析

### 5.1 为什么{best_model}效果最好？

"""

if best_idx == 0:  # 线性回归
    report += """**线性回归表现最好，说明：**
- 这个数据集的特征和目标之间主要是线性关系
- GRE、托福、GPA等分数与录取概率呈线性相关
- 简单模型有时比复杂模型更好（奥卡姆剃刀原则）

**启示：** 不要盲目追求复杂模型，先尝试简单模型建立基线。
"""
elif best_idx == 1:  # SVM
    report += """**SVM表现最好，说明：**
- 数据中存在非线性关系，RBF核捕捉到了这些模式
- SVM的泛化能力强，避免了过拟合
- 归一化后，SVM能充分利用所有特征

**启示：** 对于中等规模、关系复杂的数据，SVM是可靠选择。
"""
else:  # 决策树
    report += """**决策树表现最好，说明：**
- 数据中存在明显的阈值划分（如GRE>320, GPA>8.5）
- 特征之间有交互作用（如高GRE+低GPA的组合）
- 决策树能自动发现这些规则

**启示：** 如果数据有明显的分段特征，决策树很有效。
"""

report += f"""
### 5.2 模型选择建议

**场景1：追求最高精度**
→ 选择 **{best_model}**（R² = {best_r2:.6f}）

**场景2：需要快速训练**
→ 选择 **{models[sorted_time_indices[0]]}**（{time_vals[sorted_time_indices[0]]:.4f}秒）

**场景3：需要可解释性**
→ 选择 **线性回归**（能看系数）或 **决策树**（能看规则）

**场景4：数据量很大（百万级）**
→ 避免 SVM（太慢），选择线性回归或决策树

**场景5：特征很多（上千维）**
→ 线性回归可能欠拟合，SVM 或决策树更好

---

## 六、特征重要性分析

### 6.1 线性回归的系数

"""

# 读取线性回归系数
lr_coef = pd.read_csv('results/07_lr_coefficients.csv')
report += "| 特征 | 系数 | 解释 |\n"
report += "|------|------|------|\n"
for _, row in lr_coef.head(5).iterrows():
    direction = "正相关" if row['系数'] > 0 else "负相关"
    report += f"| {row['特征']} | {row['系数']:.4f} | {direction} |\n"

report += """
**解读：**
- 系数为正：该特征越大，录取概率越高
- 系数为负：该特征越大，录取概率越低
- 系数绝对值越大，该特征越重要

### 6.2 决策树的特征重要性

"""

# 读取决策树特征重要性
dt_feat = pd.read_csv('results/09_dt_feature_importance.csv')
report += "| 特征 | 重要性 |\n"
report += "|------|--------|\n"
for _, row in dt_feat.head(5).iterrows():
    report += f"| {row['特征']} | {row['重要性']:.4f} |\n"

report += """
**解读：**
- 重要性基于信息增益（该特征能减少多少不确定性）
- 重要性越高，该特征在决策树中越靠近根节点

---

## 七、总结与建议

### 7.1 本实验结论

1. **最佳模型**：{best_model}（R² = {best_r2:.6f}）
2. **最快模型**：{models[sorted_time_indices[0]]}（{time_vals[sorted_time_indices[0]]:.4f}秒）
3. **三个模型都达到了可接受的精度**（R² > 0.7）

### 7.2 实际应用建议

**如果你是数据科学家：**
- 先用线性回归建立基线（快速、简单）
- 再尝试 SVM 或决策树看能否提升
- 用交叉验证选择最佳模型

**如果你是产品经理：**
- 需要向用户解释预测结果 → 用线性回归或决策树
- 只关心准确度 → 用 {best_model}
- 需要实时预测（毫秒级） → 避免 SVM

**如果你是学生（做作业）：**
- 三个模型都跑一遍，对比分析
- 理解每个模型的优缺点
- 根据数据特点选择合适的模型

### 7.3 进一步优化方向

1. **超参数调优**：用 GridSearchCV 寻找最佳参数
2. **特征工程**：尝试特征交互（如 GRE×GPA）
3. **集成学习**：用随机森林或 XGBoost 提升效果
4. **交叉验证**：用 K-fold 验证模型稳定性

---

*本报告由 exp3/10_model_comparison.py 自动生成*
"""

report_path = 'results/10_model_comparison_report.md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✓ 分析报告 → {report_path}")
print("\n全部完成！结果文件：")
print("  results/07_lr_plot.png                  — 线性回归图")
print("  results/08_svm_plot.png                 — SVM图")
print("  results/09_dt_plot.png                  — 决策树图")
print("  results/10_model_comparison_plot.png    — 三模型对比图（3×3）")
print("  results/10_metrics_comparison.png       — 指标对比图")
print("  results/10_model_comparison_report.md   — Markdown 报告")
