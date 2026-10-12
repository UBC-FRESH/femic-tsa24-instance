# Campaign sensitivity (2026-10-12): even-flow epsilon and utilization

Runs on the locked campaign configuration (THLB-filtered landbase, 200-year
horizon x 10-year periods, epsilon = 0.10 baseline, regeneration age 0).

## 1. Even-flow epsilon (matched bird targets)

Scenario CSVs: `tsa<XX>-eps0.05-f{100,102,105}.csv` and
`tsa<XX>-eps0.15-f{100,102,105}.csv`. Bird floors are ABSOLUTE values derived
from the epsilon=0.10 baseline series (factors 1.02 and 1.05), so targets are
matched across epsilon settings.

Baselines (no bird floors; maximize `totvol * 0.85`):

| TSA | eps=0.05 | eps=0.10 | eps=0.15 | no even-flow |
|---|---|---|---|---|
| 24 | 1,432,262,037 | 1,443,341,327 | 1,452,511,638 | 1,909,049,820 |
| 16 | 478,866,213 | 482,512,616 | 485,977,017 | 644,005,889 |
| 08 | 590,733,115 | 596,831,254 | 602,637,488 | 814,472,788 |
| 40 | 431,387,820 | 434,793,181 | 437,999,468 | 570,784,060 |
| 41 | 288,739,849 | 291,035,361 | 293,171,269 | 382,868,669 |

The no-even-flow column is the epsilon=None runs normalized to util=1 (from the utilization runs below). Basis: these volumes are at utilization 1.0, whereas the epsilon columns are reported at 0.85. The matched-utilization even-flow cost (epsilon=0.10 versus no even-flow, both at utilization 0.85) is 10.4% (TSA40) to 13.8% (TSA08). An earlier headline of -24..-25% compared 0.85-utilization volumes with utilization-1.0 volumes; it mixes two accounting factors, is retracted, and is not a cost estimate. The epsilon level itself moves the baseline by about 1.5% over 0.05-0.15.

At the 1.05 bird floor (birds matched; harvest):

| TSA | eps=0.05 | eps=0.10 | eps=0.15 |
|---|---|---|---|
| 24 | 1,083,437,143 | 1,174,236,146 | 1,265,286,139 |
| 16 | 370,697,562 | 401,764,403 | 424,183,463 |
| 08 | 590,377,565 | 596,731,877 | 602,470,249 |
| 40 | 430,621,366 | 433,966,054 | 436,837,709 |
| 41 | 288,510,340 | 290,763,969 | 292,699,765 |

The two-regime frontier pattern (TSA24/16 constrained vs TSA08/40/41 cheap
gains) is robust across the epsilon range.

## 2. Utilization (accounting invariance)

Scenario CSVs: `tsa<XX>-util0.8-f{100,105}.csv`, `tsa<XX>-util0.9-f{100,105}.csv`
(epsilon=None for these runs). At fixed epsilon the optimal schedule is
invariant to the utilization factor (linear objective scaling): bird abundance
is identical between the 0.80 and 0.90 runs and harvest is exactly in the
0.8/0.9 ratio. Utilization is therefore an accounting factor for merchantable
volume, not a decision lever; report volumes with the factor stated.
