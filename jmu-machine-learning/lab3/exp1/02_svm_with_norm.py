"""
实验三 - 02: SVM 预测录取率（归一化版本）
运行：在 lab3/ 目录下  python 02_svm_with_norm.py
"""
import os
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

# ── 2. 划分训练集 / 测试集（与01脚本完全相同的划分）────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"训练集: {len(X_train)} 条  测试集: {len(X_test)} 条")

# ── 3. Min-Max 归一化 ─────────────────────────────────────────
# 重要规则：scaler 只能在训练集上 fit，再分别 transform 训练集和测试集
# 原因：不能让测试集的信息"污染"训练过程（这叫做避免数据泄露）
scaler = MinMaxScaler()                          # 把每个特征映射到 [0, 1]
X_train_s = scaler.fit_transform(X_train)        # fit + transform 训练集
X_test_s  = scaler.transform(X_test)             # 仅 transform 测试集

# 打印对比让你直观感受归一化的效果
print("\n归一化前（训练集，前3行）:")
print(X_train.head(3).to_string())
print("\n归一化后（训练集，前3行）— 所有值都在 [0,1] 之间:")
print(pd.DataFrame(X_train_s, columns=X.columns).head(3).round(4).to_string())

# ── 4. 训练 SVM（完全相同的超参数，唯一差别是输入做了归一化）
model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
model.fit(X_train_s, y_train)

# ── 5. 预测 & 评估 ───────────────────────────────────────────
y_pred = model.predict(X_test_s)

mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

print(f"\n=== 归一化 SVM 结果 ===")
print(f"MSE  : {mse:.6f}   （越小越好）")
print(f"RMSE : {rmse:.6f}  （越小越好）")
print(f"R²   : {r2:.6f}    （越接近1越好）")

# ── 6. 保存结果 ──────────────────────────────────────────────
pd.DataFrame({
    '真实值': y_test.values,
    '预测值': y_pred,
    '误差':   y_test.values - y_pred
}).to_csv('results/02_norm_predictions.csv', index=False, encoding='utf-8-sig')

pd.DataFrame({'MSE': [mse], 'RMSE': [rmse], 'R2': [r2]}).to_csv(
    'results/02_norm_metrics.csv', index=False
)

# ── 7. 绘图 ──────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('SVM 预测结果（归一化）', fontsize=14, fontweight='bold')

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
plt.savefig('results/02_norm_plot.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ 图片  → results/02_norm_plot.png")
print("✓ 结果  → results/02_norm_predictions.csv")
print("✓ 指标  → results/02_norm_metrics.csv")
