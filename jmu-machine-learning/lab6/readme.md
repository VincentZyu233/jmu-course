## test env
```shell
uv venv --python 3.10
# .\.venv\Scripts\activate
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
uv pip install pyqt6 matplotlib pandas numpy
uv run python -c "import torch; print('cuda:', torch.cuda.is_available()); print('device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu')"

cd lab6
uv run python .\exp1\00_env_check.py
uv run python .\exp1\01...
```