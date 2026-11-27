# Recorded evaluation outputs

These files were copied directly from the original JupyterLab final backup. They are **records of successful SageMaker executions**, not new cloud measurements.

## Five-run results (use these for comparisons)

| Configuration | Original report |
| --- | --- |
| RF-N10 | `evaluation_rf-n10.json` |
| RF-N50 | `evaluation_rf-n50.json` |
| RF-N100 | `evaluation_rf-n100.json` |
| LR-NOSCALE | `evaluation_lr-noscale.json` |
| LR-SCALE | `evaluation_lr-scale.json` |

`experiment_comparison_5runs.csv` is the original five-run comparison produced in the JupyterLab experiment. It contains no account IDs or personal execution names.

## Earlier experiment records (preserved for provenance)

- `evaluation_n10.json`, `evaluation_n50.json`, `evaluation_n100.json`: JSON saved after the initial RF-only experiment series; same metric contents as corresponding `evaluation_rf-n*.json` files.
- `experiment_comparison.csv`: original three-run RF comparison.

All JSON reports use **class 0 (malignant) as positive**, evaluate **114 test records**, and include Accuracy, Precision, Recall, F1 and the confusion matrix.

Temporary `.ipynb_checkpoints/` copies were excluded. See `docs/07-original-source-reconciliation.md` for original-source auditing.

`python scripts/inspect_results.py` is read-only by default. Use `--write-derived-csv` to create a separate generated comparison file without overwriting the original CSV.
