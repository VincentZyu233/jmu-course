from ansi2html import Ansi2HTMLConverter

converter = Ansi2HTMLConverter()
code = "\033[32mHello\033[0m, \033[34mWorld\033[0m"
html_code = converter.convert(code)

with open('output.html', 'w') as f:
    f.write(html_code)
