from typing import List

import pygame

from src.core.resolution import ResolutionHandler
from src.core.sources import load_image, load_theme
from src.entities.interactable import Interactable
from src.scenes.scene import Scene, Handled, NextScene, TerminateApp
from src.ui.clickable import ClickableArea
from src.ui.dialog import DialogPanel
from src.ui.geometry import relative_rect


class ClassRoom(Scene):
    def __init__(self, screen: pygame.Surface, resolution_handler: ResolutionHandler):
        super().__init__()
        self.screen = screen
        self.resolution_handler = resolution_handler
        self.background = load_image("background/class_room.png")
        self.background = pygame.transform.scale(self.background, self.resolution_handler.get_scaled_resolution())
        teacher_rect = relative_rect(screen, 0.475, 0.175, 0.115, 0.75)
        self.teacher = ClickableArea(teacher_rect.x, teacher_rect.y, teacher_rect.width, teacher_rect.height)

        self.theme = load_theme("fucking_school.mp3")
        pygame.mixer.music.load(self.theme)
        pygame.mixer.music.play(-1)

        dialog_rec = relative_rect(screen, 0.70, 0.0, 0.28, 1.0)
        self.dialog_panel = DialogPanel(dialog_rec.x, dialog_rec.y, dialog_rec.width, dialog_rec.height,
                                        padding=12, line_spacing=4, option_hover_sfx="option_hover.mp3")
        self.character = None
        self.overlay = None
        self.transition_target = None

    def on_area_click(self, area_id: str):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.character = Interactable(area_id)
        overlay_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 128))
        self.overlay = overlay_surface
        test_text = "\"This old, silly old man is saying something...\": How long can you sleep, you idiot! Class is no place for sleeping! Get out!"
        test_options = [
            "Get out you!",
            "Please, excuse me!",
            "*Continue sleeping!*",
            "*Escape this lesson*",
        ]
        self.dialog_panel.set_content(test_text, test_options)
        self.dialog_panel.set_is_active(True)

    def handle_events(self, events: List[pygame.event.Event]) -> Handled | NextScene | TerminateApp:
        if self.dialog_panel.text_height:
            if self.dialog_panel.handle_event(events):
                self.dialog_panel.set_is_active(False)
                self.overlay = None
            return Handled()

        for event in events:
            if event.type == pygame.QUIT:
                return TerminateApp()
            if event.type == pygame.MOUSEMOTION:
                self.teacher.check_hover(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.teacher.check_click(event.pos):
                    self.on_area_click("kek")
            if event.type == pygame.VIDEORESIZE:
                self.resolution_handler.update_resolution((event.w, event.h))
                self.background = pygame.transform.scale(self.background,
                                                         self.resolution_handler.get_scaled_resolution())
        return Handled()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, (0, 0))
        if self.overlay:
            screen.blit(self.overlay, (0, 0))
        if self.dialog_panel.is_active:
            self.dialog_panel.draw(screen)
