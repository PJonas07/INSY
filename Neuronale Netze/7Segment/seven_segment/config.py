"""All hyperparameters and file paths in one place, so every run is reproducible."""

from pathlib import Path

# Network shape: 7 segments in, one output neuron per digit (0-9).
INPUT_SIZE = 7
HIDDEN_SIZE = 8
OUTPUT_SIZE = 10

# Training
RANDOM_SEED = 42
LEARNING_RATE = 2.0
EPOCHS = 3000
# Weights start in [-INIT_RANGE, INIT_RANGE]; small values keep sigmoid out of saturation.
INIT_RANGE = 1.0
# Only every n-th loss value is stored for the loss curve (keeps model.json small).
LOSS_HISTORY_STEP = 10

# Files
PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "models" / "model.json"
WEB_DATA_PATH = PROJECT_DIR / "web" / "data.js"
