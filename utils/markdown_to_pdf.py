"""
python markdown_to_pdf.py

"""

import os
from markdown_pdf import MarkdownPdf, Section

def convert_md_to_pdf(md_file_path):
    # 获取文件夹路径和文件名
    folder_path = os.path.dirname(md_file_path)
    md_file_name = os.path.basename(md_file_path)
    
    # 将文件扩展名改为 .pdf
    pdf_file_name = os.path.splitext(md_file_name)[0] + '.pdf'
    pdf_file_path = os.path.join(folder_path, pdf_file_name)

    # 创建一个 MarkdownPdf 实例，设置 TOC 级别为 2
    pdf = MarkdownPdf(toc_level=2)

    # 读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # 添加 Markdown 内容为一个 section，TOC 设置为 True
    pdf.add_section(Section(md_content))

    # 设置 PDF 文档属性
    pdf.meta["title"] = "Generated PDF from Markdown"
    pdf.meta["author"] = "Your Name"  # 替换为您的名字或其他作者信息

    # 保存 PDF 文件
    pdf.save(pdf_file_path)
    print(f"PDF 文件已保存到: {pdf_file_path}")

if __name__ == "__main__":
    # 示例：指定 Markdown 文件路径
    md_file_path = "/home/vincentzyu/Documents/jmu-course/jmu-jizu/labs/lab1/lab1.md"  # 替换为您的 Markdown 文件路径
    convert_md_to_pdf(md_file_path)
