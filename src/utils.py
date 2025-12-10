import json
import time
from pathlib import Path

# Set a default data directory inside src/
DATA_DIR = Path(__file__).parent / "data"

def save_json(obj, filename):
    """
    Save a dictionary as JSON in src/data/ (creates folder if needed).
    """
    filepath = DATA_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)  # create directories if needed
    with open(filepath, "w") as f:
        json.dump(obj, f, indent=2)

def load_json(filename):
    filepath = DATA_DIR / filename
    with open(filepath, "r") as f:
        return json.load(f)

def timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S")
