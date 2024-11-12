##

```bash
python -m venv venv_util
venv_util\Scripts\activate
source venv_util/bin/activate

pip install markdown_pdf
pip freeze > requirements.txt
pip install -r requirements.txt

```

在linux设备上的python版本：
```bash
(venv_util) vincentzyu@Master:~/Documents/jmu-course/utils$ python --version
Python 3.10.12
(venv_util) vincentzyu@Master:~/Documents/jmu-course/utils$ 
```


git
```bash
git fetch
git status

git log origin/main..HEAD  # 查看未推送的提交
git log HEAD..origin/main  # 查看未拉取的提交

git diff origin/main
```

### pandoc
```bash
pandoc input.docx -f docx -t markdown -o output.md
pandoc template.docx -f docx -t markdown -o template.md

```

qwq