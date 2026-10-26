# Published-model recomputations

Figures in this directory recompute a result from one of my published papers
using only the model equations and the parameter values that the paper or its
public code repository released. Nothing is copied from a journal figure; the
numerical values belong to the recomputation and may differ in detail from the
published figures (different integrator tolerances, median rather than
per-host parameters, a longer horizon). The NPZD hysteresis figure in the
parent directory follows the same policy.

Run from the website repository:

```sh
uv run --python 3.12 assets/img/research/published/published_models.py
uv run --python 3.12 assets/img/research/published/published_models.py --check
```

`--check` verifies the committed hashes of the script, the three input CSV
files and every export, regenerates into a temporary directory, and compares
the recomputed trajectories and jurisdiction outcomes with the committed data
file. The `Computed figures` workflow runs it when sources or artifacts change.

## Sources

| Input file                             | Content                                                                                                                                                                                                                                                  | Source                                                                                                                                                                | Identity                                                                                                 |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `macdonald2024_amnat_strain_means.csv` | Median of the within-host parameters over the 10 000 Monte Carlo estimates per strain                                                                                                                                                                    | [jc-macdonald/FMDV-Fitting-Bootstrap](https://github.com/jc-macdonald/FMDV-Fitting-Bootstrap), `Output_analysis/FMDVMeansMay9.csv`, reduced to three median rows here | commit `e72c55d`; source file SHA-256 `48573134d0ddf8c499e693a602ccf1d9357682639410ef92ac7ce8df4c4a2003` |
| `macdonald2024_amnat_host_table.csv`   | Per-host within-host parameters with latent period, infectious period, strain transmission rate and R0                                                                                                                                                   | same repository, `Output_analysis/QualCompInd.csv`, copied unchanged                                                                                                  | SHA-256 `33a56533bd45b34195d6002fcce39203d66f3b28e19d08d8bbe8b43998ceea0a`                               |
| `macdonald2021_rsos_table2.csv`        | Table 2 of the paper: R0, lockdown factor psi, fatigue half-life, IFR and I0 for 55 state and territorial jurisdictions plus the national aggregate and summary rows; a `population` column added from the `StatePops` vector in the public fitting code | Macdonald et al. 2021, _R. Soc. Open Sci._ 8:210227, open access (PMC8334836); table extracted from the Europe PMC full-text XML                                      | populations from `USStateFitsSimplest.m`, commit `cfe41e3`                                               |

The model equations are stated in comments beside each function in
`published_models.py` and were read from the public fitting code
(`Finalized_fitting/ContactDataHaptoStimes.m` for the within-host model;
[jc-macdonald/programfilesUSCOVID](https://github.com/jc-macdonald/programfilesUSCOVID)
`USStateFitsSimplest.m`, function `theModel`, commit `cfe41e3`, for the COVID
model) and checked against the papers' methods sections.

## What each figure shows, and its check

| Figure                  | Paper                                                                        | What is recomputed                                                                                                                                                                                                                                                                                                                                                                                                                                   | Check                                                                                                                                                                                                                                                                                                                                             | Limits                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fmdv_within_host`      | Macdonald et al. 2024, _Am. Nat._ 204(2):133–146, doi 10.1086/730703         | (a, b) The within-host model integrated for 30 days at each strain's median parameters. (c) Strain transmission rate against the host median replication rate. (d) Per-host infectious period against adaptive activation rate, from the released host table.                                                                                                                                                                                        | Asserted in the code: in the median-parameter curves SAT1 has the highest and earliest viral peak, SAT2 the lowest, SAT3 the latest; strain transmission rate and host-median replication rate both increase from SAT3 to SAT2 to SAT1; infectious period decreases with activation rate across hosts (Spearman ρ = −0.77 on the released table). | Strain curves use median parameters, not any individual host; the innate baseline for the inflow term is approximated by the strain-median initial innate value. The paper's conclusions about strain differences in immune response rest on per-host fits and data, which these curves illustrate rather than test. Transmission rate was estimated once per strain, so panel (c) has three points. Not fits to data. |
| `covid_lockdown_factor` | Macdonald et al. 2021, _R. Soc. Open Sci._ 8:210227, doi 10.1098/rsos.210227 | The paper's closed forms for final size and peak outbreak size max I/N (eqs. 4.1–4.2, which carry the factor 1/(1+ψ) and hold without fatigue), drawn at the U.S. median R0; the closed form at each of the 55 state and territorial jurisdictions' published R0 and ψ; and the model solved for 400 days from each jurisdiction's published I0 (divided by its population) with its published fatigue rate. The national aggregate row is excluded. | The closed form agrees with the solved model at α = 0 within 0.2% at three ψ values. With fatigue, neither the 400-day cumulative nor the 400-day peak falls below its no-fatigue closed form in any jurisdiction (asserted, 1% tolerance).                                                                                                       | The filled markers are 400-day model outcomes, not the paper's 31 May 2020 estimates and not necessarily final epidemic sizes; with strong fatigue the epidemic continues past 400 days. Reporting, testing and IFR play no role in these two quantities.                                                                                                                                                              |

## Scope statements

- These are recomputations for illustration on a personal website. The papers
  remain the record of the methods, data and results.
- No unpublished data, parameters or results are used. Both source repositories
  are public under the licences stated in their READMEs.
- The FMDV carrier-transmission paper (Atkins et al. 2026, _Bull. Math. Biol._)
  is not yet represented here; a recomputation will be added when its public
  code location is confirmed.
