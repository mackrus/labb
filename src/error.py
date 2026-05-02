from __future__ import annotations

from itertools import combinations
from pathlib import Path

import numpy as np

SPEED_OF_LIGHT = 299_792_458.0
ELEMENTARY_CHARGE = 1.602_176_634e-19
PLANCK_CONSTANT_REFERENCE = 6.626_070_15e-34
BASE_DIR = Path(__file__).resolve().parent

SERIES_A_CONFIG = {
    "2 mm": {"voltage_col": 4, "current_col": 5, "color": "#E69F00"},
    "4 mm": {"voltage_col": 1, "current_col": 2, "color": "#56B4E9"},
    "8 mm": {"voltage_col": 7, "current_col": 8, "color": "#009E73"},
}

SERIES_B_CONFIG = {
    "365 nm": {
        "voltage_col": 7,
        "current_col": 8,
        "color": "#0072B2",
        "wavelength_m": 365e-9,
    },
    "405 nm": {
        "voltage_col": 1,
        "current_col": 2,
        "color": "#D55E00",
        "wavelength_m": 405e-9,
    },
    "546 nm": {
        "voltage_col": 4,
        "current_col": 5,
        "color": "#CC79A7",
        "wavelength_m": 546e-9,
    },
}


def load_data(path: str | Path) -> np.ndarray:
    resolved_path = _resolve_path(path)
    with resolved_path.open("r", encoding="utf-8") as handle:
        processed_data = (line.replace(",", ".") for line in handle)
        return np.genfromtxt(
            processed_data,
            delimiter=";",
            skip_header=1,
            filling_values=np.nan,
        )


def analyze_series_a(path: str | Path = "A.csv") -> dict:
    data = load_data(path)
    series = {}

    for label, config in SERIES_A_CONFIG.items():
        voltage, current = _prepare_series(
            data,
            config["voltage_col"],
            config["current_col"],
        )
        linear_mask = _select_series_a_linear_region(current)
        fit = _fit_line(voltage[linear_mask], current[linear_mask])
        x_intercept, x_intercept_std = _line_x_intercept(fit)

        series[label] = {
            "label": label,
            "color": config["color"],
            "voltage": voltage,
            "current": current,
            "linear_mask": linear_mask,
            "fit": fit,
            "slope": fit["slope"],
            "slope_std": fit["slope_std"],
            "x_intercept": x_intercept,
            "x_intercept_std": x_intercept_std,
        }

    intersections = []
    for label_a, label_b in combinations(series, 2):
        intersection = _intersect_lines(series[label_a]["fit"], series[label_b]["fit"])
        intersections.append(
            {
                "pair": (label_a, label_b),
                "pair_label": f"{label_a} vs {label_b}",
                **intersection,
            }
        )

    shared_voltages = np.array([item["voltage"] for item in intersections], dtype=float)
    shared_currents = np.array([item["current"] for item in intersections], dtype=float)
    shared_us = float(np.mean(shared_voltages))
    shared_us_std = (
        float(np.std(shared_voltages, ddof=1)) if len(shared_voltages) > 1 else 0.0
    )

    return {
        "series": series,
        "intersections": intersections,
        "shared_stopping_voltage": shared_us,
        "shared_stopping_voltage_std": shared_us_std,
        "shared_intersection_current": float(np.mean(shared_currents)),
    }


def analyze_series_b(path: str | Path = "B.csv") -> dict:
    data = load_data(path)
    series = {}

    for label, config in SERIES_B_CONFIG.items():
        voltage, current = _prepare_series(
            data,
            config["voltage_col"],
            config["current_col"],
        )
        linear_mask = _select_fractional_band(current, low=0.2, high=0.7)
        floor_mask = _select_floor_region(current, threshold=0.05)

        if int(np.sum(linear_mask)) < 3:
            raise ValueError(f"{label}: not enough points in the rising linear region")
        if int(np.sum(floor_mask)) < 3:
            raise ValueError(f"{label}: not enough points in the floor region")

        linear_fit = _fit_line(voltage[linear_mask], current[linear_mask])
        floor_fit = _fit_line(voltage[floor_mask], current[floor_mask])
        intersection = _intersect_lines(linear_fit, floor_fit)
        samples = _sample_series_b_stopping_voltages(voltage, current)
        sample_voltages = np.array([item["voltage"] for item in samples], dtype=float)
        sample_uncertainty = (
            float(np.std(sample_voltages, ddof=1)) if len(sample_voltages) > 1 else 0.0
        )
        combined_uncertainty = float(
            np.sqrt(intersection["voltage_std"] ** 2 + sample_uncertainty**2)
        )

        series[label] = {
            "label": label,
            "color": config["color"],
            "wavelength_m": config["wavelength_m"],
            "voltage": voltage,
            "current": current,
            "linear_mask": linear_mask,
            "floor_mask": floor_mask,
            "linear_fit": linear_fit,
            "floor_fit": floor_fit,
            "stopping_voltage": intersection["voltage"],
            "stopping_voltage_std": combined_uncertainty,
            "stopping_voltage_fit_std": intersection["voltage_std"],
            "stopping_voltage_window_std": sample_uncertainty,
            "intersection_current": intersection["current"],
            "absolute_stopping_voltage": abs(intersection["voltage"]),
            "stopping_voltage_samples": sample_voltages,
        }

    return {"series": series}


def fit_planck_constant(series_b_analysis: dict) -> dict:
    labels = list(SERIES_B_CONFIG.keys())
    frequencies = np.array(
        [
            SPEED_OF_LIGHT / series_b_analysis["series"][label]["wavelength_m"]
            for label in labels
        ],
        dtype=float,
    )
    stopping_voltages = np.array(
        [
            series_b_analysis["series"][label]["absolute_stopping_voltage"]
            for label in labels
        ],
        dtype=float,
    )
    stopping_voltage_std = np.array(
        [
            max(series_b_analysis["series"][label]["stopping_voltage_std"], 1e-15)
            for label in labels
        ],
        dtype=float,
    )

    fit = _fit_line(frequencies, stopping_voltages, sigma=stopping_voltage_std)

    fitted_voltage = evaluate_line(fit, frequencies)
    ss_res = float(np.sum((stopping_voltages - fitted_voltage) ** 2))
    ss_tot = float(np.sum((stopping_voltages - np.mean(stopping_voltages)) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    planck_constant = ELEMENTARY_CHARGE * fit["slope"]
    planck_constant_std = ELEMENTARY_CHARGE * fit["slope_std"]
    work_function = -ELEMENTARY_CHARGE * fit["intercept"]
    work_function_std = ELEMENTARY_CHARGE * fit["intercept_std"]
    work_function_ev = -fit["intercept"]
    work_function_ev_std = fit["intercept_std"]

    return {
        "frequencies": frequencies,
        "stopping_voltages": stopping_voltages,
        "stopping_voltage_std": stopping_voltage_std,
        "fit": fit,
        "fitted_stopping_voltages": fitted_voltage,
        "planck_constant": planck_constant,
        "planck_constant_std": planck_constant_std,
        "work_function": work_function,
        "work_function_std": work_function_std,
        "work_function_ev": work_function_ev,
        "work_function_ev_std": work_function_ev_std,
        "r_squared": r_squared,
    }


def compare_planck_to_literature(planck_fit: dict) -> dict:
    measured = planck_fit["planck_constant"]
    measured_std = planck_fit["planck_constant_std"]
    difference = measured - PLANCK_CONSTANT_REFERENCE
    signed_relative_difference = difference / PLANCK_CONSTANT_REFERENCE
    relative_deviation = abs(difference) / PLANCK_CONSTANT_REFERENCE
    sigma_difference = np.inf if measured_std == 0 else abs(difference) / measured_std

    return {
        "reference": PLANCK_CONSTANT_REFERENCE,
        "difference": difference,
        "signed_relative_difference": signed_relative_difference,
        "relative_deviation": relative_deviation,
        "sigma_difference": float(sigma_difference),
    }


def evaluate_line(fit: dict, x: np.ndarray | float) -> np.ndarray | float:
    return fit["slope"] * x + fit["intercept"]


def _sample_series_b_stopping_voltages(
    voltage: np.ndarray,
    current: np.ndarray,
) -> list[dict]:
    linear_ranges = [(0.15, 0.65), (0.20, 0.70), (0.25, 0.75)]
    floor_thresholds = [0.03, 0.05, 0.08]
    samples = []

    for low, high in linear_ranges:
        linear_mask = _select_fractional_band(current, low=low, high=high)
        if int(np.sum(linear_mask)) < 3:
            continue
        for threshold in floor_thresholds:
            floor_mask = _select_floor_region(current, threshold=threshold)
            if int(np.sum(floor_mask)) < 3:
                continue
            linear_fit = _fit_line(voltage[linear_mask], current[linear_mask])
            floor_fit = _fit_line(voltage[floor_mask], current[floor_mask])
            samples.append(_intersect_lines(linear_fit, floor_fit))

    if not samples:
        raise ValueError("No valid stopping-voltage samples could be generated")
    return samples


def main() -> None:
    series_a = analyze_series_a()
    series_b = analyze_series_b()
    planck_fit = fit_planck_constant(series_b)
    comparison = compare_planck_to_literature(planck_fit)

    print("Series A")
    print(
        "  shared Us = "
        f"{series_a['shared_stopping_voltage']:.3f} +/- "
        f"{series_a['shared_stopping_voltage_std']:.3f} V"
    )
    for label in SERIES_A_CONFIG:
        result = series_a["series"][label]
        print(
            f"  {label}: "
            f"Us = {result['x_intercept']:.3f} +/- {result['x_intercept_std']:.3f} V, "
            f"slope = {result['slope']:.3e} +/- {result['slope_std']:.3e} A/V"
        )
    for intersection in series_a["intersections"]:
        print(
            f"  {intersection['pair_label']}: "
            f"{intersection['voltage']:.3f} +/- {intersection['voltage_std']:.3f} V"
        )

    print("\nSeries B")
    for label in SERIES_B_CONFIG:
        result = series_b["series"][label]
        print(
            f"  {label}: "
            f"{result['stopping_voltage']:.3f} +/- {result['stopping_voltage_std']:.3f} V"
        )

    print("\nPlanck fit")
    print(
        "  h = "
        f"{planck_fit['planck_constant']:.3e} +/- "
        f"{planck_fit['planck_constant_std']:.3e} J s"
    )
    print(f"  h_literature = {comparison['reference']:.3e} J s")
    print(f"  Delta h = {comparison['difference']:.3e} J s")
    print(f"  Relative deviation = {comparison['relative_deviation'] * 100:.1f} %")
    print(f"  Discrepancy = {comparison['sigma_difference']:.2f} sigma")
    print(
        "  W0 = "
        f"{planck_fit['work_function']:.3e} +/- "
        f"{planck_fit['work_function_std']:.3e} J"
    )
    print(
        "  W0 = "
        f"{planck_fit['work_function_ev']:.3f} +/- "
        f"{planck_fit['work_function_ev_std']:.3f} eV"
    )
    print(f"  R^2 = {planck_fit['r_squared']:.4f}")


def _resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return BASE_DIR / candidate


def _prepare_series(
    data: np.ndarray, voltage_col: int, current_col: int
) -> tuple[np.ndarray, np.ndarray]:
    voltage = data[:, voltage_col]
    current = data[:, current_col]
    valid_mask = ~np.isnan(voltage) & ~np.isnan(current)
    voltage = voltage[valid_mask]
    current = current[valid_mask]
    order = np.argsort(voltage)
    return voltage[order], current[order]


def _current_range(current: np.ndarray) -> tuple[float, float]:
    current_min = float(np.nanmin(current))
    current_max = float(np.nanmax(current))
    current_span = current_max - current_min
    if current_span <= 0:
        raise ValueError("Current range must be positive for region selection")
    return current_min, current_span


def _select_fractional_band(current: np.ndarray, low: float, high: float) -> np.ndarray:
    current_min, current_span = _current_range(current)
    return (current > current_min + low * current_span) & (
        current < current_min + high * current_span
    )


def _select_floor_region(current: np.ndarray, threshold: float) -> np.ndarray:
    current_min, current_span = _current_range(current)
    return current < current_min + threshold * current_span


def _select_series_a_linear_region(
    current: np.ndarray,
    threshold_low: float = 0.01,
    threshold_high: float = 0.15,
) -> np.ndarray:
    mask = _select_fractional_band(current, threshold_low, threshold_high)
    if int(np.sum(mask)) >= 3:
        return mask

    current_min, current_span = _current_range(current)
    rising_indices = np.where(current > current_min + threshold_low * current_span)[0]
    if len(rising_indices) < 2:
        raise ValueError("Series A: not enough points to define a linear rise")

    fallback_mask = np.zeros_like(current, dtype=bool)
    fallback_mask[rising_indices[: min(3, len(rising_indices))]] = True
    return fallback_mask


def _fit_line(x: np.ndarray, y: np.ndarray, sigma: np.ndarray | None = None) -> dict:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size < 2:
        raise ValueError("At least two points are required for a line fit")

    x_offset = float(np.mean(x))
    centered_x = x - x_offset
    design = np.column_stack((centered_x, np.ones_like(centered_x)))
    if sigma is not None:
        sigma = np.asarray(sigma, dtype=float)
        if sigma.shape != x.shape:
            raise ValueError("sigma must match the fitted data shape")
        weights = 1.0 / np.square(sigma)
        weighted_design = design * np.sqrt(weights)[:, None]
        weighted_y = y * np.sqrt(weights)
        coefficients, _, _, _ = np.linalg.lstsq(weighted_design, weighted_y, rcond=None)
        information = weighted_design.T @ weighted_design
        residuals = y - design @ coefficients
        dof = x.size - 2
        if dof > 0:
            chi_squared = float(np.sum(np.square(residuals / sigma)))
            covariance = (chi_squared / dof) * np.linalg.inv(information)
        else:
            covariance = np.zeros((2, 2), dtype=float)
    else:
        coefficients, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
        information = design.T @ design
        residuals = y - design @ coefficients
        dof = x.size - 2
        if dof > 0:
            residual_variance = float(np.sum(np.square(residuals)) / dof)
            covariance = residual_variance * np.linalg.inv(information)
        else:
            covariance = np.zeros((2, 2), dtype=float)

    transform = np.array([[1.0, 0.0], [-x_offset, 1.0]], dtype=float)
    slope = float(coefficients[0])
    intercept = float(coefficients[1] - slope * x_offset)
    covariance = transform @ covariance @ transform.T
    slope_std, intercept_std = np.sqrt(
        np.clip(np.diag(covariance), a_min=0.0, a_max=None)
    )
    return {
        "slope": slope,
        "intercept": intercept,
        "covariance": covariance,
        "slope_std": float(slope_std),
        "intercept_std": float(intercept_std),
    }


def _line_x_intercept(fit: dict) -> tuple[float, float]:
    slope = fit["slope"]
    intercept = fit["intercept"]
    if abs(slope) < 1e-18:
        raise ValueError("Cannot determine x-intercept for a zero-slope line")

    x_intercept = -intercept / slope
    jacobian = np.array([intercept / (slope**2), -1.0 / slope], dtype=float)
    variance = float(jacobian @ fit["covariance"] @ jacobian.T)
    return float(x_intercept), float(np.sqrt(max(variance, 0.0)))


def _intersect_lines(line_a: dict, line_b: dict) -> dict:
    slope_a = line_a["slope"]
    intercept_a = line_a["intercept"]
    slope_b = line_b["slope"]
    intercept_b = line_b["intercept"]
    denominator = slope_a - slope_b
    if abs(denominator) < 1e-18:
        raise ValueError("Cannot intersect nearly parallel lines")

    voltage = (intercept_b - intercept_a) / denominator
    current = evaluate_line(line_a, voltage)

    jacobian = np.array(
        [
            -(intercept_b - intercept_a) / (denominator**2),
            -1.0 / denominator,
            (intercept_b - intercept_a) / (denominator**2),
            1.0 / denominator,
        ],
        dtype=float,
    )
    covariance = np.zeros((4, 4), dtype=float)
    covariance[:2, :2] = line_a["covariance"]
    covariance[2:, 2:] = line_b["covariance"]
    variance = float(jacobian @ covariance @ jacobian.T)

    return {
        "voltage": float(voltage),
        "current": float(current),
        "voltage_std": float(np.sqrt(max(variance, 0.0))),
    }


if __name__ == "__main__":
    main()
