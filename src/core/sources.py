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


class Resources:
    class Resources:
        def __init__(self, default_locale="en_US"):
            self.locale = default_locale

        def change_locale(self, locale: str):
            self.locale = locale

        def get_string(self, id: str) -> str:
            """Returns the localized string resource associated with the given identifier.

            Args:
                id (str): The unique key identifying the string resource.

            Returns:
                str: The localized string corresponding to the provided identifier.
            """
            # TODO(@carrotburger) implement real localisation, now the method just return id back
            return id
