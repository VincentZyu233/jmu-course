import re
import os
import sys
import argparse
from datasets import load_dataset

BASE_DIR = (
    r"D:\aaaStuffsaaa\from_git\gitee\jmu-course\jmu-machine-learning\lab1\minecraft"
)

C_RESET = "\033[0m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_CYAN = "\033[96m"
C_PURPLE = "\033[95m"


def parse_hf_url(url):
    match = re.search(r"huggingface\.co/datasets/([^/?#]+/[^/?#]+)", url)
    if not match:
        return None
    return match.group(1)


def download_hf_dataset(subfolder, url, proxy=None):
    if proxy:
        os.environ["HTTP_PROXY"] = proxy
        os.environ["HTTPS_PROXY"] = proxy
        print(f"{C_YELLOW}代理已设置: {proxy}{C_RESET}")

    repo_id = parse_hf_url(url)
    if not repo_id:
        print(f"{C_RED}无效的 Hugging Face 数据集链接！{C_RESET}")
        return False

    target_dir = os.path.join(BASE_DIR, subfolder, "dataset")
    os.makedirs(target_dir, exist_ok=True)

    print(f"\n{C_CYAN}📦 准备下载数据集: {repo_id}{C_RESET}")
    print(f"{C_CYAN}📁 目标目录: {target_dir}{C_RESET}")

    try:
        print(f"\n{C_YELLOW}⏬ 正在下载...{C_RESET}")
        ds = load_dataset(repo_id)
        print(f"{C_GREEN}✅ 下载成功！数据集结构: {ds}{C_RESET}")

        for split in ds.keys():
            split_dir = os.path.join(target_dir, split)
            os.makedirs(split_dir, exist_ok=True)
            output_path = os.path.join(split_dir, "data.jsonl")
            ds[split].to_json(output_path, orient="records", lines=True)
            print(f"{C_GREEN}💾 已保存 {split} → {output_path}{C_RESET}")

        print(f"\n{C_GREEN}🎉 完成！数据集已保存到: {target_dir}{C_RESET}")
        return True

    except Exception as e:
        print(f"{C_RED}💥 下载失败: {e}{C_RESET}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HuggingFace 数据集下载工具")
    parser.add_argument(
        "--proxy", type=str, default="", help="代理地址，如: http://192.168.31.233:7890"
    )
    args = parser.parse_args()

    proxy = args.proxy if args.proxy else None

    print(f"{C_PURPLE}{'=' * 50}{C_RESET}")
    print(f"{C_PURPLE}🔽 HuggingFace 数据集下载工具{C_RESET}")
    print(f"{C_PURPLE}{'=' * 50}{C_RESET}")

    subfolder = input(f"{C_CYAN}请输入子文件夹名称 (如 skin): {C_RESET}").strip()
    url = input(f"{C_CYAN}请输入 HuggingFace 数据集链接: {C_RESET}").strip()

    if subfolder and url:
        download_hf_dataset(subfolder, url, proxy)
    else:
        print(f"{C_RED}输入不能为空！{C_RESET}")
