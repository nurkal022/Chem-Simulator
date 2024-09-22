import pygame
import sys
from typing import List, Dict, Tuple
from collections import Counter
from constants import WIDTH, HEIGHT, COLORS, FONT_SMALL, FONT_MEDIUM, FONT_LARGE
from atom import Atom
from button import Button

class MoleculeBuilder:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Enhanced Molecule Builder")
        
        self.atom_types = [
            {"symbol": "H", "color": COLORS["WHITE"]},
            {"symbol": "O", "color": COLORS["RED"]},
            {"symbol": "C", "color": COLORS["GRAY"]},
            {"symbol": "N", "color": COLORS["BLUE"]}
        ]
        self.levels = self.load_levels("levels.txt")
        self.building_area = pygame.Rect(250, 100, 724, 518)
        self.reset_button = Button(50, 700, 150, 50, "Reset", COLORS["RED"], COLORS["WHITE"])
        self.check_button = Button(250, 700, 150, 50, "Check", COLORS["GREEN"], COLORS["WHITE"])
        self.next_level_button = Button(450, 700, 150, 50, "Next Level", COLORS["BLUE"], COLORS["WHITE"])
        self.hint_button = Button(650, 700, 150, 50, "Hint", COLORS["YELLOW"], COLORS["BLACK"])
        self.current_level = 0
        self.level_complete = False
        self.score = 0
        self.message = ""
        self.hint = ""
        self.building_atoms: List[Atom] = []
        self.dragging_atom = None

    def load_levels(self, filename: str) -> List[Dict[str, str]]:
        levels = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    name, formula, display_formula, description = line.strip().split(',')
                    levels.append({
                        "name": name,
                        "formula": formula,
                        "display_formula": display_formula,
                        "description": description
                    })
            print(f"Loaded {len(levels)} levels from {filename}")
            return levels
        except FileNotFoundError:
            print(f"Error: {filename} not found. Using default levels.")
            return [
                {"name": "Water", "formula": "HHO", "display_formula": "H2O", "description": "Essential for life, forms oceans and rivers."},
                {"name": "Carbon Dioxide", "formula": "COO", "display_formula": "CO2", "description": "Greenhouse gas, used by plants in photosynthesis."}
            ]
        except Exception as e:
            print(f"Error loading levels: {e}. Using default levels.")
            return [
                {"name": "Water", "formula": "HHO", "display_formula": "H2O", "description": "Essential for life, forms oceans and rivers."},
                {"name": "Carbon Dioxide", "formula": "COO", "display_formula": "CO2", "description": "Greenhouse gas, used by plants in photosynthesis."}
            ]

    def reset_simulation(self):
        self.building_atoms = []
        self.message = ""
        self.hint = ""
        self.level_complete = False
        print("Simulation reset.")

    def check_molecule(self) -> bool:
        print("\n--- Starting molecule check ---")
        target_molecule = self.levels[self.current_level]['formula']
        built_molecule = ''.join(sorted([atom.symbol for atom in self.building_atoms]))
        
        target_count = Counter(target_molecule)
        built_count = Counter(built_molecule)
        
        print(f"Target molecule: {target_molecule}")
        print(f"Built molecule: {built_molecule}")
        print(f"Target atom count: {dict(target_count)}")
        print(f"Built atom count: {dict(built_count)}")
        
        if built_count != target_count:
            self.message = f"Incorrect. You built {''.join(built_molecule)}, but the target is {self.levels[self.current_level]['display_formula']}."
            print(f"Check failed: {self.message}")
            return False

        self.score += 100
        self.level_complete = True
        self.message = f"Correct! You built {self.levels[self.current_level]['name']} ({self.levels[self.current_level]['display_formula']})!"
        print(f"Check passed: {self.message}")
        return True

    def show_hint(self):
        current_level = self.levels[self.current_level]
        self.hint = f"Hint: {current_level['name']} ({current_level['display_formula']}) - {current_level['description']}"
        print(f"Showing hint: {self.hint}")

    def draw(self):
        self.screen.fill(COLORS["LIGHT_BLUE"])
        pygame.draw.rect(self.screen, COLORS["WHITE"], self.building_area)
        pygame.draw.rect(self.screen, COLORS["BLACK"], self.building_area, 2)

        for i, atom_type in enumerate(self.atom_types):
            pygame.draw.rect(self.screen, atom_type["color"], (50, i * 100 + 100, 150, 80))
            pygame.draw.rect(self.screen, COLORS["BLACK"], (50, i * 100 + 100, 150, 80), 2)
            text = FONT_MEDIUM.render(atom_type["symbol"], True, COLORS["BLACK"])
            self.screen.blit(text, (110, i * 100 + 130))

        for atom in self.building_atoms:
            atom.draw(self.screen)

        level_text = FONT_LARGE.render(f"Level {self.current_level + 1}: Build {self.levels[self.current_level]['name']} ({self.levels[self.current_level]['display_formula']})", True, COLORS["BLACK"])
        self.screen.blit(level_text, (250, 20))

        score_text = FONT_MEDIUM.render(f"Score: {self.score}", True, COLORS["BLACK"])
        self.screen.blit(score_text, (900, 20))

        message_color = COLORS["GREEN"] if "Correct" in self.message else COLORS["RED"]
        message_text = FONT_MEDIUM.render(self.message, True, message_color)
        self.screen.blit(message_text, (250, 650))

        if self.hint:
            hint_text = FONT_SMALL.render(self.hint, True, COLORS["BLACK"])
            self.screen.blit(hint_text, (250, 60))

        self.reset_button.draw(self.screen)
        self.check_button.draw(self.screen)
        self.hint_button.draw(self.screen)
        if self.level_complete:
            self.next_level_button.draw(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.reset_button.is_clicked(event.pos):
                        print("Reset button clicked.")
                        self.reset_simulation()
                    elif self.check_button.is_clicked(event.pos):
                        print("Check button clicked. Performing molecule check...")
                        self.check_molecule()
                    elif self.hint_button.is_clicked(event.pos):
                        print("Hint button clicked.")
                        self.show_hint()
                    elif self.level_complete and self.next_level_button.is_clicked(event.pos):
                        print("Next level button clicked.")
                        self.current_level += 1
                        if self.current_level >= len(self.levels):
                            self.message = "Congratulations! You've completed all levels!"
                            print(self.message)
                            running = False
                        else:
                            print(f"Moving to level {self.current_level + 1}")
                            self.reset_simulation()
                    else:
                        for atom_type in self.atom_types:
                            if pygame.Rect(50, self.atom_types.index(atom_type) * 100 + 100, 150, 80).collidepoint(event.pos):
                                new_atom = Atom(atom_type["symbol"], atom_type["color"], event.pos[0], event.pos[1])
                                self.dragging_atom = new_atom
                                print(f"Created new {new_atom.symbol} atom")
                                break
                        if not self.dragging_atom:
                            for atom in self.building_atoms:
                                if atom.is_clicked(event.pos):
                                    self.dragging_atom = atom
                                    print(f"Started dragging {self.dragging_atom.symbol} atom")
                                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dragging_atom:
                        if self.building_area.collidepoint(self.dragging_atom.x, self.dragging_atom.y):
                            if self.dragging_atom not in self.building_atoms:
                                self.building_atoms.append(self.dragging_atom)
                                print(f"Added {self.dragging_atom.symbol} atom to building area")
                            for atom in self.building_atoms:
                                if atom != self.dragging_atom and self.dragging_atom.distance_to(atom) < self.dragging_atom.radius + atom.radius + 5:
                                    if self.dragging_atom.connect_to(atom):
                                        print(f"Connected {self.dragging_atom.symbol} to {atom.symbol}")
                                    break
                        else:
                            if self.dragging_atom in self.building_atoms:
                                self.building_atoms.remove(self.dragging_atom)
                                print(f"Removed {self.dragging_atom.symbol} atom from building area")
                                for atom in self.dragging_atom.connected_to:
                                    atom.connected_to.remove(self.dragging_atom)
                                    print(f"Disconnected {self.dragging_atom.symbol} from {atom.symbol}")
                        self.dragging_atom = None

            if self.dragging_atom:
                self.dragging_atom.x, self.dragging_atom.y = pygame.mouse.get_pos()

            self.draw()
            pygame.display.flip()
            clock.tick(60)