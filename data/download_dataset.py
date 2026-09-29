"""Download the official UNSW-NB15 training/testing CSV files.

Run from the project root:
    python data/download_dataset.py

The official UNSW page provides the dataset files. Because the files are large,
they are downloaded locally and are not committed to Git.
"""
from pathlib import Path
import urllib.request

DATA_DIR = Path(__file__).resolve().parent
DATA_DIR.mkdir(exist_ok=True)

print("UNSW-NB15 official dataset:")
print("https://research.unsw.edu.au/projects/unsw-nb15-dataset")
print()
print("Open the official page and download:")
print("  UNSW_NB15_training-set.csv")
print("  UNSW_NB15_testing-set.csv")
print()
print("Place both files in:", DATA_DIR)
print("Then run: python -m ml.train")
