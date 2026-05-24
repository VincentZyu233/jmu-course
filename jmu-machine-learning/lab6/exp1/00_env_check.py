"""

"""

from __future__ import annotations

import platform
import re

import torch


RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}"


def box(lines: list[str]) -> str:
    width = max(len(ANSI_RE.sub("", line)) for line in lines)
    top = f"┌{'─' * (width + 2)}┐"
    mid = [f"│ {line}{' ' * (width - len(ANSI_RE.sub('', line)))} │" for line in lines]
    bottom = f"└{'─' * (width + 2)}┘"
    return "\n".join([top, *mid, bottom])


def main() -> None:
    title = color("实验六 · 环境检查", BOLD + MAGENTA)
    print(box([title, "MNIST / PyTorch / CUDA"]))

    print(color("🐍 Python", CYAN), platform.python_version())
    print(color("🔥 Torch", CYAN), torch.__version__)
    print(color("🧠 CUDA", CYAN), torch.version.cuda)

    if torch.cuda.is_available():
        print(color("✅ GPU 可用", GREEN), torch.cuda.get_device_name(0))
        x = torch.randn(1024, 1024, device="cuda")
        y = x @ x
        torch.cuda.synchronize()
        print(color("🚀 GPU 测试通过", GREEN), tuple(y.shape))
    else:
        x = torch.randn(1024, 1024)
        y = x @ x
        print(color("⚠️ 仅 CPU 模式", YELLOW), tuple(y.shape))


if __name__ == "__main__":
    main()
