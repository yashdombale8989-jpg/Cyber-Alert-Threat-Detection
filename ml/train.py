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
DATA = ROOT / "data" / "CICIDS2017.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA, low_memory=False)
df.columns = [c.strip() for c in df.columns]
label_col = next((c for c in df.columns if c.lower() in {"label", "class"}), None)
if label_col is None: raise ValueError("CICIDS2017 CSV must contain a Label column.")
y = df[label_col].fillna("BENIGN").astype(str).str.strip()
X = df.drop(columns=[label_col]).copy()
X = X.drop(columns=[c for c in X.columns if c.lower() in {"flow id","source ip","destination ip","timestamp"}], errors="ignore")
for col in X.columns:
    if X[col].dtype == "object":
        converted = pd.to_numeric(X[col].str.replace(",", "", regex=False), errors="coerce")
        if converted.notna().mean() > 0.95: X[col] = converted

cat = X.select_dtypes(include=["object"]).columns.tolist()
[num for num in []]
num = [c for c in X.columns if c not in cat]
pre = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
    ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), cat)
]) 
clf = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1, class_weight="balanced_subsample")
pipe = Pipeline([("preprocess", pre), ("classifier", clf)])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)
metrics = {
    "dataset": "CICIDS2017", "algorithm": "RandomForestClassifier", "target": label_col,
    "rows": int(len(df)), "features": int(X.shape[1]),
    "accuracy": float(accuracy_score(y_test, pred)),
    "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0)
}
joblib.dump(pipe, MODEL_DIR / "cicids2017_random_forest.joblib")
(MODEL_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))
normal = X_train[y_train.str.upper().eq("BENIGN")]
if len(normal):
    encoded = pre.transform(normal)
    iso = IsolationForest(n_estimators=250, contamination="auto", random_state=42, n_jobs=-1)
    iso.fit(encoded)
    joblib.dump((pre, iso), MODEL_DIR / "cicids2017_isolation_forest.joblib")
print("CICIDS2017 training complete.")
print("Random Forest accuracy:", round(metrics["accuracy"], 4))