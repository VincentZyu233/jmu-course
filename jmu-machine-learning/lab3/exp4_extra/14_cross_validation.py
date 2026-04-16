"""
实验三 - 14: K-fold 交叉验证 + 学习曲线
运行：在 lab3/ 目录下  python exp4_extra/14_cross_validation.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, learning_curve
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
os.makedirs('results', exist_ok=True)

print("=" * 60)
print("交叉验证与学习曲线实验")
print("=" * 60)

# ── 1. 加载数据 ──────────────────────────────────────────────
df = pd.read_csv('data/data.csv')
df.columns = df.columns.str.strip()

X = df.drop(columns=['Serial No.', 'Chance of Admit'])
y = df['Chance of Admit']

# 归一化（用于需要归一化的模型）
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# ── 2. K-fold 交叉验证（5折）─────────────────────────────────
print("\n[1/2] 5-fold 交叉验证...")

models = {
    '线性回归': LinearRegression(),
    'SVM': SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1),
    '决策树': DecisionTreeRegressor(max_depth=5, min_samples_split=10, random_state=42),
    '随机森林': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
}

# 决定哪些模型需要归一化
needs_scaling = {'线性回归': True, 'SVM': True, '决策树': False, '随机森林': False}

cv_results = []

for name, model in models.items():
    print(f"\n{name}:")

    # 选择数据（归一化或原始）
    X_data = X_scaled if needs_scaling[name] else X

    # 5折交叉验证
    scores = cross_val_score(model, X_data, y, cv=5, scoring='r2', n_jobs=-1)

    mean_score = scores.mean()
    std_score = scores.std()

    print(f"  各折 R²: {[f'{s:.4f}' for s in scores]}")
    print(f"  平均 R²: {mean_score:.4f} ± {std_score:.4f}")

    cv_results.append({
        '模型': name,
        '平均R2': mean_score,
        '标准差': std_score,
        '最小R2': scores.min(),
        '最大R2': scores.max()
    })

cv_df = pd.DataFrame(cv_results)
cv_df = cv_df.sort_values('平均R2', ascending=False)

print("\n交叉验证排名:")
print(cv_df.to_string(index=False))

cv_df.to_csv('results/14_cross_validation_results.csv', index=False, encoding='utf-8-sig')

# ── 3. 学习曲线 ──────────────────────────────────────────────
print("\n[2/2] 生成学习曲线...")

# 选择两个代表性模型
selected_models = {
    'SVM': SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1),
    '随机森林': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
}

learning_curves_data = {}

for name, model in selected_models.items():
    print(f"  {name}...")

    X_data = X_scaled if name == 'SVM' else X

    # 学习曲线：不同训练集大小下的性能
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_data, y,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5,
        scoring='r2',
        n_jobs=-1
    )

    learning_curves_data[name] = {
        'train_sizes': train_sizes,
        'train_mean': train_scores.mean(axis=1),
        'train_std': train_scores.std(axis=1),
        'val_mean': val_scores.mean(axis=1),
        'val_std': val_scores.std(axis=1)
    }

# ── 4. 可视化 ────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# 左上：交叉验证结果（带误差棒）
ax = fig.add_subplot(gs[0, 0])
models_sorted = cv_df['模型'].values
means = cv_df['平均R2'].values
stds = cv_df['标准差'].values
colors = ['steelblue', 'mediumseagreen', 'mediumpurple', 'forestgreen']

bars = ax.barh(models_sorted, means, xerr=stds, color=colors, alpha=0.8,
               edgecolor='white', capsize=5)
for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
    ax.text(mean + std + 0.01, bar.get_y() + bar.get_height()/2,
            f'{mean:.4f}±{std:.4f}', va='center', fontsize=9)

ax.set_xlabel('R² (平均 ± 标准差)', fontsize=11)
ax.set_title('5-fold 交叉验证结果', fontsize=12)
ax.grid(True, alpha=0.3, axis='x')
ax.set_xlim([0.7, 0.85])

# 右上：交叉验证稳定性（箱线图）
ax = fig.add_subplot(gs[0, 1])
box_data = []
for name in models_sorted:
    model = models[name]
    X_data = X_scaled if needs_scaling[name] else X
    scores = cross_val_score(model, X_data, y, cv=5, scoring='r2', n_jobs=-1)
    box_data.append(scores)

bp = ax.boxplot(box_data, labels=models_sorted, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel('R²', fontsize=11)
ax.set_title('模型稳定性（箱线图）', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([0.7, 0.85])

# 下方：学习曲线
for i, (name, data) in enumerate(learning_curves_data.items()):
    ax = fig.add_subplot(gs[1, i])

    train_sizes = data['train_sizes']
    train_mean = data['train_mean']
    train_std = data['train_std']
    val_mean = data['val_mean']
    val_std = data['val_std']

    # 训练集得分
    ax.plot(train_sizes, train_mean, 'o-', color='blue', label='训练集')
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std,
                     alpha=0.2, color='blue')

    # 验证集得分
    ax.plot(train_sizes, val_mean, 'o-', color='red', label='验证集')
    ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std,
                     alpha=0.2, color='red')

    ax.set_xlabel('训练样本数', fontsize=11)
    ax.set_ylabel('R²', fontsize=11)
    ax.set_title(f'{name} 学习曲线', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0.5, 1.0])

fig.suptitle('交叉验证与学习曲线分析', fontsize=15, fontweight='bold')
plt.savefig('results/14_cross_validation_plot.png', dpi=150, bbox_inches='tight')
plt.close()

# ── 5. 额外分析：方差-偏差权衡 ────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

# 计算训练集和测试集的差距（过拟合程度）
overfit_gaps = []
for name in models_sorted:
    model = models[name]
    X_data = X_scaled if needs_scaling[name] else X
    scores = cross_val_score(model, X_data, y, cv=5, scoring='r2', n_jobs=-1)

    # 简化：用交叉验证标准差作为过拟合指标
    overfit_gaps.append(cv_df[cv_df['模型'] == name]['标准差'].values[0])

scatter = ax.scatter(means, overfit_gaps, s=200, c=colors, alpha=0.7, edgecolors='black', linewidth=2)
for i, name in enumerate(models_sorted):
    ax.annotate(name, (means[i], overfit_gaps[i]),
                xytext=(5, 5), textcoords='offset points', fontsize=10)

ax.set_xlabel('平均 R²（性能）', fontsize=12)
ax.set_ylabel('标准差（不稳定性）', fontsize=12)
ax.set_title('模型性能 vs 稳定性', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# 添加理想区域标注
ax.axhline(y=0.02, color='green', linestyle='--', alpha=0.5, label='稳定性阈值')
ax.axvline(x=0.80, color='green', linestyle='--', alpha=0.5, label='性能阈值')
ax.legend(fontsize=10)

plt.tight_layout()
plt.savefig('results/14_performance_stability.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("✓ 图片  → results/14_cross_validation_plot.png")
print("✓ 分析图 → results/14_performance_stability.png")
print("✓ 结果  → results/14_cross_validation_results.csv")
print("=" * 60)

print("\n总结:")
best_model = cv_df.iloc[0]['模型']
best_score = cv_df.iloc[0]['平均R2']
best_std = cv_df.iloc[0]['标准差']
print(f"  最佳模型: {best_model}")
print(f"  平均 R²: {best_score:.4f} ± {best_std:.4f}")
print(f"  稳定性: {'优秀' if best_std < 0.02 else '良好' if best_std < 0.03 else '一般'}")
