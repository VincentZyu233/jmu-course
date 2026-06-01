## 先patch venv里面的py文件，修改：cache.py 支持 BUZZ_CACHE_DIR 环境变量

**文件**: `.\.venv\Lib\site-packages\buzz\cache.py`

```diff
-    def __init__(self, cache_dir=user_cache_dir("Buzz")):
+    def __init__(self, cache_dir=os.getenv("BUZZ_CACHE_DIR", user_cache_dir("Buzz"))):
```

**作用**: TasksCache 的缓存目录优先读 `BUZZ_CACHE_DIR` 环境变量，未设置时回退默认路径。

## Install From Pypi

```powershell
uv venv --python 3.12
pip install buzz-captions

uv run python -c "import sys; print(sys.executable)"
$env:HF_HOME = "E:\cache\Buzz"; $env:BUZZ_MODEL_ROOT = "E:\cache\Buzz\models"; $env:BUZZ_CACHE_DIR = "E:\cache\Buzz"; uv run python -m buzz

uv run python -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"
uv pip install --force-reinstall torch==2.8.0+cu129 torchaudio==2.8.0+cu129 --index-url https://download.pytorch.org/whl/cu129
uv run python -c "import torch; print('CUDA:', torch.cuda.is_available(), torch.version.cuda, 'GPU:', torch.cuda.get_device_name(0))"

# usage: 
cd D:\aaaStuffsaaa\from_git\gitee\jmu-course\jmu-团队激励与沟通\hw0
# uv run python -m buzz add "视频素材\liwang.mp4" "视频素材\yewenlai.mp4" "视频素材\同学.mp4" -s medium --srt -d "视频素材\buzz-output"
$env:HF_HOME = "E:\cache\Buzz"; $env:BUZZ_MODEL_ROOT = "E:\cache\Buzz\models"; $env:BUZZ_CACHE_DIR = "E:\cache\Buzz"
uv run python -m buzz add "视频素材\同学.mp4" -s medium --srt -d "视频素材\buzz-output"
uv run python -m buzz add "视频素材\liwang.mp4" -s medium --srt -d "视频素材\buzz-output"
uv run python -m buzz add "视频素材\yewenlai.mp4" -s medium --srt -d "视频素材\buzz-output"

uv run python -m buzz add "视频素材\linus-linus-装机.mkv" -s medium --srt -d "视频素材\buzz-output"


```

