# -*- coding: utf-8 -*-
"""
Excel内容和公式提取工具
输出为Markdown格式

需要的第三方库:
    pip install openpyxl
"""

import os
import re
from openpyxl import load_workbook


def extract_excel_to_markdown(file_path: str, output_path: str = None):
    """
    提取Excel文件的内容和公式，输出为Markdown格式
    
    Args:
        file_path: Excel文件路径
        output_path: 输出Markdown文件路径(可选)
    """
    wb = load_workbook(file_path, data_only=False)
    
    lines = []
    lines.append(f"# {os.path.basename(file_path)}\n")
    lines.append(f"**总工作表数: {len(wb.sheetnames)}**\n")
    lines.append("---\n")
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        lines.append(f"\n## 工作表: {sheet_name}\n")
        
        # 获取有数据的区域
        if ws.max_row == 0 or ws.max_column == 0:
            lines.append("*（空表）*\n")
            continue
        
        # 创建一个表格
        # 收集所有非空单元格
        cells_data = {}
        formulas = {}
        
        for row in ws.iter_rows():
            for cell in row:
                if cell.value is not None:
                    coord = cell.coordinate
                    # 检查是否有公式
                    if hasattr(cell, 'data_type') and cell.data_type == 'f':
                        formulas[coord] = cell.value
                        cells_data[coord] = f"={cell.value}"  # 这是公式
                    else:
                        cells_data[coord] = cell.value
        
        if not cells_data:
            lines.append("*（空表）*\n")
            continue
        
        # 转换为Markdown表格
        # 找到数据范围
        min_row = min(int(re.match(r'([A-Z]+)(\d+)', c).group(2)) for c in cells_data.keys())
        max_row = max(int(re.match(r'([A-Z]+)(\d+)', c).group(2)) for c in cells_data.keys())
        min_col = re.match(r'([A-Z]+)(\d+)', list(cells_data.keys())[0]).group(1)
        max_col_letter = max(re.match(r'([A-Z]+)(\d+)', c).group(1) for c in cells_data.keys())
        
        # 列字母转数字
        def col_letter_to_num(letter):
            num = 0
            for char in letter:
                num = num * 26 + (ord(char) - ord('A') + 1)
            return num
        
        max_col = col_letter_to_num(max_col_letter)
        
        # 构建表头
        header = ["" for _ in range(max_col)]
        for col_idx in range(max_col):
            col_letter = chr(ord('A') + col_idx)
            header[col_idx] = col_letter
        
        lines.append("### 数据预览\n")
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "|".join(["---" for _ in range(max_col)]) + "|")
        
        # 逐行输出
        for row_num in range(min_row, max_row + 1):
            row_cells = []
            for col_idx in range(max_col):
                col_letter = chr(ord('A') + col_idx)
                coord = f"{col_letter}{row_num}"
                value = cells_data.get(coord, "")
                
                # 简化显示
                if value != "":
                    # 处理公式显示
                    if coord in formulas:
                        value = f"**={formulas[coord]}**"
                    else:
                        value = str(value)
                row_cells.append(value)
            
            lines.append(f"| {row_num} | " + " | ".join(row_cells[1:]) + " |")
        
        # 输出公式详情
        if formulas:
            lines.append("\n### 公式详情\n")
            lines.append("| 单元格 | 公式 | 计算结果 |")
            lines.append("|--------|------|---------|")
            
            for coord in sorted(formulas.keys(), key=lambda x: (int(re.match(r'([A-Z]+)(\d+)', x).group(2)), re.match(r'([A-Z]+)(\d+)', x).group(1))):
                formula = formulas[coord]
                # 尝试获取计算结果
                result = cells_data.get(coord, "?")
                lines.append(f"| {coord} | `{formula}` | {result} |")
        
        lines.append("\n---\n")
    
    # 写入输出文件
    output = "\n".join(lines)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"已输出到: {output_path}")
    
    return output


if __name__ == "__main__":
    # Excel文件路径
    excel_file = r"D:\aaaStuffsaaa\from_git\gitee\jmu-course\jmu-物理实验\lab11-数字示波器\（更新）重复测量数据坏值检查工具.xlsx"
    output_md = r"D:\aaaStuffsaaa\from_git\gitee\jmu-course\jmu-物理实验\lab11-数字示波器\提取结果.md"
    
    # 检查文件是否存在
    if not os.path.exists(excel_file):
        print(f"文件不存在: {excel_file}")
    else:
        result = extract_excel_to_markdown(excel_file, output_md)
        print("提取完成！")
        print("\n=== 预览 ===")
        print(result[:2000] + "..." if len(result) > 2000 else result)