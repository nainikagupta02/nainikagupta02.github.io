"""summarise one preselected window of synthetic request logs."""
import math
import numpy as np
import pandas as pd


def summarise_logs(logs):
    if logs.empty or not {'status_code', 'latency_ms'}.issubset(logs.columns):
        raise ValueError('expected non-empty request logs')
    status = pd.to_numeric(logs['status_code'], errors='raise')
    latency = pd.to_numeric(logs['latency_ms'], errors='raise').to_numpy()
    if not (status.between(100, 599).all() and (status % 1 == 0).all()):
        raise ValueError('invalid http status')
    if not np.isfinite(latency).all() or (latency < 0).any():
        raise ValueError('invalid latency')
    ordered = sorted(latency)
    return {
        'requests': len(logs),
        'server_error_fraction': float(status.between(500, 599).mean()),
        'client_error_fraction': float(status.between(400, 499).mean()),
        'p95_ms_all_requests': float(ordered[math.ceil(0.95 * len(ordered)) - 1]),
    }
