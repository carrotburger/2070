from typing import List, Optional

import pygame

from src.config.text import FONT_SIZE_36
from src.core.sources import load_sound, load_image
from src.core.text import split_text_on_lines, measure_multiline_text
from src.ui.colors import SURFACE_BACKGROUND, DIALOG_BORDER_COLOR, DEFAULT_TEXT_COLOR
from src.ui.phrase import Phrase


class DialogPanel:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            padding: int,
            line_spacing: int,
            option_hover_sfx: str,
    ):
        self.is_active = False
        self.object_image = None
        self.font = pygame.font.SysFont(None, FONT_SIZE_36)
        self.padding = padding
        self.line_spacing = line_spacing
        self.text_surface = None
        self.text_height = 0

        self.options = []
        self.rect = pygame.Rect(x, y, width, height)
        self.option_hover_sound = load_sound(option_hover_sfx)
        self.option_click_sound = load_sound(option_hover_sfx)

        self.hovered_index: Optional[int] = None

    def set_is_active(self, is_active: bool):
        self.is_active = is_active
        if not is_active:
            self.clear()

    def clear(self):
        self.is_active = False
        self.object_image = None
        self.text_surface = None
        self.text_height = 0
        self.options.clear()
        self.hovered_index = None

    def set_object_image(self, path: str):
        self.object_image = load_image(path)

    def set_content(self, text: str, options: List[str]):
        lines = split_text_on_lines(text, self.font, self.rect.width - 2 * self.padding)
        self.text_height = measure_multiline_text(lines, self.font, self.padding, self.line_spacing) + self.padding
        self.text_surface = pygame.Surface((self.rect.width, self.text_height), pygame.SRCALPHA)

        y_bottom = 0
        for line in lines:
            rendered = self.font.render(line, True, DEFAULT_TEXT_COLOR)
            self.text_surface.blit(rendered, (self.padding, y_bottom))
            y_bottom += rendered.get_height() + self.line_spacing

        self.options = []
        for option in options:
            self.options.append(Phrase(option, self.rect.width, self.padding, self.line_spacing))

    def handle_event(self, events: List[pygame.event.Event]) -> str | None:
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                current_y = self.text_height
                for i, phrase in enumerate(self.options):
                    if phrase.collidepoint(event.pos, self.rect.x, current_y):
                        if self.hovered_index != i:
                            pygame.mixer.Sound(self.option_hover_sound).play()
                            self.hovered_index = i
                            break
                    current_y += phrase.height

                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_y = self.text_height
                for option in self.options:
                    if option.collidepoint(event.pos, self.rect.x, current_y):
                        pygame.mixer.Sound(self.option_click_sound).play()
                        return "1"
                    current_y += option.height

        return None

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, SURFACE_BACKGROUND, self.rect)
        pygame.draw.rect(screen, DIALOG_BORDER_COLOR, self.rect, 2)
        if self.text_surface:
            screen.blit(self.text_surface, (self.rect.x, self.rect.y + self.padding))

        current_y = self.text_height + self.padding
        for i, phrase in enumerate(self.options):
            phrase.draw(screen, self.rect.x, current_y, hovered=(i == self.hovered_index))
            current_y += phrase.height
