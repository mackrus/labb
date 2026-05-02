# The Photoelectric Effect (Lab #3)

This project contains the data analysis and report for Lab #3 in the Quantum Physics course (1FA521). The primary goal is to experimentally determine **Planck's constant ($h$)** and the **work function ($W_0$)** of a material using the photoelectric effect.

## Overview

The photoelectric effect demonstrates the quantization of light energy. By measuring the stopping voltage ($U_s$) for different frequencies of incident light, we can verify the relationship:

$$e U_s = h f - W_0$$

Where:
- $e$ is the elementary charge.
- $h$ is Planck's constant.
- $f$ is the frequency of light.
- $W_0$ is the work function.

This repository includes Python scripts for processing experimental data, performing linear regressions, propagating uncertainties, and generating high-quality plots for the final report.

## Features

- **Automated Data Processing**: Reads and cleans experimental data from CSV files.
- **Curve Fitting**: Uses linear regression to determine stopping voltages from I-V curves.
- **Planck's Constant Estimation**: Performs a weighted fit of stopping voltage vs. frequency.
- **Error Analysis**: Comprehensive uncertainty propagation using covariance matrices.
- **Visualization**: Generates publication-ready plots using Matplotlib.
- **Typst Report**: The full lab report is included as a Typst source file (`main.typ`).

## Project Structure

```text
.
├── src/
│   ├── A.csv                # Data for intensity variation (Aperture series)
│   ├── B.csv                # Data for frequency variation (Wavelength series)
│   ├── main.py              # Main entry point for the analysis
│   ├── error.py             # Core analysis and error propagation logic
│   ├── plot_data_A.py       # Plotting scripts for Series A
│   ├── plot_data_B.py       # Plotting scripts for Series B
│   ├── plot_planck.py       # Planck's constant fit and visualization
│   ├── main.typ             # Typst report source
│   └── references.bib       # BibTeX references for the report
├── pyproject.toml           # Python dependencies and configuration
└── uv.lock                  # UV lockfile
```

## Getting Started

### Prerequisites

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

### Installation

Clone the repository and install the dependencies:

```bash
uv sync
```

### Running the Analysis

To run all data processing scripts and generate the plots:

```bash
uv run src/main.py
```

The plots will be saved in the `src/` directory as PNG files (`plot_a.png`, `plot_b.png`, `plot_planck.png`).

### Building the Report

The report is written in [Typst](https://typst.app/). If you have the Typst CLI installed, you can compile it with:

```bash
typst compile src/main.typ src/main.pdf
```

## Authors

- Filip Petrini
- Markus Bajlo
- Erik Miller
- Simplice Alain Tatanfack

## Course Information

- **Course**: Quantum Physics (1FA521)
- **Institution**: Uppsala University (implied by course code)
- **Lab**: #3
