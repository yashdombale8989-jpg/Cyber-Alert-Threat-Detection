from pathlib import Path
from collections import deque
import asyncio
import json
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse
from .monitor import collect_snapshot
from ml.predict import predict_flow, predict_anomaly, model_status

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Cyber Alert Threat Detection")
history = deque(maxlen=100)
flow_alerts = deque(maxlen=100)

@app.get("/api/status")
def status():
    item = collect_snapshot()
    history.append(item)
    return item

@app.get("/api/history")
def get_history():
    return list(history)

@app.get("/api/models")
def models():
    return model_status()

@app.post("/api/predict-flow")
def predict_live_flow(flow: dict):
    try:
        result = predict_flow(flow)
        anomaly = predict_anomaly(flow)
        result.update(anomaly)
        flow_alerts.append(result)
        return result
    except FileNotFoundError:
        raise HTTPException(
            503,
            "CICIDS2017 models are not installed. Download the successful GitHub Actions artifact into models/."
        )
    except Exception as exc:
        raise HTTPException(400, str(exc))

@app.get("/api/alerts")
def alerts():
    return list(flow_alerts)

@app.get("/")
def home():
    return HTMLResponse((ROOT / "frontend" / "index.html").read_text())

@app.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            item = collect_snapshot()
            history.append(item)
            await ws.send_text(json.dumps(item))
            await asyncio.sleep(2)
    except Exception:
        await ws.close()
