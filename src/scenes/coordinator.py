import pygame

from src.core.resolution import ResolutionHandler
from src.scenes.class_room import ClassRoom
from src.scenes.menu import MainMenu
from src.scenes.scene import Scene
from src.scenes.scene_tag import SceneTag


class Coordinator:
    def __init__(self, screen: pygame.Surface, resolution_handler: ResolutionHandler):
        self.resolution_handler = resolution_handler
        self.screen = screen

    def next_scene(self, tag: SceneTag) -> Scene:
        match tag:
            case SceneTag.MAIN_MENU:
                return MainMenu()
            case SceneTag.SAVES:
                return MainMenu()
            case SceneTag.MAIN_MENU:
                return MainMenu()
            case SceneTag.CLASS_ROOM:
                return ClassRoom(self.screen, self.resolution_handler)
        return MainMenu()
