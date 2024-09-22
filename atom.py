import pygame
import math
from typing import List, Tuple
from constants import COLORS, FONT_MEDIUM

class Atom:
    def __init__(self, symbol: str, color: Tuple[int, int, int], x: float, y: float):
        self.symbol = symbol
        self.color = color
        self.x = x
        self.y = y
        self.radius = 25
        self.dragging = False
        self.connected_to: List['Atom'] = []

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, COLORS["BLACK"], (int(self.x), int(self.y)), self.radius, 2)
        text = FONT_MEDIUM.render(self.symbol, True, COLORS["BLACK"])
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(text, text_rect)
        for atom in self.connected_to:
            self.draw_bond(surface, atom)

    def draw_bond(self, surface: pygame.Surface, other_atom: 'Atom'):
        angle = math.atan2(other_atom.y - self.y, other_atom.x - self.x)
        start_x = self.x + math.cos(angle) * self.radius
        start_y = self.y + math.sin(angle) * self.radius
        end_x = other_atom.x - math.cos(angle) * other_atom.radius
        end_y = other_atom.y - math.sin(angle) * other_atom.radius
        pygame.draw.line(surface, COLORS["BLACK"], (int(start_x), int(start_y)), (int(end_x), int(end_y)), 3)

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        return ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) <= self.radius ** 2

    def distance_to(self, other_atom: 'Atom') -> float:
        return math.sqrt((self.x - other_atom.x) ** 2 + (self.y - other_atom.y) ** 2)

    def connect_to(self, other_atom: 'Atom') -> bool:
        if other_atom not in self.connected_to and len(self.connected_to) < 4:
            self.connected_to.append(other_atom)
            other_atom.connected_to.append(self)
            angle = math.atan2(other_atom.y - self.y, other_atom.x - self.x)
            self.x = other_atom.x - math.cos(angle) * (self.radius + other_atom.radius)
            self.y = other_atom.y - math.sin(angle) * (self.radius + other_atom.radius)
            return True
        return False