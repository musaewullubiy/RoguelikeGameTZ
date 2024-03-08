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
        self.text = text

    def draw(self, screen):
        self.actor.draw()
        screen.draw.text(self.text, midtop=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2 - 25), fontsize=60, color='white')

    def is_clicked(self, pos):
        rect = Rect(*self.position, *self.size)
        return rect.collidepoint(pos)

    def change_image(self, image):
        self.actor = Actor(image, self.position)
        self.actor._surf = pygame.transform.scale(self.actor._surf, (self.size[0], self.size[1]))