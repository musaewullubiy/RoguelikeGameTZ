from pgzero.actor import Actor
from pgzero.rect import Rect
import pygame


class Button:
    def __init__(self, text, position, image=None, size=(100, 50), callback=None):
        self.text = text
        self.position = position
        self.image = image
        self.size = size
        self.callback = callback
        self.actor = Actor(image, position)
        self.actor._surf = pygame.transform.scale(self.actor._surf, (size[0], size[1]))

    def draw(self):
        self.actor.draw()

    def is_clicked(self, pos):
        rect = Rect(*self.position, *self.size)
        return rect.collidepoint(pos)