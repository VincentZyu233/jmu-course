"""
实验三 - 13: 集成学习（随机森林 + XGBoost）
运行：在 lab3/ 目录下  python exp4_extra/13_ensemble.py
注意：需要安装 xgboost: pip install xgboost
"""
import os
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
os.makedirs('results', exist_ok=True)

print("=" * 60)
print("集成学习实验")
print("=" * 60)

# ── 1. 加载数据 ──────────────────────────────────────────────
df = pd.read_csv('data/data.csv')
df.columns = df.columns.str.strip()

X = df.drop(columns=['Serial No.', 'Chance of Admit'])
y = df['Chance of Admit']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 归一化（XGBoost建议归一化，随机森林不强制）
scaler = MinMaxScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# ── 2. 随机森林 ──────────────────────────────────────────────
print("\n[1/3] 训练随机森林...")

rf_model = RandomForestRegressor(
    n_estimators=100,      # 100棵树
    max_depth=10,          # 最大深度
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

start_time = time.time()
rf_model.fit(X_train, y_train)  # 随机森林不需要归一化
rf_time = time.time() - start_time

y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"训练时间: {rf_time:.4f} 秒")
print(f"R² = {r2_rf:.6f}, MSE = {mse_rf:.6f}")

# 特征重要性
feature_importance_rf = pd.DataFrame({
    '特征': X.columns,
    '重要性': rf_model.feature_importances_
}).sort_values('重要性', ascending=False)

print("\n随机森林特征重要性（Top 5）:")
print(feature_importance_rf.head(5).to_string(index=False))

# ── 3. XGBoost ───────────────────────────────────────────────
print("\n[2/3] 训练 XGBoost...")

try:
    import xgboost as xgb

    xgb_model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )

    start_time = time.time()
    xgb_model.fit(X_train_s, y_train)  # XGBoost用归一化数据
    xgb_time = time.time() - start_time

    y_pred_xgb = xgb_model.predict(X_test_s)
    mse_xgb = mean_squared_error(y_test, y_pred_xgb)
    r2_xgb = r2_score(y_test, y_pred_xgb)

    print(f"训练时间: {xgb_time:.4f} 秒")
    print(f"R² = {r2_xgb:.6f}, MSE = {mse_xgb:.6f}")

    # 特征重要性
    feature_importance_xgb = pd.DataFrame({
        '特征': X.columns,
        '重要性': xgb_model.feature_importances_
    }).sort_values('重要性', ascending=False)

    print("\nXGBoost 特征重要性（Top 5）:")
    print(feature_importance_xgb.head(5).to_string(index=False))

    xgb_available = True

except ImportError:
    print("⚠ XGBoost 未安装，跳过此部分")
    print("  安装命令: pip install xgboost")
    xgb_available = False
    y_pred_xgb = None
    mse_xgb = None
    r2_xgb = None
    xgb_time = None

# ── 4. 对比基线模型 ──────────────────────────────────────────
print("\n[3/3] 对比基线模型...")

# 读取之前的单模型结果
baseline_results = {
    '线性回归': 0.806,
    'SVM': 0.772,
    '决策树': 0.804
}

print("\n性能对比:")
print(f"  线性回归: R² = {baseline_results['线性回归']:.6f}")
print(f"  SVM:      R² = {baseline_results['SVM']:.6f}")
print(f"  决策树:   R² = {baseline_results['决策树']:.6f}")
print(f"  随机森林: R² = {r2_rf:.6f}")
if xgb_available:
    print(f"  XGBoost:  R² = {r2_xgb:.6f}")

# ── 5. 保存结果 ──────────────────────────────────────────────
if xgb_available:
    results = pd.DataFrame({
        '模型': ['随机森林', 'XGBoost'],
        'MSE': [mse_rf, mse_xgb],
        'R2': [r2_rf, r2_xgb],
        '训练时间(秒)': [rf_time, xgb_time]
    })
else:
    results = pd.DataFrame({
        '模型': ['随机森林'],
        'MSE': [mse_rf],
        'R2': [r2_rf],
        '训练时间(秒)': [rf_time]
    })

results.to_csv('results/13_ensemble_results.csv', index=False, encoding='utf-8-sig')

feature_importance_rf.to_csv('results/13_rf_feature_importance.csv', index=False, encoding='utf-8-sig')
if xgb_available:
    feature_importance_xgb.to_csv('results/13_xgb_feature_importance.csv', index=False, encoding='utf-8-sig')

# ── 6. 可视化 ────────────────────────────────────────────────
if xgb_available:
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
else:
    fig = plt.figure(figsize=(15, 5))
    gs = fig.add_gridspec(1, 3, hspace=0.35, wspace=0.3)

lims = [0.28, 1.02]

# 随机森林
ax = fig.add_subplot(gs[0, 0])
ax.scatter(y_test, y_pred_rf, alpha=0.65, color='forestgreen', s=50,
           edgecolors='white', lw=0.4)
ax.plot(lims, lims, 'r--', lw=1.8)
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('真实值', fontsize=10)
ax.set_ylabel('预测值', fontsize=10)
ax.set_title(f'随机森林\nR² = {r2_rf:.4f}', fontsize=11)
ax.grid(True, alpha=0.3)

ax = fig.add_subplot(gs[0, 1])
residuals_rf = y_test.values - y_pred_rf
ax.scatter(y_pred_rf, residuals_rf, alpha=0.65, color='forestgreen', s=50,
           edgecolors='white', lw=0.4)
ax.axhline(0, color='r', linestyle='--', lw=1.8)
ax.set_xlabel('预测值', fontsize=10)
ax.set_ylabel('残差', fontsize=10)
ax.set_title('随机森林 残差图', fontsize=11)
ax.grid(True, alpha=0.3)

ax = fig.add_subplot(gs[0, 2])
colors_rf = plt.cm.viridis(np.linspace(0.3, 0.9, len(feature_importance_rf)))
ax.barh(feature_importance_rf['特征'], feature_importance_rf['重要性'],
        color=colors_rf, alpha=0.8, edgecolor='white')
ax.set_xlabel('重要性', fontsize=10)
ax.set_title('随机森林 特征重要性', fontsize=11)
ax.grid(True, alpha=0.3, axis='x')

if xgb_available:
    # XGBoost
    ax = fig.add_subplot(gs[1, 0])
    ax.scatter(y_test, y_pred_xgb, alpha=0.65, color='darkorange', s=50,
               edgecolors='white', lw=0.4)
    ax.plot(lims, lims, 'r--', lw=1.8)
    ax.set_xlim(lims); ax.set_ylim(lims)
    ax.set_xlabel('真实值', fontsize=10)
    ax.set_ylabel('预测值', fontsize=10)
    ax.set_title(f'XGBoost\nR² = {r2_xgb:.4f}', fontsize=11)
    ax.grid(True, alpha=0.3)

    ax = fig.add_subplot(gs[1, 1])
    residuals_xgb = y_test.values - y_pred_xgb
    ax.scatter(y_pred_xgb, residuals_xgb, alpha=0.65, color='darkorange', s=50,
               edgecolors='white', lw=0.4)
    ax.axhline(0, color='r', linestyle='--', lw=1.8)
    ax.set_xlabel('预测值', fontsize=10)
    ax.set_ylabel('残差', fontsize=10)
    ax.set_title('XGBoost 残差图', fontsize=11)
    ax.grid(True, alpha=0.3)

    ax = fig.add_subplot(gs[1, 2])
    colors_xgb = plt.cm.plasma(np.linspace(0.3, 0.9, len(feature_importance_xgb)))
    ax.barh(feature_importance_xgb['特征'], feature_importance_xgb['重要性'],
            color=colors_xgb, alpha=0.8, edgecolor='white')
    ax.set_xlabel('重要性', fontsize=10)
    ax.set_title('XGBoost 特征重要性', fontsize=11)
    ax.grid(True, alpha=0.3, axis='x')

fig.suptitle('集成学习模型结果', fontsize=15, fontweight='bold')
plt.savefig('results/13_ensemble_plot.png', dpi=150, bbox_inches='tight')
plt.close()

# 模型对比柱状图
fig, ax = plt.subplots(figsize=(10, 6))

if xgb_available:
    models = ['线性回归', 'SVM', '决策树', '随机森林', 'XGBoost']
    r2_scores = [baseline_results['线性回归'], baseline_results['SVM'],
                 baseline_results['决策树'], r2_rf, r2_xgb]
    colors = ['steelblue', 'mediumseagreen', 'mediumpurple', 'forestgreen', 'darkorange']
else:
    models = ['线性回归', 'SVM', '决策树', '随机森林']
    r2_scores = [baseline_results['线性回归'], baseline_results['SVM'],
                 baseline_results['决策树'], r2_rf]
    colors = ['steelblue', 'mediumseagreen', 'mediumpurple', 'forestgreen']

bars = ax.bar(models, r2_scores, color=colors, alpha=0.8, edgecolor='white')
for bar, val in zip(bars, r2_scores):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'{val:.4f}', ha='center', va='bottom', fontsize=10)

ax.set_ylabel('R²', fontsize=12)
ax.set_title('所有模型性能对比', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([0.7, 0.85])

plt.tight_layout()
plt.savefig('results/13_all_models_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("✓ 图片  → results/13_ensemble_plot.png")
print("✓ 对比图 → results/13_all_models_comparison.png")
print("✓ 结果  → results/13_ensemble_results.csv")
print("=" * 60)
