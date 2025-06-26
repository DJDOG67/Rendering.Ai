import json
import zipfile
from pathlib import Path


def save_project(output_path: Path, sketch_path: Path, depth_path: Path | None = None, options: dict | None = None) -> None:
    """Save a project as a .srproj zip file.

    Args:
        output_path: Destination .srproj path.
        sketch_path: Path to the original sketch image.
        depth_path: Optional path to the depth map image.
        options: Optional dictionary with render settings.
    """
    output_path = Path(output_path)
    if output_path.suffix != ".srproj":
        output_path = output_path.with_suffix(".srproj")

    with zipfile.ZipFile(output_path, "w") as zf:
        zf.write(sketch_path, arcname="sketch" + sketch_path.suffix)
        if depth_path:
            zf.write(depth_path, arcname="depth" + depth_path.suffix)
        if options is not None:
            zf.writestr("settings.json", json.dumps(options, indent=2))


def load_project(project_path: Path) -> dict:
    """Load a .srproj file and return its contents as paths and options."""
    project_path = Path(project_path)
    with zipfile.ZipFile(project_path, "r") as zf:
        members = zf.namelist()
        temp_dir = Path(project_path).with_suffix("")
        temp_dir.mkdir(exist_ok=True)
        sketch_file = next((m for m in members if m.startswith("sketch")), None)
        depth_file = next((m for m in members if m.startswith("depth")), None)
        settings = {}
        if sketch_file:
            zf.extract(sketch_file, temp_dir)
        if depth_file:
            zf.extract(depth_file, temp_dir)
        if "settings.json" in members:
            with zf.open("settings.json") as f:
                settings = json.load(f)
    return {
        "dir": temp_dir,
        "sketch": temp_dir / sketch_file if sketch_file else None,
        "depth": temp_dir / depth_file if depth_file else None,
        "settings": settings,
    }
