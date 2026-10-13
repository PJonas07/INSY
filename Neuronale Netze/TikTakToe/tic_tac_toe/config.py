"""All hyperparameters and file paths in one place, so every run is reproducible."""

from pathlib import Path

# Network shape: 9 board cells in, one output neuron per cell ("how good is a move here?").
INPUT_SIZE = 9
# 36 hidden neurons: enough to hit about 97 % of the best moves, few enough to still draw.
HIDDEN_SIZE = 36
OUTPUT_SIZE = 9

# Training
RANDOM_SEED = 42
LEARNING_RATE = 10.0
EPOCHS = 5000
# Weights start in [-INIT_RANGE, INIT_RANGE]; small values keep sigmoid out of saturation.
INIT_RANGE = 1.0
# The weights are stored every n-th epoch, so the website can replay how they changed.
SNAPSHOT_EVERY = 100
# Weights are rounded for the website to keep web/data.js small.
WEB_DECIMALS = 4

# Files
PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "models" / "model.json"
WEB_DATA_PATH = PROJECT_DIR / "web" / "data.js"
