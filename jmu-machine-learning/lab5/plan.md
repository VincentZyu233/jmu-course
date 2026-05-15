# 实验五 聚类 — 实验规划

## 数据集

- **iris**（sklearn.datasets.load_iris），4 维特征，150 条数据，3 个真实类别

## 目录结构

```
lab5/
├── exp1_kmeans/                   KMeans 不同 K 值对照
│   ├── 01_kmeans_k3.py            K=3（正确类别数，基准）
│   ├── 02_kmeans_k2.py            K=2（少分一类）
│   ├── 03_kmeans_k5.py            K=5（多分两类）
│   └── 04_k_comparison.py         K=2/3/5 对比分析 + 报告
├── exp2_params/                   KMeans 初始化参数对照
│   ├── 05_kmeans_random.py        init='random', n_init=1
│   ├── 06_kmeans_kmeanspp.py      init='k-means++', n_init=1
│   ├── 07_kmeans_n_init10.py      init='k-means++', n_init=10
│   └── 08_param_comparison.py     参数对比分析 + 报告
├── exp3_algorithms/               不同聚类算法对照
│   ├── 09_kmeans.py               KMeans（基准）
│   ├── 10_dbscan.py               DBSCAN（密度聚类）
│   ├── 11_agg.py                  Agglomerative（层次聚类）
│   ├── 12_gmm.py                  GaussianMixture（高斯混合模型）
│   └── 13_algo_comparison.py      四算法全面对比 + 总结报告
└── results/                       （所有输出自动生成至此）
```

## 每个实验脚本输出

| 项目 | 说明 |
|------|------|
| 原始2特征散点图（前两维） | `*_plot_2feat.png` |
| PCA 降维 2D 散点图 | `*_plot_pca.png` |
| 指标 CSV | `*_metrics.csv`（silhouette / calinski-harabasz / adjusted_rand / n_clusters）|
| 预测 CSV | `*_predictions.csv`（真实标签 + 聚类标签 + PCA 坐标）|
| 控制台打印 | 全部指标 + 简要分析 |

## 评价指标

| 指标 | 说明 |
|------|------|
| Silhouette Score | 聚类紧密度（无需标签），[-1, 1] 越大越好 |
| Calinski-Harabasz Index | 类间/类内方差比，越大越好 |
| Adjusted Rand Index | 与真实标签对比，[0, 1] 越大越好 |
| 聚类数量 | 实际分出几类（DBSCAN 可能有噪声点） |

## 可视化风格

- 不同簇用不同颜色，聚类中心用 `✕` 标记
- DBSCAN 噪声点用灰色标注
- 对比图：2×N 布局 + 指标柱状图
- 中文字体：`Microsoft YaHei` / `SimHei` fallback

## 执行方式

所有脚本在 `lab5/` 根目录下运行：
```
python exp1_kmeans/01_kmeans_k3.py
python exp3_algorithms/13_algo_comparison.py
```
