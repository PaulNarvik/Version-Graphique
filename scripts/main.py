import pygame
import sys
import random

from roulette import Roulette
from text import Text
from button import Button
from filter import Filter
from input import Input
from constants import *

class Game:

    def __init__(self) -> None:
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = self.SCREEN_WIDTH * 3 / 4

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Jeu du Casino")

        self.mouse = None

        self.clock = pygame.time.Clock()
        self.dt = 1
        self.FPS = 30

        self.game_mode = "chance"

        self.in_game = False

        self.balance = 100

        self.choice = None
        self.mise = 0

        self.get_elements()
        self.new_game()

    def get_elements(self):
        # Commun à tous les écrans
        self.background = pygame.image.load("./assets/background.png")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.background_rect = self.background.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        # Écran titre
        self.title = Text(self, "Jeu du Casino", PRSTARTK, int(self.SCREEN_HEIGHT // 14), (200, 50, 50), (500, 50))
        self.game_mode_1 = Text(self, "Choisissez un", PRSTARTK, int(self.SCREEN_HEIGHT // 20), (0, 0, 0), (500, 150))
        self.game_mode_2 = Text(self, "mode de jeu", PRSTARTK, int(self.SCREEN_HEIGHT // 20), (0, 0, 0), (500, 200))

        self.play = Button(self, (500, 520), (300, 90), bg_color=(255, 255, 255), content_txt="Jouer", font=PRSTARTK, font_size=int(self.SCREEN_HEIGHT // 20), font_color=(0, 0, 0))
        self.chance_button = Button(self, (500, 300), (375, 75), bg_color=(255, 255, 255), content_txt="Chance Simple", font=PRSTARTK, font_size=int(self.SCREEN_HEIGHT // 25), font_color=(0, 0, 0))
        self.numero_button = Button(self, (500, 400), (375, 75), bg_color=(255, 255, 255), content_txt="Numéro Plein", font=PRSTARTK, font_size=int(self.SCREEN_HEIGHT // 25), font_color=(0, 0, 0))

        self.selected_game = Filter(self, self.chance_button.rect.center, self.chance_button.rect[2:4], (0, 0, 255), 90)

        # Jeu - Commun aux deux jeux
        self.mise_label = Text(self, "Mise : ", PRSTARTK, 17, (0, 0, 0), (572, 170))
        self.mise_input = Input(self, (690, 170), (115, 35), min(self.balance, 99999), 5, (255, 255, 255), (0, 0, 0), PRSTARTK, 17, "€")
        self.exit_button = Button(self, (630, 520), (220, 60), bg_color=(255, 255, 255), content_txt="Quitter", font=PRSTARTK, font_size=int(self.SCREEN_HEIGHT // 25), font_color=(0, 0, 0))
        self.valid_button = Button(self, (630, 440), (220, 60), bg_color=(255, 255, 255), content_txt="Lancer", font=PRSTARTK, font_size=int(self.SCREEN_HEIGHT // 25), font_color=(0, 0, 0))

        # Jeu - Chance simple
        self.chance_title = Text(self, "Chance Simple", PRSTARTK, 30, (200, 50, 50), (575, 50))
        self.choix_label = Text(self, "Choix : ", PRSTARTK, 17, (0, 0, 0), (580, 220))
        self.pair_button = Button(self, (572, 275), (120, 45), bg_color=(255, 255, 255), content_txt="Pair", font=PRSTARTK, font_size=17, font_color=(0, 0, 0))
        self.impair_button = Button(self, (710, 275), (120, 45), bg_color=(255, 255, 255), content_txt="Impair", font=PRSTARTK, font_size=17, font_color=(0, 0, 0))

        self.selected_choice = Filter(self, self.pair_button.rect.center, self.pair_button.rect[2:4], (0, 0, 255), 90)

        # Jeu - Numéro plein
        self.numero_title = Text(self, "Numéro Plein", PRSTARTK, 30, (200, 50, 50), (575, 50))

        self.numero_label = Text(self, "Nombre : ", PRSTARTK, 17, (0, 0, 0), (588, 220))
        self.numero_input = Input(self, (688, 220), (40, 35), 36, 2, (255, 255, 255), 0, PRSTARTK, 17, "")

        self.change_values_elements()

    def change_values_elements(self):
        compens = " " * (10 - len(str(self.balance)))
        self.balance_label = Text(self, f"Balance : {self.balance}€ {compens}", PRSTARTK, 17, (0, 0, 0), (700, 120))
        self.mise_input.max = min(self.balance, 99999)

    def new_game(self):
        self.roulette = Roulette(self)

        self.main()

    def reset_inputs(self):
        for i in range(5):
            self.mise_input.change_ct(" ")
            self.numero_input.change_ct(" ")

    def handle_events(self):
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.in_game:
                    if self.play.collide_mouse():
                        self.in_game = True
                        self.roulette.transition(6)
                        if self.game_mode == "chance":
                            self.choice = "pair"
                    elif self.chance_button.collide_mouse():
                        self.game_mode = "chance"
                        self.selected_game.change_pos((500, 300))
                    elif self.numero_button.collide_mouse():
                        self.game_mode = "numero"
                        self.selected_game.change_pos((500, 400))

                else:
                    if self.exit_button.collide_mouse():
                        self.reset_inputs()
                        self.roulette.transition(-6)
                        self.in_game = False
                        self.choice = None
                        self.mise = 0
                    elif self.valid_button.collide_mouse():
                        if not (self.choice == None or self.choice == "" or self.mise == 0 or self.mise == ""):
                            self.number = random.randint(0, 36)
                            self.balance -= self.mise
                            self.change_values_elements()
                            self.win_check()

                    if self.game_mode == "chance":
                        if self.pair_button.collide_mouse():
                            self.choice = "pair"
                            self.selected_choice.change_pos((572, 275))
                        if self.impair_button.collide_mouse():
                            self.choice = "impair"
                            self.selected_choice.change_pos((710, 275))

                if self.mise_input.collide_mouse():
                    if self.in_game == True:
                        self.mise_input.targeted = True
                        self.numero_input.targeted = False
                elif self.numero_input.collide_mouse():
                    if self.in_game == True and self.game_mode == "numero":
                        self.numero_input.targeted = True
                        self.mise_input.targeted = False
                else:
                    self.mise_input.targeted = False
                    self.numero_input.targeted = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    d_value = " "
                elif 1073741913 <= event.key <= 1073741923:
                        d_value = str(event.key - 1073741912)[-1]
                elif 48 <= event.key <= 57:
                    d_value = event.key - 48
                else:
                    d_value = ""
                if self.mise_input.targeted:
                    self.mise_input.change_ct(d_value)
                if self.numero_input.targeted:
                    self.numero_input.change_ct(d_value)

                if not self.game_mode == "chance":
                    self.choice = self.numero_input.value
                self.mise = int(self.mise_input.value) if self.mise_input.value != "" else 0

    def update(self):
        pygame.display.flip()
        self.dt = self.clock.tick(self.FPS)
        pygame.display.set_caption(f"Jeu du Casino - {self.clock.get_fps() : .1f}")

    def draw(self):
        self.screen.blit(self.background, self.background_rect)

        self.roulette.draw()

        if not self.in_game:
            self.title.draw()
            self.game_mode_1.draw()
            self.game_mode_2.draw()

            self.play.draw()
            self.chance_button.draw()
            self.numero_button.draw()

            self.selected_game.draw()
        else:
            self.balance_label.draw()
            self.mise_label.draw()
            self.mise_input.draw()
            self.exit_button.draw()
            self.valid_button.draw()

            if self.game_mode == "chance":
                self.chance_title.draw()
                self.choix_label.draw()
                self.pair_button.draw()
                self.impair_button.draw()
                self.selected_choice.draw()
            else:
                self.numero_title.draw()
                self.numero_label.draw()
                self.numero_input.draw()

    def win_check(self):
        self.roulette.launch(self.number)

        if self.game_mode == "chance":
            if self.number == 0:
                print("Bof...")
                self.balance += self.mise // 2
            elif (self.choice == "pair" and self.number % 2 == 0) or (self.choice == "impair" and self.number % 2 == 1):
                print("Gagné !!!")
                self.balance += self.mise * 2
            else:
                print("Noob")
        else:
            if self.number == self.choice:
                print("Gagné !!!")
                self.balance += self.mise * 36
            else:
                print("Noob")

    def main(self):
        while True:
            self.handle_events()

            if not self.in_game:
                self.roulette.rotate(-0.8)

            self.change_values_elements()

            self.draw()

            self.update()
        
    def end(self):
        pygame.quit()
        sys.exit()

pygame.init()

game = Game()