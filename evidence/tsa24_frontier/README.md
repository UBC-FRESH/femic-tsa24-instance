# TSA24 ε-frontier (2026-10-12)

First harvest–bird frontier on the genuine model (fresh VRI 2025 -> VDYP ->
TIPSY/BTC -> ws3 sections; engine `wbi-birds` v1.0.0 + runner fix).

Scenario definition: maximize `totvol * 0.85` (harvest) subject to per-period
landscape bird floors on periods 2..16 (period 1 is fixed by the initial
inventory and is exempt). Floors are factors of the unconstrained (max-harvest)
baseline bird series. No even-flow ε in this sweep.

| factor | status | harvest (m3) | birds |
|---|---|---|---|
| 1.00 (baseline) | optimal | 41,899,621 | 59,432,388 |
| 1.02 | optimal | 41,713,440 | 60,644,438 |
| 1.05 | optimal | 37,438,217 | 62,415,561 |
| 1.08 | optimal | 23,317,282 | 64,311,348 |
| 1.10 | infeasible | - | - |

Reading: nearly free bird gains to +2%, a knee between +5% and +8% (-10.6% to
-44.4% harvest), and an achievable bird ceiling just past +8% for this
constraint structure. Scenario CSVs in this directory.
