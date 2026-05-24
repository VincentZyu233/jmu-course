from __future__ import annotations

from common import run_experiment, save_csv


def main() -> None:
    rows = [
        run_experiment("kernel_3", epochs=3, batch_size=128, lr=1e-3, kernel_size=3),
        run_experiment("kernel_5", epochs=3, batch_size=128, lr=1e-3, kernel_size=5),
    ]
    path = save_csv(rows, "02_kernel_compare_metrics.csv")
    print(path)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
