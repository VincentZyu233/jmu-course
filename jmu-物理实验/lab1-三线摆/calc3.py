"""
三线摆法测定物体转动惯量 —— 完整计算
支持交互式和命令行参数两种模式

用法:
  # 交互式模式 (直接回车使用实验数据的默认值)
  uv run calc3.py

  # 命令行参数模式
  uv run calc3.py --m 355 --M 495.84 --a-mean 4.70933 --a-unc 0.0197 ...

  # 从文件读取参数
  uv run calc3.py --from-file params.txt
"""

import sys
import math
import argparse


# ============ 实验数据默认值 ============
DEFAULT = {
    "m": 355,  # g
    "M": 495.84,  # g
    "a_mean": 4.709333,  # cm
    "a_unc": 0.01971,  # cm
    "b_mean": 11.580667,  # cm
    "b_unc": 0.02370,  # cm
    "H0_mean": 49.58125,  # cm
    "H0_unc": 0.02975,  # cm
    "t0_mean": 83.595,  # s
    "t0_unc": 0.05047,  # s
    "H1_mean": 49.8375,  # cm
    "H1_unc": 0.03174,  # cm
    "t1_mean": 69.13125,  # s
    "t1_unc": 0.04671,  # s
    "uM": 0.02887,  # g
    "g": 9.80,  # m/s²
}


# ============ 舍入辅助函数 ============


def round_up_1sig(value):
    """逢数进位：不确定度保留 1 个有效数字，只入不舍"""
    if value == 0:
        return 0.0, 0
    exp = int(math.floor(math.log10(abs(value))))
    factor = 10**exp
    rounded = math.ceil(abs(value) / factor) * factor
    return rounded if value >= 0 else -rounded, exp


def round_half_to_even(value, decimals):
    """四舍六入五凑偶：在指定小数位舍入"""
    factor = 10**decimals
    scaled = value * factor
    rounded = round(scaled)  # Python 的 round 就是银行家舍入（四舍六入五凑偶）
    return rounded / factor


def align_uncertainty_to_mean(mean, unc):
    """
    将不确定度保留 1 位有效数字（逢数进位），
    将平均值尾数与不确定度对齐（四舍六入五凑偶），
    返回 (mean_formatted, unc_formatted, decimals)
    """
    if unc <= 0:
        return f"{mean:.6e}", f"{unc}", 0

    # 不确定度保留 1 位有效数字，逢数进位
    unc_rounded, exp = round_up_1sig(unc)

    # 确定小数位数
    decimals = max(0, -exp)

    # 平均值对齐到相同小数位，四舍六入五凑偶
    mean_rounded = round_half_to_even(mean, decimals)

    return mean_rounded, unc_rounded, decimals


def format_result(mean, unc, unit=""):
    """格式化最终结果 I = Ī ± uI, (P=68.3%)"""
    mean_r, unc_r, dec = align_uncertainty_to_mean(mean, unc)

    # 判断是否用科学计数法
    if abs(mean_r) < 0.001 or abs(mean_r) >= 10000:
        # 科学计数法
        mean_exp = int(math.floor(math.log10(abs(mean_r)))) if abs(mean_r) > 0 else 0
        unc_exp = int(math.floor(math.log10(abs(unc_r)))) if abs(unc_r) > 0 else 0
        mean_sci = mean_r / (10**mean_exp)
        unc_sci = unc_r / (10**unc_exp)
        mean_str = f"{mean_sci:.{max(0, mean_exp - unc_exp)}f}×10^{mean_exp}"
        unc_str = f"{unc_sci:.0f}×10^{unc_exp}"
        return f"I = ({mean_str} ± {unc_str}) kg·m²,  (P=68.3%)"
    else:
        fmt = f".{dec}f"
        return f"I = {mean_r:{fmt}} ± {unc_r:{fmt}} kg·m²,  (P=68.3%)"


# ============ 核心计算函数 ============


def calc_I0(m, g, a, b, H0, t0, ua, ub, uH0, ut0):
    """计算空悬盘转动惯量 I₀ 及其不确定度"""
    m_si = m / 1000  # g -> kg
    a_si = a / 100  # cm -> m
    b_si = b / 100  # cm -> m
    H0_si = H0 / 100  # cm -> m
    ua_si = ua / 100  # cm -> m
    ub_si = ub / 100  # cm -> m
    uH0_si = uH0 / 100  # cm -> m

    T0 = t0 / 50  # 周期
    T0_sq = T0**2

    numerator = m_si * g * a_si * b_si
    denominator = 12 * (math.pi**2) * H0_si
    I0 = (numerator / denominator) * T0_sq

    # 相对不确定度合成
    rel_sq = (
        (ua_si / a_si) ** 2
        + (ub_si / b_si) ** 2
        + (uH0_si / H0_si) ** 2
        + (2 * ut0 / t0) ** 2
    )
    uI0 = I0 * math.sqrt(rel_sq)

    # 生成报告
    lines = []
    lines.append("=" * 60)
    lines.append("3. 空悬盘的转动惯量 I₀ 及其不确定度")
    lines.append("=" * 60)
    lines.append("")
    lines.append("公式: I₀ = (m·g·a·b) / (12π²·H₀) · (t₀/50)²")
    lines.append("")
    lines.append("单位换算 (→ SI):")
    lines.append(f"  m  = {m} g = {m_si:.6f} kg")
    lines.append(f"  a  = {a} cm = {a_si:.6f} m")
    lines.append(f"  b  = {b} cm = {b_si:.6f} m")
    lines.append(f"  H₀ = {H0} cm = {H0_si:.6f} m")
    lines.append(f"  t₀ = {t0} s (50个周期总时间)")
    lines.append(f"  g  = {g} m/s²")
    lines.append("")
    lines.append(f"周期 T₀ = t₀/50 = {t0}/{50} = {T0:.6f} s")
    lines.append(f"T₀² = {T0_sq:.8f} s²")
    lines.append("")
    lines.append("代入计算 I₀:")
    lines.append(
        f"  I₀ = ({m_si:.6f} × {g} × {a_si:.6f} × {b_si:.6f}) / (12 × π² × {H0_si:.6f}) × {T0_sq:.8f}"
    )
    lines.append(
        f"  分子 = {m_si:.6f} × {g} × {a_si:.6f} × {b_si:.6f} = {numerator:.8f}"
    )
    lines.append(f"  分母 = 12 × π² × {H0_si:.6f} = {denominator:.6f}")
    lines.append(
        f"  系数 = {numerator:.8f} / {denominator:.6f} = {numerator / denominator:.8e}"
    )
    lines.append(f"  I₀ = {numerator / denominator:.8e} × {T0_sq:.8f}")
    lines.append(f"  I₀ = {I0:.8e} kg·m²")
    lines.append("")
    lines.append("不确定度传递:")
    lines.append(f"  uI₀ = I₀ × √[(ua/a)² + (ub/b)² + (uH₀/H₀)² + (2·ut₀/t₀)²]")
    lines.append(f"  ua/a = {ua_si:.6f}/{a_si:.6f} = {ua_si / a_si:.6e}")
    lines.append(f"  ub/b = {ub_si:.6f}/{b_si:.6f} = {ub_si / b_si:.6e}")
    lines.append(f"  uH₀/H₀ = {uH0_si:.6f}/{H0_si:.6f} = {uH0_si / H0_si:.6e}")
    lines.append(f"  2·ut₀/t₀ = 2×{ut0:.6f}/{t0} = {2 * ut0 / t0:.6e}")
    lines.append(
        f"  合成相对不确定度 = √({(ua_si / a_si) ** 2:.3e} + {(ub_si / b_si) ** 2:.3e} + {(uH0_si / H0_si) ** 2:.3e} + {(2 * ut0 / t0) ** 2:.3e})"
    )
    lines.append(f"  = √({rel_sq:.6e}) = {math.sqrt(rel_sq):.6e}")
    lines.append(f"  uI₀ = {I0:.8e} × {math.sqrt(rel_sq):.6e} = {uI0:.6e} kg·m²")
    lines.append("")
    lines.append(f"结果: I₀ = {I0:.4e} kg·m²")
    lines.append(f"      uI₀ = {uI0:.4e} kg·m²")
    lines.append("=" * 60)
    lines.append("")

    return I0, uI0, "\n".join(lines)


def calc_I1(m, M, g, a, b, H1, t1, ua, ub, uH1, ut1, uM):
    """计算载物悬盘转动惯量 I₁ 及其不确定度"""
    m_si = m / 1000
    M_si = M / 1000
    M_total_si = M_si + m_si
    a_si = a / 100
    b_si = b / 100
    H1_si = H1 / 100
    ua_si = ua / 100
    ub_si = ub / 100
    uH1_si = uH1 / 100
    uM_si = uM / 1000

    T1 = t1 / 50
    T1_sq = T1**2

    numerator = M_total_si * g * a_si * b_si
    denominator = 12 * (math.pi**2) * H1_si
    I1 = (numerator / denominator) * T1_sq

    rel_sq = (
        (ua_si / a_si) ** 2
        + (ub_si / b_si) ** 2
        + (uH1_si / H1_si) ** 2
        + (2 * ut1 / t1) ** 2
        + (uM_si / M_total_si) ** 2
    )
    uI1 = I1 * math.sqrt(rel_sq)

    lines = []
    lines.append("=" * 60)
    lines.append("4. 载物悬盘的转动惯量 I₁ 及其不确定度")
    lines.append("=" * 60)
    lines.append("")
    lines.append("公式: I₁ = ((M+m)·g·a·b) / (12π²·H₁) · (t₁/50)²")
    lines.append("")
    lines.append("单位换算 (→ SI):")
    lines.append(f"  m  = {m} g = {m_si:.6f} kg")
    lines.append(f"  M  = {M} g = {M_si:.6f} kg")
    lines.append(f"  M+m = {M_total_si:.6f} kg")
    lines.append(f"  a  = {a} cm = {a_si:.6f} m")
    lines.append(f"  b  = {b} cm = {b_si:.6f} m")
    lines.append(f"  H₁ = {H1} cm = {H1_si:.6f} m")
    lines.append(f"  t₁ = {t1} s (50个周期总时间)")
    lines.append(f"  g  = {g} m/s²")
    lines.append("")
    lines.append(f"周期 T₁ = t₁/50 = {t1}/{50} = {T1:.6f} s")
    lines.append(f"T₁² = {T1_sq:.8f} s²")
    lines.append("")
    lines.append("代入计算 I₁:")
    lines.append(
        f"  I₁ = ({M_total_si:.6f} × {g} × {a_si:.6f} × {b_si:.6f}) / (12 × π² × {H1_si:.6f}) × {T1_sq:.8f}"
    )
    lines.append(
        f"  分子 = {M_total_si:.6f} × {g} × {a_si:.6f} × {b_si:.6f} = {numerator:.8f}"
    )
    lines.append(f"  分母 = 12 × π² × {H1_si:.6f} = {denominator:.6f}")
    lines.append(
        f"  系数 = {numerator:.8f} / {denominator:.6f} = {numerator / denominator:.8e}"
    )
    lines.append(f"  I₁ = {numerator / denominator:.8e} × {T1_sq:.8f}")
    lines.append(f"  I₁ = {I1:.8e} kg·m²")
    lines.append("")
    lines.append("不确定度传递:")
    lines.append(
        f"  uI₁ = I₁ × √[(ua/a)² + (ub/b)² + (uH₁/H₁)² + (2·ut₁/t₁)² + (uM/(M+m))²]"
    )
    lines.append(f"  ua/a = {ua_si:.6f}/{a_si:.6f} = {ua_si / a_si:.6e}")
    lines.append(f"  ub/b = {ub_si:.6f}/{b_si:.6f} = {ub_si / b_si:.6e}")
    lines.append(f"  uH₁/H₁ = {uH1_si:.6f}/{H1_si:.6f} = {uH1_si / H1_si:.6e}")
    lines.append(f"  2·ut₁/t₁ = 2×{ut1:.6f}/{t1} = {2 * ut1 / t1:.6e}")
    lines.append(
        f"  uM/(M+m) = {uM_si:.6f}/{M_total_si:.6f} = {uM_si / M_total_si:.6e}"
    )
    lines.append(
        f"  合成相对不确定度 = √({(ua_si / a_si) ** 2:.3e} + {(ub_si / b_si) ** 2:.3e} + {(uH1_si / H1_si) ** 2:.3e} + {(2 * ut1 / t1) ** 2:.3e} + {(uM_si / M_total_si) ** 2:.3e})"
    )
    lines.append(f"  = √({rel_sq:.6e}) = {math.sqrt(rel_sq):.6e}")
    lines.append(f"  uI₁ = {I1:.8e} × {math.sqrt(rel_sq):.6e} = {uI1:.6e} kg·m²")
    lines.append("")
    lines.append(f"结果: I₁ = {I1:.4e} kg·m²")
    lines.append(f"      uI₁ = {uI1:.4e} kg·m²")
    lines.append("=" * 60)
    lines.append("")

    return I1, uI1, "\n".join(lines)


def calc_I_diff(I1, I0, uI1, uI0):
    """计算不规则测件转动惯量 I = I₁ - I₀"""
    I = I1 - I0
    uI = math.sqrt(uI0**2 + uI1**2)

    lines = []
    lines.append("=" * 60)
    lines.append("5. 不规则测件的转动惯量 I 及其不确定度")
    lines.append("=" * 60)
    lines.append("")
    lines.append("公式: I = I₁ - I₀")
    lines.append(f"  I = {I1:.8e} - {I0:.8e}")
    lines.append(f"  I = {I:.8e} kg·m²")
    lines.append("")
    lines.append("公式: uI = √(uI₀² + uI₁²)")
    lines.append(f"  uI = √(({uI0:.6e})² + ({uI1:.6e})²)")
    lines.append(f"  uI = √({uI0 * uI0:.6e} + {uI1 * uI1:.6e})")
    lines.append(f"  uI = √({uI0 * uI0 + uI1 * uI1:.6e})")
    lines.append(f"  uI = {uI:.6e} kg·m²")
    lines.append("=" * 60)
    lines.append("")

    return I, uI, "\n".join(lines)


def calc_result(I, uI):
    """实验结果表达"""
    lines = []
    lines.append("=" * 60)
    lines.append("6. 实验结果的表达")
    lines.append("=" * 60)
    lines.append("")
    lines.append("三线摆法测定不规则物体的转动惯量的测量结果为：")
    lines.append("")

    result_str = format_result(I, uI)
    lines.append(f"  {result_str}")
    lines.append("")
    lines.append(
        "(注：不确定度保留 1 个有效数字，逢数进位；平均数尾数与不确定度对齐，四舍六入五凑偶)"
    )
    lines.append("=" * 60)

    return "\n".join(lines), result_str


# ============ 交互式输入 ============


def interactive_input():
    """交互式输入各物理量的平均值和不确定度"""
    print("=" * 60)
    print("三线摆转动惯量计算 — 交互式输入")
    print("直接回车使用来自实验数据的默认值")
    print("=" * 60)
    print("")

    params = {}

    prompts = [
        ("m (g)", "m", float),
        ("M (g)", "M", float),
        ("ā (cm)", "a_mean", float),
        ("ua (cm)", "a_unc", float),
        ("b̄ (cm)", "b_mean", float),
        ("ub (cm)", "b_unc", float),
        ("H̄₀ (cm)", "H0_mean", float),
        ("uH₀ (cm)", "H0_unc", float),
        ("t̄₀ (s)", "t0_mean", float),
        ("ut₀ (s)", "t0_unc", float),
        ("H̄₁ (cm)", "H1_mean", float),
        ("uH₁ (cm)", "H1_unc", float),
        ("t̄₁ (s)", "t1_mean", float),
        ("ut₁ (s)", "t1_unc", float),
        ("uM (g)", "uM", float),
    ]

    for prompt, key, cast in prompts:
        default = DEFAULT[key]
        user_input = input(f"  {prompt} [默认: {default}]: ").strip()
        if user_input == "":
            params[key] = default
        else:
            try:
                params[key] = cast(user_input)
            except ValueError:
                print(f"  输入无效，使用默认值 {default}")
                params[key] = default

    print("")
    return params


# ============ 命令行入口 ============


def parse_args():
    parser = argparse.ArgumentParser(description="三线摆转动惯量计算")
    parser.add_argument("--m", type=float, help="m (g)")
    parser.add_argument("--M", type=float, help="M (g)")
    parser.add_argument("--a-mean", type=float, help="ā (cm)")
    parser.add_argument("--a-unc", type=float, help="ua (cm)")
    parser.add_argument("--b-mean", type=float, help="b̄ (cm)")
    parser.add_argument("--b-unc", type=float, help="ub (cm)")
    parser.add_argument("--H0-mean", type=float, help="H̄₀ (cm)")
    parser.add_argument("--H0-unc", type=float, help="uH₀ (cm)")
    parser.add_argument("--t0-mean", type=float, help="t̄₀ (s)")
    parser.add_argument("--t0-unc", type=float, help="ut₀ (s)")
    parser.add_argument("--H1-mean", type=float, help="H̄₁ (cm)")
    parser.add_argument("--H1-unc", type=float, help="uH₁ (cm)")
    parser.add_argument("--t1-mean", type=float, help="t̄₁ (s)")
    parser.add_argument("--t1-unc", type=float, help="ut₁ (s)")
    parser.add_argument("--uM", type=float, help="uM (g)")
    parser.add_argument(
        "--g", type=float, default=9.80, help="重力加速度 (m/s²), 默认 9.80"
    )
    parser.add_argument(
        "--from-file", type=str, help="从文件读取参数 (key=value 每行一个)"
    )
    return parser.parse_args()


def load_from_file(filepath):
    """从文件加载参数"""
    params = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip().replace("-", "_")
                try:
                    params[key] = float(val.strip())
                except ValueError:
                    pass
    return params


def main():
    # 收集参数
    params = {}

    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        args = parse_args()

        if args.from_file:
            params = load_from_file(args.from_file)
        else:
            arg_map = {
                "m": args.m,
                "M": args.M,
                "a_mean": args.a_mean,
                "a_unc": args.a_unc,
                "b_mean": args.b_mean,
                "b_unc": args.b_unc,
                "H0_mean": args.H0_mean,
                "H0_unc": args.H0_unc,
                "t0_mean": args.t0_mean,
                "t0_unc": args.t0_unc,
                "H1_mean": args.H1_mean,
                "H1_unc": args.H1_unc,
                "t1_mean": args.t1_mean,
                "t1_unc": args.t1_unc,
                "uM": args.uM,
            }
            for k, v in arg_map.items():
                if v is not None:
                    params[k] = v

            # g is always available
            params["g"] = args.g
    else:
        params = interactive_input()
        params["g"] = DEFAULT["g"]

    # 补充未提供的参数为默认值
    for k, v in DEFAULT.items():
        if k not in params:
            params[k] = v

    # 打印复现命令（在顶部）
    is_interactive = len(sys.argv) <= 1
    if is_interactive:
        calc3_cmd = (
            f"uv run python calc3.py"
            f" --m {params['m']} --M {params['M']}"
            f" --a-mean {params['a_mean']} --a-unc {params['a_unc']}"
            f" --b-mean {params['b_mean']} --b-unc {params['b_unc']}"
            f" --H0-mean {params['H0_mean']} --H0-unc {params['H0_unc']}"
            f" --t0-mean {params['t0_mean']} --t0-unc {params['t0_unc']}"
            f" --H1-mean {params['H1_mean']} --H1-unc {params['H1_unc']}"
            f" --t1-mean {params['t1_mean']} --t1-unc {params['t1_unc']}"
            f" --uM {params['uM']}"
        )
    else:
        calc3_cmd = f"uv run python calc3.py {' '.join(sys.argv[1:])}"
    print(f"# 复现命令: {calc3_cmd}")
    print("")

    # 打印参数摘要
    print("")
    print("=" * 60)
    print("计算参数汇总")
    print("=" * 60)
    param_display = [
        ("m", "g"),
        ("M", "g"),
        ("ā", "cm"),
        ("ua", "cm"),
        ("b̄", "cm"),
        ("ub", "cm"),
        ("H̄₀", "cm"),
        ("uH₀", "cm"),
        ("t̄₀", "s"),
        ("ut₀", "s"),
        ("H̄₁", "cm"),
        ("uH₁", "cm"),
        ("t̄₁", "s"),
        ("ut₁", "s"),
        ("uM", "g"),
        ("g", "m/s²"),
    ]
    for key, unit in param_display:
        pkey = key.replace("̄", "").replace("₀", "0").replace("₁", "1")
        lookup = {
            "a": "a_mean",
            "b": "b_mean",
            "ua": "a_unc",
            "ub": "b_unc",
            "H0": "H0_mean",
            "uH0": "H0_unc",
            "t0": "t0_mean",
            "ut0": "t0_unc",
            "H1": "H1_mean",
            "uH1": "H1_unc",
            "t1": "t1_mean",
            "ut1": "t1_unc",
            "uM": "uM",
            "g": "g",
            "m": "m",
            "M": "M",
        }.get(pkey, pkey)
        val = params.get(lookup, DEFAULT.get(lookup, ""))
        print(f"  {key} = {val} {unit}")
    print("=" * 60)
    print("")

    # ====== 执行计算 ======
    m = params["m"]
    M = params["M"]
    g = params["g"]
    a_mean = params["a_mean"]
    a_unc = params["a_unc"]
    b_mean = params["b_mean"]
    b_unc = params["b_unc"]
    H0_mean = params["H0_mean"]
    H0_unc = params["H0_unc"]
    t0_mean = params["t0_mean"]
    t0_unc = params["t0_unc"]
    H1_mean = params["H1_mean"]
    H1_unc = params["H1_unc"]
    t1_mean = params["t1_mean"]
    t1_unc = params["t1_unc"]
    uM = params["uM"]

    # 3. I₀
    I0, uI0, report_I0 = calc_I0(
        m, g, a_mean, b_mean, H0_mean, t0_mean, a_unc, b_unc, H0_unc, t0_unc
    )
    print(report_I0)

    # 4. I₁
    I1, uI1, report_I1 = calc_I1(
        m, M, g, a_mean, b_mean, H1_mean, t1_mean, a_unc, b_unc, H1_unc, t1_unc, uM
    )
    print(report_I1)

    # 5. I = I₁ - I₀
    I, uI, report_I = calc_I_diff(I1, I0, uI1, uI0)
    print(report_I)

    # 6. 结果表达
    result_report, result_str = calc_result(I, uI)
    print(result_report)


if __name__ == "__main__":
    main()
