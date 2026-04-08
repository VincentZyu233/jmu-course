> 确实想花时间研究一下捏，但是快deadline了捏，先搞个简单的实现捏...

# 决策树实验实现规划

## 作业要求总结

1. 使用SKLearn库跑决策树模型
2. 可以跑多个数据集
3. 对比同一数据集跑不同决策树（信息增益、增益率、基尼指数）、不同参数的差别
4. 实现决策树的可视化
5. 参考链接：https://www.cnblogs.com/pinard/p/6056319.html

## 实现方案

采用模块化设计，分4个脚本完成，每个脚本直接向最终markdown报告追加内容。

### 脚本规划

#### 00_prepare_data.py - 数据准备
**功能：**
- 加载sklearn自带的Wine（葡萄酒）数据集
  - 3类，13特征，178样本
  - 特征较多，适合展示决策树的特征选择能力
- 数据探索性分析（EDA）
- 数据集划分（训练集/测试集）
- 生成报告的第一部分

**输出：**
- 追加到 `实验报告_决策树.md` - 数据集概览部分
- `output/figures/data_*.png` - 数据可视化图片

---

#### 01_compare_criteria.py - 对比不同划分标准
**功能：**
- 在Wine数据集上对比两种划分标准：
  - `criterion='gini'` - 基尼系数（CART）
  - `criterion='entropy'` - 信息增益（ID3/C4.5风格）
- 对比内容：
  - 决策树结构差异（可视化）
  - 准确率、精确率、召回率对比
  - 训练时间对比
  - 混淆矩阵对比
- 生成报告的第二部分

**输出：**
- 追加到 `实验报告_决策树.md` - 划分标准对比部分
- `output/figures/tree_gini.png` - 基尼系数决策树
- `output/figures/tree_entropy.png` - 信息增益决策树
- `output/figures/criteria_comparison.png` - 性能对比图
- `output/figures/confusion_matrix_*.png` - 混淆矩阵

---

#### 02_parameter_tuning.py - 参数调优对比
**功能：**
- 对比不同参数设置的影响：
  - `max_depth`: [3, 5, 8, 10, None] - 最大深度
  - `min_samples_split`: [2, 5, 10, 20] - 内部节点最小样本数
  - `min_samples_leaf`: [1, 2, 5, 10] - 叶子节点最小样本数
- 绘制参数-性能曲线（训练集 vs 测试集）
- 分析过拟合/欠拟合现象
- 使用网格搜索找最优参数组合
- 生成报告的第三部分

**输出：**
- 追加到 `实验报告_决策树.md` - 参数调优部分
- `output/figures/param_depth.png` - 深度影响图
- `output/figures/param_samples_split.png` - 样本分裂数影响图
- `output/figures/param_samples_leaf.png` - 叶子样本数影响图
- `output/figures/overfitting_analysis.png` - 过拟合分析图

---

#### 03_final_model.py - 最优模型与总结
**功能：**
- 使用最优参数训练最终模型
- 详细的模型评估（分类报告、特征重要性）
- 决策树完整可视化
- 实验总结与结论
- 生成报告的第四部分

**输出：**
- 追加到 `实验报告_决策树.md` - 最优模型与总结部分
- `output/figures/tree_final.png` - 最优决策树
- `output/figures/feature_importance.png` - 特征重要性图
- 完成最终报告

---

## 技术栈

- **Python 3.13**
- **核心库：**
  - `scikit-learn` - 决策树算法
  - `pandas` - 数据处理
  - `numpy` - 数值计算
  - `matplotlib` - 绘图
  - `seaborn` - 高级可视化
  - `graphviz` - 决策树可视化
  - `pydotplus` - graphviz接口

## 数据集选择

### Wine（葡萄酒）数据集
- **特点：** 3类，13特征，178样本
- **优势：**
  - 特征较多（13个），可以很好地展示决策树的特征选择能力
  - 数据量适中，训练速度快
  - 相比iris更有挑战性，不那么"烂大街"
- **用途：** 所有实验的唯一数据集

## 实验亮点

1. **完整性：** 覆盖数据准备、模型训练、参数调优、最优模型评估
2. **可视化：** 决策树可视化、混淆矩阵、参数影响曲线、特征重要性
3. **对比性：** 不同划分标准（gini vs entropy）、不同参数的系统对比
4. **自动化：** 脚本自动追加内容到markdown报告，一键生成完整报告
5. **实用性：** 使用Wine数据集，相比iris更有实际意义

## 运行方式

### 方式1：逐个运行
```bash
python 00_prepare_data.py
python 01_compare_criteria.py
python 02_parameter_tuning.py
python 03_final_model.py
```

### 方式2：一键运行（推荐）
```bash
python run_all.py
```

## 预期输出结构

```
lab2/
├── 00_prepare_data.py
├── 01_compare_criteria.py
├── 02_parameter_tuning.py
├── 03_final_model.py
├── run_all.py                    # 一键运行脚本
├── output/
│   └── figures/
│       ├── data_distribution.png
│       ├── data_correlation.png
│       ├── tree_gini.png
│       ├── tree_entropy.png
│       ├── criteria_comparison.png
│       ├── confusion_matrix_gini.png
│       ├── confusion_matrix_entropy.png
│       ├── param_depth.png
│       ├── param_samples_split.png
│       ├── param_samples_leaf.png
│       ├── overfitting_analysis.png
│       ├── tree_final.png
│       └── feature_importance.png
└── 实验报告_决策树.md              # 唯一的最终报告
```

## 注意事项

1. **环境准备：** 确保安装graphviz并配置环境变量
2. **中文支持：** matplotlib需要配置中文字体
3. **随机种子：** 设置随机种子保证结果可复现
4. **图片质量：** 保存高分辨率图片（dpi=300）
5. **代码注释：** 添加详细注释便于理解

## 下一步

确认规划后，开始编写脚本。

