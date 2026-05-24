from __future__ import annotations

from common import run_experiment, save_csv


def main() -> None:
    rows = [
        run_experiment("lr_1e-3", epochs=3, batch_size=128, lr=1e-3, kernel_size=3),
        run_experiment("lr_5e-4", epochs=3, batch_size=128, lr=5e-4, kernel_size=3),
    ]
    path = save_csv(rows, "03_lr_compare_metrics.csv")
    print(path)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
