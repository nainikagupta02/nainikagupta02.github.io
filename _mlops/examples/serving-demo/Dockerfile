FROM python:3.12-slim
WORKDIR /app
COPY requirements-lock.txt ./
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY --chmod=0444 app.py ./
COPY --chmod=0444 artifacts/run-001/pipeline.joblib ./artifacts/run-001/pipeline.joblib
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
