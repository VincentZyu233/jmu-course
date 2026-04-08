"""
01_load_data.py - 加载 Wine 数据集并进行预处理
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
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR = os.path.join(BASE_DIR, "images")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_PURPLE = "\033[95m"
C_RESET = "\033[0m"


def print_section(title):
    print(f"\n{C_CYAN}{'=' * 50}{C_RESET}")
    print(f"{C_CYAN}{title}{C_RESET}")
    print(f"{C_CYAN}{'=' * 50}{C_RESET}")


print_section("🍷 Wine 数据集加载与预处理")

# ========== 1. 加载数据 ==========
print(f"\n{C_YELLOW}📥 正在加载 sklearn 内置 wine 数据集...{C_RESET}")

wine = load_wine()
X = wine.data
y = wine.target
feature_names = wine.feature_names
target_names = wine.target_names

print(f"{C_GREEN}✅ 数据加载完成！{C_RESET}")
print(f"\n数据集信息:")
print(f"  • 样本数: {X.shape[0]}")
print(f"  • 特征数: {X.shape[1]}")
print(f"  • 特征名: {feature_names}")
print(f"  • 类别名: {list(target_names)}")

# ========== 2. 标签分布 ==========
print_section("📊 标签分布")

unique, counts = np.unique(y, return_counts=True)
print(f"类别分布:")
for u, c in zip(unique, counts):
    print(f"  • {target_names[u]}: {c} 样本 ({c / len(y) * 100:.1f}%)")

# ========== 3. 保存原始数据 ==========
df_raw = pd.DataFrame(X, columns=feature_names)
df_raw["class"] = y
df_raw["class_name"] = [target_names[i] for i in y]
df_raw.to_csv(os.path.join(DATA_DIR, "wine_raw.csv"), index=False)
print(f"\n{C_GREEN}💾 原始数据已保存到: {DATA_DIR}/wine_raw.csv{C_RESET}")

# ========== 4. 标准化 ==========
print_section("⚙️ 数据标准化 (StandardScaler)")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"标准化参数:")
print(f"  • 均值 (mean): {scaler.mean_[:3]}... (取前3个)")
print(f"  • 标准差 (std): {scaler.scale_[:3]}... (取前3个)")

# 保存标准化后的数据
df_scaled = pd.DataFrame(X_scaled, columns=feature_names)
df_scaled["class"] = y
df_scaled.to_csv(os.path.join(DATA_DIR, "wine_scaled.csv"), index=False)
print(f"\n{C_GREEN}💾 标准化数据已保存到: {DATA_DIR}/wine_scaled.csv{C_RESET}")

# ========== 5. 可视化 ==========
print_section("🎨 生成可视化图表")

# 图1: 特征分布直方图
fig, axes = plt.subplots(4, 4, figsize=(14, 12))
axes = axes.flatten()
for i in range(len(feature_names)):
    axes[i].hist(
        X_scaled[:, i], bins=20, color="steelblue", edgecolor="white", alpha=0.7
    )
    axes[i].set_title(feature_names[i], fontsize=9)
    axes[i].set_xlabel("")
for j in range(len(feature_names), 16):
    fig.delaxes(axes[j])
plt.suptitle(
    "Wine Dataset - Feature Distribution (After Standardization)", fontsize=14, y=1.02
)
plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "01_feature_distribution.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}📈 已保存: 01_feature_distribution.png{C_RESET}")

# 图2: 标签类别饼图
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
print(f"{C_GREEN}📈 已保存: 02_class_distribution.png{C_RESET}")

# 图3: 特征相关性热力图
fig, ax = plt.subplots(figsize=(12, 10))
df_corr = pd.DataFrame(X_scaled, columns=feature_names).corr()
sns.heatmap(
    df_corr, annot=False, cmap="RdBu_r", center=0, square=True, linewidths=0.5, ax=ax
)
ax.set_title("Wine Dataset - Feature Correlation Heatmap", fontsize=14)
plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "03_correlation_heatmap.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}📈 已保存: 03_correlation_heatmap.png{C_RESET}")

# ========== 完成 ==========
print_section("✅ 01_load_data.py 执行完成!")
print(f"输出目录:")
print(f"  • 数据: {DATA_DIR}")
print(f"  • 图片: {IMG_DIR}")
