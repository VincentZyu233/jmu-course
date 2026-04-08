"""
一键运行所有实验脚本
"""

import subprocess
import sys
import os

print("=" * 70)
print(" " * 20 + "决策树实验 - 一键运行")
print("=" * 70)

scripts = [
    "00_prepare_data.py",
    "01_compare_criteria.py",
    "02_parameter_tuning.py",
    "03_final_model.py"
]

for i, script in enumerate(scripts, 1):
    print(f"\n{'=' * 70}")
    print(f"[{i}/{len(scripts)}] 运行: {script}")
    print("=" * 70)

    try:
        result = subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✓ {script} 执行成功")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {script} 执行失败")
        print(f"错误信息: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n✗ 找不到文件: {script}")
        sys.exit(1)

print("\n" + "=" * 70)
print(" " * 25 + "✓ 所有实验完成！")
print("=" * 70)
print("\n生成的文件：")
print("  📄 README.md - 完整实验报告")
print("  📁 output/figures/ - 所有实验图片")
print("  💾 output/wine_data.npz - 数据集")
print("  🎯 output/best_model.npz - 最优模型参数")
print("\n👉 现在可以查看 README.md 了！")
print("=" * 70)
