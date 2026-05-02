import matplotlib.pyplot as plt
import numpy as np

from error import (
    SERIES_B_CONFIG,
    analyze_series_b,
    compare_planck_to_literature,
    fit_planck_constant,
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
    series_b = analyze_series_b()
    planck_fit = fit_planck_constant(series_b)
    comparison = compare_planck_to_literature(planck_fit)

    labels = list(SERIES_B_CONFIG.keys())
    frequencies = planck_fit["frequencies"]
    us = planck_fit["stopping_voltages"]
    us_std = planck_fit["stopping_voltage_std"]

    fig, ax = plt.subplots(figsize=(8, 5))

    for label, frequency, voltage, voltage_std in zip(
        labels,
        frequencies,
        us,
        us_std,
        strict=True,
    ):
        color = series_b["series"][label]["color"]
        ax.errorbar(
            frequency,
            voltage,
            yerr=voltage_std,
            fmt="o",
            color=color,
            markeredgecolor="black",
            markersize=8,
            capsize=4,
            linewidth=1.2,
            label=label,
        )
        ax.annotate(
            label,
            (frequency, voltage),
            xytext=(8, 8),
            textcoords="offset points",
            color=color,
        )

    frequency_range = np.linspace(frequencies.min() * 0.97, frequencies.max() * 1.03, 300)
    fitted_voltage = planck_fit["fit"]["slope"] * frequency_range + planck_fit["fit"]["intercept"]
    ax.plot(
        frequency_range,
        fitted_voltage,
        color="#000000",
        linewidth=1.8,
        label="Weighted linear fit",
    )

    ax.set_xlabel("Light Frequency $f$ (Hz)")
    ax.set_ylabel(r"Stopping Voltage Magnitude $|U_s|$ (V)")
    ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax.legend(frameon=False, loc="upper left")

    plt.savefig("plot_planck.png", dpi=400)


if __name__ == "__main__":
    main()
