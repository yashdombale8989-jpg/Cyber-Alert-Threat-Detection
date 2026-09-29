from pathlib import Path
from functools import lru_cache
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RF_MODEL = ROOT / "models" / "cicids2017_random_forest.joblib"
ISO_MODEL = ROOT / "models" / "cicids2017_isolation_forest.joblib"

@lru_cache(maxsize=1)
def load_models():
    rf = joblib.load(RF_MODEL)
    iso_pre, iso = joblib.load(ISO_MODEL)
    return rf, iso_pre, iso

def _validate_flow(flow: dict):
    if not isinstance(flow, dict) or not flow:
        raise ValueError("flow must be a non-empty JSON object containing CICFlowMeter features")


def predict_flow(flow: dict):
    _validate_flow(flow)
    rf, _, _ = load_models()
    frame = pd.DataFrame([flow])
    label = str(rf.predict(frame)[0])
    confidence = float(rf.predict_proba(frame).max()) if hasattr(rf, "predict_proba") else None
    return {
        "timestamp": pd.Timestamp.utcnow().isoformat(),
        "label": label,
        "confidence": confidence,
        "is_threat": label.upper() != "BENIGN",
    }

def predict_anomaly(flow: dict):
    _validate_flow(flow)
    _, iso_pre, iso = load_models()
    frame = pd.DataFrame([flow])
    encoded = iso_pre.transform(frame)
    prediction = int(iso.predict(encoded)[0])
    score = float(iso.decision_function(encoded)[0])
    return {
        "timestamp": pd.Timestamp.utcnow().isoformat(),
        "anomaly": prediction == -1,
        "anomaly_score": score,
    }

def model_status():
    return {
        "random_forest": RF_MODEL.exists(),
        "isolation_forest": ISO_MODEL.exists(),
    }
