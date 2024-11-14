import os
import subprocess

# 获取当前脚本的路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 图标的相对路径
icon_relative_path = "ps_logo.png"

# 拼接成绝对路径
icon_absolute_path = os.path.join(current_dir, icon_relative_path)

# 构造注册表内容
reg_content = f'''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\OpenPowerShellHere]
@="Open PowerShell Here qwq"
"Icon"="{icon_absolute_path}"

[HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\OpenPowerShellHere\\command]
@="powershell.exe -noexit -command Set-Location -literalPath \\"%V\\""
'''

# 输出到内存中的字符串
print(reg_content)

# 触发 regedit（可以使用 subprocess 来执行）
# 使用 regedit /s 来静默导入注册表
subprocess.run(['regedit', '/s', reg_content])
