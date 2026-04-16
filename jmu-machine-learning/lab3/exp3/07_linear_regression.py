"""
实验三 - 07: 多元线性回归预测录取率
运行：在 lab3/ 目录下  python exp3/07_linear_regression.py
"""
import os
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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
print(f"特征: {list(X.columns)}")

# ── 3. 归一化（线性回归虽然不强制要求，但归一化后系数更好解释）
scaler = MinMaxScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 4. 训练线性回归模型 ──────────────────────────────────────
model = LinearRegression()
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

print(f"\n=== 多元线性回归结果 ===")
print(f"MSE  : {mse:.6f}")
print(f"RMSE : {rmse:.6f}")
print(f"R²   : {r2:.6f}")
print(f"训练时间: {train_time:.4f} 秒")
print(f"预测时间: {pred_time:.4f} 秒")

# ── 6. 分析特征重要性（回归系数）─────────────────────────────
coefficients = pd.DataFrame({
    '特征': X.columns,
    '系数': model.coef_,
    '绝对值': np.abs(model.coef_)
}).sort_values('绝对值', ascending=False)

print(f"\n截距（常数项）: {model.intercept_:.4f}")
print("\n特征重要性（按系数绝对值排序）:")
print(coefficients[['特征', '系数']].to_string(index=False))

# ── 7. 保存结果 ──────────────────────────────────────────────
pd.DataFrame({
    '真实值': y_test.values,
    '预测值': y_pred,
    '误差':   y_test.values - y_pred
}).to_csv('results/07_lr_predictions.csv', index=False, encoding='utf-8-sig')

pd.DataFrame({
    'MSE': [mse], 'RMSE': [rmse], 'R2': [r2],
    'train_time': [train_time], 'pred_time': [pred_time],
    'model_type': ['Linear Regression']
}).to_csv('results/07_lr_metrics.csv', index=False)

coefficients.to_csv('results/07_lr_coefficients.csv', index=False, encoding='utf-8-sig')

# ── 8. 绘图（3个子图）────────────────────────────────────────
fig = plt.figure(figsize=(15, 5))
gs = fig.add_gridspec(1, 3)

# 左图：预测 vs 真实
ax = fig.add_subplot(gs[0, 0])
ax.scatter(y_test, y_pred, alpha=0.65, color='darkorange',
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

# 右图：特征系数（重要性）
ax = fig.add_subplot(gs[0, 2])
colors = ['green' if c > 0 else 'red' for c in coefficients['系数']]
bars = ax.barh(coefficients['特征'], coefficients['系数'],
               color=colors, alpha=0.7, edgecolor='white')
ax.axvline(0, color='black', linestyle='-', lw=1)
ax.set_xlabel('回归系数', fontsize=11)
ax.set_title('特征重要性（系数）\n绿色=正相关，红色=负相关', fontsize=12)
ax.grid(True, alpha=0.3, axis='x')

fig.suptitle('多元线性回归预测结果', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('results/07_lr_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ 图片  → results/07_lr_plot.png")
print("✓ 结果  → results/07_lr_predictions.csv")
print("✓ 指标  → results/07_lr_metrics.csv")
print("✓ 系数  → results/07_lr_coefficients.csv")
