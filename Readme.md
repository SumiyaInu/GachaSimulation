# Gacha Simulation Project

## Overview

This project simulates a typical gacha (lottery) system commonly found in mobile games. It models a player drawing from a fixed probability distribution, simulating 1000 players each drawing N times, to analyze outcomes when aiming for a target rarity.

The simulation includes statistical summaries, histograms, and boxplots to help analyze player experience and outcome distribution.

- Rarities: `N`, `R`, `SR`, `UR`
- Probabilities: `0.55`, `0.35`, `0.075`, `0.025`
- Target: `UR`
- Configurable draw count (N) and pity system (default pity is twice the expected value)

---

## File Structure

This project consists of three Python files. You can run different simulations based on your observation target.

### 1. `Gacha_function.py`
Provides four base gacha modes used by the other two files:
- 1000-player × N draws without pity
- 1000-player × N draws with pity
- Until first UR (no pity)
- Until first UR (with pity)

### 2. `Gacha_Simulation_02.py`
Simulates 1000 players drawing N times.
- Calculates: expected URs, mean, max, min, standard deviation, standard error, mode, 95% confidence interval
- Classifies players as "lucky" or "unlucky" using ±2σ bounds
- Reports: skewness, kurtosis
- Outputs: histogram, boxplot, convergence plot up to 14,976 draws based on the Central Limit Theorem
- Includes formula: S√V = S√(p(1-p)/n) < εp (used to determine n ≥ 14,976 under 95% CI, 10% error)
- Exports full draw results per player (`N`, `R`, `SR`, `UR`) to CSV

### 3. `Gacha_Simulation_02_UntilGet.py`
Simulates 1000 players drawing until their first UR and records how many draws it took.
- Calculates: mean, max, min, standard deviation, standard error, mode, 95% confidence interval
- Classifies lucky/unlucky players by ±2σ
- Reports skewness, kurtosis
- Outputs histogram and boxplot
- CSV includes draw sequence and number of draws taken per player

---

## Usage

Place `Gacha_function.py` and either `Gacha_Simulation_02.py` or `Gacha_Simulation_02_UntilGet.py` in the same folder.

After execution:
- Histogram and boxplot help visualize draw results quickly
- CSV files provide full gacha records for deeper analysis using tools like Excel or Python

---

## Requirements

- Python 3.x
- Libraries: `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`

---

## Outputs

- CSV: Per-player draw outcomes
- PNG: Histogram, boxplot, convergence chart
- Summary statistics printed via CLI

---

## Author

This is a personal study project by a self-taught developer exploring Python, statistics, and gacha system modeling. Feedback and suggestions are welcome.

