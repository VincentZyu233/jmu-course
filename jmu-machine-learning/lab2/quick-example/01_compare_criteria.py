"""
决策树实验 - 01 对比不同划分标准
对比基尼系数(gini)和信息增益(entropy)两种划分标准
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import time
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

print("=" * 60)
print("决策树实验 - 对比不同划分标准")
print("=" * 60)

# 1. 加载数据
print("\n[1/6] 加载数据...")
data = np.load('output/wine_data.npz', allow_pickle=True)
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']
feature_names = data['feature_names']
target_names = data['target_names']
print(f"✓ 数据加载完成")

# 2. 训练两种决策树
print("\n[2/6] 训练决策树模型...")

# 基尼系数决策树
print("  训练基尼系数(Gini)决策树...")
start_time = time.time()
clf_gini = DecisionTreeClassifier(criterion='gini', random_state=42, max_depth=5)
clf_gini.fit(X_train, y_train)
time_gini = time.time() - start_time
y_pred_gini = clf_gini.predict(X_test)
acc_gini = accuracy_score(y_test, y_pred_gini)
print(f"  ✓ Gini决策树训练完成 - 准确率: {acc_gini:.4f}, 耗时: {time_gini:.4f}秒")

# 信息增益决策树
print("  训练信息增益(Entropy)决策树...")
start_time = time.time()
clf_entropy = DecisionTreeClassifier(criterion='entropy', random_state=42, max_depth=5)
clf_entropy.fit(X_train, y_train)
time_entropy = time.time() - start_time
y_pred_entropy = clf_entropy.predict(X_test)
acc_entropy = accuracy_score(y_test, y_pred_entropy)
print(f"  ✓ Entropy决策树训练完成 - 准确率: {acc_entropy:.4f}, 耗时: {time_entropy:.4f}秒")

# 3. 决策树可视化
print("\n[3/6] 生成决策树可视化...")

# Gini决策树
fig, ax = plt.subplots(figsize=(20, 12))
plot_tree(clf_gini, feature_names=feature_names, class_names=target_names,
          filled=True, rounded=True, fontsize=10, ax=ax)
plt.title('Decision Tree (Gini Index)', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('output/figures/tree_gini.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/tree_gini.png")

# Entropy决策树
fig, ax = plt.subplots(figsize=(20, 12))
plot_tree(clf_entropy, feature_names=feature_names, class_names=target_names,
          filled=True, rounded=True, fontsize=10, ax=ax)
plt.title('Decision Tree (Information Gain / Entropy)', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('output/figures/tree_entropy.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/tree_entropy.png")

# 4. 混淆矩阵
print("\n[4/6] 生成混淆矩阵...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gini混淆矩阵
cm_gini = confusion_matrix(y_test, y_pred_gini)
sns.heatmap(cm_gini, annot=True, fmt='d', cmap='Blues',
            xticklabels=target_names, yticklabels=target_names, ax=axes[0])
axes[0].set_title('Confusion Matrix (Gini)', fontsize=13, fontweight='bold')
axes[0].set_ylabel('True Label', fontsize=11)
axes[0].set_xlabel('Predicted Label', fontsize=11)

# Entropy混淆矩阵
cm_entropy = confusion_matrix(y_test, y_pred_entropy)
sns.heatmap(cm_entropy, annot=True, fmt='d', cmap='Greens',
            xticklabels=target_names, yticklabels=target_names, ax=axes[1])
axes[1].set_title('Confusion Matrix (Entropy)', fontsize=13, fontweight='bold')
axes[1].set_ylabel('True Label', fontsize=11)
axes[1].set_xlabel('Predicted Label', fontsize=11)

plt.tight_layout()
plt.savefig('output/figures/confusion_matrices.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/confusion_matrices.png")

# 5. 性能对比图
print("\n[5/6] 生成性能对比图...")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 准确率对比
metrics = ['Gini', 'Entropy']
accuracies = [acc_gini, acc_entropy]
colors = ['#FF6B6B', '#4ECDC4']
axes[0].bar(metrics, accuracies, color=colors, alpha=0.8)
axes[0].set_ylabel('Accuracy', fontsize=11)
axes[0].set_title('Accuracy Comparison', fontsize=12, fontweight='bold')
axes[0].set_ylim([0.8, 1.0])
for i, v in enumerate(accuracies):
    axes[0].text(i, v + 0.01, f'{v:.4f}', ha='center', va='bottom', fontweight='bold')

# 训练时间对比
times = [time_gini * 1000, time_entropy * 1000]  # 转换为毫秒
axes[1].bar(metrics, times, color=colors, alpha=0.8)
axes[1].set_ylabel('Training Time (ms)', fontsize=11)
axes[1].set_title('Training Time Comparison', fontsize=12, fontweight='bold')
for i, v in enumerate(times):
    axes[1].text(i, v + 0.1, f'{v:.2f}ms', ha='center', va='bottom', fontweight='bold')

# 树的复杂度对比
n_nodes = [clf_gini.tree_.node_count, clf_entropy.tree_.node_count]
n_leaves = [clf_gini.tree_.n_leaves, clf_entropy.tree_.n_leaves]
x = np.arange(len(metrics))
width = 0.35
axes[2].bar(x - width/2, n_nodes, width, label='Total Nodes', color='#95E1D3')
axes[2].bar(x + width/2, n_leaves, width, label='Leaf Nodes', color='#F38181')
axes[2].set_ylabel('Count', fontsize=11)
axes[2].set_title('Tree Complexity', fontsize=12, fontweight='bold')
axes[2].set_xticks(x)
axes[2].set_xticklabels(metrics)
axes[2].legend()
for i in range(len(metrics)):
    axes[2].text(i - width/2, n_nodes[i] + 0.5, str(n_nodes[i]), ha='center', va='bottom', fontsize=9)
    axes[2].text(i + width/2, n_leaves[i] + 0.5, str(n_leaves[i]), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('output/figures/criteria_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/criteria_comparison.png")

# 6. 追加到README.md
print("\n[6/6] 追加到README.md...")

# 获取分类报告
report_gini = classification_report(y_test, y_pred_gini, target_names=target_names, output_dict=True)
report_entropy = classification_report(y_test, y_pred_entropy, target_names=target_names, output_dict=True)

with open('README.md', 'a', encoding='utf-8') as f:
    f.write("""## 三、不同划分标准对比

### 3.1 实验设计

本实验对比两种常用的决策树划分标准：

1. **基尼系数 (Gini Index)** - CART算法使用
   - 衡量数据集的不纯度
   - 计算公式: $Gini(D) = 1 - \\sum_{k=1}^{K} p_k^2$
   - 值越小表示纯度越高

2. **信息增益 (Information Gain / Entropy)** - ID3/C4.5算法使用
   - 基于信息熵的概念
   - 计算公式: $Entropy(D) = -\\sum_{k=1}^{K} p_k \\log_2(p_k)$
   - 信息增益 = 划分前熵 - 划分后熵

**实验参数：**
- 最大深度: 5层（避免过拟合，便于可视化）
- 随机种子: 42（保证可复现性）

### 3.2 决策树可视化

#### 3.2.1 基尼系数决策树

![Gini决策树](output/figures/tree_gini.png)

#### 3.2.2 信息增益决策树

![Entropy决策树](output/figures/tree_entropy.png)

**可视化说明：**
- 每个节点显示：划分条件、基尼系数/熵值、样本数、类别分布
- 颜色深浅表示类别纯度（颜色越深，纯度越高）
- 叶子节点表示最终分类结果

### 3.3 性能对比

![性能对比](output/figures/criteria_comparison.png)

**对比结果：**

| 指标 | Gini (基尼系数) | Entropy (信息增益) |
|------|----------------|-------------------|
""")

    f.write(f"| **测试集准确率** | {acc_gini:.4f} | {acc_entropy:.4f} |\n")
    f.write(f"| **训练时间** | {time_gini*1000:.2f} ms | {time_entropy*1000:.2f} ms |\n")
    f.write(f"| **树节点总数** | {clf_gini.tree_.node_count} | {clf_entropy.tree_.node_count} |\n")
    f.write(f"| **叶子节点数** | {clf_gini.tree_.n_leaves} | {clf_entropy.tree_.n_leaves} |\n")
    f.write(f"| **树的深度** | {clf_gini.tree_.max_depth} | {clf_entropy.tree_.max_depth} |\n")

    f.write("""
### 3.4 混淆矩阵分析

![混淆矩阵](output/figures/confusion_matrices.png)

**混淆矩阵解读：**
- 对角线元素：正确分类的样本数
- 非对角线元素：错误分类的样本数
- 两种方法的分类错误模式基本相似

### 3.5 详细分类报告

#### 3.5.1 基尼系数 (Gini) 分类报告

| 类别 | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
""")

    for class_name in target_names:
        p = report_gini[class_name]['precision']
        r = report_gini[class_name]['recall']
        f1 = report_gini[class_name]['f1-score']
        s = int(report_gini[class_name]['support'])
        f.write(f"| {class_name} | {p:.4f} | {r:.4f} | {f1:.4f} | {s} |\n")

    f.write(f"| **Macro Avg** | {report_gini['macro avg']['precision']:.4f} | ")
    f.write(f"{report_gini['macro avg']['recall']:.4f} | ")
    f.write(f"{report_gini['macro avg']['f1-score']:.4f} | {len(y_test)} |\n")

    f.write("""
#### 3.5.2 信息增益 (Entropy) 分类报告

| 类别 | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
""")

    for class_name in target_names:
        p = report_entropy[class_name]['precision']
        r = report_entropy[class_name]['recall']
        f1 = report_entropy[class_name]['f1-score']
        s = int(report_entropy[class_name]['support'])
        f.write(f"| {class_name} | {p:.4f} | {r:.4f} | {f1:.4f} | {s} |\n")

    f.write(f"| **Macro Avg** | {report_entropy['macro avg']['precision']:.4f} | ")
    f.write(f"{report_entropy['macro avg']['recall']:.4f} | ")
    f.write(f"{report_entropy['macro avg']['f1-score']:.4f} | {len(y_test)} |\n")

    f.write("""
### 3.6 结论

**主要发现：**

1. **准确率差异：** 两种划分标准的准确率非常接近，差异很小
2. **训练速度：** 基尼系数计算相对简单，训练速度略快
3. **树结构：** 两种方法生成的树结构可能不同，但复杂度相近
4. **实际应用：**
   - 基尼系数：计算简单，sklearn默认使用，适合大多数场景
   - 信息增益：理论基础更强，适合需要解释性的场景

**建议：** 在实际应用中，两种方法都可以尝试，通过交叉验证选择更优的方法。

---

""")

print(f"✓ README.md 第二部分已追加")

print("\n" + "=" * 60)
print("✓ 划分标准对比完成！")
print("=" * 60)
print("\n下一步: 运行 02_parameter_tuning.py")
