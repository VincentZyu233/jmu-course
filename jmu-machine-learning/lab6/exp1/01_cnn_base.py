from __future__ import annotations

from common import run_experiment, save_csv


def main() -> None:
    result = run_experiment("01_cnn_base", epochs=3, batch_size=128, lr=1e-3, kernel_size=3)
    path = save_csv([result], "01_cnn_base_metrics.csv")
    print(path)
    print(result)


if __name__ == "__main__":
    main()
