import pygame

from text import Text
from filter import Filter

class Input:

    def __init__(self, game, pos, size, max_v, len_champ, bg_color, ct_color, font, font_size, end) -> None:
        self.game = game
        self.pos = pos
        self.max_v = max_v
        self.len_champ = len_champ
        self.ct_color = ct_color
        self.font = font
        self.font_size = font_size
        self.end = end

        self.surface = pygame.surface.Surface(size)
        self.surface.fill(bg_color)
        self.rect = self.surface.get_rect(center=pos)

        self.filter = Filter(self.game, pos, size, (0, 0, 0), 0)

        self.value = ""

        self.targeted = False

        self.change_ct(" ")

    def change_ct(self, d_value):
        d_value = str(d_value)
        if d_value == "":
            pass
        elif d_value == " ":
            self.value = self.value[:-1]
        elif int(self.value + d_value) <= self.max_v :
            self.value += d_value
        
        if self.value != "":
            if self.value[0] == "0" and len(self.value) == 2:
                self.value = self.value[1]

        compens = " " * (self.len_champ - len(str(self.value)))
        self.content = Text(self.game, f"{compens + self.value}{self.end}", self.font, self.font_size, self.ct_color, self.pos)
        self.ct_surface = self.content.surface
        self.ct_rect = self.content.rect

    def draw(self):
        self.game.screen.blit(self.surface, self.rect)
        self.game.screen.blit(self.ct_surface, self.ct_rect)

        if self.targeted:
            self.filter.change_alpha(70)
            self.game.screen.blit(self.filter.surface, self.filter.rect)
        else:
            self.filter.change_alpha(0)

    def collide_mouse(self) -> bool:
        return self.rect.collidepoint(self.game.mouse)