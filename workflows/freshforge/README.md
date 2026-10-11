# FreshForge graphs

- `tsa24_model_build_workflow.yaml` — the per-MU model-build graph
  (validate -> geospatial preflight -> compile -> BTC/TIPSY bundle ->
  Woodstock export -> ws3 section handoff).

Run from the parent femic checkout:

.. code-block:: console

   freshforge plan external/femic-tsa24-instance/workflows/freshforge/tsa24_model_build_workflow.yaml
   freshforge run external/femic-tsa24-instance/workflows/freshforge/tsa24_model_build_workflow.yaml \
     --workdir runtime/freshforge --namespace tsa24/model-build --json
