"""
uv pip install python-docx
uv run python docx2md.py "团队激励与沟通课堂报告要求2026.docx" 团队激励与沟通课堂报告要求2026
"""

import sys
import re
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

STYLE_TO_HEADING = {"2": 1, "3": 2, "5": 3, "6": 4, "7": 5, "8": 6}


def extract_images(docx_path, img_dir):
    img_dir.mkdir(parents=True, exist_ok=True)
    rels_map = {}
    with ZipFile(docx_path) as z:
        for name in z.namelist():
            if name == "word/_rels/document.xml.rels":
                tree = ET.parse(z.open(name))
                for el in tree.getroot():
                    rid = el.get("Id")
                    target = el.get("Target")
                    if rid and target and "image" in (el.get("Type", "") or "").lower():
                        rels_map[rid] = target
        for rid, target in rels_map.items():
            src = f"word/{target}"
            dest = img_dir / Path(target).name
            if src in z.namelist():
                with z.open(src) as f, open(dest, "wb") as out:
                    out.write(f.read())
    return rels_map


def run_to_md(run):
    text = run.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if not text:
        return ""
    if run.bold and run.italic:
        return f"***{text}***"
    if run.bold:
        return f"**{text}**"
    if run.italic:
        return f"*{text}*"
    return text


def collect_images_in_para(para, rels_map, img_dir):
    lines = []
    for blip in para._element.iter(f"{{{A_NS}}}blip"):
        embed = blip.get(f"{{{R_NS}}}embed")
        if embed in rels_map:
            fname = Path(rels_map[embed]).name
            rel_path = f"images/{fname}"
            lines.append(f"![{fname}]({rel_path})")
    return lines


def para_to_md(para, rels_map, img_dir):
    out = []

    img_lines = collect_images_in_para(para, rels_map, img_dir)
    out.extend(img_lines)

    style_id = para.style.style_id if para.style else ""
    heading_level = STYLE_TO_HEADING.get(style_id)

    if heading_level:
        text = "".join(run_to_md(r) for r in para.runs).strip()
        if text:
            out.append(f"{'#' * heading_level} {text}")
        return out

    if style_id == "15":
        text = "".join(run_to_md(r) for r in para.runs).strip()
        if text:
            out.append(f"- {text}")
        return out

    is_center = para.alignment == WD_ALIGN_PARAGRAPH.CENTER
    is_list = style_id == "25"

    text = "".join(run_to_md(r) for r in para.runs).strip()
    if not text:
        return out

    if is_list:
        out.append(f"- {text}")
    elif is_center:
        out.append(f'<div align="center">{text}</div>')
    else:
        out.append(text)

    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python docx2md.py <path_to_docx> [output_dir]")
        sys.exit(1)

    docx_path = Path(sys.argv[1])
    if not docx_path.exists():
        print(f"Error: file not found: {docx_path}")
        sys.exit(1)

    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else docx_path.parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    img_dir = output_dir / "images"
    rels_map = extract_images(docx_path, img_dir)

    doc = Document(str(docx_path))
    lines = []
    for para in doc.paragraphs:
        md_line = para_to_md(para, rels_map, img_dir)
        if md_line:
            lines.extend(md_line)
            lines.append("")

    md_content = "\n".join(lines).strip() + "\n"
    md_path = output_dir / (docx_path.stem + ".md")
    md_path.write_text(md_content, encoding="utf-8")
    print(f"Done: {md_path}")


if __name__ == "__main__":
    main()
