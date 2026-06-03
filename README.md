# How Common Are Common Envelopes? Quantifying Their Role in Forming Gravitational-Wave Sources

**Broekgaarden et al. (2026)**

This repository contains all data, code, and figures associated with the paper *"How Common Are Common Envelopes? Quantifying Their Role in Forming Gravitational-Wave Sources"* by Floor S. Broekgaarden, Ana Lam, Sasha Levina, Jakub Klencki, Kyle A. Rocha, Steffani M. Grondin, Monica Gallegos-Garcia, Brian D. Metzger, Angela Twum, Enrico Ramirez-Ruiz, Melanie Santiago, Lieke van Son, Julia Haynes, Tyler B. Smith, Amedeo Romagnolo, Lucas M. de Sá, and Edo Berger.

The paper compiles and systematically compares formation-channel predictions from more than 200 isolated binary-evolution population-synthesis simulations for merging binary black hole (BBH), black hole–neutron star (BHNS), and binary neutron star (BNS) systems. Formation pathways are organized within a unified hierarchical taxonomy that separates systems evolving with and without common-envelope (CE) phases.

---

## Interactive Table & Figures

[![View interactive table](https://img.shields.io/badge/View-Interactive%20Table-blue)](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html)

Open directly: [Formation channel rates — interactive table](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html)

The page includes an interactive data table and the following interactive figures — click any link to jump directly to that section:

| Figure | Description |
|---|---|
| [Fig 2 — All DCOs](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig2) | CE / no-CE fraction summary for all BBH, BHNS, and BNS models on three horizontal lanes (toggle: x = without CE / with CE) |
| [Fig 3/6 — BBH](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig3) | Formation-channel fractions and merger rates for all BBH models (toggle: simple / detailed) |
| [Fig 4/7 — BHNS](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig4) | Formation-channel fractions and merger rates for all BHNS models (toggle: simple / detailed) |
| [Fig 5/8 — BNS](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig5) | Formation-channel fractions and merger rates for all BNS models (toggle: simple / detailed) |
| [Fig 9 — BBH](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig9) | BBH merger rate vs. CE / no-CE fraction, by study |
| [Fig 10 — BHNS](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig10) | BHNS merger rate vs. CE / no-CE fraction, by study |
| [Fig 12 — BBH](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig12) | BBH without-CE fraction as a function of model parameters |
| [Fig 13 — BHNS](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig13) | BHNS without-CE fraction as a function of model parameters |
| [Fig 14/15 — Formation efficiency](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig15) | 4×6 panel: formation-channel fraction vs. metallicity for Iorio, Broekgaarden, van Son, Neijssel — hover to highlight and name a line |

---

## Repository Structure

```
Rates_of_Formation_Channels/
├── papers/                            # PDFs of key source papers
├── plottingCode/                      # Notebooks to reproduce all figures
├── fc_data/                           # Compiled formation-channel data
├── figures/                           # Output PDF figures
└── interactive_figures_and_tables/    # Interactive HTML table and figures
```

### `papers/`

Contains PDF copies of several of the key papers that are sources in this study, including formation-channel results compiled from the literature (e.g., Bavera et al. 2021, Boesky et al. 2024, Briel et al. 2023, Chruślińska et al. 2018, Dorozsmai & Toonen 2024, Hendriks et al. 2023, Li et al. 2025, Olejak et al. 2021, Romagnolo et al. 2023 & 2025, Sgalletta et al. 2025, van Son et al. 2022 & 2023, Xing et al. 2024, and others).

### `plottingCode/`

Contains Jupyter notebooks to reproduce all results and recreate every figure in the paper. Each figure has a standard notebook and an `_interactive` variant that generates the interactive HTML figures hosted online.

| Notebook | Figures |
|---|---|
| `Figure1_schematic_formation_channel_taxonomy/` | Figure 1 — Hierarchical formation-channel taxonomy schematic |
| `Figure_2_formation_channels_contribution_summary.ipynb` | Figure 2 — Global overview of Level 1 formation-channel diversity across all compiled simulations |
| `Figure_2_formation_channels_contribution_summary_interactive.ipynb` | Figure 2 — Interactive version |
| `Figure_3_4_5_6_7_8_and_extra.ipynb` | Figures 3–8 — Level 1 & 2 fractional contributions and intrinsic merger rates for BBH, BHNS, and BNS |
| `Figure_3_4_5_6_7_8_and_extra_interactive.ipynb` | Figures 3–8 — Interactive version |
| `Figure_9_10_11_12_and_13_and_extra.ipynb` | Figures 9–13 — Merger rate vs. formation-channel fraction and parameter-dependence analysis |
| `Figure_14_and_appendix_Formation_Efficiency_formation_channel_contribution.ipynb` | Figures 14/15 + appendix — Formation efficiency and formation-channel contributions as a function of metallicity |
| `Figure_14_and_appendix_Formation_Efficiency_formation_channel_contribution_interactive.ipynb` | Figures 14/15 — Interactive version |

### `fc_data/`

Contains all compiled formation-channel data used in the paper:

- **`Data_formation_channels_intrinsic/`** — Main compiled dataset: CSV files with intrinsic merger rates and formation-channel fractions for BH–BH, BH–NS, and NS–NS systems from all 200+ population-synthesis simulations (`BH-BH_rates_review.csv`, `BH-NS_rates_review.csv`, `NS-NS_rates_review.csv`, and associated `fcRelations` files). Also contains `simulation_specs.csv` with model parameters for all studies.
- **`data_for_formation_efficiency/`** — Data used for the formation efficiency figures (Figures 14/15), including formation-channel fractions as a function of metallicity from Broekgaarden et al. (2022), Iorio et al. simulations, and van Son et al. (2023).
- **`other_data/`** — Additional scripts and data to retrieve or process results from specific studies:
  - `Briel2022/` — Data files for Briel et al. (2022).
  - `Calculate_formation_channels_Boesky/` — Notebook and output CSV files to calculate formation-channel fractions from Boesky et al. (2024) data.

### `figures/`

Contains output PDF figures for all figures in the paper (Figures 2–15 and appendix figures).

### `interactive_figures_and_tables/`

Contains the interactive HTML table (`formation_channel_rates_table.html`) and all interactive figure HTML files. Also accessible online via the link above.

---

## Citation

If you use this repository or the compiled data, please cite:

> Broekgaarden et al. (2026), *"How Common Are Common Envelopes? Quantifying Their Role in Forming Gravitational-Wave Sources"* (paper)

> Broekgaarden et al. (2026), *"How Common Are Common Envelopes? Quantifying Their Role in Forming Gravitational-Wave Sources — Data and Code"* (v3.0), Zenodo. https://zenodo.org/records/20524794

---

## Contact

Floor S. Broekgaarden — fbroekgaarden@ucsd.edu
