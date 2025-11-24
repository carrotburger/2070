import pygame
from typing import Tuple

from src.config.text import FONT_SIZE_36
from src.core.sources import load_sound
from src.ui.colors import BUTTON_PRESSED_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, BUTTON_TEXT_COLOR


class Button:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            color: Tuple[int, int, int] = BUTTON_COLOR,
            hover_color: Tuple[int, int, int] = BUTTON_HOVER_COLOR,
            pressed_color: Tuple[int, int, int] = BUTTON_PRESSED_COLOR,
            border_color: Tuple[int, int, int] = BUTTON_BORDER_COLOR,
            text_color: Tuple[int, int, int] = BUTTON_TEXT_COLOR,
            hover_sfx_path: str = "menu_hover.mp3",
            click_sfx_path: str = "menu_click.mp3",
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.current_color = self.color
        self.border_color = border_color
        self.text_color = text_color
        self.hover_sound = load_sound(hover_sfx_path)
        self.click_sound = load_sound(click_sfx_path)
        self.font = pygame.font.SysFont(None, FONT_SIZE_36)
        self.is_hovered = False

    def check_click(self, pos: Tuple[float, float]) -> bool:
        if self.rect.collidepoint(pos):
            pygame.mixer.Sound(self.click_sound).play()
            return True
        return False

    def check_hover(self, pos: Tuple[float, float]) -> bool:
        if self.rect.collidepoint(pos):
            if not self.is_hovered:
                pygame.mixer.Sound(self.hover_sound).play()
                self.is_hovered = True
                self.current_color = self.hover_color
        else:
            if self.is_hovered:
                self.is_hovered = False
                self.current_color = self.color
        return self.is_hovered

    def draw(self,  screen: pygame.Surface):
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)