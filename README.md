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
| [Fig 3 — BBH](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig3) | Formation-channel fractions and merger rates for all BBH models (toggle: simple / detailed) |
| [Fig 4 — BHNS](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig4) | Formation-channel fractions and merger rates for all BHNS models (toggle: simple / detailed) |
| [Fig 5 — BNS](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig5) | Formation-channel fractions and merger rates for all BNS models (toggle: simple / detailed) |
| [Fig 9 — BBH](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig9) | BBH merger rate vs. CE / no-CE fraction, by study |
| [Fig 10 — BHNS](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig10) | BHNS merger rate vs. CE / no-CE fraction, by study |
| [Fig 12 — BBH](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig12) | BBH without-CE fraction as a function of model parameters |
| [Fig 13 — BHNS](https://floorbroekgaarden.github.io/Rates_of_Formation_Channels/interactive_figures_and_tables/formation_channel_rates_table.html#fig13) | BHNS without-CE fraction as a function of model parameters |

---

## Repository Structure

```
Rates_of_Formation_Channels/
├── papers/                            # PDFs of key source papers
├── plottingCode/                      # Code to reproduce all figures
├── other_data/                        # Additional code to retrieve and process data
└── interactive_figures_and_tables/    # Interactive HTML table
```

### `papers/`

Contains PDF copies of several of the key papers that are sources in this study, including formation-channel results compiled from the literature (e.g., Bavera et al. 2021, Boesky et al. 2024, Briel et al. 2023, Chruślińska et al. 2018, Dorozsmai & Toonen 2024, Hendriks et al. 2023, Li et al. 2025, Olejak et al. 2021, Romagnolo et al. 2023 & 2025, Sgalletta et al. 2025, van Son et al. 2022 & 2023, Xing et al. 2024, and others).

### `plottingCode/`

Contains Jupyter notebooks to reproduce all results and recreate every figure in the paper. Notebooks are organized by figure number:

| Notebook | Figures |
|---|---|
| `Figure1_schematic_files_to_create_plot/` | Figure 1 — Hierarchical formation-channel taxonomy schematic |
| `Figure_2_formation_channels_contribution_summary.ipynb` | Figure 2 — Global overview of Level 1 formation-channel diversity across all compiled simulations |
| `Figure_3_4_5_and_extra.ipynb` | Figures 3–5 — Level 1 fractional contributions and intrinsic merger rates for BBH, BHNS, and BNS |
| `Figure_6_7_8_9_and_10_and_extra.ipynb` | Figures 6–10 — Level 2 subchannel decomposition and parameter-dependency analysis for BBH, BHNS, and BNS |
| `Figure_11_and_appendix_Formation_Efficiency_formation_channel_contribution.ipynb` | Figure 11 + appendix — Formation efficiency and formation-channel contributions |
| `rates_figure_formation_channels.ipynb` | Additional rates figures |

Output figures are saved to `plottingCode/All_Figures/Output_Figures/`.

### `other_data/`

Contains additional code used to retrieve and process data from external sources:

- **`Briel2022/`** — Scripts and data files for extracting formation-channel rates from Briel et al. (2022).
- **`Calculate_formation_channels_Boesky/`** — Notebook (`Calculate_and_Save_Formation_Channels_Boesky24_data.ipynb`) to calculate and save formation-channel fractions from Boesky et al. (2024) data, with output CSV files for BBH, BHNS, and BNS rates by formation channel.

### `interactive_figures_and_tables/`

Contains the interactive HTML table (`formation_channel_rates_table.html`) displaying formation-channel rates and fractions for all compiled simulations, with additional model parameters. Also accessible online via the link above.

---

## Citation

If you use this repository or the compiled data, please cite:

> Broekgaarden et al. (2026), *"How Common Are Common Envelopes? Quantifying Their Role in Forming Gravitational-Wave Sources"* (paper)
> Broekgaraden et al. (2026) 10.5281/zenodo.7815200 *"How Common Are Common Envelopes? Quantifying Their Role in Forming Gravitational-Wave Sources" Data and Code * (data and code) ; see citation at https://zenodo.org/records/7815201 

---

## Contact

Floor S. Broekgaarden — fbroekgaarden@ucsd.edu
