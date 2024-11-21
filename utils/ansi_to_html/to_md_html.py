from bs4 import BeautifulSoup

# 输入HTML字符串
html_code = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title></title>
<style type="text/css">
.ansi2html-content { display: inline; white-space: pre-wrap; word-wrap: break-word; }
.body_foreground { color: #AAAAAA; }
.body_background { background-color: #000000; }
.inv_foreground { color: #000000; }
.inv_background { background-color: #AAAAAA; }
.ansi32 { color: #00aa00; }
.ansi34 { color: #0000aa; }
</style>
</head>
<body class="body_foreground body_background" style="font-size: normal;" >
<pre class="ansi2html-content">
<span class="ansi32">Hello</span>, <span class="ansi34">World</span>
</pre>
</body>
</html>
"""

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_code, 'html.parser')

# 找到所有的<span>标签
spans = soup.find_all('span')

# 定义样式与颜色的映射
color_map = {
    'ansi32': '#00aa00',  # Green
    'ansi34': '#0000aa'   # Blue
}

# 用来存储最终的转换后的HTML
markdown_html = '<pre class="ansi2html-content">'

# 遍历所有<span>标签并替换成合适的HTML
for span in spans:
    class_name = span.get('class', [])
    color = color_map.get(class_name[0], '#FFFFFF')  # 默认颜色为白色
    text = span.get_text()

    # 用一个带颜色的<span>替代原来的<span>
    markdown_html += f'<span style="color: {color};">{text}</span>'

# 关闭<pre>标签
markdown_html += '</pre>'

# 输出转换后的Markdown HTML
print(markdown_html)
