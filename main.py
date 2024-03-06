# Тут будет сам запуск игры
import pgzrun
from config import *
from game import *


fox = AnimatedActor('images/fox.png', (30, 30))


def draw():
    screen.clear()
    fox.draw()


def update(dt):
    fox.update(dt)


pgzrun.go()
