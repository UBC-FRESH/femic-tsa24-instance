# Phase 113.5: campaign configuration + five-TSA baselines (2026-10-12)

Campaign spec locked and applied across the five AOI instances
(TSA 08/16/24/40/41). Model built with the `femic` pipeline (fresh VRI 2025 ->
VDYP7 -> TIPSY/BTC -> model-input bundle -> Woodstock exports -> ws3 sections)
and run with the `wbi-birds` engine v1.0.0.

## Locked configuration

- **Horizon**: 200 years, 10-year periods (20 periods; ~2 rotations).
- **Landbase**: THLB-filtered -- stands with mean THLB raster signal
  `thlb_raw >= 50` (`femic export woodstock --thlb-min 50`). Retained stands
  enter at full stand area (the model's existing managed-class semantics; the
  raster share is not used to scale area). Low-THLB and zero-THLB stands are
  dropped from the model.
- **Compression**: initial ages capped at 300 years and snapped to 10-year
  class midpoints; clearcut operability 80-400 years; stands regenerate to age 0
  (`*ACTION cc Y` -> targetage 0), i.e. multi-rotation.
- **Scenario**: maximize `totvol * 0.85` with even-flow epsilon = 0.1
  (symmetric +/-10% band anchored to the final period; ws3 legacy `cflw` tuple
  form). Bird floors are applied per period in the frontier sweep only.

## Landbase and model size after the THLB filter

| TSA | Stands | Landbase (ha) | Unfiltered (ha) | dtypes | curves |
|---|---|---|---|---|---|
| 24 | 277,679 | 3,314,847 | 6,016,498 | 27 | 132 |
| 16 | 117,172 | 1,513,346 | 3,249,151 | 49 | 246 |
| 08 | 112,488 | 1,400,549 | 5,188,145 | 32 | 118 |
| 40 | 115,981 | 1,015,126 | 3,039,129 | 30 | 162 |
| 41 | 41,308 | 731,150 | 2,255,651 | 38 | 217 |

## Five-TSA baselines (even-flow epsilon = 0.1, no bird floors)

| TSA | Status | Harvest (m3) | Birds |
|---|---|---|---|
| 24 | optimal | 1,443,341,327 | 50,616,966 |
| 16 | optimal | 482,512,616 | 23,038,597 |
| 08 | optimal | 596,831,254 | 6,745,036 |
| 40 | optimal | 434,793,181 | 8,598,516 |
| 41 | optimal | 291,035,361 | 5,066,902 |

## ws3 time-unit contract fixes (this phase)

Two section-writer bugs were found by validation and fixed in
`src/femic/ws3_bridge.py` (tests in `tests/test_ws3_bridge.py`):

- **`.yld` curve ages are periods**, not years (ws3 converts age-based yield
  components by the model period length). Yearly samples are now collapsed to
  one sample per period (midpoint-closest), avoiding duplicate x values.
- **`.trn` `*TARGET` trailing token is a target proportion in percent**
  (`tprop = value * 0.01`), not an age; the post-treatment age comes from the
  action's `Y` flag (`*ACTION cc Y` -> targetage 0, regeneration).

## Notes

- The published instance outputs were re-exported with the THLB filter
  (woodstock CSVs + ws3 sections) and re-published to the `arbutus-s3` special
  remote (new Arbutus cloud, `object-arbutus.alliancecan.ca`).
- The bird-floor frontier sweep (factors 1.00-1.15 of the epsilon=0.1 baseline
  per-period bird series, periods 2..20, maximize harvest) is recorded in
  `evidence/campaign_frontier_2026-10-12.md`.
