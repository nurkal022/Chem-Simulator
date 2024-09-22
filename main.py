from molecule_builder import MoleculeBuilder
import pygame

def main():
    game = MoleculeBuilder()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()