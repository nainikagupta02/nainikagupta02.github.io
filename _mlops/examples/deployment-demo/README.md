# local deployment checks

- the download includes the synthetic lifecycle and serving exercise plus a compose file, release probe, and sequential benchmark
- use python 3.12, install `requirements.in`, train using `python lifecycle_demo.py --output artifacts/run-001`, and record dependencies using `python -m pip freeze > requirements-lock.txt`
- with the docker engine running, build using `docker build -t mlops-demo:local .`
- validate the compose file using `docker compose config --quiet`
- start locally using `docker compose up -d --wait`
- check the running service using `python check_release.py`
- measure a small warmed-up sequential run using `python benchmark.py --requests 30`
- stop the compose project using `docker compose down`
- set `DEMO_IMAGE` and `DEMO_PORT` to choose an existing reviewed image and another local port
- the benchmark excludes warmup requests and reports failures separately from successful-request latency
- this exercise has no public traffic routing or automatic rollback and does not measure concurrent capacity
- the short model id is a fingerprint for this exercise, not an image digest or a security attestation
