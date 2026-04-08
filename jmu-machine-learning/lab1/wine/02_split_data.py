"""
================================================================================
02_split_data.py - Data Splitting Methods Comparison
================================================================================

PURPOSE:
  1. Simple Split (Multiple Times): Use different random seeds for train_test_split
  2. K-Fold Cross-Validation: Use StratifiedKFold to show result stability
  3. Compare the differences between the two methods

OUTPUT CHARTS:
  - 04: Simple Split Accuracy Fluctuation (scatter + line chart)
  - 05: K-Fold CV Stability (boxplot + violin plot)
  - 06: Statistics Comparison Table
  - 07: Split Process Visualization
  - 08: Accuracy Distribution Comparison

KEY CONCEPTS:
  * Simple Split: Randomly split data into "training set" and "test set"
  * K-Fold CV: Split data into K parts, use each part as test set in turn
  * Purpose: Evaluate model performance on unseen data
"""

# ================================================================================
# IMPORT LIBRARIES
# ================================================================================

import os  # File path operations
import numpy as np  # Numerical computation
import pandas as pd  # Data manipulation

import matplotlib.pyplot as plt  # Plotting
import seaborn as sns  # Advanced plotting (optional)

# Machine learning libraries
from sklearn.datasets import load_wine  # Load wine dataset
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# Set plot style
plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


# ================================================================================
# PATH CONFIGURATION
# ================================================================================

BASE_DIR = r"D:\aaaStuffsaaa\from_git\gitee\jmu-course\jmu-machine-learning\lab1\wine"
IMG_DIR = os.path.join(BASE_DIR, "images")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

C_CYAN = ""
C_GREEN = ""
C_YELLOW = ""
C_RESET = ""


# ================================================================================
# STEP 1: LOAD DATA
# ================================================================================

print(f"{C_CYAN}[LOAD] Loading Wine dataset...{C_RESET}")

wine = load_wine()
X = wine.data  # Feature data (178 samples, 13 features)
y = wine.target  # Label data (3 classes)
feature_names = wine.feature_names
target_names = wine.target_names

# Standardize features (mean=0, std=1)
# WHY? Different features have very different value ranges
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"[INFO] Dataset: {X.shape[0]} samples, {X.shape[1]} features")
print(f"[INFO] Classes: {target_names}")
print(f"[INFO] Class counts: {np.bincount(y)}")


# ================================================================================
# STEP 2: DEFINE CLASSIFIERS
# ================================================================================

# Use 4 different classifiers to demonstrate the effect of splitting methods
classifiers = {
    # 1. Logistic Regression - Linear classifier, simple and fast
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    # 2. SVM (RBF kernel) - Support Vector Machine, non-linear classifier
    "SVM (RBF)": SVC(kernel="rbf", random_state=42),
    # 3. K-Nearest Neighbors - Vote based on K nearest neighbors
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    # 4. Random Forest - Ensemble method, multiple decision trees voting
    "Random Forest": RandomForestClassifier(n_estimators=50, random_state=42),
}


# ================================================================================
# STEP 3: SIMPLE SPLIT (MULTIPLE TIMES)
# ================================================================================

# DESCRIPTION: Simple split randomly divides data into training and test sets
# PROBLEM: Different splits may yield very different results, leading to unstable accuracy

print(
    f"\n{C_YELLOW}[RUN] Running Simple Split Experiment (10 random splits)...{C_RESET}"
)

N_SPLITS = 10  # Number of split experiments
TEST_SIZE = 0.2  # Test set ratio: 20% of data as test set

# Storage: {classifier_name: [list of 10 accuracy scores]}
simple_split_results = {name: [] for name in classifiers.keys()}

np.random.seed(42)  # Set base random seed (for reproducibility)
base_seed = 42

for i in range(N_SPLITS):
    # Use different random seeds: 42, 43, 44, ... 51
    seed = base_seed + i

    # Split data using train_test_split
    # Parameters:
    #   - X_scaled, y: features and labels
    #   - test_size=0.2: 20% as test set
    #   - random_state=seed: random seed for reproducibility
    #   - stratify=y: stratified sampling, maintain class proportions
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=TEST_SIZE, random_state=seed, stratify=y
    )

    # Train and evaluate each classifier
    for name, clf in classifiers.items():
        clf_copy = type(clf)(**clf.get_params())  # Clone classifier
        clf_copy.fit(X_train, y_train)  # Train model
        score = clf_copy.score(X_test, y_test)  # Evaluate accuracy
        simple_split_results[name].append(score)  # Record result

print(f"{C_GREEN}[DONE] Simple Split experiment completed!{C_RESET}")


# ================================================================================
# STEP 4: K-FOLD CROSS-VALIDATION
# ================================================================================

# DESCRIPTION: K-Fold CV splits data into K parts, using each part as test set in turn
# ADVANTAGE: All data is used for both training and testing, results are more stable

print(f"\n{C_YELLOW}[RUN] Running K-Fold Cross-Validation Experiment...{C_RESET}")

K = 5  # K folds: split data into 5 parts

# Storage for K-fold CV results
kfold_results = {name: [] for name in classifiers.keys()}

# Create stratified K-fold splitter
# Parameters:
#   - n_splits=5: split into 5 folds
#   - shuffle=True: shuffle data
#   - random_state=42: for reproducibility
skf = StratifiedKFold(n_splits=K, shuffle=True, random_state=42)

# Perform K-fold CV for each classifier
for name, clf in classifiers.items():
    # cross_val_score automatically performs K-fold CV and returns accuracy for each fold
    # Parameters:
    #   - clf: classifier
    #   - X_scaled, y: features and labels
    #   - cv=skf: use our K-fold splitter
    #   - scoring="accuracy": evaluation metric is accuracy
    scores = cross_val_score(clf, X_scaled, y, cv=skf, scoring="accuracy")
    kfold_results[name] = scores.tolist()

print(f"{C_GREEN}[DONE] K-Fold Cross-Validation experiment completed!{C_RESET}")


# ================================================================================
# STEP 5: CALCULATE STATISTICS
# ================================================================================


def calculate_stats(scores_list):
    """
    Calculate statistics for a list of scores

    Returns:
        Dictionary with statistics:
        - mean: average value
        - std: standard deviation (measures data fluctuation)
        - min: minimum value
        - max: maximum value
        - range: max - min
        - median: median value
        - q1: 25th percentile
        - q3: 75th percentile
        - iqr: interquartile range (Q3 - Q1)
    """
    scores = np.array(scores_list)
    return {
        "mean": np.mean(scores),
        "std": np.std(scores),
        "min": np.min(scores),
        "max": np.max(scores),
        "range": np.max(scores) - np.min(scores),
        "median": np.median(scores),
        "q1": np.percentile(scores, 25),
        "q3": np.percentile(scores, 75),
        "iqr": np.percentile(scores, 75) - np.percentile(scores, 25),
    }


# Calculate statistics for both methods
simple_stats = {
    name: calculate_stats(scores) for name, scores in simple_split_results.items()
}
kfold_stats = {name: calculate_stats(scores) for name, scores in kfold_results.items()}


# ================================================================================
# STEP 6: VISUALIZATION
# ================================================================================


# +===========================================================================+
# |  CHART 04: Simple Split Accuracy Fluctuation                             |
# |  Purpose: Show accuracy variation of simple split (10 times)             |
# +===========================================================================+

print(f"\n{C_YELLOW}[PLOT] Generating 04: Simple Split Accuracy Fluctuation{C_RESET}")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]

for idx, (name, scores) in enumerate(simple_split_results.items()):
    ax = axes[idx]

    # X-axis: 1-10 splits
    x = np.arange(1, N_SPLITS + 1)

    # Calculate mean and standard deviation
    mean_score = np.mean(scores)
    std_score = np.std(scores)

    # Draw line chart and scatter plot
    #   'o-': circle scatter + solid line
    ax.plot(
        x, scores, "o-", color=colors[idx], linewidth=2, markersize=8, label="Accuracy"
    )

    # Draw mean line (red dashed)
    ax.axhline(
        y=mean_score,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean = {mean_score:.4f}",
    )

    # Draw mean +/- std region (red semi-transparent fill)
    ax.fill_between(
        x,
        mean_score - std_score,
        mean_score + std_score,
        color="red",
        alpha=0.1,
        label=f"+/-1 Std ({std_score:.4f})",
    )

    # Label each scatter point with accuracy
    for i, score in enumerate(scores):
        ax.annotate(
            f"{score:.3f}",
            (i + 1, score),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=7,
            color=colors[idx],
        )

    # Set axis labels
    ax.set_xlabel("Split Number", fontsize=10)
    ax.set_ylabel("Accuracy", fontsize=10)
    ax.set_title(f"{name}", fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_ylim(min(scores) - 0.05, max(scores) + 0.05)
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle(
    "Simple Train-Test Split (10 times) - Accuracy Fluctuation",
    fontsize=14,
    fontweight="bold",
    y=1.02,
)

plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "04_simple_split_fluctuation.png"),
    dpi=150,
    bbox_inches="tight",
)
print(f"{C_GREEN}[SAVE] 04_simple_split_fluctuation.png{C_RESET}")
plt.close()


# +===========================================================================+
# |  CHART 05: K-Fold CV Stability Chart                                    |
# |  Purpose: Show stability of K-fold CV results                            |
# |  Content: Left=Boxplot, Right=Violin plot                                |
# +===========================================================================+

print(f"\n{C_YELLOW}[PLOT] Generating 05: K-Fold CV Stability Chart{C_RESET}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# ===========================================================================
# Left: Box Plot
# ===========================================================================

ax1 = axes[0]

data_boxplot = [kfold_results[name] for name in classifiers.keys()]

bp = ax1.boxplot(data_boxplot, tick_labels=list(classifiers.keys()), patch_artist=True)

for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Overlay scatter points on boxplot
for i, (name, scores) in enumerate(kfold_results.items()):
    for j, score in enumerate(scores):
        ax1.scatter(
            i + 1 + np.random.uniform(-0.1, 0.1),
            score,
            color=colors[i],
            s=30,
            alpha=0.6,
            zorder=5,
        )

ax1.set_xlabel("Classifier", fontsize=11)
ax1.set_ylabel("Accuracy", fontsize=11)
ax1.set_title("5-Fold Cross-Validation - Box Plot", fontsize=12, fontweight="bold")
ax1.grid(True, alpha=0.3, axis="y")
ax1.set_ylim(0.6, 1.05)

# ===========================================================================
# Right: Violin Plot
# ===========================================================================

ax2 = axes[1]

# Draw violin plot
#   showmeans=True: show mean points
#   showmedians=True: show median lines
parts = ax2.violinplot(
    data_boxplot,
    positions=range(1, len(classifiers) + 1),
    showmeans=True,
    showmedians=True,
)

for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(colors[i])
    pc.set_alpha(0.7)

ax2.set_xlabel("Classifier", fontsize=11)
ax2.set_ylabel("Accuracy", fontsize=11)
ax2.set_title("5-Fold Cross-Validation - Violin Plot", fontsize=12, fontweight="bold")
ax2.grid(True, alpha=0.3, axis="y")
ax2.set_xticks(range(1, len(classifiers) + 1))
ax2.set_xticklabels(list(classifiers.keys()))
ax2.set_ylim(0.6, 1.05)

plt.suptitle(
    "K-Fold Cross-Validation Stability Analysis", fontsize=14, fontweight="bold", y=1.02
)

plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "05_kfold_stability.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}[SAVE] 05_kfold_stability.png{C_RESET}")
plt.close()


# +===========================================================================+
# |  CHART 06: Statistics Comparison Table                                  |
# |  Purpose: Directly compare statistics of both methods                   |
# +===========================================================================+

print(f"\n{C_YELLOW}[PLOT] Generating 06: Statistics Comparison Table{C_RESET}")

table_data = []
for name in classifiers.keys():
    s_stats = simple_stats[name]  # Simple split stats
    k_stats = kfold_stats[name]  # K-fold CV stats
    table_data.append(
        [
            name,
            f"{s_stats['mean']:.4f}",
            f"{s_stats['std']:.4f}",
            f"{s_stats['range']:.4f}",
            f"{k_stats['mean']:.4f}",
            f"{k_stats['std']:.4f}",
            f"{k_stats['range']:.4f}",
            f"{abs(s_stats['std'] - k_stats['std']):.4f}",
        ]
    )

fig, ax = plt.subplots(figsize=(16, 6))
ax.axis("off")

columns = [
    "Classifier",
    "Simple Split\nMean",
    "Simple Split\nStd",
    "Simple Split\nRange",
    "K-Fold\nMean",
    "K-Fold\nStd",
    "K-Fold\nRange",
    "Std Diff",
]

table = ax.table(
    cellText=table_data,
    colLabels=columns,
    cellLoc="center",
    loc="center",
    colWidths=[0.18, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 2)

# Set table style
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight="bold", color="white")
        cell.set_facecolor("#4472C4")
    else:
        cell.set_facecolor("#D9E2F3" if row % 2 == 0 else "white")
        if col in [2, 5]:
            cell.set_facecolor("#FFE699" if row % 2 == 0 else "#FFF2CC")

plt.title(
    "Comparison: Simple Split vs K-Fold Cross-Validation",
    fontsize=14,
    fontweight="bold",
    pad=20,
)

plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "06_split_comparison_table.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}[SAVE] 06_split_comparison_table.png{C_RESET}")
plt.close()


# +===========================================================================+
# |  CHART 07: Split Process Visualization                                   |
# |  Purpose: Visually demonstrate how data is split in both methods        |
# +===========================================================================+

print(f"\n{C_YELLOW}[PLOT] Generating 07: Split Process Visualization{C_RESET}")

fig, axes = plt.subplots(1, 2, figsize=(14, 8))

n_samples = len(y)  # Total samples: 178
n_test = int(n_samples * TEST_SIZE)  # Test set size: 35
n_train = n_samples - n_test  # Training set size: 143
n_per_fold = n_samples // K  # Samples per fold: 35

train_color = "#4472C4"
test_color = "#FF6B6B"
fold_colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]

# ===========================================================================
# Left: Simple Split Visualization
# ===========================================================================

ax1 = axes[0]

np.random.seed(42)
all_indices = np.arange(n_samples)
np.random.shuffle(all_indices)
ax1.barh(0, n_samples, height=0.8, color="lightgray", edgecolor="black", alpha=0.3)

ax1.text(
    n_samples / 2,
    0,
    f"Total Dataset\n{n_samples} samples",
    ha="center",
    va="center",
    fontsize=11,
    fontweight="bold",
)

# Demonstrate 3 splits
for i in range(3):
    y_pos = 2 + i * 1.5
    seed = 42 + i

    np.random.seed(seed)
    indices = np.arange(n_samples)
    np.random.shuffle(indices)

    test_idx = indices[:n_test]
    train_idx = indices[n_test:]

    ax1.barh(
        y_pos,
        len(train_idx),
        left=0,
        height=0.6,
        color=train_color,
        edgecolor="black",
        alpha=0.7,
        label="Training" if i == 0 else "",
    )

    ax1.barh(
        y_pos,
        len(test_idx),
        left=len(train_idx),
        height=0.6,
        color=test_color,
        edgecolor="black",
        alpha=0.7,
        label="Test" if i == 0 else "",
    )

    ax1.text(-5, y_pos, f"Split {i + 1}", ha="right", va="center", fontsize=10)

ax1.set_xlim(-15, n_samples + 5)
ax1.set_ylim(-1, 7)
ax1.set_title("Simple Train-Test Split", fontsize=12, fontweight="bold")
ax1.set_xlabel("Sample Index", fontsize=10)
ax1.set_yticks([])
ax1.legend(loc="upper right")

ax1.axvline(x=n_train, color="black", linestyle="--", linewidth=2, alpha=0.5)
ax1.text(n_train / 2, -0.5, f"Training\n{n_train}", ha="center", va="top", fontsize=9)
ax1.text(
    n_train + n_test / 2, -0.5, f"Test\n{n_test}", ha="center", va="top", fontsize=9
)

# ===========================================================================
# Right: K-Fold CV Visualization
# ===========================================================================

ax2 = axes[1]

skf = StratifiedKFold(n_splits=K, shuffle=True, random_state=42)
all_folds = []
for fold_idx, (train_idx, val_idx) in enumerate(skf.split(X_scaled, y)):
    all_folds.append((train_idx, val_idx))

for fold_idx in range(K):
    y_pos = K - fold_idx - 1

    train_idx, val_idx = all_folds[fold_idx]

    ax2.barh(
        y_pos,
        len(train_idx),
        left=0,
        height=0.6,
        color=train_color,
        edgecolor="black",
        alpha=0.3,
    )

    ax2.barh(
        y_pos,
        len(val_idx),
        left=len(train_idx),
        height=0.6,
        color=fold_colors[fold_idx],
        edgecolor="black",
        alpha=0.9,
        label=f"Fold {fold_idx + 1}" if fold_idx == 0 else "",
    )

    ax2.text(-5, y_pos, f"Fold {fold_idx + 1}", ha="right", va="center", fontsize=10)

ax2.set_xlim(-15, n_samples + 5)
ax2.set_ylim(-1, K)
ax2.set_title("5-Fold Cross-Validation", fontsize=12, fontweight="bold")
ax2.set_xlabel("Sample Index", fontsize=10)
ax2.set_yticks([])
ax2.legend(loc="upper right", title="Validation Set")

ax2.text(
    n_train - 20,
    K + 0.3,
    f"Training: {n_train - n_per_fold} samples\nValidation: {n_per_fold} samples",
    ha="left",
    va="bottom",
    fontsize=9,
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
)

plt.suptitle(
    "Data Splitting Methods Visualization", fontsize=14, fontweight="bold", y=1.02
)

plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "07_split_visualization.png"), dpi=150, bbox_inches="tight"
)
print(f"{C_GREEN}[SAVE] 07_split_visualization.png{C_RESET}")
plt.close()


# +===========================================================================+
# |  CHART 08: Accuracy Distribution Comparison                              |
# |  Purpose: Compare accuracy distributions of both methods                |
# +===========================================================================+

print(f"\n{C_YELLOW}[PLOT] Generating 08: Accuracy Distribution Comparison{C_RESET}")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, name in enumerate(classifiers.keys()):
    ax = axes[idx]

    simple_scores = simple_split_results[name]
    kfold_scores = kfold_results[name]

    bins = np.linspace(0.85, 1.0, 16)

    ax.hist(
        simple_scores,
        bins=bins,
        alpha=0.6,
        label=f"Simple Split (10 times)",
        color="#4472C4",
        edgecolor="white",
    )

    ax.hist(
        kfold_scores,
        bins=bins,
        alpha=0.6,
        label=f"5-Fold CV (5 times)",
        color="#FF6B6B",
        edgecolor="white",
    )

    ax.axvline(
        np.mean(simple_scores),
        color="#4472C4",
        linestyle="--",
        linewidth=2,
        label=f"Simple Mean: {np.mean(simple_scores):.4f}",
    )
    ax.axvline(
        np.mean(kfold_scores),
        color="#FF6B6B",
        linestyle="--",
        linewidth=2,
        label=f"K-Fold Mean: {np.mean(kfold_scores):.4f}",
    )

    ax.set_xlabel("Accuracy", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.set_title(f"{name}", fontsize=12, fontweight="bold")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle(
    "Accuracy Distribution Comparison: Simple Split vs K-Fold CV",
    fontsize=14,
    fontweight="bold",
    y=1.02,
)

plt.tight_layout()
plt.savefig(
    os.path.join(IMG_DIR, "08_accuracy_distribution_comparison.png"),
    dpi=150,
    bbox_inches="tight",
)
print(f"{C_GREEN}[SAVE] 08_accuracy_distribution_comparison.png{C_RESET}")
plt.close()


# ================================================================================
# STEP 7: PRINT STATISTICS RESULTS
# ================================================================================

print(
    f"\n{C_CYAN}==================== STATISTICS SUMMARY ===================={C_RESET}"
)

print(f"\n{C_YELLOW}[STAT] Simple Split (10 random splits) Results:{C_RESET}")
print(
    f"{'Classifier':<25} {'Mean':<10} {'Std':<10} {'Min':<10} {'Max':<10} {'Range':<10}"
)
print("-" * 75)
for name in classifiers.keys():
    s = simple_stats[name]
    print(
        f"{name:<25} {s['mean']:<10.4f} {s['std']:<10.4f} {s['min']:<10.4f} {s['max']:<10.4f} {s['range']:<10.4f}"
    )

print(f"\n{C_YELLOW}[STAT] 5-Fold Cross-Validation Results:{C_RESET}")
print(
    f"{'Classifier':<25} {'Mean':<10} {'Std':<10} {'Min':<10} {'Max':<10} {'Range':<10}"
)
print("-" * 75)
for name in classifiers.keys():
    k = kfold_stats[name]
    print(
        f"{name:<25} {k['mean']:<10.4f} {k['std']:<10.4f} {k['min']:<10.4f} {k['max']:<10.4f} {k['range']:<10.4f}"
    )

print(f"\n{C_YELLOW}[STAT] Method Comparison Summary:{C_RESET}")
for name in classifiers.keys():
    s = simple_stats[name]
    k = kfold_stats[name]
    print(f"\n{name}:")
    print(
        f"  Simple Split - Mean: {s['mean']:.4f}, Std: {s['std']:.4f}, Range: {s['range']:.4f}"
    )
    print(
        f"  K-Fold CV   - Mean: {k['mean']:.4f}, Std: {k['std']:.4f}, Range: {k['range']:.4f}"
    )
    if k["std"] < s["std"]:
        print(
            f"  --> K-Fold CV has smaller std, more stable ({s['std']:.4f} -> {k['std']:.4f})"
        )
    else:
        print(f"  --> Simple Split has smaller std ({s['std']:.4f} < {k['std']:.4f})")


# ================================================================================
# STEP 8: SAVE RESULTS TO CSV
# ================================================================================

results_df = pd.DataFrame(
    {
        "Classifier": list(classifiers.keys()) * 2,
        "Method": ["Simple Split (10 times)"] * 4 + ["5-Fold CV"] * 4,
        "Mean": [simple_stats[n]["mean"] for n in classifiers.keys()]
        + [kfold_stats[n]["mean"] for n in classifiers.keys()],
        "Std": [simple_stats[n]["std"] for n in classifiers.keys()]
        + [kfold_stats[n]["std"] for n in classifiers.keys()],
        "Min": [simple_stats[n]["min"] for n in classifiers.keys()]
        + [kfold_stats[n]["min"] for n in classifiers.keys()],
        "Max": [simple_stats[n]["max"] for n in classifiers.keys()]
        + [kfold_stats[n]["max"] for n in classifiers.keys()],
        "Range": [simple_stats[n]["range"] for n in classifiers.keys()]
        + [kfold_stats[n]["range"] for n in classifiers.keys()],
    }
)

results_df.to_csv(
    os.path.join(DATA_DIR, "02_split_comparison_results.csv"), index=False
)
print(f"\n{C_GREEN}[SAVE] 02_split_comparison_results.csv{C_RESET}")


# ================================================================================
# COMPLETION
# ================================================================================

print(f"\n{C_CYAN}==================== COMPLETED ===================={C_RESET}")
print(f"\nGenerated Images:")
print(f"  04_simple_split_fluctuation.png         - Simple Split Accuracy Fluctuation")
print(f"  05_kfold_stability.png                  - K-Fold CV Stability Chart")
print(f"  06_split_comparison_table.png           - Statistics Comparison Table")
print(f"  07_split_visualization.png              - Split Process Visualization")
print(f"  08_accuracy_distribution_comparison.png - Accuracy Distribution Comparison")
print(f"\nData File:")
print(f"  02_split_comparison_results.csv         - Comparison Results Data")
