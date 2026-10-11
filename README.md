# femic-tsa24-instance

FEMIC deployment instance for **TSA 24** — one of the five WBI birds AOI
management units (TSAs 08/16/24/40/41). Part of Phase 113 of the
[femic](https://github.com/UBC-FRESH/femic) roadmap (`UBC-FRESH/femic#316`).

Builds the forest-estate model inputs for the MU and the ws3 handoff
(`output/ws3/<model>.{lan,are,yld,act,trn}`) consumed by the
[WBI birds engine](https://github.com/UBC-FRESH/wbi-birds).

## Structure

- `config/` — run profile, TIPSY rules, rebuild spec, Patchworks runtime config
- `workflows/freshforge/` — per-MU model-build graph (P113.3)
- `docs/` — Sphinx site (published to GitHub Pages)
- `data/`, `output/`, `models/`, `runbooks/`, `evidence/`

## Quickstart

See `QUICKSTART.md` and the docs site.

## Data

Fresh public data only: VRI 2025 (BCDC) + FADM boundaries/SiteProd
(`external/femic-public-data`). Annex remote: `arbutus-s3`
(bucket `ubc-fresh-femic-tsa24-instance`).
