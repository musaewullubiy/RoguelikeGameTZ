# Тут будет сам запуск игры
import pgzrun
from config import *
from game import *


fox = AnimatedActor('images/fox.png', (30, 30), scale=4)


def draw():
    screen.clear()
    fox.draw()


def update(dt):
    fox.update(dt)


def on_key_down(key):
    if key == keys.RIGHT:
        fox.is_moving = True
        fox.move_direction = 1
    elif key == keys.LEFT:
        fox.is_moving = True
        fox.move_direction = -1


def on_key_up(key):
    if key in [keys.RIGHT, keys.LEFT]:
        fox.is_moving = False


pgzrun.go()
