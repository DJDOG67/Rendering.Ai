import json
from pathlib import Path

PRESET_DIR = Path(__file__).resolve().parent.parent / "presets"


def load_preset(name: str):
    path = PRESET_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_preset(name: str, data: dict):
    PRESET_DIR.mkdir(exist_ok=True)
    path = PRESET_DIR / f"{name}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
