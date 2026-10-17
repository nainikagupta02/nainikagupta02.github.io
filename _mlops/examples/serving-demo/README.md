# local packaging and serving exercise

- use python 3.12 to match the docker base image
- create a virtual environment and install `requirements.in`
- run `python lifecycle_demo.py --output artifacts/run-001`
- capture the resolved environment with `python -m pip freeze > requirements-lock.txt`
- run `uvicorn app:app --host 127.0.0.1 --port 8000`
- send json with a `rows` field containing 1 to 256 rows, each with ten finite numeric values in the synthetic model's original feature order
- probabilities correspond to class 1 and rows retain their request order
- use `python predict_batch.py` with a headerless ten-column `features.csv` for batch inference
- with docker running, build using `docker build -t mlops-demo:local .`
- run using `docker run --rm -p 127.0.0.1:8000:8000 mlops-demo:local`
- this exercise has no authentication or production traffic controls and is intended for local learning
- only load artifacts you trust and keep the training and serving dependency versions compatible
