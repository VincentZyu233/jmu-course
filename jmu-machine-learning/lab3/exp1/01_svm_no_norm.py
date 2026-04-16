"""
实验三 - 01: SVM 预测录取率（不归一化）
运行：在 lab3/ 目录下  python 01_svm_no_norm.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
os.makedirs('results', exist_ok=True)

# ── 1. 加载数据 ──────────────────────────────────────────────
df = pd.read_csv('data/data.csv')
df.columns = df.columns.str.strip()          # 去掉列名首尾空格

X = df.drop(columns=['Serial No.', 'Chance of Admit'])
y = df['Chance of Admit']

# ── 2. 划分训练集 / 测试集（8:2，固定随机种子保证可复现）──
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"训练集: {len(X_train)} 条  测试集: {len(X_test)} 条")
print("特征范围（训练集）:")
print(X_train.describe().loc[['min', 'max']].to_string())

# ── 3. 训练 SVM（不做任何归一化）────────────────────────────
# RBF核：C=100控制拟合松紧，gamma=0.1控制影响范围，epsilon=0.1是容忍误差带
model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
model.fit(X_train, y_train)

# ── 4. 预测 & 评估 ───────────────────────────────────────────
y_pred = model.predict(X_test)

mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

print(f"\n=== 不归一化 SVM 结果 ===")
print(f"MSE  : {mse:.6f}   （越小越好）")
print(f"RMSE : {rmse:.6f}  （越小越好）")
print(f"R²   : {r2:.6f}    （越接近1越好）")

# ── 5. 保存结果（供 03_analysis.py 读取）────────────────────
pd.DataFrame({
    '真实值': y_test.values,
    '预测值': y_pred,
    '误差':   y_test.values - y_pred
}).to_csv('results/01_no_norm_predictions.csv', index=False, encoding='utf-8-sig')

pd.DataFrame({'MSE': [mse], 'RMSE': [rmse], 'R2': [r2]}).to_csv(
    'results/01_no_norm_metrics.csv', index=False
)

# ── 6. 绘图 ──────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('SVM 预测结果（不归一化）', fontsize=14, fontweight='bold')

# 左图：预测值 vs 真实值
ax = axes[0]
ax.scatter(y_test, y_pred, alpha=0.65, color='steelblue',
           edgecolors='white', linewidth=0.4, s=55, label='预测点')
lims = [0.28, 1.02]
ax.plot(lims, lims, 'r--', lw=1.8, label='理想预测线 (y=x)')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('真实录取概率', fontsize=11)
ax.set_ylabel('预测录取概率', fontsize=11)
ax.set_title(f'预测值 vs 真实值\nR² = {r2:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 右图：残差图（残差 = 真实值 - 预测值，越靠近0越准）
ax = axes[1]
residuals = y_test.values - y_pred
ax.scatter(y_pred, residuals, alpha=0.65, color='coral',
           edgecolors='white', linewidth=0.4, s=55)
ax.axhline(0, color='r', linestyle='--', lw=1.8, label='零误差线')
ax.set_xlabel('预测录取概率', fontsize=11)
ax.set_ylabel('残差（真实值 - 预测值）', fontsize=11)
ax.set_title(f'残差图\nRMSE = {rmse:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/01_no_norm_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ 图片  → results/01_no_norm_plot.png")
print("✓ 结果  → results/01_no_norm_predictions.csv")
print("✓ 指标  → results/01_no_norm_metrics.csv")
