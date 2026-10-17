"""check a running local service against a trusted saved pipeline."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from urllib.request import Request, urlopen
import joblib
import numpy as np


def read_json(url, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urlopen(request, timeout=5) as response:
        return json.load(response)


def check_release(base_url, model_path):
    base_url = base_url.rstrip('/')
    model_path = Path(model_path)
    expected_id = hashlib.sha256(model_path.read_bytes()).hexdigest()[:12]
    health = read_json(base_url + '/health')
    if health.get('status') != 'ready' or health.get('model_id') != expected_id:
        raise ValueError('readiness or model identity check failed')
    rows = [[0.0] * 10]
    result = read_json(base_url + '/predict', {'rows': rows})
    expected = float(joblib.load(model_path).predict_proba(np.asarray(rows))[:, 1][0])
    probabilities = result.get('probabilities', [])
    if (result.get('model_id') != expected_id or len(probabilities) != 1
            or not math.isclose(float(probabilities[0]), expected, rel_tol=1e-7, abs_tol=1e-9)):
        raise ValueError('prediction check failed')
    return {'status': 'passed', 'model_id': expected_id, 'base_url': base_url}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8000')
    parser.add_argument('--model-path', type=Path, default=Path('artifacts/run-001/pipeline.joblib'))
    args = parser.parse_args()
    print(json.dumps(check_release(args.base_url, args.model_path), indent=2))
