from typing import List

import pygame

from src.scenes.scene import Scene, Handled, NextScene, TerminateApp
from src.scenes.scene_tag import SceneTag
from src.ui.button import Button
from src.ui.colors import SURFACE_BACKGROUND


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        self.start_button = Button(400, 200, 200, 50, "Start", click_sfx_path="menu_start.mp3")
        self.saves_button = Button(400, 300, 200, 50, "Saves")
        self.settings_button = Button(400, 400, 200, 50, "Settings")
        self.exit_button = Button(400, 500, 200, 50, "Exit")

    def handle_events(self, events: List[pygame.event.Event]) -> Handled | NextScene | TerminateApp:
        for event in events:
            if event.type == pygame.QUIT:
                return TerminateApp()
            if event.type == pygame.MOUSEMOTION:
                self.start_button.check_hover(event.pos)
                self.saves_button.check_hover(event.pos)
                self.settings_button.check_hover(event.pos)
                self.exit_button.check_hover(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.check_click(event.pos):
                    return NextScene(SceneTag.CLASS_ROOM)
                if self.saves_button.check_click(event.pos):
                    return NextScene(SceneTag.SAVES)
                if self.settings_button.check_click(event.pos):
                    return NextScene(SceneTag.SETTINGS)
                if self.exit_button.check_click(event.pos):
                    return TerminateApp()
        return Handled()

    def draw(self, screen):
        screen.fill(SURFACE_BACKGROUND)
        self.start_button.draw(screen)
        self.saves_button.draw(screen)
        self.settings_button.draw(screen)
        self.exit_button.draw(screen)
