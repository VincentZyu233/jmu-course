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