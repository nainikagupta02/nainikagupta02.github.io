# testing and workflow exercise

- this download includes the earlier synthetic lifecycle and serving exercise plus tests, a quality gate, a sequential workflow runner, and a github actions template
- use python 3.12 and a fresh virtual environment
- install dependencies with `python -m pip install -r requirements-test.in`
- run `python run_workflow.py --run-id run-001` to train and validate the synthetic candidate
- run `python -m pytest -q` to exercise the prediction contract, saved-pipeline agreement, missing-artifact behaviour, quality gate, and workflow failure handling
- successful candidates are recorded in `workflow-runs/run-001.json` and are not deployed
- choose another run id for another workflow execution; the serving tests expect the original `artifacts/run-001/pipeline.joblib`
- the validation auc floor of 0.75 is a toy example, not a general release standard
- the workflow file assumes these files are placed at the root of a dedicated exercise repository
- requirements are intentionally unpinned for first setup; capture and review resolved versions for a repeatable project
- the github template runs training and checks only and has no deployment credentials or release step
