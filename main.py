# Тут будет сам запуск игры
import random
import time

import pgzrun
from config import *
from game import *


fox = AnimatedActor('/fox/move/', '/fox/stand/', (WIDTH // 2, HEIGHT // 2), scale=2, move_speed=3)
default_tiles = {'tiles': [*(['tile1'] * 50), *(['tile2'] * 25), *(['tile4'] * 12), 'tile3'], 'tiles_z': ['tile5', 'tile6', *([-1] * 50)]}
sand_tiles = {'tiles': [*(['tile_s2'] * 5), *(['tile_s3'] * 20), *(['tile_s4'] * 30), *(['tile_s5'] * 5)], 'tiles_z': ['tile_s6', *([-1] * 50)]}
room = Room(WIDTH, HEIGHT, 30, 20, **default_tiles)
enemy = Enemy('/slime/move/', '/slime/stand/', '/slime/attack/', (200, 200), (400, 400), (room.x, room.y, room.width, room.height), scale=5, move_speed=3)

collision_time = None
game_stop = False


def draw():
    screen.clear()
    rect = room.draw(screen.surface).inflate(10, 10)
    screen.draw.rect(rect, (128, 128, 128))
    if not game_stop:
        fox.draw()
    enemy.draw()


def update(dt):
    global collision_time
    global room
    global game_stop

    fox.update(dt)
    enemy.update(dt)

    # Рассчитываем новые координаты лисы
    new_x = fox.position[0] + int(fox.is_moving_x) * fox.x_move_direction * fox.move_speed
    new_y = fox.position[1] + int(fox.is_moving_y) * fox.y_move_direction * fox.move_speed

    # Проверяем, выходит ли лиса за пределы комнаты
    if new_x < room.x:
        new_x = room.x
    elif new_x + fox.frame_width * fox.scale > room.x + room.width:
        new_x = room.x + room.width - fox.frame_width * fox.scale

    if new_y < room.y:
        new_y = room.y
    elif new_y + fox.frame_height * fox.scale > room.y + room.height:
        new_y = room.y + room.height - fox.frame_height * fox.scale

    fox.position = (new_x, new_y)

    if fox.position[0] > enemy.position[0]:
        enemy.x_move_direction = -1
    else:
        enemy.x_move_direction = 1

    fox_rect = Rect(fox.position[0], fox.position[1], fox.frame_width * fox.scale, fox.frame_height * fox.scale)
    enemy_rect = Rect(enemy.position[0], enemy.position[1], enemy.frame_width * enemy.scale,
                      enemy.frame_height * enemy.scale)
    enemy.is_attack = False
    if fox_rect.colliderect(enemy_rect):
        enemy.is_attack = True
        enemy.stop = True
        if collision_time is None:
            collision_time = time.time()
        elif time.time() - collision_time >= 2:
            enemy.game_stop = game_stop = True


def on_key_down(key):
    if not game_stop:
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
    global room

    if key in [keys.RIGHT, keys.LEFT]:
        fox.is_moving_x = False
    if key in [keys.UP, keys.DOWN]:
        fox.is_moving_y = False
    if key == key.SPACE:
        tiles = random.choice([default_tiles, sand_tiles])
        temp_actor = Rect(fox.position[0], fox.position[1], fox.frame_width * fox.scale, fox.frame_height * fox.scale)
        if room.is_collided_with_door(temp_actor):
            room = Room(WIDTH, HEIGHT, random.randint(5, 30), random.randint(5, 20), **tiles)


def on_mouse_down(pos):
    print("Позиция клика мыши:", pos)


pgzrun.go()
