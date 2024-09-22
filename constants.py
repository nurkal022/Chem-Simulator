import pygame

pygame.init()  # Initialize pygame here

WIDTH, HEIGHT = 1024, 768

COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "GRAY": (128, 128, 128),
    "YELLOW": (255, 255, 0),
    "LIGHT_BLUE": (173, 216, 230),
    "ORANGE": (255, 165, 0)
}

FONT_SMALL = pygame.font.Font(None, 24)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_LARGE = pygame.font.Font(None, 48)