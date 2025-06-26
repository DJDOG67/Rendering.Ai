import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

PRESETS_FILE = Path('presets.json')

@dataclass
class Preset:
    name: str
    settings: Dict[str, Any]
    thumbnail: str | None = None


def load_presets() -> List[Preset]:
    if PRESETS_FILE.exists():
        with open(PRESETS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Preset(**p) for p in data]
    return []


def save_presets(presets: List[Preset]) -> None:
    with open(PRESETS_FILE, 'w', encoding='utf-8') as f:
        json.dump([asdict(p) for p in presets], f, ensure_ascii=False, indent=2)
