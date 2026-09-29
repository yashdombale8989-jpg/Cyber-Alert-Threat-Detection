from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "UNSW_NB15_training-set.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df.columns = [c.strip() for c in df.columns]
if "label" not in df.columns:
    raise ValueError("Expected a 'label' column in UNSW_NB15_training-set.csv")

y = df["label"].astype(int)
X = df.drop(columns=["label"]).copy()
X = X.drop(columns=[c for c in ["id"] if c in X.columns])

cat = X.select_dtypes(include=["object"]).columns.tolist()
num = [c for c in X.columns if c not in cat]
pre = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ]), cat)
])

clf = RandomForestClassifier(
    n_estimators=250, random_state=42, n_jobs=-1,
    class_weight="balanced_subsample"
)
pipe = Pipeline([("preprocess", pre), ("classifier", clf)])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)

metrics = {
    "accuracy": float(accuracy_score(y_test, pred)),
    "classification_report": classification_report(y_test, pred, output_dict=True)
}
joblib.dump(pipe, MODEL_DIR / "threat_classifier.joblib")
(MODEL_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))

normal = X_train[y_train == 0]
encoded = pre.transform(normal)
iso = IsolationForest(n_estimators=200, contamination="auto", random_state=42, n_jobs=-1)
iso.fit(encoded)
joblib.dump((pre, iso), MODEL_DIR / "anomaly_detector.joblib")

print("Training complete.")
print("Accuracy:", round(metrics["accuracy"], 4))
