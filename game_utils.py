from pathlib import Path
from typing import Optional

import pygame

from game_constants import HEIGHT, PREFERRED_FONTS, WIDTH


def load_map_surface() -> pygame.Surface:
    project_dir = Path(__file__).resolve().parent
    map_path = project_dir / "map.png"
    if map_path.exists():
        image = pygame.image.load(str(map_path))
        return pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill((10, 18, 28))
    return surface


def load_font(size: int) -> pygame.font.Font:
    for name in PREFERRED_FONTS:
        font_path = pygame.font.match_font(name)
        if font_path:
            try:
                return pygame.font.Font(font_path, size)
            except Exception:
                continue
    return pygame.font.Font(None, size)

