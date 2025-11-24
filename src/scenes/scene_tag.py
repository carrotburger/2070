from enum import Enum, unique

@unique
class SceneTag(Enum):
    MAIN_MENU = 1
    SAVES = 2
    SETTINGS = 3
    CLASS_ROOM = 4