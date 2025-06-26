# Rendering.Ai

Prototype Windows application for sketch-based rendering with AI assistance. The goal is to keep the original sketch while applying style, texture and lighting information to produce a Photoshop-like render.

## Project Overview

- **Target users:** product, industrial and automotive designers, illustrators
- **Environment:** Windows 10+, GPU recommended, works offline
- **Distribution:** packaged as a standalone `.exe` with an installer

## Core Features

| Group | Feature | Notes |
|-------|---------|------|
| **Input** | Sketch upload | JPG/PNG/PSD supported |
| **Pre‑process** | Sketch cleanup | Noise removal and contrast enhancement |
| **Depth** | Automatic MiDaS DPT-Large | Visualised as a heatmap |
| **Depth Edit** | Manual corrections | Brush/slider tools |
| **Lighting** | Text based control | e.g. "from top left" |
| **Texture** | Per part materials | e.g. "door: metal" |
| **Background** | Style description | e.g. "white studio" |
| **Style** | Photo style extraction | Keywords shown in English |
| **Rendering** | SDXL + ControlNet + IPAdapter | ONNX runtime |
| **Project** | `.srproj` save/load | Zip containing sketch, depth and settings |
| **Presets** | JSON based styles | Managed with thumbnail list |

## GUI Flow

1. **Sketch tab** – upload and optionally clean the sketch
2. **Depth tab** – view automatic depth heatmap and edit
3. **Lighting / Texture tab** – set lighting angle, part materials and background
4. **Preset tab** – apply or create style presets
5. **Render tab** – generate final image and preview
6. **Save tab** – export `.srproj` and rendered images

## File Structure

```
user_presets.json    # stored presets
render_cache/        # temporary render outputs
projects/*.srproj    # saved projects
```

## Running

```bash
python app/main.py
```

A simple PyQt5 window will open. The backend in `backend/renderer.py` and project
utilities in `app/project.py` are placeholders and need proper model
integration.

## Packaging

The final application is intended to be packaged with **PyInstaller** and
shipped using an **NSIS** installer.
