import pygame

class Filter:

    def __init__(self, game, pos, size, color, alpha):
        self.game = game

        self.surface = pygame.surface.Surface(size)
        self.surface.set_alpha(alpha)
        self.surface.fill(color)

        self.change_pos(pos)

    def change_pos(self, pos):
        self.rect = self.surface.get_rect(center=pos)

    def change_alpha(self, alpha):
        self.surface.set_alpha(alpha)

    def draw(self):
        self.game.screen.blit(self.surface, self.rect)