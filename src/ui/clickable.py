import pygame
from typing import Tuple

from src.core.sources import load_sound


class ClickableArea:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            hover_sfx_path: str = "object_hover.mp3",
            click_sfx_path: str = "object_click.mp3",
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.hover_sound = load_sound(hover_sfx_path)
        self.click_sound = load_sound(click_sfx_path)
        self.is_hovered = False

    def check_click(self, pos: Tuple[float, float]) -> bool:
        if self.rect.collidepoint(pos):
            pygame.mixer.Sound(self.click_sound).play()
            return True
        return False

    def check_hover(self, pos: Tuple[float, float]) -> bool:
        if self.rect.collidepoint(pos):
            if not self.is_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.mixer.Sound(self.hover_sound).play()
                self.is_hovered = True
        else:
            if self.is_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.is_hovered = False
        return self.is_hovered

