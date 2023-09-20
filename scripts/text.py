import pygame

class Text:
    """
    Paramètres d'entrées : 
        - game (Game) : instance de la classe Game
        - text (str) : texte à afficher
        - font (str) : police utilisée
        - font_size (int) : taille de texte
        - font_color (str | tuple[int, int, int]) : couleur du texte
        - pos (tuple[int, int]) : position du texte
    """

    def __init__(self, game, text, font, font_size, font_color, pos=(0, 0)) -> None:
        self.game = game

        used_font = pygame.font.Font(font, font_size)
        self.surface = used_font.render(text, True, font_color)
        self.rect = self.surface.get_rect(center=pos)

    def draw(self):
        self.game.screen.blit(self.surface, self.rect)