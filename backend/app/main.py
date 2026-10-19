from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from threading import RLock

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parents[2]
ML_SRC = ROOT / "ml" / "src"

if str(ML_SRC) not in sys.path:
    sys.path.insert(0, str(ML_SRC))

from predictor_interface import TwinPulsePredictor  # noqa: E402

# Load DigitalTwinState from the existing hyphenated directory.
TWIN_FILE = ROOT / "digital-twin" / "twin_state.py"
spec = spec_from_file_location("twin_state", TWIN_FILE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load Digital Twin module: {TWIN_FILE}")

twin_module = module_from_spec(spec)
spec.loader.exec_module(twin_module)
DigitalTwinState = twin_module.DigitalTwinState

app = FastAPI(
    title="TwinPulse API",
    description=(
        "Research prototype for exploring a dynamic patient state. "
        "Outputs are not clinically validated."
    ),
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

predictor = TwinPulsePredictor()
twins: dict[str, DigitalTwinState] = {}
twins_lock = RLock()


class PatientFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    age: float | None = Field(ge=18, le=120)
    bmi: float | None = Field(ge=10, le=100)
    sbp: float | None = Field(ge=50, le=300)
    dbp: float | None = Field(ge=30, le=200)
    imt_max: float | None = Field(ge=0, le=5)
    lvmi: float | None = Field(ge=0, le=1000)
    ef: float | None = Field(ge=0, le=100)
    gender: str = Field(min_length=1, max_length=30)
    smoker: str = Field(min_length=1, max_length=30)


class PhysiologicalObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    heart_rate_bpm: float | None = Field(default=None, ge=20, le=250)
    mean_rr_ms: float | None = Field(default=None, ge=200, le=3000)
    sdnn_ms: float | None = Field(default=None, ge=0, le=2000)
    rmssd_ms: float | None = Field(default=None, ge=0, le=2000)
    source: str = Field(default="demo_simulation", max_length=50)


def get_twin(patient_id: str) -> DigitalTwinState:
    with twins_lock:
        twin = twins.get(patient_id)
        if twin is None:
            raise HTTPException(status_code=404, detail="Patient twin not found")
        return twin


@app.get("/")
def root():
    return {
        "success": True,
        "message": "TwinPulse API is running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "service": "TwinPulse API",
        "model_loaded": True,
        "digital_twin_engine_loaded": True,
    }


@app.post("/api/predict")
def predict(features: PatientFeatures):
    try:
        result = predictor.predict(features.model_dump())
        return {
            "success": True,
            "patient_state": features.model_dump(),
            "prediction": result,
            "disclaimer": (
                "Research prototype only. This score is not a "
                "clinically validated risk estimate and must not "
                "guide diagnosis or treatment."
            ),
        }
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/twins/{patient_id}")
def create_twin(patient_id: str, features: PatientFeatures):
    with twins_lock:
        if patient_id in twins:
            raise HTTPException(
                status_code=409,
                detail="A twin with this patient ID already exists",
            )
        twin = DigitalTwinState(patient_id)
        twin.update_clinical_state(features.model_dump())
        twins[patient_id] = twin

    return {
        "success": True,
        "message": "Digital Twin created",
        "twin": twin.snapshot(),
    }


@app.get("/api/twins/{patient_id}")
def read_twin(patient_id: str):
    return {"success": True, "twin": get_twin(patient_id).snapshot()}


@app.post("/api/twins/{patient_id}/physiology")
def update_physiology(
    patient_id: str,
    observation: PhysiologicalObservation,
):
    twin = get_twin(patient_id)
    twin.update_physiological_state(observation.model_dump(exclude_none=True))
    return {"success": True, "twin": twin.snapshot()}


@app.post("/api/twins/{patient_id}/predict")
def predict_for_twin(patient_id: str):
    twin = get_twin(patient_id)
    state = twin.snapshot()
    clinical = state["clinical_state"]

    try:
        result = predictor.predict(clinical)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    twin.update_prediction(result)
    return {
        "success": True,
        "twin": twin.snapshot(),
        "disclaimer": (
            "Research prototype only. This score is not clinically "
            "validated and must not guide diagnosis or treatment."
        ),
    }
