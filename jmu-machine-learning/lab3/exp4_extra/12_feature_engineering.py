"""
实验三 - 12: 特征工程（交互特征 + 多项式特征）
运行：在 lab3/ 目录下  python exp4_extra/12_feature_engineering.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
os.makedirs('results', exist_ok=True)

print("=" * 60)
print("特征工程实验")
print("=" * 60)

# ── 1. 加载数据 ──────────────────────────────────────────────
df = pd.read_csv('data/data.csv')
df.columns = df.columns.str.strip()

X = df.drop(columns=['Serial No.', 'Chance of Admit'])
y = df['Chance of Admit']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n原始特征数: {X.shape[1]}")
print(f"特征列表: {list(X.columns)}")

# ── 2. 基线模型（原始特征）────────────────────────────────────
print("\n[1/3] 基线模型（原始7个特征）...")
scaler_base = MinMaxScaler()
X_train_base = scaler_base.fit_transform(X_train)
X_test_base = scaler_base.transform(X_test)

model_base = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
model_base.fit(X_train_base, y_train)
y_pred_base = model_base.predict(X_test_base)

mse_base = mean_squared_error(y_test, y_pred_base)
r2_base = r2_score(y_test, y_pred_base)

print(f"R² = {r2_base:.6f}, MSE = {mse_base:.6f}")

# ── 3. 手动交互特征 ──────────────────────────────────────────
print("\n[2/3] 添加手动交互特征...")

# 创建有意义的交互特征
X_train_interact = X_train.copy()
X_test_interact = X_test.copy()

# 学术能力综合指标
X_train_interact['GRE_TOEFL'] = X_train['GRE Score'] * X_train['TOEFL Score']
X_test_interact['GRE_TOEFL'] = X_test['GRE Score'] * X_test['TOEFL Score']

X_train_interact['GRE_CGPA'] = X_train['GRE Score'] * X_train['CGPA']
X_test_interact['GRE_CGPA'] = X_test['GRE Score'] * X_test['CGPA']

X_train_interact['TOEFL_CGPA'] = X_train['TOEFL Score'] * X_train['CGPA']
X_test_interact['TOEFL_CGPA'] = X_test['TOEFL Score'] * X_test['CGPA']

# 软实力综合指标
X_train_interact['SOP_LOR'] = X_train['SOP'] * X_train['LOR']
X_test_interact['SOP_LOR'] = X_test['SOP'] * X_test['LOR']

# 学术+研究
X_train_interact['CGPA_Research'] = X_train['CGPA'] * X_train['Research']
X_test_interact['CGPA_Research'] = X_test['CGPA'] * X_test['Research']

# 院校+研究
X_train_interact['Rating_Research'] = X_train['University Rating'] * X_train['Research']
X_test_interact['Rating_Research'] = X_test['University Rating'] * X_test['Research']

print(f"新增特征数: {X_train_interact.shape[1] - X_train.shape[1]}")
print(f"总特征数: {X_train_interact.shape[1]}")
print(f"新增特征: {[col for col in X_train_interact.columns if col not in X_train.columns]}")

# 归一化并训练
scaler_interact = MinMaxScaler()
X_train_interact_s = scaler_interact.fit_transform(X_train_interact)
X_test_interact_s = scaler_interact.transform(X_test_interact)

model_interact = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
model_interact.fit(X_train_interact_s, y_train)
y_pred_interact = model_interact.predict(X_test_interact_s)

mse_interact = mean_squared_error(y_test, y_pred_interact)
r2_interact = r2_score(y_test, y_pred_interact)

print(f"R² = {r2_interact:.6f}, MSE = {mse_interact:.6f}")
print(f"R² 提升: {r2_interact - r2_base:+.6f}")

# ── 4. 多项式特征（2次）─────────────────────────────────────
print("\n[3/3] 添加多项式特征（2次）...")

# 只对数值型特征做多项式（避免特征爆炸）
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

print(f"多项式特征数: {X_train_poly.shape[1]}")
print(f"特征增长: {X_train.shape[1]} → {X_train_poly.shape[1]}")

# 归一化并训练
scaler_poly = MinMaxScaler()
X_train_poly_s = scaler_poly.fit_transform(X_train_poly)
X_test_poly_s = scaler_poly.transform(X_test_poly)

model_poly = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
model_poly.fit(X_train_poly_s, y_train)
y_pred_poly = model_poly.predict(X_test_poly_s)

mse_poly = mean_squared_error(y_test, y_pred_poly)
r2_poly = r2_score(y_test, y_pred_poly)

print(f"R² = {r2_poly:.6f}, MSE = {mse_poly:.6f}")
print(f"R² 提升: {r2_poly - r2_base:+.6f}")

# ── 5. 保存结果 ──────────────────────────────────────────────
results = pd.DataFrame({
    '方法': ['原始特征', '手动交互特征', '多项式特征(2次)'],
    '特征数': [X_train.shape[1], X_train_interact.shape[1], X_train_poly.shape[1]],
    'MSE': [mse_base, mse_interact, mse_poly],
    'R2': [r2_base, r2_interact, r2_poly],
    'R2提升': [0, r2_interact - r2_base, r2_poly - r2_base]
})

results.to_csv('results/12_feature_engineering_results.csv', index=False, encoding='utf-8-sig')

# 保存预测结果
pd.DataFrame({
    '真实值': y_test.values,
    '原始特征': y_pred_base,
    '交互特征': y_pred_interact,
    '多项式特征': y_pred_poly
}).to_csv('results/12_predictions.csv', index=False, encoding='utf-8-sig')

# ── 6. 可视化 ────────────────────────────────────────────────
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
lims = [0.28, 1.02]

predictions = [
    (y_pred_base, '原始特征', 'steelblue', r2_base),
    (y_pred_interact, '交互特征', 'darkorange', r2_interact),
    (y_pred_poly, '多项式特征', 'mediumseagreen', r2_poly)
]

for i, (y_pred, name, color, r2) in enumerate(predictions):
    # 预测 vs 真实
    ax = fig.add_subplot(gs[0, i])
    ax.scatter(y_test, y_pred, alpha=0.65, color=color, s=50,
               edgecolors='white', lw=0.4)
    ax.plot(lims, lims, 'r--', lw=1.8)
    ax.set_xlim(lims); ax.set_ylim(lims)
    ax.set_xlabel('真实值', fontsize=10)
    ax.set_ylabel('预测值', fontsize=10)
    ax.set_title(f'{name}\nR² = {r2:.4f}', fontsize=11)
    ax.grid(True, alpha=0.3)

    # 残差图
    ax = fig.add_subplot(gs[1, i])
    residuals = y_test.values - y_pred
    ax.scatter(y_pred, residuals, alpha=0.65, color=color, s=50,
               edgecolors='white', lw=0.4)
    ax.axhline(0, color='r', linestyle='--', lw=1.8)
    ax.set_xlabel('预测值', fontsize=10)
    ax.set_ylabel('残差', fontsize=10)
    ax.set_title(f'{name} 残差图', fontsize=11)
    ax.grid(True, alpha=0.3)

fig.suptitle('特征工程效果对比', fontsize=15, fontweight='bold')
plt.savefig('results/12_feature_engineering_plot.png', dpi=150, bbox_inches='tight')
plt.close()

# 对比柱状图
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# R² 对比
ax = axes[0]
methods = results['方法']
r2_vals = results['R2']
colors = ['steelblue', 'darkorange', 'mediumseagreen']
bars = ax.bar(methods, r2_vals, color=colors, alpha=0.8, edgecolor='white')
for bar, val in zip(bars, r2_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'{val:.4f}', ha='center', va='bottom', fontsize=10)
ax.set_ylabel('R²', fontsize=11)
ax.set_title('R² 对比（越大越好）', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([0.7, 0.85])

# 特征数对比
ax = axes[1]
feat_nums = results['特征数']
bars = ax.bar(methods, feat_nums, color=colors, alpha=0.8, edgecolor='white')
for bar, val in zip(bars, feat_nums):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{int(val)}', ha='center', va='bottom', fontsize=10)
ax.set_ylabel('特征数量', fontsize=11)
ax.set_title('特征数量对比', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

plt.suptitle('特征工程指标对比', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('results/12_metrics_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("✓ 图片  → results/12_feature_engineering_plot.png")
print("✓ 对比图 → results/12_metrics_comparison.png")
print("✓ 结果  → results/12_feature_engineering_results.csv")
print("=" * 60)
