Data and provenance
===================

Sources (fresh public data):

- **VRI 2025** — `VEG_COMP_LYR_R1_POLY_2025` (L1 R1) and
  `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025`, resolved via
  `femic data bcdc-resolve`; direct zips under
  `https://pub.data.gov.bc.ca/datasets/02dba161-fdb7-48ae-a4bb-bd6ef017c36d/current/`.
- **FADM TSA boundaries** + **SiteProd** — `external/femic-public-data`
  (DataLad, Arbutus S3 special remote).

This dataset is DataLad-managed; large/derived artifacts are annexed to the
`arbutus-s3` special remote (bucket `ubc-fresh-femic-tsa24-instance`, public read).

Provenance for each run is recorded in `runtime/logs/run_manifest-*.json`
and the ws3 handoff checksums in the instance manifest.
