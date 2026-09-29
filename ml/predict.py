from pathlib import Path
import joblib
import pandas as pd

MODEL = Path(__file__).resolve().parents[1] / "models" / "threat_classifier.joblib"

def predict(row: dict):
    model = joblib.load(MODEL)
    frame = pd.DataFrame([row])
    label = int(model.predict(frame)[0])
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(model.predict_proba(frame).max())
    return {"label": label, "confidence": confidence}
