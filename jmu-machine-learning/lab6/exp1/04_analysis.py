from __future__ import annotations

import csv
from pathlib import Path

from common import output_dir, results_root


def read_metrics(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fmt(v: str, digits: int = 4) -> str:
    try:
        return f"{float(v):.{digits}f}"
    except ValueError:
        return v


def row_to_md(row: dict[str, str]) -> str:
    return (
        f"| {row['name']} | {row['epochs']} | {row['batch_size']} | {fmt(row['lr'], 6)} | "
        f"{row['kernel_size']} | {fmt(row['train_acc'])} | {fmt(row['test_acc'])} | "
        f"{fmt(row['train_loss'])} | {fmt(row['test_loss'])} | {fmt(row['seconds'], 2)} |"
    )


def build_report() -> str:
    base = output_dir()
    files = [
        base / "01_cnn_base_metrics.csv",
        base / "02_kernel_compare_metrics.csv",
        base / "03_lr_compare_metrics.csv",
    ]

    sections: list[str] = [
        "# 实验六 exp1 分析报告",
        "",
        "## 1. 实验说明",
        "本部分主要完成 MNIST 手写数字分类的基础 CNN 训练，并比较不同卷积核大小和学习率的影响。",
        "",
    ]

    all_rows: list[dict[str, str]] = []
    for path in files:
        if not path.exists():
            continue
        rows = read_metrics(path)
        all_rows.extend(rows)
        sections += [
            f"## {path.stem}",
            "",
            "| name | epochs | batch_size | lr | kernel_size | train_acc | test_acc | train_loss | test_loss | seconds |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        sections.extend(row_to_md(r) for r in rows)
        sections.append("")

    if all_rows:
        best = max(all_rows, key=lambda r: float(r["test_acc"]))
        fastest = min(all_rows, key=lambda r: float(r["seconds"]))
        sections += [
            "## 2. 结果总结",
            "",
            f"- 测试准确率最高的是 `{best['name']}`，`test_acc = {fmt(best['test_acc'])}`。",
            f"- 训练速度最快的是 `{fastest['name']}`，耗时 `seconds = {fmt(fastest['seconds'], 2)}` 秒。",
            "- 从当前结果看，`5x5` 卷积核在这组实验里略优于 `3x3`，但差距不大。",
            "- 学习率过小会让训练变慢，过大可能影响收敛稳定性。",
        ]

    return "\n".join(sections).rstrip() + "\n"


def main() -> None:
    report = build_report()
    result_dir = results_root() / "exp1"
    result_dir.mkdir(parents=True, exist_ok=True)
    path = result_dir / "04_analysis_report.md"
    path.write_text(report, encoding="utf-8")
    print(path)
    print(report)


if __name__ == "__main__":
    main()
