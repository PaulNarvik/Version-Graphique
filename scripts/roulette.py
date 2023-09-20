import pygame
from math import sqrt
from numpy import cbrt

class Roulette(pygame.sprite.Sprite):

    def __init__(self, game):
        super(Roulette, self).__init__()

        self.game = game

        self.x, self.y = 0, self.game.SCREEN_HEIGHT // 2

        self.image = pygame.image.load("./assets/roulette.png")
        self.image = pygame.transform.scale(self.image, (self.game.SCREEN_HEIGHT * 4 / 5, self.game.SCREEN_HEIGHT * 4 / 5))

        self.copy_image = self.image.copy()

        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.angle = 0

        self.angles = {
            0: 0,
            1: 360 / 38 * 24,
            2: 360 / 38 * 6,
            3: 360 / 38 * 36,
            4: 360 / 38 * 4,
            5: 360 / 38 * 20,
            6: 360 / 38 * 11,
            7: 360 / 38 * 32,
            8: 360 / 38 * 17,
            9: 360 / 38 * 28,
            10: 360 / 38 * 19,
            11: 360 / 38 * 15,
            12: 360 / 38 * 34,
            13: 360 / 38 * 13,
            14: 360 / 38 * 26,
            15: 360 / 38 * 2,
            16: 360 / 38 * 22,
            17: 360 / 38 * 8,
            18: 360 / 38 * 30,
            19: 360 / 38 * 3,
            20: 360 / 38 * 25,
            21: 360 / 38 * 5,
            22: 360 / 38 * 29,
            23: 360 / 38 * 18,
            24: 360 / 38 * 21,
            25: 360 / 38 * 7,
            26: 360 / 38 * 37,
            27: 360 / 38 * 12,
            28: 360 / 38 * 33,
            29: 360 / 38 * 31,
            30: 360 / 38 * 16,
            31: 360 / 38 * 27,
            32: 360 / 38 * 1,
            33: 360 / 38 * 23,
            34: 360 / 38 * 9,
            35: 360 / 38 * 35,
            36: 360 / 38 * 14,
            37: 360 / 38 * 10 # Ne sert pas car randint(0, 36)
        }

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def rotate(self, d_angle):
        self.image = pygame.transform.rotate(self.copy_image, self.angle)

        self.angle += d_angle
        self.angle %= 360

        self.rect = self.image.get_rect(center=self.rect.center)

    def transition(self, speed):
        if self.x == 252:
            target_pos = 0
        else:
            target_pos = 252

        while abs(self.x - target_pos) > 1 :
            self.x += speed
            self.rect = self.image.get_rect(center=(self.x, self.y))
            
            self.rotate(- speed / 3)

            self.game.draw()

            self.game.update()

    def launch(self, target):
        target_dist = 360 * 7 - self.angles[target] + self.angle
        runned_dist = 0
        target_time = 6
        t = 0

        a_coeff = target_dist / cbrt(sqrt(target_time)) # f(x) = a * sqrt(x) tel que f(target_time) = target_dist <=> a = target_dist / sqrt(target_time)
        f = lambda x : a_coeff * cbrt(sqrt(x))

        while runned_dist < target_dist:
            dt = self.game.dt / 1000
            dist = f(t + dt) - f(t)
            t += dt
            runned_dist += dist

            self.rotate(- dist)

            self.game.draw()

            self.game.update()
        print(target)
