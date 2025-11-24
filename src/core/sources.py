import pygame
import os

def load_image(path: str) -> pygame.Surface:
    full_path = os.path.join("assets", "images", path)
    return pygame.image.load(full_path).convert_alpha()

def load_sound(path: str) -> pygame.mixer.Sound:
    full_path = os.path.join("assets", "sounds", "sfx", path)
    return pygame.mixer.Sound(full_path)

def load_theme(path: str) -> str:
    full_path = os.path.join("assets", "sounds", "theme", path)
    return full_path