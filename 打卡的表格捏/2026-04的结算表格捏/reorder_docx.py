from docx import Document
from docx.oxml.ns import qn
from datetime import datetime

src = r"软件2312-张喻-集美大学学生校内勤工助学工时记录表（记录表编号：JD02XS00807） (1).docx"

doc = Document(src)
table = doc.tables[0]

rows = table._tbl.findall(qn("w:tr"))

header = rows[:6]
footer = rows[22:]


def get_date(i):
    return datetime.strptime(table.rows[i].cells[1].text.strip(), "%Y-%m-%d")


data_sorted = [rows[i] for i in sorted(range(6, 22), key=get_date)]

for r in rows:
    table._tbl.remove(r)

for r in header + data_sorted + footer:
    table._tbl.append(r)

out = r"软件2312-张喻-排序后.docx"
doc.save(out)
print(f"OK -> {out}")
