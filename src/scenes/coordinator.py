import pygame

from src.core.resolution import ResolutionHandler
from src.core.sources import Resources
from src.repositories.consequences import ConsequencesRepository
from src.scenes.demo_class_room import ClassRoom
from src.scenes.menu import MainMenu
from src.scenes.scene import Scene
from src.scenes.scene_tag import SceneTag


class Coordinator:
    def __init__(
            self,
            screen: pygame.Surface,
            resolution_handler: ResolutionHandler,
            resources: Resources,
            consequences: ConsequencesRepository,
    ):
        self.resolution_handler = resolution_handler
        self.screen = screen
        self.resources = resources
        self.consequences = consequences

    def next_scene(self, tag: SceneTag) -> Scene:
        match tag:
            case SceneTag.MAIN_MENU:
                return MainMenu()
            case SceneTag.SAVES:
                return MainMenu()
            case SceneTag.MAIN_MENU:
                return MainMenu()
            case SceneTag.CLASS_ROOM:
                return ClassRoom(
                    self.screen,
                    self.resolution_handler,
                    self.resources,
                    self.consequences,
                )
        return MainMenu()
