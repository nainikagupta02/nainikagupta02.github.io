# synthetic monitoring exercise

- use a fresh python environment and install `requirements.in`
- run `python demo.py --output monitoring-output` to generate synthetic request logs, numeric features, predictions, available labels, and a summary report
- the score functions are fixed simulations, not fitted or deployed models
- labels become available three simulated days after prediction and the evaluation cutoff is day seven
- evaluation uses the same mature labelled rows for incumbent and candidate outputs
- the toy review rule requires at least 30 labels, 90% coverage, lower candidate brier loss, and no lower roc auc
- thresholds and outcomes are for learning and do not automatically approve or deploy a candidate
- run `python instrumentation.py` to print example prometheus metrics for one illustrative request
- the metrics example does not launch prometheus, grafana, an api server, or a scheduled monitor
- use a fresh output folder for each demo run and record resolved package versions for repeatability
