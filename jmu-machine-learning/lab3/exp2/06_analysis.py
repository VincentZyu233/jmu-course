"""
实验三 - 06: PCA降维对比分析 + 生成 Markdown 报告
先运行 04 和 05，再运行此脚本。
运行：在 lab3/ 目录下  python exp2/06_analysis.py
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

# ── 1. 读取两组结果 ──────────────────────────────────────────
m1 = pd.read_csv('results/04_no_pca_metrics.csv')
m2 = pd.read_csv('results/05_pca_metrics.csv')
p1 = pd.read_csv('results/04_no_pca_predictions.csv')
p2 = pd.read_csv('results/05_pca_predictions.csv')
pca_info = pd.read_csv('results/05_pca_components.csv')

mse1, rmse1, r2_1 = m1['MSE'].iloc[0], m1['RMSE'].iloc[0], m1['R2'].iloc[0]
mse2, rmse2, r2_2 = m2['MSE'].iloc[0], m2['RMSE'].iloc[0], m2['R2'].iloc[0]
time1, time2 = m1['train_time'].iloc[0], m2['train_time'].iloc[0]
n_feat1 = int(m1['n_features'].iloc[0])
n_feat2 = int(m2['n_components'].iloc[0])
explained_var = m2['explained_variance'].iloc[0]

print(f"{'指标':<12} {'不降维(7特征)':>15} {'PCA降维({n_feat2}特征)':>15}")
print("-" * 45)
print(f"{'MSE':<12} {mse1:>15.6f} {mse2:>15.6f}")
print(f"{'RMSE':<12} {rmse1:>15.6f} {rmse2:>15.6f}")
print(f"{'R²':<12} {r2_1:>15.6f} {r2_2:>15.6f}")
print(f"{'训练时间(秒)':<12} {time1:>15.4f} {time2:>15.4f}")
print(f"{'特征数':<12} {n_feat1:>15} {n_feat2:>15}")
print(f"{'方差保留':<12} {'100.0%':>15} {f'{explained_var:.1%}':>15}")

# ── 2. 对比图（2×3）─────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
lims = [0.28, 1.02]

# 第一行：不降维
ax = fig.add_subplot(gs[0, 0])
ax.scatter(p1['真实值'], p1['预测值'], alpha=0.65, color='steelblue', s=50,
           edgecolors='white', lw=0.4, label='预测点')
ax.plot(lims, lims, 'r--', lw=1.8, label='理想线')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('真实录取概率'); ax.set_ylabel('预测录取概率')
ax.set_title(f'[不降维] 预测 vs 真实\nR² = {r2_1:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

ax = fig.add_subplot(gs[0, 1])
residuals1 = p1['真实值'] - p1['预测值']
ax.scatter(p1['预测值'], residuals1, alpha=0.65, color='coral', s=50,
           edgecolors='white', lw=0.4)
ax.axhline(0, color='r', linestyle='--', lw=1.8, label='零误差线')
ax.set_xlabel('预测录取概率'); ax.set_ylabel('残差')
ax.set_title(f'[不降维] 残差图\nRMSE = {rmse1:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

ax = fig.add_subplot(gs[0, 2])
ax.text(0.5, 0.5, f'特征数: {n_feat1}\n方差保留: 100%\n训练时间: {time1:.4f}秒',
        ha='center', va='center', fontsize=14,
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('[不降维] 统计信息', fontsize=12)

# 第二行：PCA降维
ax = fig.add_subplot(gs[1, 0])
ax.scatter(p2['真实值'], p2['预测值'], alpha=0.65, color='mediumseagreen', s=50,
           edgecolors='white', lw=0.4, label='预测点')
ax.plot(lims, lims, 'r--', lw=1.8, label='理想线')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('真实录取概率'); ax.set_ylabel('预测录取概率')
ax.set_title(f'[PCA降维] 预测 vs 真实\nR² = {r2_2:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

ax = fig.add_subplot(gs[1, 1])
residuals2 = p2['真实值'] - p2['预测值']
ax.scatter(p2['预测值'], residuals2, alpha=0.65, color='mediumpurple', s=50,
           edgecolors='white', lw=0.4)
ax.axhline(0, color='r', linestyle='--', lw=1.8, label='零误差线')
ax.set_xlabel('预测录取概率'); ax.set_ylabel('残差')
ax.set_title(f'[PCA降维] 残差图\nRMSE = {rmse2:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

ax = fig.add_subplot(gs[1, 2])
x_pos = np.arange(1, len(pca_info) + 1)
bars = ax.bar(x_pos, pca_info['variance_ratio'], alpha=0.7, color='skyblue',
              edgecolor='white')
ax.plot(x_pos, pca_info['cumulative_variance'], 'ro-', linewidth=2, markersize=6)
for i, cum in enumerate(pca_info['cumulative_variance']):
    ax.text(i+1, cum + 0.02, f'{cum:.1%}', ha='center', va='bottom', fontsize=8)
ax.set_xlabel('主成分'); ax.set_ylabel('方差解释率')
ax.set_title(f'[PCA降维] 方差解释\n{n_feat2}个主成分保留{explained_var:.1%}信息', fontsize=12)
ax.set_xticks(x_pos)
ax.set_xticklabels([f'PC{i}' for i in x_pos])
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([0, 1.1])

fig.suptitle('SVM：PCA降维 vs 不降维 — 全面对比', fontsize=15, fontweight='bold')
plt.savefig('results/06_pca_comparison_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ 对比图 → results/06_pca_comparison_plot.png")

# ── 3. 生成 Markdown 报告 ────────────────────────────────────
better = "PCA降维" if r2_2 > r2_1 else "不降维"
r2_change = r2_2 - r2_1
time_speedup = (time1 - time2) / time1 * 100
dim_reduction = (n_feat1 - n_feat2) / n_feat1 * 100

report = f"""# 实验三 — SVM 预测录取率：PCA降维对比分析报告

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、实验背景

本实验对比 **PCA降维** 对 SVM 模型性能的影响。
两组实验都使用归一化（实验1已证明归一化效果更好），唯一区别是是否使用PCA降维。

---

## 二、什么是PCA降维？

### 2.1 核心思想

PCA（主成分分析）是一种降维技术，把多个相关的特征合并成少数几个"主成分"。

**通俗比喻：**
- 原始数据：7个特征（GRE、托福、GPA等）
- PCA降维：找出数据中"最重要的方向"，用{n_feat2}个综合指标代替原来的7个
- 这{n_feat2}个主成分保留了原始数据 **{explained_var:.1%}** 的信息

### 2.2 为什么要降维？

**优点：**
1. **减少计算量**：特征少了，训练更快
2. **去除冗余**：GRE和托福往往相关，PCA能合并这些相关信息
3. **避免过拟合**：特征太多容易"记住"训练数据，降维能提高泛化能力
4. **可视化**：降到2-3维可以画图观察数据分布

**缺点：**
1. **损失信息**：{n_feat2}个主成分只保留{explained_var:.1%}信息，丢失了{100-explained_var*100:.1f}%
2. **可解释性差**：主成分是原始特征的线性组合，不像"GRE分数"那么直观

---

## 三、实验设置

- **模型**：SVR（支持向量回归），RBF 核，C=100，gamma=0.1，epsilon=0.1
- **数据划分**：训练集 400 条（80%），测试集 100 条（20%），随机种子=42
- **预处理**：两组都用 MinMaxScaler 归一化
- **唯一变量**：
  - **对比组A**：归一化 → SVM（7个特征）
  - **对比组B**：归一化 → PCA降维 → SVM（{n_feat2}个主成分）

---

## 四、实验结果

### 4.1 数值对比

| 指标 | 不降维（7特征） | PCA降维（{n_feat2}特征） | 变化 |
|------|----------------|---------------------|------|
| **MSE**（↓越小越好） | {mse1:.6f} | {mse2:.6f} | {(mse2-mse1)/mse1*100:+.1f}% |
| **RMSE**（↓越小越好） | {rmse1:.6f} | {rmse2:.6f} | {(rmse2-rmse1)/rmse1*100:+.1f}% |
| **R²**（↑越大越好） | {r2_1:.6f} | {r2_2:.6f} | {r2_change:+.6f} |
| **训练时间** | {time1:.4f}秒 | {time2:.4f}秒 | {time_speedup:+.1f}% |
| **特征数** | {n_feat1} | {n_feat2} | -{dim_reduction:.0f}% |
| **方差保留** | 100.0% | {explained_var:.1%} | -{100-explained_var*100:.1f}% |

> **结论：{better}效果更好。**

### 4.2 PCA主成分分析

降维后的{n_feat2}个主成分及其方差贡献：

| 主成分 | 方差贡献 | 累计方差 |
|--------|----------|----------|
"""

for _, row in pca_info.iterrows():
    report += f"| {row['PC']} | {row['variance_ratio']:.2%} | {row['cumulative_variance']:.2%} |\n"

report += f"""
**解读：**
- **PC1（第一主成分）**：解释了 {pca_info['variance_ratio'].iloc[0]:.1%} 的数据变化，是最重要的综合指标
- 可能代表"学术能力"（GRE+托福+GPA的综合）
"""

if n_feat2 >= 2:
    report += f"- **PC2（第二主成分）**：解释了 {pca_info['variance_ratio'].iloc[1]:.1%}，可能代表'软实力'（推荐信+SOP）\n"

report += f"""
### 4.3 可视化分析

#### 不降维结果图

![不降维](04_no_pca_plot.png)

#### PCA降维结果图

![PCA降维](05_pca_plot.png)

#### 全面对比图

![对比图](06_pca_comparison_plot.png)

**图中包含 6 个子图（2行×3列）：**
- **第一行**：不降维的预测图、残差图、统计信息
- **第二行**：PCA降维的预测图、残差图、方差解释图

---

## 五、深入分析

### 5.1 为什么降维后效果{"变好" if r2_2 > r2_1 else "变差"}了？

"""

if r2_2 > r2_1:
    report += f"""**降维提升了模型性能（R² 从 {r2_1:.4f} → {r2_2:.4f}）**

可能原因：
1. **去除噪声**：原始7个特征中可能有噪声或不重要的特征，PCA过滤掉了
2. **避免过拟合**：特征从{n_feat1}个减少到{n_feat2}个，模型更简洁，泛化能力更强
3. **特征相关性**：GRE、托福、GPA等特征高度相关，PCA合并后消除了多重共线性

**结论：** 对于这个数据集，{n_feat2}个主成分已经足够，额外的特征反而引入了噪声。
"""
else:
    report += f"""**降维降低了模型性能（R² 从 {r2_1:.4f} → {r2_2:.4f}）**

可能原因：
1. **信息损失**：{n_feat2}个主成分只保留了{explained_var:.1%}信息，丢失的{100-explained_var*100:.1f}%可能包含重要信息
2. **非线性关系**：PCA是线性降维，如果特征之间有非线性关系，PCA无法捕捉
3. **数据集特点**：这个数据集只有7个特征，本身维度不高，降维收益有限

**结论：** 对于这个数据集，保留所有7个特征效果更好。
"""

report += f"""
### 5.2 计算效率对比

- **训练时间**：降维后 {time_speedup:+.1f}%（{"更快" if time_speedup > 0 else "更慢"}）
- **特征数**：从{n_feat1}个减少到{n_feat2}个，减少{dim_reduction:.0f}%

**注意：** 在这个小数据集上（500条），时间差异不明显。
但在大数据集（百万级样本、上千特征）上，降维能显著加速训练。

---

## 六、结论与建议

### 6.1 何时使用PCA降维？

**适合降维的场景：**
- 特征数量很多（几十到上千个）
- 特征之间高度相关（如图像的像素、文本的词频）
- 计算资源有限，需要加速训练
- 需要可视化高维数据（降到2-3维）

**不适合降维的场景：**
- 特征数量本身就很少（如本实验的7个）
- 特征之间相互独立，没有冗余
- 需要保留特征的可解释性（如医疗诊断、金融风控）

### 6.2 实际开发中的最佳实践

1. **先尝试不降维**：如果特征不多（<20个），先用全部特征训练
2. **观察方差解释率**：如果前几个主成分就能解释95%以上方差，可以考虑降维
3. **交叉验证**：用交叉验证对比降维前后的效果，选择更好的方案
4. **注意顺序**：归一化 → PCA → 模型训练（PCA前必须归一化）

### 6.3 本实验总结

- **数据集**：研究生录取预测，7个特征，500条数据
- **PCA结果**：{n_feat2}个主成分保留{explained_var:.1%}信息
- **模型效果**：{better}效果更好（R² = {max(r2_1, r2_2):.4f}）
- **建议**：对于这个数据集，{"使用PCA降维" if r2_2 > r2_1 else "保留全部特征"}

---

*本报告由 exp2/06_analysis.py 自动生成*
"""

report_path = 'results/06_pca_analysis_report.md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✓ 分析报告 → {report_path}")
print("\n全部完成！结果文件：")
print("  results/04_no_pca_plot.png           — 不降维图")
print("  results/05_pca_plot.png              — PCA降维图")
print("  results/06_pca_comparison_plot.png   — 对比图")
print("  results/06_pca_analysis_report.md    — Markdown 报告")
