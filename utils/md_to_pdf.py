"""
python md_to_pdf.py
"""

import markdown
import pdfkit

input_path = "/home/vincentzyu/Documents/jmu-course/jmu-basic/homework/hw1/hw1.md"
with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# 将 Markdown 转为 HTML
html = markdown.markdown(text)

# 设置 wkhtmltopdf 的配置和选项
config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
options = {
    'no-images': '',  # 禁用图片加载
    'disable-smart-shrinking': ''  # 禁用智能缩放
}

# 将 HTML 转换为 PDF
pdfkit.from_string(html, "output.pdf", configuration=config, options=options)
