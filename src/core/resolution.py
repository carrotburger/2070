from typing import Tuple

from src.config.display import BASE_RESOLUTION, ASPECT_RATIO


class ResolutionHandler:
    def __init__(self, current_resolution: Tuple[int, int]) -> None:
        self.current_resolution = current_resolution
        self.base_width, self.base_height = BASE_RESOLUTION
        self.base_aspect = ASPECT_RATIO

    def update_resolution(self, new_resolution: Tuple[int, int]) -> None:
        self.current_resolution = new_resolution

    def get_scaled_resolution(self) -> Tuple[int, int]:
        current_width, current_height = self.current_resolution
        current_aspect = current_width / current_height

        if current_aspect > self.base_aspect:
            new_height = current_height
            new_width = int(current_height * self.base_aspect)
        else:
            new_width = current_width
            new_height = int(current_width / self.base_aspect)

        return new_width, new_height