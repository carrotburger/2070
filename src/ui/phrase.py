from typing import Tuple

import pygame

from src.config.text import FONT_SIZE_36
from src.core.text import split_text_on_lines, measure_multiline_text
from src.ui.colors import TRANSPARENT, OPTION_HOVER_COLOR, OPTION_SIMPLE_TEXT_COLOR


class Phrase:
    def __init__(
            self,
            text: str,
            available_width: int,
            padding: int = 12,
            line_spacing: int = 2,
            text_color: Tuple[int, int, int] = OPTION_SIMPLE_TEXT_COLOR,
            hover_bg: Tuple[int, int, int] = OPTION_HOVER_COLOR,
    ) -> None:
        self.available_width = available_width
        font = pygame.font.SysFont(None, FONT_SIZE_36)
        self.lines = split_text_on_lines(text, font, available_width - 2 * padding)
        self.height = measure_multiline_text(self.lines, font, padding, line_spacing)

        self.text_surface = pygame.Surface((available_width, self.height), pygame.SRCALPHA)
        self.hover_surface = pygame.Surface((available_width, self.height), pygame.SRCALPHA)
        self.hover_surface.fill(hover_bg)

        y = padding
        for line in self.lines:
            rendered = font.render(line, True, text_color)
            self.text_surface.blit(rendered, (padding, y))
            y += rendered.get_height() + line_spacing

    def draw(self, surface: pygame.Surface, x: int, y: int, hovered: bool = False) -> None:
        if hovered:
            surface.blit(self.hover_surface, (x, y))
        surface.blit(self.text_surface, (x, y))

    def collidepoint(self, pos: Tuple[float, float], x_right: float, y_top: float) -> bool:
        x, y = pos
        return x_right <= x < self.available_width + x_right and y_top <= y < y_top + self.height
