"""
直接测量量不确定度计算
用法: uv run calc2.py <逗号分隔的数据> --delta <仪器误差> [--name <名称>] [--unit <单位>]

示例:
  uv run calc2.py 4.670,4.730,4.728 --delta 0.002 --name a --unit cm
  uv run calc2.py 83.56,83.46,83.56,83.44,83.67,83.80,83.62,83.65 --delta 0.05 --name t0 --unit s
  uv run calc2.py 495.84 --delta 0.05 --name M --unit g  (单值)
"""

import sys
import math


def round_up_1sig(value):
    """逢数进位：保留 1 位有效数字，只入不舍"""
    if value == 0:
        return 0.0
    exp = int(math.floor(math.log10(abs(value))))
    factor = 10**exp
    return math.ceil(abs(value) / factor) * factor


def round_2sig(value):
    """四舍六入五凑偶：保留 2 位有效数字"""
    if value == 0:
        return 0.0
    exp = int(math.floor(math.log10(abs(value))))
    factor = 10 ** (exp - 1)
    return round(value / factor) * factor


def calc_uncertainty(data, delta, name="x", unit=""):
    """计算均值、标准差、A/B类及合成不确定度"""
    n = len(data)
    mean = sum(data) / n

    if n > 1:
        var = sum((x - mean) ** 2 for x in data) / (n - 1)
        std = math.sqrt(var)
        uA = std / math.sqrt(n)
    else:
        std = 0.0
        uA = 0.0

    uB = delta / math.sqrt(3)
    u = math.sqrt(uA**2 + uB**2)
    rel_u = (u / abs(mean)) * 100 if mean != 0 else 0

    lines = []
    lines.append("=" * 60)
    lines.append("直接测量量不确定度计算")
    lines.append("=" * 60)
    lines.append(f"物理量: {name}")
    lines.append(f"输入数据: {data}  (单位: {unit})" if unit else f"输入数据: {data}")
    lines.append(f"仪器误差 Δ = {delta} {unit}".strip())
    lines.append("")
    lines.append(f"n = {n}")
    lines.append(f"x̄ = {mean:.6f} {unit}".strip())
    lines.append("")

    if n > 1:
        lines.append("S = √[ Σ(xi-x̄)²/(n-1) ]")
        dev_sq_sum = sum((x - mean) ** 2 for x in data)
        lines.append(f"  = √({dev_sq_sum:.6f}/{n - 1})")
        lines.append(f"  = {std:.6f} {unit}".strip())
        lines.append("")

        lines.append(f"uA = S/√n")
        lines.append(f"   = {std:.6f}/√{n}")
        uA_2sig = round_2sig(uA)
        lines.append(
            f"   = {uA:.6f} {unit}  ≈ {uA_2sig:.4g} {unit}  (2 位有效数字)".strip()
        )
        lines.append("")
    else:
        lines.append("n=1，S=0，uA=0")
        lines.append("")

    lines.append(f"uB = Δ/√3")
    lines.append(f"   = {delta}/{math.sqrt(3):.6f}")
    uB_formatted = f"{uB:.6f}"
    uB_2sig = round_2sig(uB)
    uB_1sig = round_up_1sig(uB)
    lines.append(
        f"   = {uB_formatted} {unit}  ≈ {uB_1sig:.4g} {unit}  (1 位有效数字, 逢数进位)".strip()
    )
    lines.append("")

    lines.append(f"u = √(uA²+uB²)")
    lines.append(f"  = √({uA:.6f}² + {uB:.6f}²)")
    lines.append(f"  = √({uA * uA:.8f} + {uB * uB:.8f})")
    u_2sig = round_2sig(u)
    lines.append(f"  = {u:.6f} {unit}  ≈ {u_2sig:.4g} {unit}  (2 位有效数字)".strip())
    lines.append("")

    lines.append(f"相对不确定度: u_rel = {rel_u:.4f}%")
    lines.append("=" * 60)

    return lines, mean, std, uA, uB, u


def main():
    args = sys.argv[1:]

    # 打印复现命令（在顶部）
    cmd = f"uv run python calc2.py {' '.join(args)}"
    print(f"# 复现命令: {cmd}")
    print("")

    if not args:
        print(
            "用法: uv run calc2.py <逗号分隔的数据> --delta <仪器误差> [--name <名称>] [--unit <单位>]"
        )
        print("")
        print("全部实验数据复现命令:")
        print(
            "  uv run python calc2.py 4.670,4.730,4.728 --delta 0.002 --name a --unit cm"
        )
        print(
            "  uv run python calc2.py 11.580,11.540,11.622 --delta 0.002 --name b --unit cm"
        )
        print(
            "  uv run python calc2.py 49.55,49.57,49.59,49.58,49.60,49.61,49.56,49.59 --delta 0.05 --name H0 --unit cm"
        )
        print(
            "  uv run python calc2.py 83.56,83.46,83.56,83.44,83.67,83.80,83.62,83.65 --delta 0.05 --name t0 --unit s"
        )
        print(
            "  uv run python calc2.py 49.84,49.85,49.88,49.86,49.88,49.81,49.78,49.80 --delta 0.05 --name H1 --unit cm"
        )
        print(
            "  uv run python calc2.py 69.19,69.28,69.13,69.06,68.97,69.10,69.25,69.07 --delta 0.05 --name t1 --unit s"
        )
        print("  uv run python calc2.py 495.84 --delta 0.05 --name M --unit g")
        return

    data_str = args[0]
    delta = None
    name = "x"
    unit = ""

    if "--delta" in args:
        idx = args.index("--delta")
        if idx + 1 < len(args):
            delta = float(args[idx + 1])
    if "--name" in args:
        idx = args.index("--name")
        if idx + 1 < len(args):
            name = args[idx + 1]
    if "--unit" in args:
        idx = args.index("--unit")
        if idx + 1 < len(args):
            unit = args[idx + 1]

    if delta is None:
        print("错误：必须指定 --delta <仪器误差>")
        return

    try:
        data = [float(v.strip()) for v in data_str.split(",")]
    except ValueError:
        print("错误：数据格式不正确，请用逗号分隔数值")
        return

    lines, mean, std, uA, uB, u = calc_uncertainty(data, delta, name=name, unit=unit)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
