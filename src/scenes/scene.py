from typing import List

import pygame

from src.scenes.scene_tag import SceneTag


class TerminateApp:
        pass


class NextScene:
    def __init__(self, tag: SceneTag):
        self.tag = tag

    def get_tag(self) -> SceneTag:
        return self.tag


class Handled:
        pass


class Scene:
    def __init__(self):
        pass

    def handle_events(self, events: List[pygame.event.Event]) -> Handled | NextScene | TerminateApp:
        pass

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        pass
