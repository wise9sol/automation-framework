import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def load_json(relative_path: str) -> dict:
    path = PROJECT_ROOT / relative_path
    return json.loads(path.read_text(encoding="utf-8"))