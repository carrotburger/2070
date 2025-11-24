import pygame


# Params must be in range [0.0, 1.0]
def relative_rect(
    screen: pygame.Surface,
    rel_x: float,
    rel_y: float,
    rel_w: float,
    rel_h: float
) -> pygame.Rect:
    w, h = screen.get_size()
    return pygame.Rect(
        int(w * rel_x),
        int(h * rel_y),
        int(w * rel_w),
        int(h * rel_h)
    )