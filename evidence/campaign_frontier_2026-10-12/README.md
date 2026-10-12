# Campaign frontier (2026-10-12): harvest vs bird abundance

Five-TSA bird-floor frontier on the locked campaign configuration: THLB-filtered
landbase (`thlb_raw >= 50`), 200-year horizon x 10-year periods, even-flow
epsilon = 0.1 (symmetric band anchored to the final period), regeneration to
age 0. Scenario: maximize `totvol * 0.85` subject to per-period landscape bird
floors on periods 2..20 (period 1 is fixed by the initial inventory and is
exempt). Floors are factors of each TSA's epsilon=0.1 baseline per-period bird
series.

Scenario CSVs for this instance are in this directory (`tsa<XX>-f100.csv` =
baseline, `f102`... = floor factors). Infeasible factors have no CSV: the floor
exceeds the achievable bird ceiling for that TSA.

## Results (harvest m3 / birds; deltas vs the 1.00 baseline)

| TSA | factor | harvest (m3) | birds | dHarvest | dBirds |
|---|---|---|---|---|---|
| 24 | 1.00 | 1,443,341,327 | 50,616,966 | | |
| 24 | 1.02 | 1,414,914,713 | 51,580,631 | -2.0% | +1.9% |
| 24 | 1.05 | 1,174,236,146 | 53,026,242 | -18.6% | +4.8% |
| 24 | 1.08+ | infeasible | | | |
| 16 | 1.00 | 482,512,616 | 23,038,597 | | |
| 16 | 1.02 | 474,208,019 | 23,517,645 | -1.7% | +2.1% |
| 16 | 1.05 | 401,764,403 | 24,143,923 | -16.7% | +4.8% |
| 16 | 1.08+ | infeasible | | | |
| 08 | 1.00 | 596,831,254 | 6,745,036 | | |
| 08 | 1.02 | 596,831,091 | 6,971,591 | -0.0% | +3.4% |
| 08 | 1.05 | 596,731,877 | 7,136,577 | -0.0% | +5.8% |
| 08 | 1.08 | 595,774,650 | 7,443,931 | -0.2% | +10.4% |
| 08 | 1.10 | 594,155,887 | 7,662,344 | -0.4% | +13.6% |
| 08 | 1.12 | 591,109,533 | 7,850,385 | -1.0% | +16.4% |
| 08 | 1.15 | 578,469,514 | 8,194,856 | -3.1% | +21.5% |
| 40 | 1.00 | 434,793,181 | 8,598,516 | | |
| 40 | 1.02 | 434,632,539 | 8,765,466 | -0.0% | +1.9% |
| 40 | 1.05 | 433,966,054 | 9,015,891 | -0.2% | +4.9% |
| 40 | 1.08 | 432,985,552 | 9,266,315 | -0.4% | +7.8% |
| 40 | 1.10 | 432,125,373 | 9,433,265 | -0.6% | +9.7% |
| 40 | 1.12 | 431,064,975 | 9,616,013 | -0.9% | +11.8% |
| 40 | 1.15 | 428,608,460 | 9,902,528 | -1.4% | +15.2% |
| 41 | 1.00 | 291,035,361 | 5,066,902 | | |
| 41 | 1.02 | 290,973,031 | 5,174,799 | -0.0% | +2.1% |
| 41 | 1.05 | 290,763,969 | 5,330,489 | -0.1% | +5.2% |
| 41 | 1.08 | 290,409,342 | 5,493,663 | -0.2% | +8.4% |
| 41 | 1.10 | 290,108,020 | 5,604,664 | -0.3% | +10.6% |
| 41 | 1.12 | 289,738,265 | 5,715,122 | -0.4% | +12.8% |
| 41 | 1.15 | 288,953,419 | 5,884,595 | -0.7% | +16.1% |

## Reading

Two regimes emerge:

- **TSA24 / TSA16 (north/Peace)**: small bird gains are nearly free (+1.9% /
  +2.1% at 1.02), but the frontier steepens sharply (-17% to -19% harvest at
  +4.8% birds) and hits a hard bird ceiling between +5% and +8%.
- **TSA08 / TSA40 / TSA41 (east/south)**: bird abundance gains of +10% to +22%
  are available for 0.2% to 3% harvest loss, with no ceiling through 1.15.

Landscape context (species composition and age structure) governs whether bird
abundance gains are cheap or tightly constrained by harvest.

Evidence: engine `wbi-birds` v1.0.0 (`run_scenario`, `constraint_floor`), femic
P113.5 campaign sections. Method: `femic/external/femic-tsa24-instance/evidence/p113_5_campaign_config_2026-10-12.md`.
