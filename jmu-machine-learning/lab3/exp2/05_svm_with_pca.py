"""
实验三 - 05: SVM 预测录取率（归一化 + PCA降维）
运行：在 lab3/ 目录下  python exp2/05_svm_with_pca.py
"""
import os
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
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
print(f"原始特征数量: {X.shape[1]} 个")

# ── 3. 归一化（PCA前必须归一化）──────────────────────────────
scaler = MinMaxScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 4. PCA 降维 ───────────────────────────────────────────────
# 保留95%的方差，让PCA自动决定主成分数量
pca = PCA(n_components=0.95, random_state=42)
X_train_pca = pca.fit_transform(X_train_s)
X_test_pca  = pca.transform(X_test_s)

n_components = pca.n_components_
explained_var = pca.explained_variance_ratio_
cumsum_var = np.cumsum(explained_var)

print(f"\n=== PCA 降维结果 ===")
print(f"降维后特征数: {n_components} 个（原始7个）")
print(f"总方差解释率: {cumsum_var[-1]:.2%}")
print("\n各主成分方差贡献:")
for i, (var, cum) in enumerate(zip(explained_var, cumsum_var), 1):
    print(f"  PC{i}: {var:.2%}  (累计: {cum:.2%})")

# ── 5. 训练 SVM（记录训练时间）────────────────────────────────
model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
start_time = time.time()
model.fit(X_train_pca, y_train)
train_time = time.time() - start_time

# ── 6. 预测 & 评估（记录预测时间）────────────────────────────
start_time = time.time()
y_pred = model.predict(X_test_pca)
pred_time = time.time() - start_time

mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

print(f"\n=== 归一化 + PCA降维 ===")
print(f"MSE  : {mse:.6f}")
print(f"RMSE : {rmse:.6f}")
print(f"R²   : {r2:.6f}")
print(f"训练时间: {train_time:.4f} 秒")
print(f"预测时间: {pred_time:.4f} 秒")

# ── 7. 保存结果 ──────────────────────────────────────────────
pd.DataFrame({
    '真实值': y_test.values,
    '预测值': y_pred,
    '误差':   y_test.values - y_pred
}).to_csv('results/05_pca_predictions.csv', index=False, encoding='utf-8-sig')

pd.DataFrame({
    'MSE': [mse], 'RMSE': [rmse], 'R2': [r2],
    'train_time': [train_time], 'pred_time': [pred_time],
    'n_components': [n_components], 'explained_variance': [cumsum_var[-1]]
}).to_csv('results/05_pca_metrics.csv', index=False)

# 保存PCA详细信息
pd.DataFrame({
    'PC': [f'PC{i+1}' for i in range(n_components)],
    'variance_ratio': explained_var,
    'cumulative_variance': cumsum_var
}).to_csv('results/05_pca_components.csv', index=False)

# ── 8. 绘图（3个子图）────────────────────────────────────────
fig = plt.figure(figsize=(15, 5))
gs = fig.add_gridspec(1, 3)

# 左图：预测 vs 真实
ax = fig.add_subplot(gs[0, 0])
ax.scatter(y_test, y_pred, alpha=0.65, color='mediumseagreen',
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
ax.scatter(y_pred, residuals, alpha=0.65, color='mediumpurple',
           edgecolors='white', linewidth=0.4, s=55)
ax.axhline(0, color='r', linestyle='--', lw=1.8, label='零误差线')
ax.set_xlabel('预测录取概率', fontsize=11)
ax.set_ylabel('残差（真实值 - 预测值）', fontsize=11)
ax.set_title(f'残差图\nRMSE = {rmse:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 右图：PCA方差解释率
ax = fig.add_subplot(gs[0, 2])
x_pos = np.arange(1, n_components + 1)
bars = ax.bar(x_pos, explained_var, alpha=0.7, color='skyblue',
              edgecolor='white', label='单个主成分')
ax.plot(x_pos, cumsum_var, 'ro-', linewidth=2, markersize=6,
        label='累计方差解释率')
for i, (bar, cum) in enumerate(zip(bars, cumsum_var)):
    ax.text(bar.get_x() + bar.get_width()/2, cum + 0.02,
            f'{cum:.1%}', ha='center', va='bottom', fontsize=9)
ax.set_xlabel('主成分', fontsize=11)
ax.set_ylabel('方差解释率', fontsize=11)
ax.set_title(f'PCA 方差解释\n{n_components}个主成分保留{cumsum_var[-1]:.1%}信息', fontsize=12)
ax.set_xticks(x_pos)
ax.set_xticklabels([f'PC{i}' for i in x_pos])
ax.legend(fontsize=9); ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([0, 1.1])

fig.suptitle('SVM 预测结果（归一化 + PCA降维）', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/05_pca_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ 图片  → results/05_pca_plot.png")
print("✓ 结果  → results/05_pca_predictions.csv")
print("✓ 指标  → results/05_pca_metrics.csv")
print("✓ PCA详情 → results/05_pca_components.csv")
