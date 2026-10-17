"""predict rows from a headerless csv containing ten numeric columns."""
import joblib
import numpy as np

model = joblib.load('artifacts/run-001/pipeline.joblib')
x = np.loadtxt('features.csv', delimiter=',', ndmin=2)
if x.shape[0] == 0 or x.shape[1] != model.n_features_in_ or not np.isfinite(x).all():
    raise ValueError('expected non-empty finite rows with ten features')
probabilities = model.predict_proba(x)[:, 1]
np.savetxt('predictions.csv', probabilities, delimiter=',', header='probability', comments='')
