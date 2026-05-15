#!/usr/bin/env python3
"""
最小二乘法线性回归计算 + 拟合图。
每行输入一对数据 x, y（逗号/空格分隔），输入 quit 结束。
输出 → output/ 文件夹
"""

import math
import re
import os
from datetime import datetime
from pathlib import Path


def main():
    print("最小二乘法线性回归")
    print("每行输入一对数据: x, y  (逗号或空格分隔)")
    print("输入 quit 结束\n")

    xs, ys = [], []

    while True:
        line = input().strip()
        if not line:
            continue
        if line.lower() == "quit":
            break
        parts = re.split(r"[,，\s]+", line)
        if len(parts) < 2:
            print("格式错误，请用逗号或空格分隔 x 和 y")
            continue
        try:
            x, y = float(parts[0]), float(parts[1])
            xs.append(x)
            ys.append(y)
        except ValueError:
            print("数字解析失败，请重新输入")

    n = len(xs)
    if n < 2:
        print("至少需要 2 个数据点")
        return

    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    syy = sum(y * y for y in ys)
    sxy = sum(x * y for x, y in zip(xs, ys))

    mx = sx / n
    my = sy / n
    mxy = sxy / n
    mxx = sxx / n
    myy = syy / n

    k = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    b = (sy - k * sx) / n

    num = n * sxy - sx * sy
    denom = (n * sxx - sx * sx) * (n * syy - sy * sy)
    r = num / math.sqrt(denom) if denom > 0 else 0.0

    residuals = [y - (k * x + b) for x, y in zip(xs, ys)]
    rss = sum(res * res for res in residuals)
    sy_err = math.sqrt(rss / (n - 2)) if n > 2 else 0.0
    dx = n * (mxx - mx * mx)
    uk = math.sqrt(1.0 / dx) * sy_err if dx > 0 else 0.0

    # --- 终端输出 ---
    print(f"\n{'=' * 40}")
    print(f"n        = {n}")
    print(f"\u03a3x       = {sx}")
    print(f"\u03a3y       = {sy}")
    print(f"\u03a3x\u00b2      = {sxx}")
    print(f"\u03a3y\u00b2      = {syy}")
    print(f"\u03a3xy      = {sxy}")
    print(f"x\u0304        = {mx}")
    print(f"\u0233        = {my}")
    print(f"(xy)\u0304    = {mxy}")
    print(f"(x\u00b2)\u0304    = {mxx}")
    print(f"(y\u00b2)\u0304    = {myy}")
    print(f"k (\u659c\u7387) = {k}")
    print(f"b (\u622a\u8ddd) = {b}")
    print(f"r (\u76f8\u5173\u7cfb\u6570) = {r}")
    print(f"S_y      = {sy_err}")
    print(f"u_k      = {uk}")
    print(f"{'=' * 40}")

    # --- 输出目录 ---
    ts = datetime.now()
    ts_str = ts.strftime("%Y-%m-%d-%H-%M-%S")
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    # --- 生成拟合图 ---
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print(
            "\n\u63d0\u793a: \u5b89\u88c5 matplotlib \u53ef\u81ea\u52a8\u751f\u6210\u62df\u5408\u56fe"
        )
        print("  pip install matplotlib")
        plt = None

    img_rel = ""
    if plt is not None:
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(xs, ys, color="#1f77b4", s=50, zorder=5, label="Data points")

        x_min, x_max = min(xs), max(xs)
        pad = (x_max - x_min) * 0.1 or 1
        x_line = [x_min - pad, x_max + pad]
        y_line = [k * x + b for x in x_line]
        ax.plot(x_line, y_line, "r-", linewidth=2, label="Fitted line")

        eq_text = f"y = {k:.6g}x {b:+.6g}\nk = {k:.6g} ± {uk:.6g}\nr = {r:.6g}"
        ax.text(
            0.05,
            0.95,
            eq_text,
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.8),
        )

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Linear Regression (Least Squares)")
        ax.legend(loc="lower right")
        ax.grid(True, alpha=0.3)

        img_name = f"fit_plot-{ts_str}.png"
        img_path = out_dir / img_name
        fig.savefig(img_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        img_rel = f"./{img_name}"
        print(f"\n\u62df\u5408\u56fe  → {img_path}")

    # --- Markdown ---
    def esc(v):
        return f"{v:.6g}" if isinstance(v, float) else str(v)

    sk, sb, sr = esc(k), esc(b), esc(r)
    ssy_err = esc(sy_err)
    suk = esc(uk)
    ssx, ssy = esc(sx), esc(sy)
    ssxx, ssyy = esc(sxx), esc(syy)
    ssxy = esc(sxy)
    smx, smy = esc(mx), esc(my)
    smxy, smyy_ = esc(mxy), esc(myy)
    smxx = esc(mxx)

    lines = []
    lines.append("# 最小二乘法线性回归计算过程")
    lines.append("")
    lines.append(f"计算时间：{ts.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## 原始数据")
    lines.append("")
    lines.append("| i | $x$ | $y$ |")
    lines.append("|---|---|---|")
    for i, (x, y) in enumerate(zip(xs, ys), 1):
        lines.append(f"| {i} | {x} | {y} |")
    lines.append("")
    lines.append("## 统计量")
    lines.append("")
    lines.append(f"- 样本数 $n = {n}$")
    lines.append(f"- $\\sum x = {ssx}$")
    lines.append(f"- $\\sum y = {ssy}$")
    lines.append(f"- $\\sum x^2 = {ssxx}$")
    lines.append(f"- $\\sum y^2 = {ssyy}$")
    lines.append(f"- $\\sum xy = {ssxy}$")
    lines.append("")
    lines.append("## 平均值")
    lines.append("")
    lines.append(
        f"$\\bar{{x}} = \\dfrac{{\\sum x}}{{n}} = \\dfrac{{{ssx}}}{{{n}}} = {smx}$"
    )
    lines.append(
        f"$\\bar{{y}} = \\dfrac{{\\sum y}}{{n}} = \\dfrac{{{ssy}}}{{{n}}} = {smy}$"
    )
    lines.append(
        f"$\\overline{{xy}} = \\dfrac{{\\sum xy}}{{n}}"
        f" = \\dfrac{{{ssxy}}}{{{n}}} = {smxy}$"
    )
    lines.append(
        f"$\\overline{{x^2}} = \\dfrac{{\\sum x^2}}{{n}}"
        f" = \\dfrac{{{ssxx}}}{{{n}}} = {smxx}$"
    )
    lines.append(
        f"$\\overline{{y^2}} = \\dfrac{{\\sum y^2}}{{n}}"
        f" = \\dfrac{{{ssyy}}}{{{n}}} = {smyy_}$"
    )
    lines.append("")
    lines.append("## 斜率 $k$")
    lines.append("")
    lines.append("$k = \\dfrac{n\\sum xy - \\sum x \\sum y}{n\\sum x^2 - (\\sum x)^2}$")
    lines.append("")
    lines.append(
        f"$k = \\dfrac{{{n} \\times {ssxy} - {ssx} \\times {ssy}}}"
        f"{{{n} \\times {ssxx} - ({ssx})^2}}$"
    )
    lines.append("")
    lines.append(f"$k = {sk}$")
    lines.append("")
    lines.append("## 截距 $b$")
    lines.append("")
    lines.append(f"$b = \\dfrac{{\\sum y - k\\sum x}}{{n}}$")
    lines.append("")
    lines.append(f"$b = \\dfrac{{{ssy} - {sk} \\times {ssx}}}{{{n}}}$")
    lines.append("")
    lines.append(f"$b = {sb}$")
    lines.append("")
    lines.append("## 相关系数 $r$")
    lines.append("")
    lines.append(
        "$r = \\dfrac{n\\sum xy - \\sum x \\sum y}"
        "{\\sqrt{[n\\sum x^2 - (\\sum x)^2][n\\sum y^2 - (\\sum y)^2]}}$"
    )
    lines.append("")
    sxx_val = n * sxx - sx * sx
    syy_val = n * syy - sy * sy
    lines.append(
        f"$r = \\dfrac{{{n} \\times {ssxy} - {ssx} \\times {ssy}}}"
        f"{{\\sqrt{{({n} \\times {ssxx} - {ssx}^2)"
        f"({n} \\times {ssyy} - {ssy}^2)}}}}$"
    )
    lines.append("")
    lines.append(f"$r = {sr}$")
    lines.append("")
    lines.append("## 残差与剩余标准差 $S_y$")
    lines.append("")
    lines.append("残差：$\\varepsilon_i = y_i - (k x_i + b)$")
    lines.append("")
    lines.append(
        "| $i$ | $x_i$ | $y_i$ | $kx_i + b$ | $\\varepsilon_i$ | $\\varepsilon_i^2$ |"
    )
    lines.append("|---|---|---|---|---|---|")
    for i, (x, y, res) in enumerate(zip(xs, ys, residuals), 1):
        y_hat = k * x + b
        lines.append(
            f"| {i} | {x:.6g} | {y:.6g} | {y_hat:.6g} | {res:.6g} | {res * res:.6g} |"
        )
    lines.append("")
    lines.append(f"$\\mathrm{{RSS}} = \\sum \\varepsilon_i^2 = {rss:.6g}$")
    lines.append("")
    lines.append(
        f"$S_y = \\sqrt{{\\dfrac{{\\mathrm{{RSS}}}}{{n-2}}}} = \\sqrt{{\\dfrac{{{rss:.6g}}}{{{n - 2}}}}} = {sy_err:.6g}$"
    )
    lines.append("")
    lines.append("## 斜率不确定度 $u_k$")
    lines.append("")
    lines.append("$$u_k = \\sqrt{\\frac{1}{n(\\overline{x^2} - \\bar{x}^2)}} \\; S_y$$")
    lines.append("")
    lines.append(
        f"$\\overline{{x^2}} - \\bar{{x}}^2 = {mxx:.6g} - ({mx:.6g})^2 = {mxx - mx * mx:.6g}$"
    )
    lines.append("")
    lines.append(
        f"$u_k = \\sqrt{{\\dfrac{{1}}{{{n} \\times {mxx - mx * mx:.6g}}}}} \\times {sy_err:.6g}$"
    )
    lines.append("")
    lines.append(f"$u_k = {uk:.6g}$")
    lines.append("")
    lines.append("## 回归方程")
    lines.append("")
    lines.append(f"$y = ({sk} \\pm {suk})x + ({sb})$")
    lines.append("")

    if img_rel:
        lines.append("## 拟合图")
        lines.append("")
        lines.append(f"![]({img_rel})")
        lines.append("")

    md_name = f"least_squares-{ts_str}.md"
    md_path = out_dir / md_name
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Markdown → {md_path}")


if __name__ == "__main__":
    main()
