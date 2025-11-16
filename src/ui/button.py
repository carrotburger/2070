import pygame
from typing import Tuple

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (70, 70, 70)
        self.hover_color = (100, 100, 100)
        self.pressed_color = (50, 50, 50)
        self.current_color = self.color
        self.font = pygame.font.SysFont(None, 24)
        self.is_hovered = False

    def check_click(self, pos: Tuple[float, float]):
        if self.rect.collidepoint(pos):
            return True
        return False

    def check_hover(self, pos: Tuple[float, float]):
        if self.rect.collidepoint(pos):
            if not self.is_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.is_hovered = True
            self.current_color = self.hover_color
        else:
            if self.is_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.is_hovered = False
            self.current_color = self.color

    def draw(self,  screen: pygame.Surface):
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)