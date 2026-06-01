"""
uv run python clean4word.py 课程报告.md
wsl
apt update && apt install pandoc
pandoc "课程报告-整理过格式的word版本.md" -o "课程报告-整理过格式的word版本.docx"
"""

import sys
import re
from pathlib import Path

IMG_PLACEHOLDER = re.compile(
    r"^>\s*📷\s*\*{1,3}此处插入图(\d+)[：:](.+?)\*{1,3}\s*（.*?）\s*$"
)
IMG_PLACEHOLDER2 = re.compile(r"^>\s*📷\s*\*{1,3}此处插入图(\d+)[：:](.+?)\*{1,3}\s*$")


def clean_line(line):
    m = IMG_PLACEHOLDER.match(line)
    if m:
        return f"**图{m.group(1)}：{m.group(2).strip()}**\n\n"
    m = IMG_PLACEHOLDER2.match(line)
    if m:
        return f"**图{m.group(1)}：{m.group(2).strip()}**\n\n"
    return line


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python clean4word.py <path_to_md>")
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"Error: file not found: {src}")
        sys.exit(1)

    content = src.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    cleaned = []
    for line in lines:
        cleaned.append(clean_line(line))

    dst = src.parent / f"{src.stem}-整理过格式的word版本.md"
    dst.write_text("".join(cleaned), encoding="utf-8")
    print(f"Done: {dst}")


if __name__ == "__main__":
    main()
