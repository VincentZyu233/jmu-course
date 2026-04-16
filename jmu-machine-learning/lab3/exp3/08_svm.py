"""
实验三 - 08: SVM 预测录取率（用于模型对比）
运行：在 lab3/ 目录下  python exp3/08_svm.py
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

# ── 3. 归一化 ─────────────────────────────────────────────────
scaler = MinMaxScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 4. 训练 SVM ───────────────────────────────────────────────
model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
start_time = time.time()
model.fit(X_train_s, y_train)
train_time = time.time() - start_time

# ── 5. 预测 & 评估 ───────────────────────────────────────────
start_time = time.time()
y_pred = model.predict(X_test_s)
pred_time = time.time() - start_time

mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

print(f"\n=== SVM 结果 ===")
print(f"MSE  : {mse:.6f}")
print(f"RMSE : {rmse:.6f}")
print(f"R²   : {r2:.6f}")
print(f"训练时间: {train_time:.4f} 秒")
print(f"预测时间: {pred_time:.4f} 秒")

# ── 6. 保存结果 ──────────────────────────────────────────────
pd.DataFrame({
    '真实值': y_test.values,
    '预测值': y_pred,
    '误差':   y_test.values - y_pred
}).to_csv('results/08_svm_predictions.csv', index=False, encoding='utf-8-sig')

pd.DataFrame({
    'MSE': [mse], 'RMSE': [rmse], 'R2': [r2],
    'train_time': [train_time], 'pred_time': [pred_time],
    'model_type': ['SVM']
}).to_csv('results/08_svm_metrics.csv', index=False)

# ── 7. 绘图 ──────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('SVM 预测结果', fontsize=14, fontweight='bold')

ax = axes[0]
ax.scatter(y_test, y_pred, alpha=0.65, color='mediumseagreen',
           edgecolors='white', linewidth=0.4, s=55, label='预测点')
lims = [0.28, 1.02]
ax.plot(lims, lims, 'r--', lw=1.8, label='理想预测线 (y=x)')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('真实录取概率', fontsize=11)
ax.set_ylabel('预测录取概率', fontsize=11)
ax.set_title(f'预测值 vs 真实值\nR² = {r2:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

ax = axes[1]
residuals = y_test.values - y_pred
ax.scatter(y_pred, residuals, alpha=0.65, color='mediumpurple',
           edgecolors='white', linewidth=0.4, s=55)
ax.axhline(0, color='r', linestyle='--', lw=1.8, label='零误差线')
ax.set_xlabel('预测录取概率', fontsize=11)
ax.set_ylabel('残差（真实值 - 预测值）', fontsize=11)
ax.set_title(f'残差图\nRMSE = {rmse:.4f}', fontsize=12)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/08_svm_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ 图片  → results/08_svm_plot.png")
print("✓ 结果  → results/08_svm_predictions.csv")
print("✓ 指标  → results/08_svm_metrics.csv")
