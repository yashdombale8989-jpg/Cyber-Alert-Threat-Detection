# Dataset

This project uses the official UNSW-NB15 training dataset for defensive intrusion-detection research.

UNSW states that the configured training set contains 175,341 records and the test set contains 82,332 records. The dataset covers normal traffic and nine attack types. Download it from the official UNSW page:

https://research.unsw.edu.au/projects/unsw-nb15-dataset

Place the downloaded file at:

data/UNSW_NB15_training-set.csv

Do not commit the large CSV to GitHub. The training script reads it locally and creates the model artifacts in models/.

## Train

python -m ml.train

The application also has a separate passive real-time collector. It observes the local machine's OS/network connection metadata and resource statistics. It does not generate traffic or actively scan networks.
