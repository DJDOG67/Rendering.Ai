# Rendering.Ai

Prototype Windows application for sketch-based rendering with AI assistance.

This repository contains a minimal PyQt5 application and placeholder backend
modules. The target architecture is based on the following components:

- **UI Framework:** PyQt5
- **AI Backend:** Stable Diffusion XL + ControlNet (Canny, Depth) + IPAdapter
- **Depth Model:** MiDaS DPT-Large
- **Preset Storage:** JSON files
- **Local Execution:** ONNX models
- **Project Format:** `.srproj`
- **Preset UI:** Thumbnail and name list

The code here is a starting point and does not include actual model files.

## Running

```bash
python app/main.py
```

This launches a simple window with buttons for uploading a sketch, cleaning it
up, and running a render. Backend functions in `backend/renderer.py` are
placeholders that should be replaced with real implementations.

## Presets

Example presets are stored in the `presets/` directory. Use `app/presets.py` to
load or save presets programmatically.

