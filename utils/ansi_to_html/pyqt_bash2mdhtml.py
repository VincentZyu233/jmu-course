"""
python pyqt_bash2mdhtml.py
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from ansi2html import Ansi2HTMLConverter
from bs4 import BeautifulSoup


class TerminalToMarkdownHTMLConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Terminal Output to Markdown HTML Converter")
        self.setGeometry(100, 100, 600, 400)

        # 创建布局
        layout = QVBoxLayout()

        # 创建输入框，用于输入终端文本
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("Enter terminal output here...")
        layout.addWidget(self.input_text)

        # 创建按钮，用于触发转换
        self.convert_button = QPushButton("Convert to Markdown HTML", self)
        self.convert_button.clicked.connect(self.convert_to_markdown_html)
        layout.addWidget(self.convert_button)

        # 创建输出框，用于显示转换后的Markdown HTML
        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText("Converted Markdown HTML will appear here...")
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def convert_to_markdown_html(self):
        # 获取输入框中的文本
        input_content = self.input_text.toPlainText()

        # 定义颜色映射，模拟 VS Code 终端颜色
        color_map = {
            '0': '#000000',  # 黑色
            '1': '#d16969',  # 红色
            '2': '#6a9955',  # 绿色
            '3': '#d7ba7d',  # 黄色
            '4': '#569cd6',  # 蓝色
            '5': '#f5978e',  # 品红
            '6': '#4ec9b0',  # 青色
            '7': '#d4d4d4',  # 白色
        }

        # 使用ansi2html将ANSI转义字符转换为HTML
        converter = Ansi2HTMLConverter()
        html_content = converter.convert(input_content)

        # 使用BeautifulSoup清理HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 提取所有的 <span> 标签并替换颜色样式
        for span in soup.find_all('span'):
            class_name = span.get('class', [])
            if class_name:
                color_code = class_name[0].replace('ansi', '')
                color = color_map.get(color_code, '#FFFFFF')  # 默认颜色为白色
                span['style'] = f'color: {color};'

        # 生成Markdown格式的HTML：保持纯文本形式，只是转换为HTML
        markdown_html = f"```html\n{str(soup.pre)}\n```"

        # 显示转换后的Markdown HTML
        self.output_text.setText(markdown_html)


# 创建应用并运行
app = QApplication(sys.argv)
window = TerminalToMarkdownHTMLConverter()
window.show()
sys.exit(app.exec_())
