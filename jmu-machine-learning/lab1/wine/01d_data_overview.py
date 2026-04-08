"""
01d_data_overview.py - Wine 数据集概览（合并版）

功能：
- 加载 wine 数据集
- 打印标准化参数
- 生成所有可视化图表：
  - 01: 标准化直方图（中位数分色）
  - 01a: 标准化直方图（横轴 -5~5）
  - 01b: 原始数据直方图（横轴反推）
  - 02: 类别分布饼图
  - 03: 特征相关性热力图（对角线=X）
  - 01d: 特征统计表格
  - 01e: 特征中英名称对照表
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

BASE_DIR = r"D:\aaaStuffsaaa\from_git\gitee\jmu-course\jmu-machine-learning\lab1\wine"
IMG_DIR = os.path.join(BASE_DIR, "images")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RESET = "\033[0m"

FEATURE_CN = {
    "alcohol": "酒精度",
    "malic_acid": "苹果酸",
    "ash": "灰分",
    "alcalinity_of_ash": "灰分碱度",
    "magnesium": "镁含量",
    "total_phenols": "总酚",
    "flavanoids": "黄酮类",
    "nonflavanoid_phenols": "非黄酮酚",
    "proanthocyanins": "原花青素",
    "color_intensity": "色彩强度",
    "hue": "色调",
    "od280/od315_of_diluted_wines": "稀释酒OD值",
    "proline": "脯氨酸",
}

print(f"{C_CYAN}加载 wine 数据集...{C_RESET}")
wine = load_wine()
X = wine.data
y = wine.target
feature_names = wine.feature_names
target_names = wine.target_names

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"数据集: {X.shape[0]} 样本, {X.shape[1]} 特征")

# ========== 打印标准化参数 ==========
print(f"\n{C_YELLOW}📐 标准化参数 (StandardScaler):{C_RESET}")
print(f"{'特征名':<40} {'均值 (Mean)':<15} {'标准差 (Std)':<15}")
print("-" * 70)
for i, name in enumerate(feature_names):
    cn = FEATURE_CN.get(name, name)
    print(f"{name} ({cn}): {scaler.mean_[i]:<15.4f} {scaler.scale_[i]:<15.4f}")

# ========== 保存数据 ==========
df_raw = pd.DataFrame(X, columns=feature_names)
df_raw["class"] = y
df_raw["class_name"] = [target_names[i] for i in y]
df_raw.to_csv(os.path.join(DATA_DIR, "wine_raw.csv"), index=False)
print(f"{C_GREEN}💾 已保存: wine_raw.csv{C_RESET}")

df_scaled = pd.DataFrame(X_scaled, columns=feature_names)
df_scaled["class"] = y
df_scaled.to_csv(os.path.join(DATA_DIR, "wine_scaled.csv"), index=False)
print(f"{C_GREEN}💾 已保存: wine_scaled.csv{C_RESET}")

n_features = len(feature_names)
n_cols = 2
n_rows = (n_features + n_cols - 1) // n_cols

# ========== 01: 标准化直方图（中位数分色） ==========
print(f"\n{C_YELLOW}生成 01: 标准化直方图（中位数分色）{C_RESET}")

fig, axes = plt.subplots(4, 4, figsize=(14, 12))
axes = axes.flatten()

for i in range(n_features):
    data = X_scaled[:, i]
    median = np.median(data)
    left_data = data[data < median]
    right_data = data[data >= median]

    axes[i].hist(left_data, bins=20, color="steelblue", edgecolor="white", alpha=0.7)
    axes[i].hist(right_data, bins=20, color="orange", edgecolor="white", alpha=0.7)
    axes[i].axvline(
        x=median,
        color="green",
        linestyle=":",
        linewidth=1.5,
        label=f"Median={median:.2f}",
    )
    axes[i].set_title(feature_names[i], fontsize=9)
    axes[i].set_xlabel("")
    axes[i].legend(fontsize=6)

for j in range(n_features, 16):
    fig.delaxes(axes[j])

plt.suptitle(
    "Wine Dataset - Feature Distribution (Standardized, Median Split)",
    fontsize=14,
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "01_feature_distribution.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}✅ 已保存: 01_feature_distribution.png{C_RESET}")

# ========== 01a: 标准化直方图（横轴 -5~5） ==========
print(f"\n{C_YELLOW}生成 01a: 标准化直方图（横轴 -5~5）{C_RESET}")

fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows))
axes = axes.flatten()

for i in range(n_features):
    ax = axes[i]
    data = X_scaled[:, i]
    cn = FEATURE_CN.get(feature_names[i], feature_names[i])
    median = np.median(data)

    left_data = data[data < median]
    right_data = data[data >= median]

    ax.hist(left_data, bins=20, color="steelblue", edgecolor="white", alpha=0.7)
    ax.hist(right_data, bins=20, color="orange", edgecolor="white", alpha=0.7)
    ax.axvline(x=0, color="red", linestyle="--", linewidth=1, label="Mean=0")
    ax.axvline(
        x=median,
        color="green",
        linestyle=":",
        linewidth=1,
        label=f"Median={median:.2f}",
    )
    ax.set_xlim(-5, 5)
    ax.set_title(f"{feature_names[i]} ({cn})\nMean=0, Std=1", fontsize=10)
    ax.set_xlabel("Standardized Value")
    ax.set_ylabel("Count")
    ax.legend(fontsize=6)

for j in range(n_features, len(axes)):
    fig.delaxes(axes[j])

plt.suptitle(
    "Wine Dataset - Feature Distribution (Standardized, X-axis: -5 to 5)",
    fontsize=14,
    y=1.01,
)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "01a_feature_std.png"), dpi=150, bbox_inches="tight")
print(f"{C_GREEN}✅ 已保存: 01a_feature_std.png{C_RESET}")

# ========== 01b: 原始数据直方图（横轴反推） ==========
print(f"\n{C_YELLOW}生成 01b: 原始数据直方图（横轴反推）{C_RESET}")

fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows))
axes = axes.flatten()

for i in range(n_features):
    ax = axes[i]
    data_raw = X[:, i]
    mean = scaler.mean_[i]
    std = scaler.scale_[i]
    var = std**2
    cn = FEATURE_CN.get(feature_names[i], feature_names[i])
    median_raw = np.median(data_raw)

    left_data = data_raw[data_raw < median_raw]
    right_data = data_raw[data_raw >= median_raw]

    x_min = mean + (-5) * std
    x_max = mean + 5 * std

    ax.hist(left_data, bins=20, color="steelblue", edgecolor="white", alpha=0.7)
    ax.hist(right_data, bins=20, color="orange", edgecolor="white", alpha=0.7)
    ax.axvline(
        x=mean, color="red", linestyle="--", linewidth=1, label=f"Mean={mean:.2f}"
    )
    ax.axvline(
        x=median_raw,
        color="green",
        linestyle=":",
        linewidth=1,
        label=f"Median={median_raw:.2f}",
    )
    ax.set_xlim(x_min, x_max)
    ax.set_title(
        f"{feature_names[i]} ({cn})\nMean={mean:.2f}, Var={var:.2f}", fontsize=10
    )
    ax.set_xlabel("Original Value")
    ax.set_ylabel("Count")
    ax.legend(fontsize=6)

for j in range(n_features, len(axes)):
    fig.delaxes(axes[j])

plt.suptitle(
    "Wine Dataset - Feature Distribution (Original, X-axis scaled)", fontsize=14, y=1.01
)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "01b_feature_raw.png"), dpi=150, bbox_inches="tight")
print(f"{C_GREEN}✅ 已保存: 01b_feature_raw.png{C_RESET}")

# ========== 02: 类别分布饼图 ==========
print(f"\n{C_YELLOW}生成 02: 类别分布饼图{C_RESET}")

unique, counts = np.unique(y, return_counts=True)

fig, ax = plt.subplots(figsize=(8, 6))
colors = ["#ff9999", "#66b3ff", "#99ff99"]
wedges, texts, autotexts = ax.pie(
    counts,
    labels=target_names,
    autopct="%1.1f%%",
    colors=colors,
    explode=(0.02, 0.02, 0.02),
    shadow=True,
    startangle=90,
)
ax.set_title("Wine Dataset - Class Distribution", fontsize=14)
plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "02_class_distribution.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}✅ 已保存: 02_class_distribution.png{C_RESET}")

# ========== 03: 特征相关性热力图（对角线=X） ==========
print(f"\n{C_YELLOW}生成 03: 特征相关性热力图（对角线=X）{C_RESET}")

df_corr = pd.DataFrame(X_scaled, columns=feature_names).corr()
for i in range(len(feature_names)):
    df_corr.iloc[i, i] = np.nan
mask = df_corr.isna()

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(
    df_corr,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    square=True,
    linewidths=0.5,
    ax=ax,
    annot_kws={"size": 8},
    mask=mask,
)
for i in range(len(feature_names)):
    ax.text(
        i + 0.5,
        i + 0.5,
        "×",
        ha="center",
        va="center",
        fontsize=12,
        color="white",
        fontweight="bold",
    )

ax.set_title("Wine Dataset - Feature Correlation Heatmap (Diagonal = X)", fontsize=14)
plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "03_correlation_heatmap.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}✅ 已保存: 03_correlation_heatmap.png{C_RESET}")

# ========== 01d: 特征统计表格 ==========
print(f"\n{C_YELLOW}生成 01d: 特征统计表格{C_RESET}")

stats_list = []
for i, name in enumerate(feature_names):
    data = X[:, i]
    cn = FEATURE_CN.get(name, name)
    stats_dict = {
        "Feature": f"{name}\n({cn})",
        "Mean\n均值": f"{np.mean(data):.2f}",
        "Std\n标准差": f"{np.std(data):.2f}",
        "Median\n中位数": f"{np.median(data):.2f}",
        "Min\n最小值": f"{np.min(data):.2f}",
        "Max\n最大值": f"{np.max(data):.2f}",
        "Q1 (25%)\n第一四分位": f"{np.percentile(data, 25):.2f}",
        "Q3 (75%)\n第三四分位": f"{np.percentile(data, 75):.2f}",
        "IQR\n四分位距": f"{np.percentile(data, 75) - np.percentile(data, 25):.2f}",
        "Range\n极差": f"{np.max(data) - np.min(data):.2f}",
    }
    stats_list.append(stats_dict)

df_stats = pd.DataFrame(stats_list)

fig, ax = plt.subplots(figsize=(16, 10))
ax.axis("off")
table = ax.table(
    cellText=df_stats.values,
    colLabels=df_stats.columns,
    cellLoc="center",
    loc="center",
    colWidths=[0.2] + [0.08] * 9,
)
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.8)

for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight="bold", color="white")
        cell.set_facecolor("#4472C4")
    else:
        cell.set_facecolor("#D9E2F3" if row % 2 == 0 else "white")

plt.title(
    "Wine Dataset - Feature Statistics (10 Metrics)",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "01d_feature_stats.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}✅ 已保存: 01d_feature_stats.png{C_RESET}")

# ========== 01e: 特征中英名称对照表 ==========
print(f"\n{C_YELLOW}生成 01e: 特征中英名称对照表{C_RESET}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")
cn_names = [FEATURE_CN.get(name, name) for name in feature_names]
table_data = [[name, cn] for name, cn in zip(feature_names, cn_names)]

table = ax.table(
    cellText=table_data,
    colLabels=["English Name\n英文名", "Chinese Name\n中文名"],
    cellLoc="center",
    loc="center",
    colWidths=[0.5, 0.5],
)
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 2)

for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight="bold", color="white")
        cell.set_facecolor("#4472C4")
    else:
        cell.set_facecolor("#D9E2F3" if row % 2 == 0 else "white")

plt.title(
    "Wine Dataset - Feature Name Reference", fontsize=14, fontweight="bold", pad=20
)
plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "01e_feature_names.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}✅ 已保存: 01e_feature_names.png{C_RESET}")

# ========== 完成 ==========
print(f"\n{C_CYAN}🎉 01d 执行完成! 生成的图片:{C_RESET}")
print(f"  • 01_feature_distribution.png   - 标准化直方图（中位数分色）")
print(f"  • 01a_feature_std.png          - 标准化直方图（横轴 -5~5）")
print(f"  • 01b_feature_raw.png          - 原始数据直方图（横轴反推）")
print(f"  • 02_class_distribution.png    - 类别分布饼图")
print(f"  • 03_correlation_heatmap.png   - 相关性热力图（对角线=X）")
print(f"  • 01d_feature_stats.png         - 特征统计表格")
print(f"  • 01e_feature_names.png         - 特征中英名称对照表")
