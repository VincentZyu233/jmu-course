"""
肖维涅法则 (Chauvenet's Criterion) 剔除坏值
用法: uv run calc1.py <逗号分隔的数据> [--table]
示例: uv run calc1.py 4.670,4.730,4.728
      uv run calc1.py 83.56,83.46,83.56,83.44,83.67,83.80,83.62,83.65
"""

import sys
import math


def norm_cdf(x):
    """标准正态分布累积分布函数 Φ(x)"""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def norm_ppf(p, tol=1e-10, max_iter=100):
    """标准正态分布分位函数 Φ⁻¹(p)，二分法求解"""
    if p <= 0 or p >= 1:
        raise ValueError("p must be in (0, 1)")
    # 初始区间
    lo, hi = -10, 10
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            return (lo + hi) / 2
    return (lo + hi) / 2


def chauvenet_critical(n):
    """计算肖维涅法则临界 z 值: Φ(z_crit) = 1 - 1/(4n)"""
    p = 1 - 1 / (4 * n)
    return norm_ppf(p)


def chauvenet_check(data, name="x"):
    """对 data 列表执行肖维涅检验，返回 (保留的数据, 被剔除的数据, 报告文本)"""
    n = len(data)
    mean = sum(data) / n
    if n > 1:
        var = sum((x - mean) ** 2 for x in data) / (n - 1)
        std = math.sqrt(var)
    else:
        std = 0.0

    z_crit = chauvenet_critical(n)

    lines = []
    lines.append("=" * 60)
    lines.append("肖维涅法则检验 (Chauvenet's Criterion)")
    lines.append("=" * 60)
    lines.append(f"物理量: {name}")
    lines.append(f"输入数据: {data}")
    lines.append(f"数据个数 n = {n}")
    lines.append(f"平均值 x̄ = {mean:.6f}")
    if n > 1:
        lines.append(f"标准偏差 S = {std:.6f}")
    lines.append(f"临界值 z_crit = {z_crit:.4f}  (n={n}, P=1/(2n)={1 / (2 * n):.4f})")
    lines.append("")

    kept = []
    rejected = []
    lines.append("逐个检验:")
    for x in data:
        if n > 1 and std > 0:
            d = abs(x - mean) / std
            status = "✗ 剔除!" if d > z_crit else "✓ 保留"
            if d > z_crit:
                rejected.append(x)
            else:
                kept.append(x)
            lines.append(
                f"  x={x:.6f}, |d|={d:.4f}  {'>' if d > z_crit else '<'} {z_crit:.4f}  {status}"
            )
        else:
            kept.append(x)
            lines.append(f"  x={x}, n=1 或 S=0，无条件保留")

    lines.append("")
    if rejected:
        lines.append(f"结论：发现 {len(rejected)} 个坏值，已被剔除: {rejected}")
        lines.append(f"保留数据: {kept}")
    else:
        lines.append("结论：无坏值，全部保留。")
    lines.append("=" * 60)

    return kept, rejected, "\n".join(lines)


def main():
    args = sys.argv[1:]

    # 打印复现命令（在顶部）
    cmd = f"uv run python calc1.py {' '.join(args)}"
    print(f"# 复现命令: {cmd}")
    print("")

    if not args:
        print("用法: uv run calc1.py <逗号分隔的数据> [--name 物理量名称]")
        print("")
        print("全部实验数据复现命令:")
        print("  uv run python calc1.py 4.670,4.730,4.728 --name a")
        print("  uv run python calc1.py 11.580,11.540,11.622 --name b")
        print(
            "  uv run python calc1.py 49.55,49.57,49.59,49.58,49.60,49.61,49.56,49.59 --name H0"
        )
        print(
            "  uv run python calc1.py 83.56,83.46,83.56,83.44,83.67,83.80,83.62,83.65 --name t0"
        )
        print(
            "  uv run python calc1.py 49.84,49.85,49.88,49.86,49.88,49.81,49.78,49.80 --name H1"
        )
        print(
            "  uv run python calc1.py 69.19,69.28,69.13,69.06,68.97,69.10,69.25,69.07 --name t1"
        )
        return

    # 解析参数
    data_str = args[0]
    name = "x"
    if "--name" in args:
        idx = args.index("--name")
        if idx + 1 < len(args):
            name = args[idx + 1]

    try:
        data = [float(v.strip()) for v in data_str.split(",")]
    except ValueError:
        print("错误：数据格式不正确，请用逗号分隔数值")
        return

    if len(data) < 1:
        print("错误：至少需要 1 个数据")
        return

    kept, rejected, report = chauvenet_check(data, name=name)
    print(report)


if __name__ == "__main__":
    main()
