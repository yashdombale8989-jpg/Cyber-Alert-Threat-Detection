from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'models' / 'cicids2017_random_forest.joblib'

def predict_flow(flow: dict):
    model = joblib.load(MODEL)
    frame = pd.DataFrame([flow])
    label = str(model.predict(frame)[0])
    confidence = float(model.predict_proba(frame).max()) if hasattr(model, 'predict_proba') else None
    return {'timestamp': pd.Timestamp.utcnow().isoformat(), 'label': label, 'confidence': confidence}
