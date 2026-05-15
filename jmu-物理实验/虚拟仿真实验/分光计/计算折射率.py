import math

def calculate_n():
    print("请输入四个数值（A度 A分 delta度 delta分），空格隔开：")
    try:
        # 获取输入并拆分
        data = input("> ").split()
        if len(data) != 4:
            print("错误：请输入四个数值。")
            return

        # 转换为浮点数
        a_deg, a_min, d_deg, d_min = map(float, data)

        # 1. 将“度分”转换为“十进制角度”
        # 公式：角度 = 度 + 分/60
        A = a_deg + a_min / 60
        D = d_deg + d_min / 60

        # 2. Python 的 math.sin 使用弧度(radians)，需要转换
        # math.radians 会把角度转换为弧度
        A_rad = math.radians(A)
        D_rad = math.radians(D)

        # 3. 代入折射率公式
        # n = sin((A + D) / 2) / sin(A / 2)
        numerator = math.sin((A_rad + D_rad) / 2)
        denominator = math.sin(A_rad / 2)
        
        n = numerator / denominator

        # 输出结果，保留 4 位小数
        print("-" * 30)
        print(f"测量顶角 A: {A:.4f}°")
        print(f"最小偏向角 delta: {D:.4f}°")
        print(f"计算得到的折射率 n = {n:.4f}")
        print("-" * 30)

    except ValueError:
        print("错误：请输入有效的数字。")

if __name__ == "__main__":
    calculate_n()