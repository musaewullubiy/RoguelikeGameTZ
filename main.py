# Тут будет сам запуск игры
import pgzrun
from config import *
from game import *


fox = AnimatedActor('fox.png', (WIDTH // 2, HEIGHT // 2), scale=3)
room = Room(WIDTH, HEIGHT, 33, 20,
            tiles=[*(['tile1'] * 50), *(['tile2'] * 25), *(['tile4'] * 12), 'tile3'],
            tiles_z=['tile5', 'tile6', *([-1] * 50)])


def draw():
    screen.clear()
    rect = room.draw(screen.surface).inflate(10, 10)
    screen.draw.rect(rect, (128, 128, 128))
    fox.draw()


def update(dt):
    fox.update(dt)

    # Рассчитываем новые координаты лисы
    new_x = fox.position[0] + int(fox.is_moving_x) * fox.x_move_direction * fox.move_speed
    new_y = fox.position[1] + int(fox.is_moving_y) * fox.y_move_direction * fox.move_speed

    # Проверяем, выходит ли лиса за пределы комнаты
    if new_x < room.x - 10:
        new_x = room.x - 10
    elif new_x + fox.frame_width * fox.scale > room.x + room.width:
        new_x = room.x + room.width - fox.frame_width * fox.scale

    if new_y < room.y - 10:
        new_y = room.y - 10
    elif new_y + fox.frame_height * fox.scale > room.y + room.height - 10:
        new_y = room.y + room.height - fox.frame_height * fox.scale - 10

    fox.position = (new_x, new_y)


def on_key_down(key):
    if key == keys.RIGHT:
        fox.is_moving_x = True
        fox.x_move_direction = 1
    if key == keys.LEFT:
        fox.is_moving_x = True
        fox.x_move_direction = -1
    if key == keys.UP:
        fox.is_moving_y = True
        fox.y_move_direction = -1
    if key == key.DOWN:
        fox.is_moving_y = True
        fox.y_move_direction = 1


def on_key_up(key):
    if key in [keys.RIGHT, keys.LEFT]:
        fox.is_moving_x = False
    if key in [keys.UP, keys.DOWN]:
        fox.is_moving_y = False


pgzrun.go()
