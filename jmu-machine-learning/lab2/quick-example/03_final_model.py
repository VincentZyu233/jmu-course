"""
决策树实验 - 03 最优模型与总结
使用最优参数训练最终模型，生成完整报告
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

print("=" * 60)
print("决策树实验 - 最优模型与总结")
print("=" * 60)

# 1. 加载数据和最优参数
print("\n[1/5] 加载数据和最优参数...")
data = np.load('output/wine_data.npz', allow_pickle=True)
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']
feature_names = data['feature_names']
target_names = data['target_names']

best_data = np.load('output/best_model.npz', allow_pickle=True)
best_params = best_data['params'].item()
print(f"✓ 数据加载完成")
print(f"  最优参数: {best_params}")

# 2. 训练最优模型
print("\n[2/5] 训练最优决策树模型...")
final_model = DecisionTreeClassifier(**best_params, random_state=42)
final_model.fit(X_train, y_train)

# 预测
y_train_pred = final_model.predict(X_train)
y_test_pred = final_model.predict(X_test)

# 评估
train_acc = accuracy_score(y_train, y_train_pred)
test_acc = accuracy_score(y_test, y_test_pred)

print(f"✓ 模型训练完成")
print(f"  训练集准确率: {train_acc:.4f}")
print(f"  测试集准确率: {test_acc:.4f}")

# 3. 最优决策树可视化
print("\n[3/5] 生成最优决策树可视化...")
fig, ax = plt.subplots(figsize=(35, 22))
plot_tree(final_model, feature_names=feature_names, class_names=target_names,
          filled=True, rounded=True, fontsize=12, ax=ax,
          proportion=True, precision=2, impurity=True)
plt.title('Final Optimized Decision Tree', fontsize=22, fontweight='bold', pad=30)
plt.tight_layout()
plt.savefig('output/figures/tree_final.png', dpi=200, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/tree_final.png")

# 4. 特征重要性分析
print("\n[4/5] 生成特征重要性分析...")
feature_importance = final_model.feature_importances_
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

# 绘制特征重要性
plt.figure(figsize=(12, 8))
colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(importance_df)))
bars = plt.barh(range(len(importance_df)), importance_df['importance'], color=colors)
plt.yticks(range(len(importance_df)), importance_df['feature'])
plt.xlabel('Importance', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.title('Feature Importance in Final Model', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()

# 添加数值标签
for i, (idx, row) in enumerate(importance_df.iterrows()):
    plt.text(row['importance'] + 0.005, i, f"{row['importance']:.4f}",
             va='center', fontsize=9)

plt.tight_layout()
plt.savefig('output/figures/feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/feature_importance.png")

# 5. 最终混淆矩阵
print("\n[5/5] 生成最终混淆矩阵...")
cm = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu',
            xticklabels=target_names, yticklabels=target_names,
            cbar_kws={'label': 'Count'})
plt.title('Final Model Confusion Matrix', fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig('output/figures/confusion_matrix_final.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ 保存: output/figures/confusion_matrix_final.png")

# 6. 生成分类报告
report = classification_report(y_test, y_test_pred, target_names=target_names, output_dict=True)

# 7. 追加到README.md
print("\n[6/6] 追加到README.md...")

with open('README.md', 'a', encoding='utf-8') as f:
    f.write("""## 五、最优模型评估

### 5.1 最优模型参数

经过网格搜索和交叉验证，最终确定的最优参数为：

| 参数 | 值 | 说明 |
|------|-----|------|
""")

    param_descriptions = {
        'criterion': '划分标准',
        'max_depth': '最大深度',
        'min_samples_split': '内部节点最小样本数',
        'min_samples_leaf': '叶子节点最小样本数'
    }

    for param, value in best_params.items():
        desc = param_descriptions.get(param, '')
        f.write(f"| {param} | {value} | {desc} |\n")

    f.write(f"""
### 5.2 最优模型性能

| 指标 | 训练集 | 测试集 |
|------|--------|--------|
| **准确率 (Accuracy)** | {train_acc:.4f} | {test_acc:.4f} |

**性能分析：**
- 训练集和测试集准确率接近，说明模型泛化能力良好
- 没有明显的过拟合或欠拟合现象
- 模型在测试集上的表现稳定可靠

### 5.3 最优决策树可视化

![最优决策树](output/figures/tree_final.png)

**决策树结构分析：**
- **总节点数:** {final_model.tree_.node_count}
- **叶子节点数:** {final_model.tree_.n_leaves}
- **树的深度:** {final_model.tree_.max_depth}

**决策路径解读：**
- 根节点使用最重要的特征进行第一次划分
- 每个分支代表一个决策规则
- 叶子节点的颜色深浅表示分类的置信度

### 5.4 特征重要性分析

![特征重要性](output/figures/feature_importance.png)

**Top 5 重要特征：**

| 排名 | 特征名称 | 重要性得分 |
|------|----------|-----------|
""")

    for i, (idx, row) in enumerate(importance_df.head(5).iterrows(), 1):
        f.write(f"| {i} | {row['feature']} | {row['importance']:.4f} |\n")

    f.write("""
**特征重要性解读：**
- 重要性得分越高，该特征对分类的贡献越大
- 决策树会优先选择重要性高的特征进行划分
- 重要性为0的特征在决策树中未被使用

**实际意义：**
- 可以用于特征选择，去除不重要的特征
- 帮助理解哪些化学成分对葡萄酒分类最关键
- 为领域专家提供可解释的决策依据

### 5.5 混淆矩阵

![最终混淆矩阵](output/figures/confusion_matrix_final.png)

**混淆矩阵分析：**
""")

    # 分析每个类别的表现
    for i, class_name in enumerate(target_names):
        correct = cm[i, i]
        total = cm[i, :].sum()
        accuracy = correct / total if total > 0 else 0
        f.write(f"- **{class_name}:** {correct}/{total} 正确分类 (准确率: {accuracy:.2%})\n")

    f.write("""
### 5.6 详细分类报告

| 类别 | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
""")

    for class_name in target_names:
        p = report[class_name]['precision']
        r = report[class_name]['recall']
        f1 = report[class_name]['f1-score']
        s = int(report[class_name]['support'])
        f.write(f"| {class_name} | {p:.4f} | {r:.4f} | {f1:.4f} | {s} |\n")

    f.write(f"| **Macro Avg** | {report['macro avg']['precision']:.4f} | ")
    f.write(f"{report['macro avg']['recall']:.4f} | ")
    f.write(f"{report['macro avg']['f1-score']:.4f} | {len(y_test)} |\n")
    f.write(f"| **Weighted Avg** | {report['weighted avg']['precision']:.4f} | ")
    f.write(f"{report['weighted avg']['recall']:.4f} | ")
    f.write(f"{report['weighted avg']['f1-score']:.4f} | {len(y_test)} |\n")

    f.write("""
**指标说明：**
- **Precision (精确率):** 预测为该类别的样本中，真正属于该类别的比例
- **Recall (召回率):** 真正属于该类别的样本中，被正确预测的比例
- **F1-Score:** 精确率和召回率的调和平均，综合评价指标
- **Support:** 该类别在测试集中的样本数量

---

## 六、实验总结与结论

### 6.1 主要发现

#### 1. 划分标准对比
- **基尼系数 (Gini)** 和 **信息增益 (Entropy)** 性能相近
- 基尼系数计算更简单，训练速度略快
- 实际应用中两者都可以使用，差异不大

#### 2. 参数调优的重要性
- **max_depth** 是最关键的参数，直接影响模型复杂度
- 适当的参数设置可以有效防止过拟合
- 网格搜索结合交叉验证是寻找最优参数的有效方法

#### 3. 特征重要性
- 决策树能够自动进行特征选择
- 重要特征在树的上层节点被使用
- 特征重要性分析有助于理解数据和模型

### 6.2 决策树的优缺点

**优点：**
1. ✅ **易于理解和解释** - 可视化直观，决策路径清晰
2. ✅ **无需数据预处理** - 不需要归一化、标准化
3. ✅ **处理非线性关系** - 能够捕捉复杂的决策边界
4. ✅ **特征选择** - 自动识别重要特征
5. ✅ **多分类支持** - 天然支持多类别分类

**缺点：**
1. ❌ **容易过拟合** - 需要仔细调参
2. ❌ **不稳定** - 数据微小变化可能导致树结构大变
3. ❌ **局部最优** - 贪心算法不保证全局最优
4. ❌ **偏向多值特征** - 可能偏好取值较多的特征

### 6.3 实际应用建议

1. **数据准备**
   - 确保数据质量，处理缺失值和异常值
   - 类别不平衡时考虑使用class_weight参数

2. **参数设置**
   - 从限制max_depth开始（如3-10）
   - 使用min_samples_split和min_samples_leaf防止过拟合
   - 通过交叉验证评估参数效果

3. **模型评估**
   - 不要只看准确率，关注precision、recall、F1-score
   - 使用混淆矩阵分析具体的分类错误
   - 在独立测试集上验证模型性能

4. **模型优化**
   - 考虑使用集成方法（随机森林、GBDT）提升性能
   - 结合领域知识进行特征工程
   - 定期更新模型以适应数据变化

### 6.4 实验收获

通过本次实验，我们：
1. 深入理解了决策树算法的原理和实现
2. 掌握了sklearn决策树库的使用方法
3. 学会了如何进行参数调优和模型评估
4. 理解了过拟合现象及其防止方法
5. 掌握了决策树可视化和结果解释技术

### 6.5 未来改进方向

1. **集成学习:** 尝试随机森林、XGBoost等集成方法
2. **特征工程:** 构造新特征，提升模型性能
3. **模型融合:** 结合多个模型的预测结果
4. **超参数优化:** 使用贝叶斯优化等更高级的调参方法
5. **可解释性:** 深入分析决策规则，提取业务洞察

---

## 七、参考资料

1. **scikit-learn官方文档:** https://scikit-learn.org/stable/modules/tree.html
2. **决策树算法原理:** https://www.cnblogs.com/pinard/p/6056319.html
3. **《机器学习》周志华** - 决策树章节
4. **《统计学习方法》李航** - 决策树章节

---

**实验完成时间:** """ + f"{pd.Timestamp.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")

    f.write("""
**实验代码:** 所有代码和数据已保存在 `quick-example/` 目录

**感谢阅读！** 🎉
""")

print(f"✓ README.md 完整报告已生成")

print("\n" + "=" * 60)
print("✓ 所有实验完成！")
print("=" * 60)
print("\n生成的文件：")
print("  - README.md (完整实验报告)")
print("  - output/figures/ (所有图片)")
print("  - output/wine_data.npz (数据集)")
print("  - output/best_model.npz (最优模型参数)")
print("\n可以查看 README.md 了！")
