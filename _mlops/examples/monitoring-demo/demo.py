"""generate synthetic monitoring records and compare fixed simulated scores."""
import argparse
import json
from pathlib import Path
from importlib.metadata import version
import numpy as np
import pandas as pd
from monitor_metrics import summarise_logs
from drift_metrics import compare_feature
from evaluate_models import evaluate_models


def run_demo(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(42)
    n = 600
    reference = rng.normal(0, 1, n)
    latent = rng.normal(0.6, 1, n)
    current = latent.copy()
    current[rng.random(n) < 0.05] = np.nan
    visible = np.nan_to_num(current, nan=0.0)
    sigmoid = lambda x: 1 / (1 + np.exp(-x))
    # fixed simulated scores; no candidate is fitted or tuned on these rows.
    incumbent = sigmoid(0.7 * visible + 0.1)
    candidate = sigmoid(1.3 * visible + 0.1)
    target = rng.binomial(1, sigmoid(1.2 * latent + 0.1))
    day = rng.integers(0, 8, n)
    ids = ['request-' + str(i) for i in range(n)]
    predictions = pd.DataFrame({'request_id': ids, 'prediction_day': day,
                                'incumbent_score': incumbent, 'candidate_score': candidate})
    labels = pd.DataFrame({'request_id': ids, 'target': target, 'available_day': day + 3})
    labels = labels[labels['available_day'] <= 7]
    logs = pd.DataFrame({'request_id': ids, 'status_code': np.where(rng.random(n) < 0.02, 500, 200),
                         'latency_ms': rng.lognormal(mean=3.2, sigma=0.4, size=n)})
    pd.DataFrame({'feature': reference}).to_csv(output / 'reference.csv', index=False)
    pd.DataFrame({'feature': current}).to_csv(output / 'current.csv', index=False)
    predictions.to_csv(output / 'predictions.csv', index=False)
    labels.to_csv(output / 'available_labels.csv', index=False)
    logs.to_csv(output / 'requests.csv', index=False)
    report = {'seed': 42, 'cutoff_day': 7, 'label_horizon_days': 3,
              'versions': {name: version(name) for name in ['numpy', 'pandas', 'scipy', 'scikit-learn']},
              'service': summarise_logs(logs),
              'input_comparison': compare_feature(reference, current),
              'model_comparison': evaluate_models(predictions, labels)}
    (output / 'report.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('monitoring-output'))
    print(json.dumps(run_demo(parser.parse_args().output), indent=2, allow_nan=False))
