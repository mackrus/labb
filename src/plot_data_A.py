import matplotlib.pyplot as plt
import numpy as np

from error import analyze_series_a, evaluate_line

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
    analysis = analyze_series_a()
    fig, ax = plt.subplots(figsize=(8, 5))
    intersection_voltages = [item["voltage"] for item in analysis["intersections"]]
    fit_window_min = min(intersection_voltages) - 0.3
    fit_window_max = max(intersection_voltages) + 0.3

    for label, series in analysis["series"].items():
        voltage = series["voltage"]
        current = series["current"]
        linear_mask = series["linear_mask"]
        color = series["color"]

        ax.scatter(
            voltage,
            current,
            s=14,
            color=color,
            alpha=0.30,
            edgecolors="none",
            label=f"Aperture {label}",
        )
        ax.plot(voltage, current, "-", color=color, linewidth=1.0, alpha=0.35)
        ax.scatter(
            voltage[linear_mask],
            current[linear_mask],
            s=36,
            color=color,
            edgecolors="black",
            linewidths=0.4,
            zorder=4,
        )

        fit_voltage = np.linspace(
            min(fit_window_min, float(voltage[linear_mask].min()) - 0.2),
            max(fit_window_max, float(voltage[linear_mask].max()) + 0.2),
            200,
        )
        ax.plot(
            fit_voltage,
            evaluate_line(series["fit"], fit_voltage),
            color=color,
            linewidth=1.4,
            alpha=0.85,
        )

    for index, intersection in enumerate(analysis["intersections"]):
        legend_label = "Pairwise intersections" if index == 0 else "_nolegend_"
        ax.plot(
            intersection["voltage"],
            intersection["current"],
            "o",
            color="black",
            markersize=6,
            label=legend_label,
            zorder=5,
        )

    shared_us = analysis["shared_stopping_voltage"]
    shared_us_std = analysis["shared_stopping_voltage_std"]
    ax.axvline(
        shared_us,
        color="black",
        linestyle=":",
        linewidth=1.2,
        alpha=0.6,
        label=rf"Shared $U_s = {shared_us:.3f} \pm {shared_us_std:.3f}$ V",
    )

    ax.set_xlabel("Anode Voltage $V$ (V)")
    ax.set_ylabel("Photocurrent $I$ (A)")
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.3)
    ax.legend(frameon=False, loc="upper left")

    plt.savefig("plot_a.png", dpi=400)


if __name__ == "__main__":
    main()
