# Operational projections

`flu_scenario_projections` plots ACCIDDA's public submission to Round 1 of the
2025–26 Flu Scenario Modeling Hub. The source file is
`model-output/ACCIDDA-FlepiMoP/2025-08-10-ACCIDDA-FlepiMoP.gz.parquet` in
[midas-network/flu-scenario-modeling-hub](https://github.com/midas-network/flu-scenario-modeling-hub)
(SHA-256 in `provenance.json`). The team's model metadata
(`model-metadata/ACCIDDA-FlepiMoP.yml`) releases the projections under the MIT
licence. The scenario labels follow the round's scenario table in the hub
README (A-2025-07-29 business-as-usual coverage, B-2025-07-29 low coverage,
C-2025-07-29 no vaccination).

Run from the website repository:

```sh
uv run --python 3.12 assets/img/research/operational/operational_projections.py --from-hub PATH/TO/2025-08-10-ACCIDDA-FlepiMoP.gz.parquet
uv run --python 3.12 assets/img/research/operational/operational_projections.py
uv run --python 3.12 assets/img/research/operational/operational_projections.py --check
```

`--from-hub` reduces the 28 MB submission to the two tables kept here. Both use
the national location (`US`), all ages (`0-130`) and the `inc hosp` target.

| File                                         | Content                                                                                                                                              |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `flu_2025_26_round1_us_weekly_quantiles.csv` | 5th, 25th, 50th, 75th and 95th percentiles of weekly incident hospitalizations across the 600 trajectories, by scenario and weekly horizon (1 to 43) |
| `flu_2025_26_round1_us_season_totals.csv`    | Each trajectory's season total, identified by `run_grouping` and `stochastic_run`                                                                    |

Panel (b) pairs trajectories across scenarios by `run_grouping` and
`stochastic_run`, as the hub's pairing requirement provides, and reports the
difference from the no-vaccination scenario. `--check` verifies the hashes of
the script, tables and exports and recomputes the summaries in
`operational_data.json`.

## Scope statements

- These are one team's scenario projections, conditional on the round's
  assumptions. They are not forecasts, not the hub's multi-model ensemble and
  not an evaluation against observed data.
- The weekly horizon is shown as weeks after the round's origin date
  (10 August 2025) rather than as calendar dates.
