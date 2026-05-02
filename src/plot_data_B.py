import matplotlib.pyplot as plt
import numpy as np

from error import (
    analyze_series_b,
    evaluate_line,
)

plt.rcParams.update(
    {
        "text.usetex": False,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "axes.labelsize": 13,
        "axes.labelweight": "bold",
        "font.size": 12,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "--",
        "figure.constrained_layout.use": True,
    }
)


def main() -> None:
    analysis = analyze_series_b()

    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot I-V characteristics for each wavelength
    for label, series in analysis["series"].items():
        voltage = series["voltage"]
        current = series["current"]
        linear_mask = series["linear_mask"]
        floor_mask = series["floor_mask"]
        color = series["color"]

        ax.scatter(
            voltage,
            current,
            s=14,
            color=color,
            alpha=0.35,
            edgecolors="none",
            label=f"{label} data",
        )
        ax.scatter(
            voltage[linear_mask],
            current[linear_mask],
            s=36,
            color=color,
            edgecolors="black",
            linewidths=0.4,
            zorder=4,
        )
        ax.scatter(
            voltage[floor_mask],
            current[floor_mask],
            s=28,
            facecolors="none",
            edgecolors=color,
            linewidths=0.9,
            zorder=4,
        )

        fit_voltage = np.linspace(voltage.min(), voltage.max(), 300)
        ax.plot(
            fit_voltage,
            evaluate_line(series["linear_fit"], fit_voltage),
            color=color,
            linewidth=1.4,
            alpha=0.85,
        )
        ax.plot(
            fit_voltage,
            evaluate_line(series["floor_fit"], fit_voltage),
            color=color,
            linewidth=1.2,
            alpha=0.65,
            linestyle="--",
        )

        stopping_voltage = series["stopping_voltage"]
        stopping_voltage_std = series["stopping_voltage_std"]
        ax.plot(
            stopping_voltage,
            series["intersection_current"],
            "o",
            color=color,
            markersize=8,
            markeredgecolor="black",
            label=rf"{label} ($U_s = {stopping_voltage:.3f} \pm {stopping_voltage_std:.3f}$ V)",
            zorder=5,
        )
        ax.axvline(stopping_voltage, color=color, linestyle=":", alpha=0.35, linewidth=1.0)

    ax.set_xlabel("Anode Voltage $V$ (V)")
    ax.set_ylabel("Photocurrent $I$ (A)")
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylim(-1e-10, 6e-10)
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.3)
    ax.legend(frameon=False, loc="upper left")
    ax.set_title("Current-Voltage Characteristics")

    plt.savefig("plot_b.png", dpi=400)



if __name__ == "__main__":
    main()
