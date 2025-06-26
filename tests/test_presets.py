import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/"src"))
from presets import Preset, load_presets, save_presets, PRESETS_FILE
import os


def test_save_load(tmp_path):
    orig = [Preset(name="test", settings={"a": 1}, thumbnail=None)]
    old_file = PRESETS_FILE
    try:
        test_file = tmp_path / "p.json"
        globals()['PRESETS_FILE'] = test_file
        save_presets(orig)
        loaded = load_presets()
        assert len(loaded) == 1
        assert loaded[0].name == "test"
        assert loaded[0].settings["a"] == 1
    finally:
        globals()['PRESETS_FILE'] = old_file
