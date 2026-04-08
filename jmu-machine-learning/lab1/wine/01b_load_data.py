"""
01b_load_data.py - 加载 Wine 数据集并进行预处理（详细注释版）

本脚本用于：
1. 加载 sklearn 内置的 wine 数据集
2. 对数据进行标准化处理
3. 生成三张可视化图表

🤔 为什么需要这个脚本？
   - 机器学习第一步：先"认识"你的数据
   - 了解数据分布、特征之间的关系
"""

import os
import numpy as np  # 数值计算库
import pandas as pd  # 数据处理库
import matplotlib.pyplot as plt  # 绘图库
import seaborn as sns  # 基于 matplotlib 的美化库
from sklearn.datasets import load_wine  # sklearn 内置数据集
from sklearn.preprocessing import StandardScaler  # 标准化工具

# ========== 配置部分 ==========
# 设置中文字体（避免乱码）
plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 📁 定义路径
BASE_DIR = r"D:\aaaStuffsaaa\from_git\gitee\jmu-course\jmu-machine-learning\lab1\wine"
DATA_DIR = os.path.join(BASE_DIR, "data")  # 数据保存目录
IMG_DIR = os.path.join(BASE_DIR, "images")  # 图片保存目录

# 创建目录（如果不存在）
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# 🎨 定义颜色（终端输出用）
C_CYAN = "\033[96m"  # 青色
C_GREEN = "\033[92m"  # 绿色
C_YELLOW = "\033[93m"  # 黄色
C_PURPLE = "\033[95m"  # 紫色
C_RESET = "\033[0m"  # 重置


def print_section(title):
    """打印带分隔线的标题"""
    print(f"\n{C_CYAN}{'=' * 50}{C_RESET}")
    print(f"{C_CYAN}{title}{C_RESET}")
    print(f"{C_CYAN}{'=' * 50}{C_RESET}")


# ========== 主程序开始 ==========
print_section("🍷 Wine 数据集加载与预处理")

# ============================================================
# 📥 第一步：加载数据
# ============================================================
# 🤔 什么是 load_wine()？
#    sklearn 内置的数据集，不需要联网下载，数据已经打包在库里
#    返回一个类似字典的对象，包含：
#    - data: 特征矩阵 (178, 13)
#    - target: 标签向量 (178,)
#    - feature_names: 特征名称
#    - target_names: 类别名称

print(f"\n{C_YELLOW}📥 正在加载 sklearn 内置 wine 数据集...{C_RESET}")

wine = load_wine()  # 加载数据
X = wine.data  # 特征矩阵 (178行样本, 13列特征)
y = wine.target  # 标签向量 (每个样本的类别 0/1/2)
feature_names = wine.feature_names  # 13个特征名
target_names = wine.target_names  # 3个类别名

print(f"{C_GREEN}✅ 数据加载完成！{C_RESET}")
print(f"\n📊 数据集基本信息:")
print(f"  • 样本数（行数）: {X.shape[0]}")
print(f"  • 特征数（列数）: {X.shape[1]}")
print(f"  • 特征名: {feature_names}")
print(f"  • 类别名: {list(target_names)}")

# ============================================================
# 📊 第二步：查看标签分布
# ============================================================
print_section("📊 标签（类别）分布")

# np.unique() 找出所有不同的值，return_counts=True 统计每个值的数量
unique, counts = np.unique(y, return_counts=True)

print(f"🍷 三个类别的样本数量:")
for u, c in zip(unique, counts):
    print(f"  • {target_names[u]}: {c} 样本 ({c / len(y) * 100:.1f}%)")

# 💾 保存原始数据到 CSV 文件
# DataFrame = 表格，类似于 Excel
df_raw = pd.DataFrame(X, columns=feature_names)
df_raw["class"] = y
df_raw["class_name"] = [target_names[i] for i in y]
raw_path = os.path.join(DATA_DIR, "wine_raw.csv")
df_raw.to_csv(raw_path, index=False)
print(f"\n{C_GREEN}💾 原始数据已保存到: {raw_path}{C_RESET}")

# ============================================================
# ⚙️ 第三步：数据标准化
# ============================================================
# 🤔 为什么要标准化？
#    不同特征的数值范围差异很大！
#    例如：proline 可能是几百，hue 可能是 1 左右
#    如果不标准化，有些模型（如 SVM、KNN）会被大数值特征主导
#
# 🤔 StandardScaler 做了什么？
#    公式：z = (x - mean) / std
#    转换后：每个特征的均值=0，标准差=1
#    相当于把不同特征拉到同一个"量级"进行比较

print_section("⚙️ 数据标准化 (StandardScaler)")

scaler = StandardScaler()  # 创建标准化器
X_scaled = scaler.fit_transform(X)  # 对数据进行拟合+转换

# 打印标准化参数（可选，了解即可）
print(f"📐 标准化参数（每个特征的均值和标准差）:")
print(f"  • 均值 (mean): {scaler.mean_[:3]}... (只显示前3个)")
print(f"  • 标准差 (std): {scaler.scale_[:3]}... (只显示前3个)")

# 💾 保存标准化后的数据
df_scaled = pd.DataFrame(X_scaled, columns=feature_names)
df_scaled["class"] = y
scaled_path = os.path.join(DATA_DIR, "wine_scaled.csv")
df_scaled.to_csv(scaled_path, index=False)
print(f"\n{C_GREEN}💾 标准化数据已保存到: {scaled_path}{C_RESET}")

# ============================================================
# 🎨 第四步：生成可视化图表
# ============================================================
print_section("🎨 生成可视化图表")

# -------------------------------------------------
# 📈 图1: 特征分布直方图（中位数分左右颜色）
# 🤔 这个图展示什么？
#    每个特征的数值分布情况
#    柱子越高 = 该值出现的次数越多
#    中位数左侧=蓝色，右侧=橙色
# -------------------------------------------------
fig, axes = plt.subplots(4, 4, figsize=(14, 12))  # 4x4=16个子图（13个特征+3个空白）
axes = axes.flatten()

for i in range(len(feature_names)):
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
    axes[i].set_xlabel("")  # X轴标签
    axes[i].legend(fontsize=6)

# 删除多余的空白子图
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

# -------------------------------------------------
# 🥧 图2: 类别分布饼图
# 🤔 这个图展示什么？
#    三个类别（品种）的占比
#    饼越大 = 该类别样本越多
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
colors = ["#ff9999", "#66b3ff", "#99ff99"]  # 红、蓝、绿
wedges, texts, autotexts = ax.pie(
    counts,
    labels=target_names,
    autopct="%1.1f%%",  # 显示百分比
    colors=colors,
    explode=(0.02, 0.02, 0.02),  # 稍微分离三个扇形
    shadow=True,
    startangle=90,
)
ax.set_title("Wine Dataset - Class Distribution", fontsize=14)
plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "02_class_distribution.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}📈 已保存: 02_class_distribution.png{C_RESET}")

# -------------------------------------------------
# 🔥 图3: 特征相关性热力图（带数值显示，对角线为X）
# 🤔 这个图展示什么？
#    每两个特征之间的相关程度
#    - 红色 = 正相关 (一个变大，另一个也变大)
#    - 蓝色 = 负相关 (一个变大，另一个变小)
#    - 白色 = 几乎无关
#    数值范围：-1 到 +1
#    |数值|越接近1，相关性越强
#    - 对角线设为白色，显示 X（自己和自己相关性=1，没意义）
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 10))

# 计算相关性矩阵
df_corr = pd.DataFrame(X_scaled, columns=feature_names).corr()

# 将对角线设为 NaN（这样会显示为空白或可自定义）
for i in range(len(feature_names)):
    df_corr.iloc[i, i] = np.nan

# 绘制热力图，mask 忽略 NaN 值
mask = df_corr.isna()
sns.heatmap(
    df_corr,
    annot=True,  # 📊 显示数值
    fmt=".2f",  # 保留2位小数
    cmap="RdBu_r",  # 红蓝配色
    center=0,  # 0为中心（白色）
    vmin=-1,
    vmax=1,  # 固定范围
    square=True,
    linewidths=0.5,
    ax=ax,
    annot_kws={"size": 8},  # 数值字体大小
    mask=mask,  # 屏蔽对角线
)

# 在对角线位置画 X
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
print(f"{C_GREEN}📈 已保存: 03_correlation_heatmap.png (对角线为X){C_RESET}")

# ========== 完成 ==========
print_section("✅ 01b_load_data.py 执行完成!")
print(f"\n📁 输出目录:")
print(f"  • 数据文件: {DATA_DIR}")
print(f"  • 图片文件: {IMG_DIR}")
print(f"\n💡 下一步：运行 02_split_data.py 学习数据划分！")
