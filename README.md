# Cyber Alert Threat Detection

AI-assisted defensive network intrusion detection project.

## ML stack
- **Dataset:** CICIDS2017
- **Classifier:** Random Forest
- **Anomaly detector:** Isolation Forest
- **Evaluation:** accuracy and per-class precision/recall/F1
- **Live telemetry:** passive local OS/network statistics
- **Live flow inference:** `POST /api/predict-flow` for CICFlowMeter-compatible flow features
- **Dashboard:** FastAPI + WebSocket

## Train the CICIDS2017 model

### Local
Download the CICIDS2017 machine-learning CSV files from the official Canadian Institute for Cybersecurity source and place them under `data/cicids2017/`.

Then run:

    pip install -r requirements.txt
    python -m ml.train

### GitHub Actions
Open **Actions → Train CICIDS2017 IDS → Run workflow**. The workflow downloads the public Hugging Face mirror of CICIDS2017, trains on a capped 300,000-row sample, and stores the trained model and metrics as a workflow artifact. The official dataset source remains the UNB/CIC page.

## Run the dashboard

    uvicorn backend.app:app --reload

Open `http://127.0.0.1:8000`.

The dashboard uses real telemetry from the computer running the application. The ML endpoint accepts actual flow-feature records matching CICIDS2017. It does not generate fake attack traffic or actively scan networks.

## Dataset source
The Canadian Institute for Cybersecurity states that CICIDS2017 provides labeled flow CSVs produced with CICFlowMeter and includes benign traffic and multiple attack scenarios. Cite the dataset paper when using the data.

Official source: https://www.unb.ca/cic/datasets/ids-2017.html
