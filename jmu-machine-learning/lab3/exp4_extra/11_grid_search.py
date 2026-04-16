"""
实验三 - 11: 超参数调优（GridSearchCV）
运行：在 lab3/ 目录下  python exp4_extra/11_grid_search.py
注意：这个脚本会花较长时间（5-10分钟），因为要尝试多种参数组合
"""
import os
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
os.makedirs('results', exist_ok=True)

print("=" * 60)
print("超参数调优实验")
print("=" * 60)

# ── 1. 加载数据 ──────────────────────────────────────────────
df = pd.read_csv('data/data.csv')
df.columns = df.columns.str.strip()

X = df.drop(columns=['Serial No.', 'Chance of Admit'])
y = df['Chance of Admit']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 归一化（SVM需要）
scaler = MinMaxScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── 2. SVM 网格搜索 ───────────────────────────────────────────
print("\n[1/2] SVM 超参数调优中...")
print("尝试的参数组合：")

# 定义参数网格（较小范围，避免太慢）
param_grid_svm = {
    'C': [10, 50, 100, 200],
    'gamma': [0.01, 0.05, 0.1, 0.5],
    'epsilon': [0.01, 0.05, 0.1, 0.2]
}

print(f"  C: {param_grid_svm['C']}")
print(f"  gamma: {param_grid_svm['gamma']}")
print(f"  epsilon: {param_grid_svm['epsilon']}")
print(f"  总共: {len(param_grid_svm['C']) * len(param_grid_svm['gamma']) * len(param_grid_svm['epsilon'])} 种组合")

# GridSearchCV（3折交叉验证）
grid_svm = GridSearchCV(
    SVR(kernel='rbf'),
    param_grid_svm,
    cv=3,
    scoring='r2',
    n_jobs=-1,  # 使用所有CPU核心
    verbose=1
)

start_time = time.time()
grid_svm.fit(X_train_s, y_train)
svm_time = time.time() - start_time

# 最佳参数
best_svm = grid_svm.best_estimator_
best_params_svm = grid_svm.best_params_
best_score_svm = grid_svm.best_score_

print(f"\n✓ SVM 调优完成（耗时 {svm_time:.1f} 秒）")
print(f"最佳参数: {best_params_svm}")
print(f"最佳交叉验证 R²: {best_score_svm:.6f}")

# 测试集评估
y_pred_svm = best_svm.predict(X_test_s)
mse_svm = mean_squared_error(y_test, y_pred_svm)
r2_svm = r2_score(y_test, y_pred_svm)

print(f"测试集 R²: {r2_svm:.6f}")

# ── 3. 决策树 网格搜索 ────────────────────────────────────────
print("\n[2/2] 决策树 超参数调优中...")
print("尝试的参数组合：")

param_grid_dt = {
    'max_depth': [3, 5, 7, 10, None],
    'min_samples_split': [2, 5, 10, 20],
    'min_samples_leaf': [1, 2, 5, 10]
}

print(f"  max_depth: {param_grid_dt['max_depth']}")
print(f"  min_samples_split: {param_grid_dt['min_samples_split']}")
print(f"  min_samples_leaf: {param_grid_dt['min_samples_leaf']}")
print(f"  总共: {len(param_grid_dt['max_depth']) * len(param_grid_dt['min_samples_split']) * len(param_grid_dt['min_samples_leaf'])} 种组合")

grid_dt = GridSearchCV(
    DecisionTreeRegressor(random_state=42),
    param_grid_dt,
    cv=3,
    scoring='r2',
    n_jobs=-1,
    verbose=1
)

start_time = time.time()
grid_dt.fit(X_train, y_train)  # 决策树不需要归一化
dt_time = time.time() - start_time

best_dt = grid_dt.best_estimator_
best_params_dt = grid_dt.best_params_
best_score_dt = grid_dt.best_score_

print(f"\n✓ 决策树 调优完成（耗时 {dt_time:.1f} 秒）")
print(f"最佳参数: {best_params_dt}")
print(f"最佳交叉验证 R²: {best_score_dt:.6f}")

y_pred_dt = best_dt.predict(X_test)
mse_dt = mean_squared_error(y_test, y_pred_dt)
r2_dt = r2_score(y_test, y_pred_dt)

print(f"测试集 R²: {r2_dt:.6f}")

# ── 4. 保存结果 ──────────────────────────────────────────────
results = pd.DataFrame({
    '模型': ['SVM (调优后)', '决策树 (调优后)'],
    'MSE': [mse_svm, mse_dt],
    'R2': [r2_svm, r2_dt],
    '调优时间(秒)': [svm_time, dt_time]
})

results.to_csv('results/11_grid_search_results.csv', index=False, encoding='utf-8-sig')

# 保存最佳参数
with open('results/11_best_params.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 60 + "\n")
    f.write("超参数调优结果\n")
    f.write("=" * 60 + "\n\n")

    f.write("SVM 最佳参数:\n")
    for k, v in best_params_svm.items():
        f.write(f"  {k}: {v}\n")
    f.write(f"  交叉验证 R²: {best_score_svm:.6f}\n")
    f.write(f"  测试集 R²: {r2_svm:.6f}\n\n")

    f.write("决策树 最佳参数:\n")
    for k, v in best_params_dt.items():
        f.write(f"  {k}: {v}\n")
    f.write(f"  交叉验证 R²: {best_score_dt:.6f}\n")
    f.write(f"  测试集 R²: {r2_dt:.6f}\n")

# ── 5. 可视化：参数影响分析 ────────────────────────────────────
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# SVM: C 参数影响
ax = fig.add_subplot(gs[0, 0])
cv_results_svm = pd.DataFrame(grid_svm.cv_results_)
for gamma in param_grid_svm['gamma']:
    mask = cv_results_svm['param_gamma'] == gamma
    subset = cv_results_svm[mask]
    ax.plot(subset['param_C'], subset['mean_test_score'],
            marker='o', label=f'gamma={gamma}')
ax.set_xlabel('C 参数', fontsize=11)
ax.set_ylabel('交叉验证 R²', fontsize=11)
ax.set_title('SVM: C 参数对性能的影响', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# SVM: gamma 参数影响
ax = fig.add_subplot(gs[0, 1])
for c in param_grid_svm['C']:
    mask = cv_results_svm['param_C'] == c
    subset = cv_results_svm[mask]
    ax.plot(subset['param_gamma'], subset['mean_test_score'],
            marker='o', label=f'C={c}')
ax.set_xlabel('gamma 参数', fontsize=11)
ax.set_ylabel('交叉验证 R²', fontsize=11)
ax.set_title('SVM: gamma 参数对性能的影响', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# 决策树: max_depth 影响
ax = fig.add_subplot(gs[1, 0])
cv_results_dt = pd.DataFrame(grid_dt.cv_results_)
for split in [2, 10, 20]:
    mask = cv_results_dt['param_min_samples_split'] == split
    subset = cv_results_dt[mask].groupby('param_max_depth')['mean_test_score'].mean()
    ax.plot(subset.index.astype(str), subset.values,
            marker='o', label=f'min_samples_split={split}')
ax.set_xlabel('max_depth', fontsize=11)
ax.set_ylabel('交叉验证 R²', fontsize=11)
ax.set_title('决策树: max_depth 对性能的影响', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# 对比：调优前后
ax = fig.add_subplot(gs[1, 1])
# 读取之前的结果
old_svm_r2 = 0.771848  # 从 exp3/08_svm 的结果
old_dt_r2 = 0.803797   # 从 exp3/09_dt 的结果

models = ['SVM', '决策树']
old_scores = [old_svm_r2, old_dt_r2]
new_scores = [r2_svm, r2_dt]

x = np.arange(len(models))
width = 0.35

bars1 = ax.bar(x - width/2, old_scores, width, label='调优前',
               color='lightcoral', alpha=0.8)
bars2 = ax.bar(x + width/2, new_scores, width, label='调优后',
               color='mediumseagreen', alpha=0.8)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.005,
                f'{height:.4f}', ha='center', va='bottom', fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylabel('测试集 R²', fontsize=11)
ax.set_title('超参数调优效果对比', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([0.7, 0.85])

fig.suptitle('超参数调优分析', fontsize=15, fontweight='bold')
plt.savefig('results/11_grid_search_plot.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("✓ 图片  → results/11_grid_search_plot.png")
print("✓ 结果  → results/11_grid_search_results.csv")
print("✓ 参数  → results/11_best_params.txt")
print("=" * 60)
