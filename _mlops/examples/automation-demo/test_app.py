import json
from pathlib import Path
import subprocess
from unittest.mock import patch

import joblib
import numpy as np
import pytest
from fastapi.testclient import TestClient
import app as serving
from quality_gate import check_candidate
from run_workflow import run_workflow


@pytest.fixture
def client():
    with TestClient(serving.app) as active:
        yield active


def test_predictions_match_saved_pipeline(client):
    rows = np.array([[0.0] * 10, [1.0] * 10, [-1.0] * 10])
    response = client.post('/predict', json={'rows': rows.tolist()})
    assert response.status_code == 200
    model = joblib.load('artifacts/run-001/pipeline.joblib')
    expected = model.predict_proba(rows)[:, 1]
    np.testing.assert_allclose(response.json()['probabilities'], expected)
    assert response.json()['model_id'] == client.get('/health').json()['model_id']


@pytest.mark.parametrize('payload', [
    {}, {'rows': []}, {'rows': [[0] * 9]}, {'rows': [[0] * 10] * 257},
    {'rows': [['0'] * 10]}, {'rows': [[0] * 10], 'unexpected': 1},
])
def test_rejects_invalid_input(client, payload):
    assert client.post('/predict', json=payload).status_code == 422


def test_rejects_nonfinite_input(client):
    response = client.post('/predict', content='{"rows": [[1e400,0,0,0,0,0,0,0,0,0]]}',
                           headers={'Content-Type': 'application/json'})
    assert response.status_code == 422


def test_missing_artifact_stops_startup(monkeypatch):
    def missing(_path):
        raise FileNotFoundError('missing artifact')
    monkeypatch.setattr(serving.joblib, 'load', missing)
    with pytest.raises(FileNotFoundError), TestClient(serving.app):
        pass


@pytest.mark.parametrize('score,baseline', [(0.6, 0.5), (float('nan'), 0.5), (1.2, 0.5), (0.8, 0.9)])
def test_quality_gate_rejects_bad_candidates(score, baseline):
    report = {'selected_validation_auc': score, 'baseline_validation_auc': baseline}
    with pytest.raises(ValueError):
        check_candidate(report)


def test_quality_gate_accepts_candidate():
    assert check_candidate({'selected_validation_auc': 0.8,
                            'baseline_validation_auc': 0.5}) == 0.8


def test_workflow_records_training_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch('run_workflow.subprocess.run', side_effect=subprocess.CalledProcessError(1, 'train')):
        with pytest.raises(subprocess.CalledProcessError):
            run_workflow('failed-run')
    state = json.loads(Path('workflow-runs/failed-run.json').read_text())
    assert state['status'] == 'failed' and state['stage'] == 'train'
    assert 'model_path' not in state


def test_workflow_records_validation_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    def train_with_bad_candidate(command, **_kwargs):
        output = Path(command[-1])
        output.mkdir(parents=True)
        (output / 'run.json').write_text(json.dumps({
            'selected_validation_auc': 0.6, 'baseline_validation_auc': 0.5,
        }))
    with patch('run_workflow.subprocess.run', side_effect=train_with_bad_candidate):
        with pytest.raises(ValueError):
            run_workflow('rejected-run')
    state = json.loads(Path('workflow-runs/rejected-run.json').read_text())
    assert state['status'] == 'failed' and state['stage'] == 'validate'
    assert 'model_path' not in state
