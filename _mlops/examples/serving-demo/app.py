"""local serving exercise for the synthetic lifecycle model."""
from contextlib import asynccontextmanager
import hashlib
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import joblib
import numpy as np
from pydantic import BaseModel, ConfigDict, Field

Number = Annotated[float, Field(strict=True, allow_inf_nan=False)]
Row = Annotated[list[Number], Field(min_length=10, max_length=10)]

class PredictRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    rows: list[Row] = Field(min_length=1, max_length=256)

class PredictResponse(BaseModel):
    probabilities: list[float]
    model_id: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    path = Path('artifacts/run-001/pipeline.joblib')
    model = joblib.load(path)  # load only our trusted local artifact
    if model.n_features_in_ != 10 or list(model.classes_) != [0, 1]:
        raise ValueError('expected the ten-feature binary lifecycle model')
    app.state.model = model
    app.state.model_id = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    yield
    del app.state.model

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def invalid_request(_request, error: RequestValidationError):
    # omit raw inputs so non-finite values cannot break json error responses
    details = [
        {'loc': list(item['loc']), 'msg': item['msg'], 'type': item['type']}
        for item in error.errors()
    ]
    return JSONResponse(status_code=422, content={'detail': details})

@app.get('/health')
def health():
    return {'status': 'ready', 'model_id': app.state.model_id}

@app.post('/predict', response_model=PredictResponse)
def predict(request: PredictRequest):
    x = np.asarray(request.rows, dtype=float)
    return {
        'probabilities': app.state.model.predict_proba(x)[:, 1].tolist(),
        'model_id': app.state.model_id,
    }
