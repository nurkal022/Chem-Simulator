import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Molecule Builder")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Atom class
class Atom:
    def __init__(self, symbol, color, x, y):
        self.symbol = symbol
        self.color = color
        self.x = x
        self.y = y
        self.radius = 20
        self.dragging = False
        self.connected_to = []

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        text = font.render(self.symbol, True, BLACK)
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(text, text_rect)
        for atom in self.connected_to:
            self.draw_bond(surface, atom)

    def draw_bond(self, surface, other_atom):
        angle = math.atan2(other_atom.y - self.y, other_atom.x - self.x)
        start_x = self.x + math.cos(angle) * self.radius
        start_y = self.y + math.sin(angle) * self.radius
        end_x = other_atom.x - math.cos(angle) * other_atom.radius
        end_y = other_atom.y - math.sin(angle) * other_atom.radius
        pygame.draw.line(surface, BLACK, (int(start_x), int(start_y)), (int(end_x), int(end_y)), 2)

    def is_clicked(self, pos):
        return ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) <= self.radius ** 2

    def distance_to(self, other_atom):
        return math.sqrt((self.x - other_atom.x) ** 2 + (self.y - other_atom.y) ** 2)

    def connect_to(self, other_atom):
        if other_atom not in self.connected_to and len(self.connected_to) < 4:  # Limit connections to 4
            self.connected_to.append(other_atom)
            other_atom.connected_to.append(self)
            # Adjust positions to connect at the edge
            angle = math.atan2(other_atom.y - self.y, other_atom.x - self.x)
            self.x = other_atom.x - math.cos(angle) * (self.radius + other_atom.radius)
            self.y = other_atom.y - math.sin(angle) * (self.radius + other_atom.radius)

# Available atom types
atom_types = [
    {"symbol": "H", "color": WHITE},
    {"symbol": "O", "color": RED},
    {"symbol": "C", "color": GRAY},
    {"symbol": "N", "color": BLUE}
]

# Molecule building area
building_area = pygame.Rect(200, 50, 550, 400)

# Levels (molecules to build)
levels = [
    {"name": "Water", "formula": "H2O"},
    {"name": "Carbon Dioxide", "formula": "CO2"},
    {"name": "Nitrogen Dioxide", "formula": "NO2"},
    {"name": "Ammonia", "formula": "NH3"}
]
current_level = 0

# Atoms in the building area
building_atoms = []

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Reset button
reset_button = Button(650, 500, 100, 50, "Reset", RED, WHITE)

# Next level button (initially hidden)
next_level_button = Button(500, 500, 150, 50, "Next Level", GREEN, WHITE)

# Game loop
running = True
dragging_atom = None
message = ""
level_complete = False

def reset_simulation():
    global building_atoms, message, level_complete
    building_atoms = []
    message = ""
    level_complete = False

def check_molecule():
    if len(building_atoms) != len(levels[current_level]['formula']):
        return False

    # Проверка количества атомов
    atom_count = {}
    for atom in building_atoms:
        atom_count[atom.symbol] = atom_count.get(atom.symbol, 0) + 1

    target_count = {}
    for symbol in levels[current_level]['formula']:
        target_count[symbol] = target_count.get(symbol, 0) + 1

    if atom_count != target_count:
        return False

    # Проверка структуры молекулы
    if levels[current_level]['name'] == "Water":
        oxygen = next((atom for atom in building_atoms if atom.symbol == 'O'), None)
        if oxygen is None or len(oxygen.connected_to) != 2:
            return False
        if not all(atom.symbol == 'H' for atom in oxygen.connected_to):
            return False
    elif levels[current_level]['name'] == "Carbon Dioxide":
        carbon = next((atom for atom in building_atoms if atom.symbol == 'C'), None)
        if carbon is None or len(carbon.connected_to) != 2:
            return False
        if not all(atom.symbol == 'O' for atom in carbon.connected_to):
            return False
    elif levels[current_level]['name'] == "Nitrogen Dioxide":
        nitrogen = next((atom for atom in building_atoms if atom.symbol == 'N'), None)
        if nitrogen is None or len(nitrogen.connected_to) != 2:
            return False
        if not all(atom.symbol == 'O' for atom in nitrogen.connected_to):
            return False
    elif levels[current_level]['name'] == "Ammonia":
        nitrogen = next((atom for atom in building_atoms if atom.symbol == 'N'), None)
        if nitrogen is None or len(nitrogen.connected_to) != 3:
            return False
        if not all(atom.symbol == 'H' for atom in nitrogen.connected_to):
            return False

    return True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button.is_clicked(event.pos):
                reset_simulation()
            elif level_complete and next_level_button.is_clicked(event.pos):
                current_level += 1
                if current_level >= len(levels):
                    print("Congratulations! You've completed all levels!")
                    running = False
                else:
                    reset_simulation()
            else:
                for atom_type in atom_types:
                    if pygame.Rect(50, atom_types.index(atom_type) * 100 + 50, 100, 100).collidepoint(event.pos):
                        new_atom = Atom(atom_type["symbol"], atom_type["color"], event.pos[0], event.pos[1])
                        dragging_atom = new_atom
                        break
                if not dragging_atom:
                    for atom in building_atoms:
                        if atom.is_clicked(event.pos):
                            dragging_atom = atom
                            break
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_atom:
                if building_area.collidepoint(dragging_atom.x, dragging_atom.y):
                    if dragging_atom not in building_atoms:
                        building_atoms.append(dragging_atom)
                    for atom in building_atoms:
                        if atom != dragging_atom and dragging_atom.distance_to(atom) < dragging_atom.radius + atom.radius + 5:
                            dragging_atom.connect_to(atom)
                            break
                else:
                    if dragging_atom in building_atoms:
                        building_atoms.remove(dragging_atom)
                        for atom in dragging_atom.connected_to:
                            atom.connected_to.remove(dragging_atom)
                dragging_atom = None

    # Update positions of dragged atoms
    if dragging_atom:
        dragging_atom.x, dragging_atom.y = pygame.mouse.get_pos()

    # Clear the screen
    screen.fill(WHITE)

    # Draw building area
    pygame.draw.rect(screen, (200, 200, 200), building_area)

    # Draw atom menu
    for i, atom_type in enumerate(atom_types):
        pygame.draw.rect(screen, atom_type["color"], (50, i * 100 + 50, 100, 100))
        text = font.render(atom_type["symbol"], True, BLACK)
        screen.blit(text, (85, i * 100 + 85))

    # Draw atoms in building area
    for atom in building_atoms:
        atom.draw(screen)

    # Draw current level info
    level_text = font.render(f"Level {current_level + 1}: Build {levels[current_level]['name']} ({levels[current_level]['formula']})", True, BLACK)
    screen.blit(level_text, (200, 10))

    # Check if the correct molecule is built
    if not level_complete and check_molecule():
        message = f"Correct! You built {levels[current_level]['name']}!"
        level_complete = True
    elif len(building_atoms) > 0 and not level_complete:
        message = "Keep building..."
    
    # Draw message
    message_text = font.render(message, True, GREEN if "Correct" in message else BLACK)
    screen.blit(message_text, (200, 500))

    # Draw reset button
    reset_button.draw(screen)

    # Draw next level button if level is complete
    if level_complete:
        next_level_button.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()