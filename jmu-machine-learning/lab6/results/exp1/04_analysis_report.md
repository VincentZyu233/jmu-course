# 实验六 exp1 分析报告

## 1. 实验说明
本部分主要完成 MNIST 手写数字分类的基础 CNN 训练，并比较不同卷积核大小和学习率的影响。

## 01_cnn_base_metrics

| name | epochs | batch_size | lr | kernel_size | train_acc | test_acc | train_loss | test_loss | seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 01_cnn_base | 3 | 128 | 0.001000 | 3 | 0.9687 | 0.9716 | 0.1028 | 0.0842 | 5.74 |

## 02_kernel_compare_metrics

| name | epochs | batch_size | lr | kernel_size | train_acc | test_acc | train_loss | test_loss | seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| kernel_3 | 3 | 128 | 0.001000 | 3 | 0.9687 | 0.9716 | 0.1028 | 0.0842 | 5.80 |
| kernel_5 | 3 | 128 | 0.001000 | 5 | 0.9749 | 0.9746 | 0.0803 | 0.0778 | 5.85 |

## 03_lr_compare_metrics

| name | epochs | batch_size | lr | kernel_size | train_acc | test_acc | train_loss | test_loss | seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| lr_1e-3 | 3 | 128 | 0.001000 | 3 | 0.9687 | 0.9716 | 0.1028 | 0.0842 | 5.68 |
| lr_5e-4 | 3 | 128 | 0.000500 | 3 | 0.9561 | 0.9606 | 0.1484 | 0.1217 | 5.46 |

## 2. 结果总结

- 测试准确率最高的是 `kernel_5`，`test_acc = 0.9746`。
- 训练速度最快的是 `lr_5e-4`，耗时 `seconds = 5.46` 秒。
- 从当前结果看，`5x5` 卷积核在这组实验里略优于 `3x3`，但差距不大。
- 学习率过小会让训练变慢，过大可能影响收敛稳定性。
