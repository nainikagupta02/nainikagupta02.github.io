"""a local learning example; not a production deployment."""
import argparse
import hashlib
import json
import platform
from pathlib import Path

import joblib
import numpy as np
import sklearn
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=Path('artifacts/run-001'))
args = parser.parse_args()
seed = 42
x, y = make_classification(
    n_samples=1000, n_features=10, n_informative=5, random_state=seed
)
# independent synthetic rows: 60% train, 20% validation, 20% test.
x_dev, x_test, y_dev, y_test = train_test_split(
    x, y, test_size=0.2, stratify=y, random_state=seed
)
x_train, x_val, y_train, y_val = train_test_split(
    x_dev, y_dev, test_size=0.25, stratify=y_dev, random_state=seed
)
baseline = DummyClassifier(strategy='prior').fit(x_train, y_train)
baseline_auc = roc_auc_score(y_val, baseline.predict_proba(x_val)[:, 1])
candidates = []
for c in [0.1, 1.0, 10.0]:
    model = make_pipeline(
        StandardScaler(), LogisticRegression(C=c, max_iter=1000, random_state=seed)
    )
    model.fit(x_train, y_train)
    auc = roc_auc_score(y_val, model.predict_proba(x_val)[:, 1])
    candidates.append((float(auc), c, model))

# choose using validation data; only then touch the held-out test set.
val_auc, chosen_c, chosen_model = max(candidates, key=lambda run: run[0])
if val_auc <= baseline_auc:
    raise SystemExit('candidate did not beat the baseline; investigate before proceeding')
test_auc = roc_auc_score(y_test, chosen_model.predict_proba(x_test)[:, 1])
args.output.mkdir(parents=True, exist_ok=False)
joblib.dump(chosen_model, args.output / 'pipeline.joblib')
report = {
    'seed': seed,
    'data_sha256': hashlib.sha256(x.tobytes() + y.tobytes()).hexdigest(),
    'split_sizes': {'train': len(y_train), 'validation': len(y_val), 'test': len(y_test)},
    'validation_runs': [{'c': c, 'roc_auc': auc} for auc, c, _ in candidates],
    'baseline_validation_auc': float(baseline_auc),
    'selected_c': chosen_c,
    'selected_validation_auc': val_auc,
    'test_auc': float(test_auc),
    'versions': {
        'python': platform.python_version(), 'scikit-learn': sklearn.__version__,
        'numpy': np.__version__, 'joblib': joblib.__version__
    },
}
(args.output / 'run.json').write_text(json.dumps(report, indent=2) + '\n')
# smoke test: reload our own artifact and compare predictions.
restored = joblib.load(args.output / 'pipeline.joblib')
np.testing.assert_allclose(
    restored.predict_proba(x_test[:5]), chosen_model.predict_proba(x_test[:5])
)
print(json.dumps(report, indent=2))
print('saved pipeline, run record, and verified reload predictions')
