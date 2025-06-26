import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any

@dataclass
class Project:
    sketch_path: str
    depth_map_path: str | None = None
    material_settings: Dict[str, Any] | None = None
    lighting_settings: Dict[str, Any] | None = None

    def save(self, path: Path) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(path: Path) -> 'Project':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Project(**data)
