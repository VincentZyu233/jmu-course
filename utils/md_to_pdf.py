import markdown
import pdfkit
import os

# input_path = "/home/vincentzyu/Documents/jmu-course/jmu-basic/homework/hw1/hw1.md"
input_path = "/home/vincentzyu/Documents/jmu-course/jmu-jizu/labs/lab1/lab1.md"

# 读取 Markdown 文件
with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# 将 Markdown 转为 HTML
html = markdown.markdown(text)

# 设置 wkhtmltopdf 的配置和选项
config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

# 指定输出路径为输入文件所在的文件夹
output_dir = os.path.dirname(input_path)
output_path = os.path.join(output_dir, "output.pdf")

# 设置 PDF 输出选项，指定字体以避免乱码
options = {
    'no-images': '',  # 禁用图片加载
    'disable-smart-shrinking': '',  # 禁用智能缩放
    'encoding': 'utf-8',  # 设置编码
    'page-size': 'A4',  # 设置页面大小为A4
    'margin-top': '10mm',  # 设置上边距
    'margin-right': '10mm',  # 设置右边距
    'margin-bottom': '10mm',  # 设置下边距
    'margin-left': '10mm',  # 设置左边距
}

# 将 HTML 转换为 PDF
pdfkit.from_string(html, output_path, configuration=config, options=options)

print(f"PDF successfully created at: {output_path}")
