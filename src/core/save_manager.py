# src/core/save_manager.py

from pathlib import Path
import json
from src.scenes.scene_tag import SceneTag

SAVE_PATH = Path("save.json")


def save_scene(tag: SceneTag) -> None:
    data = {"scene": tag.name}  # "CLASS_ROOM" など
    with SAVE_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f)


def load_scene() -> SceneTag | None:
    if not SAVE_PATH.exists():
        return None

    with SAVE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    name = data.get("scene")
    if not name:
        return None

    try:
        return SceneTag[name]  # "CLASS_ROOM" → SceneTag.CLASS_ROOM
    except KeyError:
        return None