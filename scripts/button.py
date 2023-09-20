import pygame

from text import Text
from filter import Filter

class Button:
    """
    Paramètres d'entrées :
        - Paramètres obligatoires : 
            - game (Game): instance de la classe Game
            - pos (tuple[int, int]) : position du centre du bouton
            - size (tuple[int, int]) : taille du bouton
        - Paramètre pour une image en fond : 
            - bg_image (str) : chemin vers l'image servant de fond
        - Paramètre pour une couleur en fond : 
            - bg_color (str | tuple[int, int, int]) : couleur du fond
        - Paramètres pour une image en contenu : 
            - content_img (str) : chemin vers l'image servant de contenu
            - content_size (tuple[int, int]) : taille de contenu
        - Paramètres pour un texte en contenu :
            - content_txt (str) : texte à afficher
            - font (str) : chemin vers la police du texte
            - font_size (int) : taille du texte
            - font_color (str | tuple[int, int, int]) : couleur du texte
    """

    def __init__(self, game, pos : tuple[int, int], size : tuple[int, int], **kwargs) -> None:
        self.game = game

        self.surface = None
        self.content = None

        for arg in kwargs:
            if arg == "bg_image":
                self.surface = pygame.image.load(kwargs[arg])
                self.surface = pygame.transform.scale(self.surface, size)
            elif arg == "bg_color":
                self.surface = pygame.surface.Surface(size)
                self.surface.fill(kwargs[arg])

            if arg == "content_img":
                self.content = pygame.image.load(kwargs[arg])
                self.content = pygame.transform.scale(self.content, kwargs["content_size"])
            elif arg == "content_txt":
                text =  Text(self.game, kwargs[arg], kwargs["font"], kwargs["font_size"], kwargs["font_color"])
                self.content = text.surface
            

        if self.surface is not None:
            self.rect = self.surface.get_rect(center=pos)
        if self.content is not None:
            self.content_rect = self.content.get_rect(center=pos)

        self.hover_filter = Filter(self.game, self.rect.center, self.rect[2:4], (0, 0, 0), 75)
        

    def draw(self) -> None:
        self.game.screen.blit(self.surface, self.rect)
        self.game.screen.blit(self.content, self.content_rect)

        self.hover()

    def collide_mouse(self) -> bool:
        return self.rect.collidepoint(self.game.mouse)

    def hover(self) -> None:
        if self.collide_mouse():
            self.hover_filter.draw()