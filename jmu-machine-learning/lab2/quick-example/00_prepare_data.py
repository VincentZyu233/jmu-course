"""
决策树实验 - 00 数据准备
加载Wine数据集，进行探索性分析，生成报告第一部分
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
import os
from datetime import datetime

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# 创建输出目录
os.makedirs('output/figures', exist_ok=True)

# 设置随机种子
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

print("=" * 60)
print("决策树实验 - 数据准备")
print("=" * 60)

# 1. 加载Wine数据集
print("\n[1/5] 加载Wine数据集...")
wine = load_wine()
X = wine.data
y = wine.target
feature_names = wine.feature_names
target_names = wine.target_names

print(f"✓ 数据集加载完成")
print(f"  - 样本数: {X.shape[0]}")
print(f"  - 特征数: {X.shape[1]}")
print(f"  - 类别数: {len(target_names)}")
print(f"  - 类别名称: {target_names}")

# 2. 创建DataFrame便于分析
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y
df['target_name'] = df['target'].map({i: name for i, name in enumerate(target_names)})

# 3. 数据集划分
print("\n[2/5] 划分训练集和测试集...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=RANDOM_STATE, stratify=y
)
print(f"✓ 数据集划分完成")
print(f"  - 训练集: {X_train.shape[0]} 样本")
print(f"  - 测试集: {X_test.shape[0]} 样本")

# 保存数据集供后续脚本使用
np.savez('output/wine_data.npz',
         X_train=X_train, X_test=X_test,
         y_train=y_train, y_test=y_test,
         feature_names=feature_names,
         target_names=target_names)
print(f"✓ 数据集已保存到 output/wine_data.npz")

# 4. 数据分布可视化
print("\n[3/5] 生成数据分布图...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 类别分布
class_counts = pd.Series(y).value_counts().sort_index()
axes[0].bar(range(len(target_names)), class_counts.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
axes[0].set_xlabel('Wine Class', fontsize=11)
axes[0].set_ylabel('Count', fontsize=11)
axes[0].set_title('Class Distribution', fontsize=12, fontweight='bold')
axes[0].set_xticks(range(len(target_names)))
axes[0].set_xticklabels(target_names, rotation=0)
for i, v in enumerate(class_counts.values):
    axes[0].text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')

# 训练集/测试集分布
train_counts = pd.Series(y_train).value_counts().sort_index()
test_counts = pd.Series(y_test).value_counts().sort_index()
x = np.arange(len(target_names))
width = 0.35
axes[1].bar(x - width/2, train_counts.values, width, label='Train', color='#95E1D3')
axes[1].bar(x + width/2, test_counts.values, width, label='Test', color='#F38181')
axes[1].set_xlabel('Wine Class', fontsize=11)
axes[1].set_ylabel('Count', fontsize=11)
axes[1].set_title('Train/Test Split Distribution', fontsize=12, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(target_names, rotation=0)
axes[1].legend()

plt.tight_layout()
plt.savefig('output/figures/data_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ 保存: output/figures/data_distribution.png")

# 5. 特征相关性热图
print("\n[4/5] 生成特征相关性热图...")
plt.figure(figsize=(14, 12))
correlation = df[feature_names].corr()
mask = np.triu(np.ones_like(correlation, dtype=bool))
sns.heatmap(correlation, mask=mask, annot=True, fmt='.2f',
            cmap='coolwarm', center=0, square=True,
            linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('output/figures/data_correlation.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ 保存: output/figures/data_correlation.png")

# 6. 生成README.md第一部分
print("\n[5/5] 生成README.md...")
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(f"""# 决策树算法实验报告

**实验日期:** {datetime.now().strftime('%Y年%m月%d日')}
**数据集:** Wine (葡萄酒分类)

---

## 一、实验目的

1. 掌握决策树算法的基本原理和实现方法
2. 理解不同划分标准（基尼系数、信息增益）的差异
3. 学习决策树参数调优的方法
4. 掌握决策树的可视化技术

---

## 二、数据集介绍

### 2.1 数据集概述

本实验使用sklearn自带的**Wine数据集**，这是一个经典的葡萄酒分类数据集。

**数据集基本信息：**
- **样本总数:** {X.shape[0]} 个
- **特征数量:** {X.shape[1]} 个
- **类别数量:** {len(target_names)} 类
- **类别名称:** {', '.join(target_names)}

**数据集划分：**
- **训练集:** {X_train.shape[0]} 个样本 (70%)
- **测试集:** {X_test.shape[0]} 个样本 (30%)
- **划分策略:** 分层抽样（保持类别比例）

### 2.2 特征说明

数据集包含13个化学特征：

""")

    for i, feature in enumerate(feature_names, 1):
        f.write(f"{i}. **{feature}**\n")

    f.write(f"""
### 2.3 数据分布

![数据分布](output/figures/data_distribution.png)

**类别分布分析：**
""")

    for i, name in enumerate(target_names):
        count = class_counts[i]
        percentage = count / len(y) * 100
        f.write(f"- **{name}:** {count} 个样本 ({percentage:.1f}%)\n")

    f.write(f"""
数据集的类别分布相对均衡，有利于模型训练。

### 2.4 特征相关性分析

![特征相关性](output/figures/data_correlation.png)

**相关性分析：**
- 部分特征之间存在较强的相关性（如flavanoids与total_phenols）
- 决策树算法对特征相关性不敏感，无需特征去相关处理
- 高相关性特征可能在决策树中选择其中之一作为分裂节点

---

""")

print(f"✓ README.md 第一部分已生成")

print("\n" + "=" * 60)
print("✓ 数据准备完成！")
print("=" * 60)
print("\n下一步: 运行 01_compare_criteria.py")
