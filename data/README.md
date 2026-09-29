CIC-IDS2017 is now the training dataset for this project.

Official source: https://www.unb.ca/cic/datasets/ids-2017.html
The official page describes labeled network-flow CSV files with more than 80 flow features and benign traffic plus common attacks including brute force, DoS/DDoS, Heartbleed, web attacks, infiltration and botnet. The full raw capture is large, so the CSV is intentionally not committed to GitHub.

Recommended layout:

    data/cicids2017/*.csv

The training script reads every CSV in that directory, removes identifier fields, combines the files, and can cap the training sample with CICIDS_MAX_ROWS.

Train locally:

    python -m ml.train

The resulting model is written to models/cicids2017_random_forest.joblib and metrics to models/metrics.json.
