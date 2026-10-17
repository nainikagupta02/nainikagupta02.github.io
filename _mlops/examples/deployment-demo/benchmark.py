"""a sequential local timing exercise, not a concurrent capacity test."""
import argparse
import json
import math
import statistics
import time
from http.client import HTTPException
from urllib.request import Request, urlopen


def predict(base_url):
    data = json.dumps({'rows': [[0.0] * 10]}).encode()
    request = Request(base_url.rstrip('/') + '/predict', data=data,
                      headers={'Content-Type': 'application/json'})
    with urlopen(request, timeout=5) as response:
        result = json.load(response)
    values = result.get('probabilities', [])
    if len(values) != 1 or not math.isfinite(float(values[0])) or not 0 <= float(values[0]) <= 1:
        raise ValueError('unexpected prediction response')
    model_id = result.get('model_id')
    if not isinstance(model_id, str) or not model_id:
        raise ValueError('missing model id')
    return model_id


def benchmark(base_url, count=30, warmup=3):
    if count < 1 or warmup < 0:
        raise ValueError('use at least one request and a non-negative warmup')
    for _ in range(warmup):
        predict(base_url)
    durations, model_ids, failures = [], set(), 0
    started = time.perf_counter()
    for _ in range(count):
        before = time.perf_counter()
        try:
            model_ids.add(predict(base_url))
            durations.append((time.perf_counter() - before) * 1000)
        except (OSError, HTTPException, ValueError, KeyError, TypeError):
            failures += 1
    elapsed = time.perf_counter() - started
    ordered = sorted(durations)
    return {
        'requests': count, 'successes': len(ordered), 'failures': failures,
        'success_fraction': len(ordered) / count,
        'successful_requests_per_second': len(ordered) / elapsed,
        'successful_p50_ms': statistics.median(ordered) if ordered else None,
        'successful_p95_ms': ordered[math.ceil(0.95 * len(ordered)) - 1] if ordered else None,
        'model_ids_seen': sorted(model_ids), 'warmup_requests_excluded': warmup,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8000')
    parser.add_argument('--requests', type=int, default=30)
    parser.add_argument('--warmup', type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(benchmark(args.base_url, args.requests, args.warmup), indent=2))
