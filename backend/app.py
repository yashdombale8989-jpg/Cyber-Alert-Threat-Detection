from pathlib import Path
from collections import deque
import asyncio, json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from .monitor import collect_snapshot
ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title='Cyber Alert Threat Detection')
history = deque(maxlen=100)
@app.get('/api/status')
def status():
    item = collect_snapshot()
    history.append(item)
    return item
@app.get('/api/history')
def get_history():
    return list(history)
@app.get('/')
def home():
    return HTMLResponse((ROOT / 'frontend' / 'index.html').read_text())
@app.websocket('/ws')
async def websocket(ws: WebSocket):
    await ws.accept()
    while True:
        item = collect_snapshot()
        history.append(item)
        await ws.send_text(json.dumps(item))
        await asyncio.sleep(2)