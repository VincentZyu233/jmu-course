from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None


@dataclass
class TrainResult:
    name: str
    epochs: int
    batch_size: int
    lr: float
    kernel_size: int
    train_acc: float
    test_acc: float
    train_loss: float
    test_loss: float
    seconds: float


class SimpleCNN(nn.Module):
    def __init__(self, kernel_size: int = 3, dropout: float = 0.25):
        super().__init__()
        padding = kernel_size // 2
        self.conv1 = nn.Conv2d(1, 32, kernel_size=kernel_size, padding=padding)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=kernel_size, padding=padding)
        self.pool = nn.MaxPool2d(2)
        self.drop = nn.Dropout(dropout)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = self.drop(F.relu(self.fc1(x)))
        return self.fc2(x)


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def results_root() -> Path:
    out = project_root() / "results"
    out.mkdir(parents=True, exist_ok=True)
    return out


def output_dir() -> Path:
    out = results_root() / "exp1"
    out.mkdir(parents=True, exist_ok=True)
    return out


def data_dir() -> Path:
    path = project_root() / "data" / "mnist"
    path.mkdir(parents=True, exist_ok=True)
    return path


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def make_loaders(batch_size: int = 128, limit_train: int | None = 20000, limit_test: int | None = 5000):
    tfm = transforms.Compose([transforms.ToTensor()])
    train_set = datasets.MNIST(root=data_dir(), train=True, download=True, transform=tfm)
    test_set = datasets.MNIST(root=data_dir(), train=False, download=True, transform=tfm)

    if limit_train is not None:
        train_set = Subset(train_set, list(range(limit_train)))
    if limit_test is not None:
        test_set = Subset(test_set, list(range(limit_test)))

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=torch.cuda.is_available())
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=torch.cuda.is_available())
    return train_loader, test_loader


def iter_loader(loader: DataLoader, desc: str):
    if tqdm is None:
        return loader
    return tqdm(loader, desc=desc, leave=False, ncols=100)


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    *,
    epoch: int,
    epochs: int,
) -> tuple[float, float]:
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    loss_fn = nn.CrossEntropyLoss()

    for x, y in iter_loader(loader, f"train {epoch}/{epochs}"):
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad(set_to_none=True)
        out = model(x)
        loss = loss_fn(out, y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * y.size(0)
        pred = out.argmax(dim=1)
        correct += (pred == y).sum().item()
        total += y.size(0)

    return total_loss / total, correct / total


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, device: torch.device, *, epoch: int, epochs: int) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    loss_fn = nn.CrossEntropyLoss()

    for x, y in iter_loader(loader, f"eval  {epoch}/{epochs}"):
        x, y = x.to(device), y.to(device)
        out = model(x)
        loss = loss_fn(out, y)
        total_loss += loss.item() * y.size(0)
        pred = out.argmax(dim=1)
        correct += (pred == y).sum().item()
        total += y.size(0)

    return total_loss / total, correct / total


def run_experiment(
    name: str,
    *,
    epochs: int = 3,
    batch_size: int = 128,
    lr: float = 1e-3,
    kernel_size: int = 3,
    device: torch.device | None = None,
    limit_train: int | None = 20000,
    limit_test: int | None = 5000,
) -> TrainResult:
    device = device or get_device()
    set_seed(42)
    print(f"[start] experiment={name}")
    print(f"[config] device={device} epochs={epochs} batch_size={batch_size} lr={lr} kernel_size={kernel_size}")
    train_loader, test_loader = make_loaders(batch_size=batch_size, limit_train=limit_train, limit_test=limit_test)
    print(f"[data] train_samples={len(train_loader.dataset)} test_samples={len(test_loader.dataset)}")
    model = SimpleCNN(kernel_size=kernel_size).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    start = perf_counter()
    train_loss = train_acc = test_loss = test_acc = 0.0
    for epoch in range(1, epochs + 1):
        epoch_start = perf_counter()
        train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, device, epoch=epoch, epochs=epochs)
        test_loss, test_acc = evaluate(model, test_loader, device, epoch=epoch, epochs=epochs)
        epoch_seconds = perf_counter() - epoch_start
        print(
            "[epoch] "
            f"{epoch}/{epochs} "
            f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} "
            f"test_loss={test_loss:.4f} test_acc={test_acc:.4f} "
            f"time={epoch_seconds:.2f}s"
        )
    seconds = perf_counter() - start

    save_model(model, name)
    print(f"[done] experiment={name} total_time={seconds:.2f}s")
    return TrainResult(
        name=name,
        epochs=epochs,
        batch_size=batch_size,
        lr=lr,
        kernel_size=kernel_size,
        train_acc=train_acc,
        test_acc=test_acc,
        train_loss=train_loss,
        test_loss=test_loss,
        seconds=seconds,
    )


def save_model(model: nn.Module, name: str) -> Path:
    path = output_dir() / f"{name}.pt"
    torch.save(model.state_dict(), path)
    return path


def save_csv(rows: list[TrainResult], filename: str) -> Path:
    path = output_dir() / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "epochs", "batch_size", "lr", "kernel_size", "train_acc", "test_acc", "train_loss", "test_loss", "seconds"])
        for r in rows:
            writer.writerow([r.name, r.epochs, r.batch_size, r.lr, r.kernel_size, r.train_acc, r.test_acc, r.train_loss, r.test_loss, r.seconds])
    return path
