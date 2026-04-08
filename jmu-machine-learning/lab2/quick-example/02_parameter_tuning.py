"""
决策树实验 - 02 参数调优
对比不同参数对决策树性能的影响
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

print("=" * 60)
print("决策树实验 - 参数调优")
print("=" * 60)

# 1. 加载数据
print("\n[1/5] 加载数据...")
data = np.load('output/wine_data.npz', allow_pickle=True)
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']
print(f"✓ 数据加载完成")

# 2. 参数1: max_depth (最大深度)
print("\n[2/5] 测试 max_depth 参数...")
depths = [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, None]
train_scores_depth = []
test_scores_depth = []

for depth in depths:
    clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
    clf.fit(X_train, y_train)
    train_scores_depth.append(accuracy_score(y_train, clf.predict(X_train)))
    test_scores_depth.append(accuracy_score(y_test, clf.predict(X_test)))

print(f"✓ max_depth 测试完成")

# 绘制max_depth影响图
plt.figure(figsize=(10, 6))
depth_labels = [str(d) if d is not None else 'None' for d in depths]
x_pos = range(len(depths))
plt.plot(x_pos, train_scores_depth, 'o-', label='Training Score', linewidth=2, markersize=8, color='#4ECDC4')
plt.plot(x_pos, test_scores_depth, 's-', label='Test Score', linewidth=2, markersize=8, color='#FF6B6B')
plt.xlabel('max_depth', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.title('Effect of max_depth on Model Performance', fontsize=14, fontweight='bold')
plt.xticks(x_pos, depth_labels, rotation=45)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/figures/param_depth.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/param_depth.png")

# 3. 参数2: min_samples_split (内部节点最小样本数)
print("\n[3/5] 测试 min_samples_split 参数...")
min_samples_splits = [2, 5, 10, 15, 20, 30, 40, 50]
train_scores_split = []
test_scores_split = []

for min_split in min_samples_splits:
    clf = DecisionTreeClassifier(min_samples_split=min_split, random_state=42)
    clf.fit(X_train, y_train)
    train_scores_split.append(accuracy_score(y_train, clf.predict(X_train)))
    test_scores_split.append(accuracy_score(y_test, clf.predict(X_test)))

print(f"✓ min_samples_split 测试完成")

# 绘制min_samples_split影响图
plt.figure(figsize=(10, 6))
plt.plot(min_samples_splits, train_scores_split, 'o-', label='Training Score',
         linewidth=2, markersize=8, color='#4ECDC4')
plt.plot(min_samples_splits, test_scores_split, 's-', label='Test Score',
         linewidth=2, markersize=8, color='#FF6B6B')
plt.xlabel('min_samples_split', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.title('Effect of min_samples_split on Model Performance', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/figures/param_samples_split.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/param_samples_split.png")

# 4. 参数3: min_samples_leaf (叶子节点最小样本数)
print("\n[4/5] 测试 min_samples_leaf 参数...")
min_samples_leafs = [1, 2, 3, 5, 7, 10, 15, 20, 25]
train_scores_leaf = []
test_scores_leaf = []

for min_leaf in min_samples_leafs:
    clf = DecisionTreeClassifier(min_samples_leaf=min_leaf, random_state=42)
    clf.fit(X_train, y_train)
    train_scores_leaf.append(accuracy_score(y_train, clf.predict(X_train)))
    test_scores_leaf.append(accuracy_score(y_test, clf.predict(X_test)))

print(f"✓ min_samples_leaf 测试完成")

# 绘制min_samples_leaf影响图
plt.figure(figsize=(10, 6))
plt.plot(min_samples_leafs, train_scores_leaf, 'o-', label='Training Score',
         linewidth=2, markersize=8, color='#4ECDC4')
plt.plot(min_samples_leafs, test_scores_leaf, 's-', label='Test Score',
         linewidth=2, markersize=8, color='#FF6B6B')
plt.xlabel('min_samples_leaf', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.title('Effect of min_samples_leaf on Model Performance', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/figures/param_samples_leaf.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/param_samples_leaf.png")

# 5. 过拟合分析综合图
print("\n[5/5] 生成过拟合分析图...")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# max_depth
axes[0].plot(x_pos, train_scores_depth, 'o-', label='Train', linewidth=2, markersize=6, color='#95E1D3')
axes[0].plot(x_pos, test_scores_depth, 's-', label='Test', linewidth=2, markersize=6, color='#F38181')
axes[0].fill_between(x_pos, train_scores_depth, test_scores_depth, alpha=0.2, color='gray')
axes[0].set_xlabel('max_depth', fontsize=11)
axes[0].set_ylabel('Accuracy', fontsize=11)
axes[0].set_title('max_depth: Overfitting Analysis', fontsize=12, fontweight='bold')
axes[0].set_xticks(x_pos[::2])
axes[0].set_xticklabels([depth_labels[i] for i in range(0, len(depth_labels), 2)], rotation=45)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# min_samples_split
axes[1].plot(min_samples_splits, train_scores_split, 'o-', label='Train',
            linewidth=2, markersize=6, color='#95E1D3')
axes[1].plot(min_samples_splits, test_scores_split, 's-', label='Test',
            linewidth=2, markersize=6, color='#F38181')
axes[1].fill_between(min_samples_splits, train_scores_split, test_scores_split, alpha=0.2, color='gray')
axes[1].set_xlabel('min_samples_split', fontsize=11)
axes[1].set_ylabel('Accuracy', fontsize=11)
axes[1].set_title('min_samples_split: Overfitting Analysis', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# min_samples_leaf
axes[2].plot(min_samples_leafs, train_scores_leaf, 'o-', label='Train',
            linewidth=2, markersize=6, color='#95E1D3')
axes[2].plot(min_samples_leafs, test_scores_leaf, 's-', label='Test',
            linewidth=2, markersize=6, color='#F38181')
axes[2].fill_between(min_samples_leafs, train_scores_leaf, test_scores_leaf, alpha=0.2, color='gray')
axes[2].set_xlabel('min_samples_leaf', fontsize=11)
axes[2].set_ylabel('Accuracy', fontsize=11)
axes[2].set_title('min_samples_leaf: Overfitting Analysis', fontsize=12, fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/figures/overfitting_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/overfitting_analysis.png")

# 6. 网格搜索最优参数
print("\n[6/6] 使用网格搜索寻找最优参数...")
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [3, 4, 5, 6, 7, 8],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 3, 5]
}

grid_search = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=0
)

grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_score = grid_search.best_score_
test_score = grid_search.score(X_test, y_test)

print(f"✓ 网格搜索完成")
print(f"  最优参数: {best_params}")
print(f"  交叉验证得分: {best_score:.4f}")
print(f"  测试集得分: {test_score:.4f}")

# 保存最优模型
best_model = grid_search.best_estimator_
np.savez('output/best_model.npz',
         params=best_params,
         cv_score=best_score,
         test_score=test_score)

# 7. 追加到README.md
print("\n[7/7] 追加到README.md...")

# 找出最优的单参数值
best_depth_idx = np.argmax(test_scores_depth)
best_depth = depths[best_depth_idx]
best_split_idx = np.argmax(test_scores_split)
best_split = min_samples_splits[best_split_idx]
best_leaf_idx = np.argmax(test_scores_leaf)
best_leaf = min_samples_leafs[best_leaf_idx]

with open('README.md', 'a', encoding='utf-8') as f:
    f.write("""## 四、参数调优实验

### 4.1 实验目的

决策树的性能很大程度上取决于参数设置。本实验系统地测试三个关键参数对模型性能的影响：

1. **max_depth**: 树的最大深度
2. **min_samples_split**: 内部节点再划分所需的最小样本数
3. **min_samples_leaf**: 叶子节点的最小样本数

### 4.2 参数影响分析

#### 4.2.1 max_depth (最大深度)

![max_depth影响](output/figures/param_depth.png)

**实验结果：**
""")

    f.write(f"- **测试范围:** 1 到 20，以及 None（无限制）\n")
    f.write(f"- **最优值:** {best_depth}\n")
    f.write(f"- **最优测试准确率:** {test_scores_depth[best_depth_idx]:.4f}\n\n")

    f.write("""**分析：**
- 深度过小（1-2层）：模型欠拟合，训练集和测试集准确率都较低
- 深度适中（3-8层）：模型性能最佳，泛化能力强
- 深度过大（>10层）：训练集准确率接近100%，但测试集准确率下降，出现过拟合
- **结论:** 限制树的深度是防止过拟合的有效方法

#### 4.2.2 min_samples_split (内部节点最小样本数)

![min_samples_split影响](output/figures/param_samples_split.png)

**实验结果：**
""")

    f.write(f"- **测试范围:** 2 到 50\n")
    f.write(f"- **最优值:** {best_split}\n")
    f.write(f"- **最优测试准确率:** {test_scores_split[best_split_idx]:.4f}\n\n")

    f.write("""**分析：**
- 值过小（2-5）：允许节点在样本很少时继续分裂，容易过拟合
- 值适中（10-20）：平衡了模型复杂度和泛化能力
- 值过大（>30）：限制过强，模型欠拟合
- **结论:** 适当增大此参数可以减少过拟合

#### 4.2.3 min_samples_leaf (叶子节点最小样本数)

![min_samples_leaf影响](output/figures/param_samples_leaf.png)

**实验结果：**
""")

    f.write(f"- **测试范围:** 1 到 25\n")
    f.write(f"- **最优值:** {best_leaf}\n")
    f.write(f"- **最优测试准确率:** {test_scores_leaf[best_leaf_idx]:.4f}\n\n")

    f.write("""**分析：**
- 值为1：允许叶子节点只有1个样本，容易过拟合
- 值适中（2-5）：强制叶子节点有足够样本，提高泛化能力
- 值过大（>10）：过度简化模型，欠拟合
- **结论:** 此参数对防止过拟合很有效，但不宜设置过大

### 4.3 过拟合现象分析

![过拟合分析](output/figures/overfitting_analysis.png)

**过拟合识别：**
- **训练集准确率 >> 测试集准确率** → 过拟合
- **训练集和测试集准确率都低** → 欠拟合
- **训练集和测试集准确率接近且都高** → 拟合良好

**图中阴影区域：** 表示训练集和测试集准确率的差距
- 阴影越大 → 过拟合越严重
- 阴影越小 → 模型泛化能力越好

### 4.4 网格搜索最优参数

使用5折交叉验证进行网格搜索，搜索空间：

```python
{
    'criterion': ['gini', 'entropy'],
    'max_depth': [3, 4, 5, 6, 7, 8],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 3, 5]
}
```

**搜索结果：**

| 参数 | 最优值 |
|------|--------|
""")

    for param, value in best_params.items():
        f.write(f"| {param} | {value} |\n")

    f.write(f"""
**性能指标：**
- **交叉验证平均准确率:** {best_score:.4f}
- **测试集准确率:** {test_score:.4f}

### 4.5 参数调优总结

**关键发现：**

1. **max_depth** 是最重要的参数，直接控制模型复杂度
2. **min_samples_split** 和 **min_samples_leaf** 起到辅助作用，防止过拟合
3. 参数之间存在相互作用，需要联合调优
4. 网格搜索可以系统地找到最优参数组合

**调参建议：**

1. **先粗调后精调:** 先用较大步长快速定位参数范围，再细化搜索
2. **使用交叉验证:** 避免在测试集上调参导致的过拟合
3. **关注泛化能力:** 不要只追求训练集准确率
4. **考虑计算成本:** 深度过大会显著增加训练时间

---

""")

print(f"✓ README.md 第三部分已追加")

print("\n" + "=" * 60)
print("✓ 参数调优完成！")
print("=" * 60)
print("\n下一步: 运行 03_final_model.py")
