# Dataset

`breast_cancer.csv` is exported from `sklearn.datasets.load_breast_cancer(as_frame=True).frame`.

- Source: Wisconsin Diagnostic Breast Cancer dataset, distributed by scikit-learn (originally University of Wisconsin / UCI Machine Learning Repository).
- Features: 30 numeric inputs; label column: `target`
- Label encoding: 0 = malignant, 1 = benign
- Dataset size: 569 records

Regenerate from the installed version of scikit-learn:

```bash
python scripts/prepare_dataset.py
```

The source CSV contains no patient names, direct personal identifiers, or AWS identifiers.
