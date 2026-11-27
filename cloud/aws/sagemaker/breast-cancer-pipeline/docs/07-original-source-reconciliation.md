# Original-source reconciliation

This project bundle was reconciled against a privately retained SageMaker JupyterLab final-backup ZIP. The private backup is **not** published.

## What now comes from the original JupyterLab files

The following files were copied **byte-for-byte** from that original backup rather than recreated:

- `src/preprocess.py`, `src/train.py`, `src/train_multi.py`, `src/evaluate.py`
- `data/breast_cancer.csv`
- All non-checkpoint files under `results/`: five final per-configuration JSONs, earlier RF JSON snapshots, and both comparison CSVs

The data and five final evaluation JSONs preserve the values recorded after the real AWS runs. All labels use positive class `0 = malignant`. The `train_multi.py` source contains the exact model/scaler branching used in the successful run.

## Notebook handling

- `notebooks/00_environment_check.ipynb` and `notebooks/01_pipeline_build.ipynb`: **curated runnable/readable notebooks** for clean reuse. They are not asserted to be the original executed files.
- `notebooks/archive/00_environment_check_redacted.ipynb` and `notebooks/archive/01_pipeline_build_redacted.ipynb`: **read-only historical source** taken from the original JupyterLab notebook cells in their original order. Every code cell was converted into a Markdown code block. Execution outputs, account and personal identifiers were removed to make these suitable for public review. These archival notebooks are *not directly executable*.
- `src/sagemaker_pipeline.py`, `scripts/`, `tests/`, and descriptive Markdown in `docs/` were curated for public reuse. The original notebook contains the matching SDK 3.x pipeline definitions and property references; the public module is a refactoring of those actions, not an exact copy.

## Excluded private/temporary files

- Original notebooks **with execution output** (AWS account IDs, run names, paths, permission logs)
- The original private-backup ZIP and generated course report
- Original AWS screenshots containing private execution identifiers
- `.ipynb_checkpoints/`, test scratch directories, models and intermediate archives

## Verification boundaries

The original notebook reports five successful AWS executions and the five saved per-run `evaluation.json` files. The local test suite checks source-script functionality; it does **not** rerun or reverify billable AWS Processing/Training jobs in a new environment. Full model reproducibility depends on package/container versions and infrastructure.
