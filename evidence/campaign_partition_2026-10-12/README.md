# Campaign partition (2026-10-12): 11 bird scenarios from nadir to maximum

Implements the manuscript's epsilon-constraint design: the bird-abundance range
between the nadir (max-harvest) and maximum (max-bird objective) solutions is
partitioned into 10 evenly-spaced intervals (11 scenarios). Per-period bird
floors interpolate linearly between the two series (periods 2..20; period 1 is
exempt -- it is fixed by the initial inventory, verified identical across
solutions). Even-flow epsilon = 0.1 on harvest (`flow_expr` = `totvol * 0.85`).

## Endpoints

Max-bird solve: objective = bird abundance, subject to the harvest even-flow
row (engine `objective_expr="bird"` + `flow_expr`, `UBC-FRESH/wbi-birds#31`).
Scenario CSVs: `tsa<XX>-bmax.csv` + `tsa<XX>-bmax-series.json`.

| TSA | nadir harvest / birds | max-bird harvest / birds | bird range |
|---|---|---|---|
| 24 | 1,443,341,327 / 50,616,966 | 250,236,228 / 59,822,453 | +18.2% |
| 16 | 482,512,616 / 23,038,597 | 153,309,115 / 25,856,372 | +12.2% |
| 08 | 596,831,254 / 6,745,036 | 528,893,314 / 9,228,827 | +36.8% |
| 40 | 434,793,181 / 8,598,516 | 266,576,430 / 12,731,123 | +48.1% |
| 41 | 291,035,361 / 5,066,902 | 146,074,451 / 8,623,482 | +70.2% |

## Partition scenarios

Scenario CSVs: `tsa<XX>-cbird<0.00..1.00>.csv` (deltas vs the nadir).

| TSA | scenario | harvest (m3) | birds | dHarvest | dBirds |
|---|---|---|---|---|---|
| 24 | cbird0.00 | 1,443,341,327 | 50,616,966 | +0.0% | +0.0% |
| 24 | cbird0.10 | 1,411,794,233 | 51,554,794 | -2.2% | +1.9% |
| 24 | cbird0.20 | 1,349,320,531 | 52,458,063 | -6.5% | +3.6% |
| 24 | cbird0.30 | 1,271,319,685 | 53,378,612 | -11.9% | +5.5% |
| 24 | cbird0.40 | 1,178,861,350 | 54,299,161 | -18.3% | +7.3% |
| 24 | cbird0.50 | 1,072,912,732 | 55,219,710 | -25.7% | +9.1% |
| 24 | cbird0.60 | 958,336,886 | 56,140,258 | -33.6% | +10.9% |
| 24 | cbird0.70 | 833,421,999 | 57,060,807 | -42.3% | +12.7% |
| 24 | cbird0.80 | 695,696,606 | 57,981,356 | -51.8% | +14.5% |
| 24 | cbird0.90 | 526,339,237 | 58,901,905 | -63.5% | +16.4% |
| 24 | cbird1.00 | 250,236,228 | 59,822,453 | -82.7% | +18.2% |
| 16 | cbird0.00 | 482,512,616 | 23,038,597 | +0.0% | +0.0% |
| 16 | cbird0.10 | 477,724,880 | 23,392,048 | -1.0% | +1.5% |
| 16 | cbird0.20 | 463,613,930 | 23,641,745 | -3.9% | +2.6% |
| 16 | cbird0.30 | 447,037,311 | 23,886,418 | -7.4% | +3.7% |
| 16 | cbird0.40 | 427,118,543 | 24,165,707 | -11.5% | +4.9% |
| 16 | cbird0.50 | 403,678,137 | 24,447,485 | -16.3% | +6.1% |
| 16 | cbird0.60 | 376,603,779 | 24,729,262 | -21.9% | +7.3% |
| 16 | cbird0.70 | 344,713,683 | 25,011,040 | -28.6% | +8.6% |
| 16 | cbird0.80 | 304,943,894 | 25,292,817 | -36.8% | +9.8% |
| 16 | cbird0.90 | 255,163,116 | 25,574,595 | -47.1% | +11.0% |
| 16 | cbird1.00 | 153,610,167 | 25,856,348 | -68.2% | +12.2% |
| 08 | cbird0.00 | 596,831,254 | 6,745,036 | +0.0% | +0.0% |
| 08 | cbird0.10 | 596,809,666 | 7,074,021 | -0.0% | +4.9% |
| 08 | cbird0.20 | 596,630,017 | 7,292,234 | -0.0% | +8.1% |
| 08 | cbird0.30 | 596,106,341 | 7,532,476 | -0.1% | +11.7% |
| 08 | cbird0.40 | 594,926,691 | 7,757,143 | -0.3% | +15.0% |
| 08 | cbird0.50 | 593,016,954 | 8,030,442 | -0.6% | +19.1% |
| 08 | cbird0.60 | 589,949,219 | 8,322,667 | -1.2% | +23.4% |
| 08 | cbird0.70 | 584,913,901 | 8,592,901 | -2.0% | +27.4% |
| 08 | cbird0.80 | 574,357,583 | 8,831,185 | -3.8% | +30.9% |
| 08 | cbird0.90 | 558,461,736 | 9,027,182 | -6.4% | +33.8% |
| 08 | cbird1.00 | 528,893,314 | 9,228,827 | -11.4% | +36.8% |
| 40 | cbird0.00 | 434,793,181 | 8,598,516 | +0.0% | +0.0% |
| 40 | cbird0.10 | 433,893,859 | 9,013,811 | -0.2% | +4.8% |
| 40 | cbird0.20 | 432,225,150 | 9,425,038 | -0.6% | +9.6% |
| 40 | cbird0.30 | 429,848,522 | 9,838,298 | -1.1% | +14.4% |
| 40 | cbird0.40 | 426,612,282 | 10,251,559 | -1.9% | +19.2% |
| 40 | cbird0.50 | 422,814,107 | 10,664,820 | -2.8% | +24.0% |
| 40 | cbird0.60 | 417,221,255 | 11,089,281 | -4.0% | +29.0% |
| 40 | cbird0.70 | 405,995,534 | 11,511,397 | -6.6% | +33.9% |
| 40 | cbird0.80 | 386,998,761 | 11,915,557 | -11.0% | +38.6% |
| 40 | cbird0.90 | 361,569,531 | 12,327,020 | -16.8% | +43.4% |
| 40 | cbird1.00 | 266,628,649 | 12,731,110 | -38.7% | +48.1% |
| 41 | cbird0.00 | 291,035,361 | 5,066,902 | +0.0% | +0.0% |
| 41 | cbird0.10 | 290,570,075 | 5,427,720 | -0.2% | +7.1% |
| 41 | cbird0.20 | 289,411,452 | 5,790,628 | -0.6% | +14.3% |
| 41 | cbird0.30 | 287,540,816 | 6,158,450 | -1.2% | +21.5% |
| 41 | cbird0.40 | 284,718,102 | 6,529,813 | -2.2% | +28.9% |
| 41 | cbird0.50 | 278,935,961 | 6,981,465 | -4.2% | +37.8% |
| 41 | cbird0.60 | 266,543,519 | 7,384,367 | -8.4% | +45.7% |
| 41 | cbird0.70 | 249,649,629 | 7,684,853 | -14.2% | +51.7% |
| 41 | cbird0.80 | 229,825,492 | 7,966,251 | -21.0% | +57.2% |
| 41 | cbird0.90 | 204,402,302 | 8,276,644 | -29.8% | +63.3% |
| 41 | cbird1.00 | 146,074,451 | 8,623,482 | -49.8% | +70.2% |

## Notes

- The top scenario (cbird1.00) reproduces the max-bird endpoint when the floors
  bind (TSA24/08/41); for TSA16/40 the exact-max floors sit on the LP
  feasibility boundary, so the top point was solved with a 1e-6 floor
  relaxation (TSA16 153,610,167 / 25,856,348; TSA40 266,628,649 / 12,731,110).
- An earlier variant approximated the maximum by bisection on a flat multiple
  of the nadir series; it underestimates the bird range (e.g. TSA24 +8.2% vs
  +18.2% true). The proxy CSVs are preserved in the run environment only.
- Bird-abundance steps are even by construction (the floors interpolate between
  the two endpoint series); harvest steps steepen with the bird level (convex
  opportunity cost).
