import math


def chauvenet_criterion():
    """
    使用肖维涅准则交互式处理数据，剔除异常值。

    💡 你的实验数据备忘（方便复制粘贴测试）：
    D 组  : 10.030, 10.030, 10.032, 10.034, 10.032, 10.030, 10.030, 10.028
    t1 组 : 12.97, 12.97, 13.03, 13.09, 13.06, 12.94, 13.00, 12.97
    t2 组 : 18.41, 18.25, 18.34, 18.40, 18.32, 18.37, 18.40, 18.40
    t 组  : 25.34, 25.53, 25.47, 25.34, 25.47, 25.53, 25.34, 25.53
    """

    print("====== ⚖️ 肖维涅准则数据剔除工具 ======")
    print("你可以直接复制下方数据进行测试：")
    print("👉 D 组 : 10.030, 10.030, 10.032, 10.034, 10.032, 10.030, 10.030, 10.028")
    print("👉 t1组: 12.97, 12.97, 13.03, 13.09, 13.06, 12.94, 13.00, 12.97")
    print("👉 t2组: 18.41, 18.25, 18.34, 18.40, 18.32, 18.37, 18.40, 18.40")
    print("👉 t 组 : 25.34, 25.53, 25.47, 25.34, 25.47, 25.53, 25.34, 25.53\n")

    # 1. 获取控制台输入
    raw_input = input("请输入你的原始数据（多个数据请用英文或中文逗号隔开）：\n")

    # 2. 解析数据（兼容中文逗号和英文逗号）
    normalized_input = raw_input.replace("，", ",")
    try:
        data = [float(x.strip()) for x in normalized_input.split(",") if x.strip()]
    except ValueError:
        print("\n❌ 错误：输入数据格式有误，请确保全是数字并用逗号隔开。")
        return

    if not data:
        print("\n❌ 错误：未检测到有效数字。")
        return

    # 3. 肖维涅临界系数表 (n=3 到 15)
    chauvenet_table = {
        3: 1.38,
        4: 1.54,
        5: 1.65,
        6: 1.73,
        7: 1.80,
        8: 1.86,
        9: 1.92,
        10: 1.96,
        11: 2.00,
        12: 2.04,
        13: 2.07,
        14: 2.10,
        15: 2.13,
    }

    orig_data = data.copy()
    eliminated_elements = []

    # 4. 循环迭代检验坏值
    while True:
        n = len(data)
        if n < 3:
            print(
                f"\n⚠️ 提示：当前剩余样本量 n={n} 太小，已无法继续使用肖维涅法则进行检验。"
            )
            break

        c_n = chauvenet_table.get(n)
        if not c_n:
            print(
                f"\n⚠️ 提示：当前测量次数 n={n} 超出内置临界表范围（目前支持3-15次）。"
            )
            break

        mean = sum(data) / n
        # 计算样本标准差 (Bessel修正，使用 n-1)
        variance = sum((x - mean) ** 2 for x in data) / (n - 1)
        std_dev = math.sqrt(variance)

        if std_dev == 0:
            break  # 标准差为0说明数据完全一致，无坏值

        max_deviation = -1
        target_index = -1

        for i, val in enumerate(data):
            dev = abs(val - mean) / std_dev
            if dev > max_deviation:
                max_deviation = dev
                target_index = i

        # 判定是否满足剔除条件
        if max_deviation > c_n:
            removed_val = data.pop(target_index)
            eliminated_elements.append(removed_val)
        else:
            break  # 最大偏差也未超过临界值，结束循环

    # 5. 打印最终分析报告
    print("\n" + "=" * 45)
    print(f"📊 原始输入数据 (n={len(orig_data)}): {orig_data}")

    if eliminated_elements:
        print(f"🚨 检测到并剔除的坏值: {eliminated_elements}")
        print(f"✅ 剔除后的有效数据 (n={len(data)}): {data}")
    else:
        print("✅ 未检测到异常坏值，所有原始数据均有效。")

    final_mean = sum(data) / len(data)
    final_variance = sum((x - final_mean) ** 2 for x in data) / (len(data) - 1)
    final_std = math.sqrt(final_variance)
    print(f"📈 最终有效平均值  : {final_mean:.5f}")
    print("=" * 45)

    # 6. 询问是否生成 Markdown 结果文件
    ans = input("\n是否生成 Markdown 结果文件？(y/N): ").strip()
    if ans.lower() == "y":
        name = input("请输入文件名标识: ").strip()
        if not name:
            print("⚠️ 文件名标识为空，跳过生成。")
            return

        md_lines = [
            "## 肖维涅准则数据分析报告\n",
            f"- **文件名标识**: {name}",
            f"- **原始数据** (n={len(orig_data)}): {orig_data}",
        ]
        if eliminated_elements:
            md_lines.append(f"- **剔除坏值**: {eliminated_elements}")
            md_lines.append(f"- **有效数据** (n={len(data)}): {data}")
        else:
            md_lines.append("- **未检测到异常坏值**，所有原始数据均有效。")
        md_lines.extend(
            [
                f"- **有效数据个数**: {len(data)}",
                f"- **最终平均值**: {final_mean:.5f}",
                f"- **样本标准差**: {final_std:.5f}",
            ]
        )

        filename = f"chauvenet_{name}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"✅ 已保存结果至: {filename}")


if __name__ == "__main__":
    chauvenet_criterion()
