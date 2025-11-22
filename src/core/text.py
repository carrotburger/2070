from typing import List, Tuple

import pygame


def split_text_on_lines(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current.rstrip())
            current = word + " "
    if current:
        lines.append(current.rstrip())
    return lines


def measure_multiline_text(lines: List[str], font: pygame.font.Font, padding: int, line_spacing: int) -> int:
    total_h = sum(font.size(line)[1] for line in lines) + max(0, len(lines) - 1) * line_spacing
    return total_h + 2 * padding
