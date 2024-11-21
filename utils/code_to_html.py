from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import TextLexer  # 使用 TextLexer 来解析任意文本

code = "\033[32mHello\033[0m, \033[34mWorld\033[0m"
formatter = HtmlFormatter(style='monokai')  # 选择一个你喜欢的样式
html_code = highlight(code, TextLexer(), formatter)  # 使用 TextLexer 来解析

with open('output.html', 'w') as f:
    f.write(html_code)
