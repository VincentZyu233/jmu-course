"""
实验三 - 09: 决策树预测录取率
运行：在 lab3/ 目录下  python exp3/09_decision_tree.py
"""
import os
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
os.makedirs('results', exist_ok=True)

# ── 1. 加载数据 ──────────────────────────────────────────────
df = pd.read_csv('data/data.csv')
df.columns = df.columns.str.strip()

X = df.drop(columns=['Serial No.', 'Chance of Admit'])
y = df['Chance of Admit']

# ── 2. 划分训练集 / 测试集 ────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"训练集: {len(X_train)} 条  测试集: {len(X_test)} 条")
print("注意：决策树不需要归一化（基于阈值划分，不受特征尺度影响）")

# ── 3. 训练决策树（不归一化）─────────────────────────────────
# max_depth=5 防止过拟合，min_samples_split=10 确保节点有足够样本
model = DecisionTreeRegressor(max_depth=5, min_samples_split=10, random_state=42)
start_time = time.time()
model.fit(X_train, y_train)
train_time = time.time() - start_time

# ── 4. 预测 & 评估 ───────────────────────────────────────────
start_time = time.time()
y_pred = model.predict(X_test)
pred_time = time.time() - start_time

mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

print(f"\n=== 决策树结果 ===")
print(f"MSE  : {mse:.6f}")
print(f"RMSE : {rmse:.6f}")
print(f"R²   : {r2:.6f}")
print(f"训练时间: {train_time:.4f} 秒")
print(f"预测时间: {pred_time:.4f} 秒")
print(f"树的深度: {model.get_depth()}")
print(f"叶子节点数: {model.get_n_leaves()}")

# ── 5. 特征重要性 ─────────────────────────────────────────────
feature_importance = pd.DataFrame({
    '特征': X.columns,
    '重要性': model.feature_importances_
}).sort_values('重要性', ascending=False)

print("\n特征重要性（按重要性排序）:")
print(feature_importance.to_string(index=False))

# ── 6. 保存结果 ──────────────────────────────────────────────
pd.DataFrame({
    '真实值': y_test.values,
    '预测值': y_pred,
    '误差':   y_test.values - y_pred
}).to_csv('results/09_dt_predictions.csv', index=False, encoding='utf-8-sig')

pd.DataFrame({
    'MSE': [mse], 'RMSE': [rmse], 'R2': [r2],
    'train_time': [train_time], 'pred_time': [pred_time],
    'model_type': ['Decision Tree'],
    'tree_depth': [model.get_depth()],
    'n_leaves': [model.get_n_leaves()]
}).to_csv('results/09_dt_metrics.csv', index=False)

feature_importance.to_csv('results/09_dt_feature_importance.csv', index=False, encoding='utf-8-sig')

# ── 7. 绘图（3个子图）────────────────────────────────────────
fig = plt.figure(figsize=(15, 5))
gs = fig.add_gridspec(1, 3)

# 左图：预测 vs 真实
ax = fig.add_subplot(gs[0, 0])
ax.scatter(y_test, y_pred, alpha=0.65, color='mediumpurple',
           edgecolors='white', linewidth=0.4, s=55, label='预测点')
lims = [0.28, 1.02]
ax.plot(lims, lims, 'r--', lw=1.8, label='理想预测线 (y=x)')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('真实录取概率', fontsize=11)
ax.set_ylabel('预测录取概率', fontsize=11)
ax.set_title(f'预测值 vs 真实值\nR² = {r2:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 中图：残差图
ax = fig.add_subplot(gs[0, 1])
residuals = y_test.values - y_pred
ax.scatter(y_pred, residuals, alpha=0.65, color='coral',
           edgecolors='white', linewidth=0.4, s=55)
ax.axhline(0, color='r', linestyle='--', lw=1.8, label='零误差线')
ax.set_xlabel('预测录取概率', fontsize=11)
ax.set_ylabel('残差（真实值 - 预测值）', fontsize=11)
ax.set_title(f'残差图\nRMSE = {rmse:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 右图：特征重要性
ax = fig.add_subplot(gs[0, 2])
colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(feature_importance)))
bars = ax.barh(feature_importance['特征'], feature_importance['重要性'],
               color=colors, alpha=0.8, edgecolor='white')
ax.set_xlabel('重要性得分', fontsize=11)
ax.set_title('特征重要性\n（基于信息增益）', fontsize=12)
ax.grid(True, alpha=0.3, axis='x')

fig.suptitle('决策树预测结果', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('results/09_dt_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ 图片  → results/09_dt_plot.png")
print("✓ 结果  → results/09_dt_predictions.csv")
print("✓ 指标  → results/09_dt_metrics.csv")
print("✓ 特征重要性 → results/09_dt_feature_importance.csv")
