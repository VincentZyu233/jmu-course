"""Parallel axis theorem verification — data processing and plotting."""

import math
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. Known data
# ============================================================
I0 = 4.508e-4  # cylinder moment of inertia (kg·m²)
t1_avg = 13.00375  # plastic cylinder 20-period avg time (s)
t2_avg = 18.37714  # cylinder+tube 20-period avg time (s)
t_bar_empty = 19.78  # empty bar 10-period time (s)

positions_cm = [5, 10, 15, 20, 25]
times_s = [22.47, 28.88, 37.72, 46.75, 56.82]

# ============================================================
# 2. Compute torsional constant K
# ============================================================
T1 = t1_avg / 20
T2 = t2_avg / 20
K = 4 * math.pi**2 * I0 / (T2**2 - T1**2)

print("=" * 65)
print("Parallel Axis Theorem — Data Processing Results")
print("=" * 65)
print(f"Cylinder I₀               = {I0:.4e}  kg·m²")
print(f"T₁ = {t1_avg}/20 = {T1:.6f}  s")
print(f"T₂ = {t2_avg}/20 = {T2:.6f}  s")
print(f"Torsional constant K      = {K:.4f}  N·m")

# ============================================================
# 3. Compute empty bar moment of inertia
# ============================================================
T_empty = t_bar_empty / 10
I_bar = K * T_empty**2 / (4 * math.pi**2)
print(f"\nEmpty bar T = {t_bar_empty}/10 = {T_empty:.4f}  s")
print(f"Empty bar I_bar            = {I_bar:.4e}  kg·m²")

# ============================================================
# 4. Compute data for each position
# ============================================================
print(
    f"\n{'x (cm)':>8} {'x² (cm²)':>10} {'t (s)':>8} {'T (s)':>8} "
    f"{'I_total (kg·m²)':>18} {'I_slider (kg·m²)':>18}"
)
print("-" * 80)

x2_list = []
I_slider_list = []

for x, t in zip(positions_cm, times_s):
    T = t / 10
    I_total = K * T**2 / (4 * math.pi**2)
    I_slider = I_total - I_bar
    x2 = x**2

    x2_list.append(x2)
    I_slider_list.append(I_slider)

    print(f"{x:>8} {x2:>10} {t:>8.2f} {T:>8.4f} {I_total:>16.4e} {I_slider:>16.4e}")

# ============================================================
# 5. Linear fit: I_slider = a * x² + b
# ============================================================
coeffs = np.polyfit(x2_list, I_slider_list, 1)
a, b = coeffs
print(f"\nLinear fit: I_slider = {a:.4e} * x² + {b:.4e}")
print(f"Slope a = {a:.4e}")

y_pred = np.polyval(coeffs, x2_list)
ss_res = sum((np.array(I_slider_list) - y_pred) ** 2)
ss_tot = sum((np.array(I_slider_list) - np.mean(I_slider_list)) ** 2)
r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1
print(f"R² = {r2:.6f}")

# ============================================================
# 6. Plot
# ============================================================
x2_fit = np.linspace(0, max(x2_list) * 1.05, 200)
y_fit = np.polyval(coeffs, x2_fit)

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.scatter(x2_list, I_slider_list, color="#2c7bb6", s=80, zorder=5, label="Data points")
ax.plot(
    x2_fit,
    y_fit,
    color="#d7191c",
    linewidth=1.5,
    linestyle="--",
    label=f"Linear fit: y = {a:.2e}x + {b:.2e}\n$R^2 = {r2:.4f}$",
)

ax.set_xlabel("$X^2$ (cm$^2$)", fontsize=13)
ax.set_ylabel("$I_{\\mathrm{slider}}$ (kg$\\cdot$m$^2$)", fontsize=13)
ax.set_title(
    "Parallel Axis Theorem Verification — $I$ vs $X^2$", fontsize=14, fontweight="bold"
)
ax.legend(fontsize=11, loc="upper left")
ax.grid(True, alpha=0.35)
ax.set_xlim(0, max(x2_list) * 1.08)
ax.set_ylim(bottom=0)

plt.tight_layout()
output_png = "lab2-扭摆法测转动惯量/parallel_axis.png"
plt.savefig(output_png, dpi=200)
print(f"\nSaved: {output_png}")
plt.close()
