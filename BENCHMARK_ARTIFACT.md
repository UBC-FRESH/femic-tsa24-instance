# TSA24 even-flow benchmark artifact

Release: `ws4-tsa24-evenflow-v1`  
https://github.com/UBC-FRESH/femic-tsa24-instance/releases/tag/ws4-tsa24-evenflow-v1

## Contents

- `compiled/` — frozen WS4 compiled dataset (12 Parquet tables).
- `evenflow_tsa24.yaml` — WS4 even-flow/level target.
- `seed_oldest_first_tsa24.csv` — initial feasible schedule.
- `README.md`, `MANIFEST.sha256`.

Asset SHA-256:

```text
be8625804b2a3b93e89afaa013b6dde401bf7309f47b7a64554a5b2c5523a20f
```

## Licence

- Code and documentation: MIT (`LICENSE`).
- Derived benchmark artifacts: CC BY 4.0 (`DATA_LICENSES.md`).
- Source data retains OGL-BC and other source terms.

## Pinned solver

The GPU results use the `feature/gpu-acceleration` branch of
[`UBC-FRESH/ws4`](https://github.com/UBC-FRESH/ws4) at commit `f60ce64`.

The CPU-SA baseline uses `UBC-FRESH/ws4` main at `f23d450`.

## GPU rebuild

The effect table and caches are excluded from the 4.5 MB release because they are
gigabyte-scale. Rebuild them from the frozen artifact:

```bash
git clone https://github.com/UBC-FRESH/ws4.git ws4-gpu
git -C ws4-gpu checkout f60ce64
export WS4_GPU_ROOT="$PWD/ws4-gpu"
export TSA24_ROOT="$PWD"
export GPU_CACHE="$TSA24_ROOT/runtime/gpu-cache"
export GPU_TABLE="$TSA24_ROOT/runtime/gpu-effects/effects-lean.pt"

mkdir -p "$GPU_CACHE" "$TSA24_ROOT/runtime/gpu-effects"
PYTHONPATH="$WS4_GPU_ROOT" python "$WS4_GPU_ROOT/examples/gpu_effects/build_effect_table.py" \
  --dataset "$TSA24_ROOT/compiled" \
  --targets "$TSA24_ROOT/evenflow_tsa24.yaml" \
  --candidates-cache "$GPU_CACHE/candidates.pkl" \
  --simulator-cache "$GPU_CACHE/simulator.pkl" \
  --out "$GPU_TABLE" --years 200
```

Then run the recorded configuration:

```bash
PYTHONPATH="$WS4_GPU_ROOT" python -m ws4.cli gpu-run \
  --dataset "$TSA24_ROOT/compiled" \
  --targets "$TSA24_ROOT/evenflow_tsa24.yaml" \
  --seed-schedule "$TSA24_ROOT/seed_oldest_first_tsa24.csv" \
  --table "$GPU_TABLE" \
  --cache-dir "$GPU_CACHE" \
  --out-dir "$TSA24_ROOT/runtime/gpu-run-100k" \
  --seeds 1,2,3,4,5 --population 64 --generations 100000 --device cuda \
  --json-out "$TSA24_ROOT/runtime/gpu-run-100k/summary.json"
```

Recorded results:

- 1,000 generations, seed 7: 8,588,725.370498415.
- 10,000 generations, seed 7: 76,540.74073269201.
- 100,000 generations, seeds 1–5: 512.574139–518.621452.
- 100,000 generations, seed 7: 517.8619818205188.

The 70M m³/period level targets are deliberately unattainable pull-up
aspirations; the weight-10,000 even-flow target selects the maximum even-flow
level. The result is a weighted compromise, not a hard-feasibility claim.

## Replay

The paper repository contains exact CPU replay scripts and schedules for every
recorded run. The replay uses WS4's exact `IncrementalObjective`, not the GPU
device objective.
