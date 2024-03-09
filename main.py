import pgzrun
from config import *
from game import *
from interface import *

# фоновая музыка
sounds.bg_music.play(-1)

# создаем интерфейс
button_start = Button('START', (100 + WIDTH // 2 - 400 // 2, HEIGHT // 2 - 50 // 2 - 100 + 200), 'start', size=(400, 50))
button_exit = Button('EXIT', (100 + WIDTH // 2 - 400 // 2, HEIGHT // 2 - 50 // 2 + 200), 'exit', size=(400, 50))
button_music = Button('', (100 + WIDTH // 2 - 150 // 2 - 300, HEIGHT // 2 - 150 + 25 + 200), 'musicon', size=(150, 150))


# важные игровые переменные
fox = None
default_tiles = None
sand_tiles = None
room = None
game_stop = False
game_over = True
game_played = False
sound = True
score = 0
stage = 1
record = [0, 1]


# при нажатии на старт
def start_game():
    global fox, room, default_tiles, sand_tiles, game_over, game_stop
    game_over = game_stop = False
    fox = AnimatedActor('/fox/move/', '/fox/stand/', (WIDTH // 2, HEIGHT // 2), scale=2, move_speed=2)
    default_tiles = {'tiles': [*(['tile1'] * 50), *(['tile2'] * 25), *(['tile4'] * 12), 'tile3'],
                     'tiles_z': ['tile5', 'tile6', *([-1] * 50)]}
    sand_tiles = {'tiles': [*(['tile_s2'] * 5), *(['tile_s3'] * 20), *(['tile_s4'] * 30), *(['tile_s5'] * 5)],
                  'tiles_z': ['tile_s6', *([-1] * 50)]}
    room = Room(WIDTH, HEIGHT, 30, 20, **default_tiles)


def on_collide_enemy_and_fox():
    global game_stop, game_over, game_played, score, stage, record
    temp_actor = Rect(fox.position[0], fox.position[1], fox.frame_width * fox.scale, fox.frame_height * fox.scale)
    collided_enemy = room.is_collided_with_enemy(temp_actor)
    if collided_enemy != 0:
        for enemy in room.enemies:
            enemy.game_stop = game_stop = True
        if score != 0:
            record = [score, stage]
        if sound:
            sounds.slap.play()
        fox.stop = True
        collided_enemy.stop = True
        score = 0
        stage = 1
        game_over = True
        game_played = True


def draw():
    if not game_over:
        # рисуем игру
        screen.clear()
        rect = room.draw().inflate(10, 10)
        screen.draw.rect(rect, (128, 128, 128))
        screen.draw.text(f"Счет: {score}", (100, 25), color="white", fontsize=30)
        screen.draw.text(f"Комната #{stage}", (300, 25), color="white", fontsize=30)
        if not game_stop:
            fox.draw()
    else:
        # рисуем интерфейс
        screen.clear()
        if game_played:
            screen.draw.text(f'Игра закончилась с счетом: {record[0]}', (250, 100), fontsize=40, color='white')
            screen.draw.text(f'Вы прошли {record[1]} комнат', (250, 140), fontsize=40, color='white')
        button_start.draw(screen)
        button_music.draw(screen)
        button_exit.draw(screen)


def update(dt):
    global room, score
    if not game_over:
        fox.update(dt)
        room.update(dt)

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

        for enemy in room.enemies:
            if fox.position[0] >= enemy.position[0] and not game_stop:
                enemy.x_move_direction = -1
            else:
                enemy.x_move_direction = 1

        temp_actor = Rect(fox.position[0], fox.position[1], fox.frame_width * fox.scale, fox.frame_height * fox.scale)
        collided_enemy = room.is_collided_with_enemy(temp_actor)
        if collided_enemy != 0:
            clock.schedule(on_collide_enemy_and_fox, 1)
            collided_enemy.is_attack = True
            collided_enemy.animation_speed = 0.2
            if sound:
                sounds.attack.play()
        else:
            for enemy in room.enemies:
                enemy.is_attack = False

        collided_coin = room.is_collided_with_coin(temp_actor)
        if collided_coin:
            if sound:
                sounds.coin.play()
            score += 1


def on_key_down(key):
    if not game_stop and not fox.stop:
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
    global stage
    if not game_over:
        if key in [keys.RIGHT, keys.LEFT]:
            fox.is_moving_x = False
        if key in [keys.UP, keys.DOWN]:
            fox.is_moving_y = False
        if key == key.SPACE:
            tiles = random.choice([default_tiles, sand_tiles])
            temp_actor = Rect(fox.position[0], fox.position[1], fox.frame_width * fox.scale, fox.frame_height * fox.scale)
            if room.is_collided_with_door(temp_actor):
                stage += 1
                room = Room(WIDTH, HEIGHT, random.randint(5, 30), random.randint(5, 20), stage=stage, **tiles)
                if sound:
                    sounds.door.play()


def on_mouse_down(pos):
    global game_over, sound
    if game_over:
        print("Позиция клика мыши:", pos)
        if button_start.is_clicked(pos):
            clock.schedule(start_game, 1)
        if button_exit.is_clicked(pos):
            quit()
        if button_music.is_clicked(pos):
            if sound:
                button_music.change_image('musicoff')
                sounds.bg_music.stop()
                sound = False
            else:
                button_music.change_image('musicon')
                sounds.bg_music.play()
                sound = True


pgzrun.go()
