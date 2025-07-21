"""Simple backend utilities used by the GUI.

These functions are **minimal implementations** meant to demonstrate the
expected workflow. They avoid heavy ML dependencies so the prototype can run
in restricted environments. If Pillow is not installed, the functions will
fallback to returning the original input unchanged.
"""

from __future__ import annotations

import shutil
from pathlib import Path

try:  # Optional dependency
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
except Exception:  # pragma: no cover - optional dependency may not be present
    Image = None  # type: ignore


def _ensure_image(path: str | Path) -> Path:
    return Path(path).resolve()


def clean_up(image_path: str | Path) -> Path:
    """Apply a basic denoise and contrast enhancement to ``image_path``.

    If Pillow is unavailable the file is simply copied. The cleaned image path
    is returned.
    """

    src = _ensure_image(image_path)
    dst = src.with_name(src.stem + "_clean" + src.suffix)
    if Image is None:
        shutil.copy(src, dst)
        return dst

    img = Image.open(src)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img.save(dst)
    return dst


def detect_depth(image_path: str | Path) -> Path:
    """Generate a fake depth map from the given image.

    The real application would run MiDaS DPT-Large here. This placeholder
    simply converts the image to grayscale, finds edges and applies a colourmap
    so that the GUI can display something resembling a depth heatmap.
    """

    src = _ensure_image(image_path)
    dst = src.with_name(src.stem + "_depth" + src.suffix)

    if Image is None:
        shutil.copy(src, dst)
        return dst

    img = Image.open(src).convert("L")
    edges = img.filter(ImageFilter.FIND_EDGES)
    depth = ImageOps.colorize(edges, "blue", "red")
    depth.save(dst)
    return dst


def render_image(sketch_path: str | Path, depth_path: str | Path | None, options: dict | None = None) -> Path:
    """Generate a mock rendered image based on the sketch and depth map.

    The function overlays the depth map (if provided) with reduced opacity to
    mimic shading. Real rendering would involve SDXL and ControlNet models.
    """

    src = _ensure_image(sketch_path)
    dst = src.with_name(src.stem + "_render" + src.suffix)

    if Image is None:
        shutil.copy(src, dst)
        return dst

    sketch = Image.open(src).convert("RGBA")
    if depth_path:
        depth = Image.open(depth_path).resize(sketch.size).convert("RGBA")
        depth.putalpha(128)
        sketch = Image.alpha_composite(sketch, depth)

    sketch = sketch.filter(ImageFilter.SMOOTH)
    sketch.save(dst)
    return dst
