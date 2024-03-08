# Тут будут классы
import os
import pygame
from pgzero import game
from pgzero.actor import Actor
from pgzero.rect import Rect
import random


class AnimatedActor:
    def __init__(self, movepath, standpath, position,
                 frame_width=24, frame_height=16,
                 move_speed=5, frames_count=14, scale=1.0):
        self.position = position
        self.standpath = standpath
        self.movepath = movepath
        self.scale = scale

        self.frame = 0
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames_count = frames_count

        self.move_images = []
        self.load_move_images()

        self.stand_images = []
        self.load_stand_images()

        self.is_moving_x = False
        self.is_moving_y = False
        self.move_speed = move_speed
        self.x_move_direction = 0
        self.y_move_direction = 0
        self.is_flip = False
        self.time_since_last_frame = 0
        self.animation_speed = 0.6
        self.stop = False

    def load_move_images(self):
        imagecount = len(os.listdir('images/' + self.movepath))
        for x in range(0, imagecount):
            actor = Actor(self.movepath[1::] + f'move_{x}.png', pos=self.position)
            actor._surf = pygame.transform.scale(actor._surf,
                                                 (self.frame_width * self.scale, self.frame_height * self.scale))
            self.move_images.append(actor)

    def load_stand_images(self):
        imagecount = len(os.listdir('images/' + self.movepath))
        for x in range(0, imagecount):
            actor = Actor(self.standpath[1::] + f'stand_{x}.png', pos=self.position)
            actor._surf = pygame.transform.scale(actor._surf,
                                                 (self.frame_width * self.scale, self.frame_height * self.scale))
            self.stand_images.append(actor)

    def scale_it(self, scale):
        self.scale = scale
        self.load_stand_images()
        self.load_move_images()

    def on_move(self):
        return self.move_images[self.frame % len(self.move_images)]

    def on_stand(self):
        return self.stand_images[self.frame % len(self.stand_images)]

    def update(self, dt):
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.animation_speed:
            self.frame = (self.frame + 1) % len(self.move_images)
            self.time_since_last_frame -= self.animation_speed

        self.position = (self.position[0] + int(self.is_moving_x) * self.x_move_direction * self.move_speed,
                         self.position[1] + int(self.is_moving_y) * self.y_move_direction * self.move_speed)

    def draw(self):
        if self.is_moving_x or self.is_moving_y:
            image = self.on_move()
        else:
            image = self.on_stand()
        if self.x_move_direction == -1:
            image._surf = pygame.transform.flip(image._surf, True, False)
        image.pos = self.position
        image.draw()
        if self.x_move_direction == -1:
            image._surf = pygame.transform.flip(image._surf, True, False)


class Enemy(AnimatedActor):
    def __init__(self, movepath, standpath, attackpath, position, move_to, borders, **kwargs):
        super().__init__(movepath, standpath, position, **kwargs)
        self.move_to = move_to
        self.borders = borders

        self.attackpath = attackpath
        self.attack_images = []
        self.load_attack_images()
        self.is_attack = False
        self.game_stop = False

    def load_attack_images(self):
        imagecount = len(os.listdir('images/' + self.attackpath))
        for x in range(0, imagecount):
            actor = Actor(self.attackpath[1::] + f'attack_{x}.png', pos=self.position)
            actor._surf = pygame.transform.scale(actor._surf,
                                                 (self.frame_width * self.scale, self.frame_height * self.scale))
            self.attack_images.append(actor)

    def on_attack(self):
        return self.attack_images[self.frame % len(self.attack_images)]

    def update(self, dt):
        super().update(dt)
        if not self.stop:
            if random.randint(1, 1000) == 1 or self.move_to == self.position:
                try:
                    self.move_to = (random.randint(self.borders[0], self.borders[2]),
                                    random.randint(self.borders[1], self.borders[3]))
                except ValueError:
                    self.move_to = (400, 300)
            if random.randint(1, 20) == 1:
                self.move_towards_destination()

    def draw(self):
        if self.game_stop:
            image = self.stand_images[0]
            if self.x_move_direction == -1:
                image._surf = pygame.transform.flip(image._surf, True, False)
            image.pos = self.position
            image.draw()
            return None
        if not self.is_attack:
            if self.is_moving_x or self.is_moving_y:
                image = self.on_move()
            else:
                image = self.on_stand()
        else:
            image = self.on_attack()
        if self.x_move_direction == -1:
            image._surf = pygame.transform.flip(image._surf, True, False)
        image.pos = self.position
        image.draw()
        if self.x_move_direction == -1:
            image._surf = pygame.transform.flip(image._surf, True, False)

    def move_towards_destination(self):
        dx = self.move_to[0] - self.position[0]
        dy = self.move_to[1] - self.position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            speed = self.move_speed / distance
            self.position = (self.position[0] + dx * speed, self.position[1] + dy * speed)
        if abs(dx) < self.move_speed and abs(dy) < self.move_speed:
            try:
                self.move_to = (
                random.randint(self.borders[0], self.borders[2]), random.randint(self.borders[1], self.borders[3]))
            except ValueError:
                self.move_to = (400, 300)


class Tile:
    def __init__(self, x, y, size, image):
        self.x = x
        self.y = y
        self.size = size
        self.image = image
        self.actor = Actor(image, pos=(x, y))
        self.actor._surf = pygame.transform.scale(self.actor._surf, (size, size))

    def draw(self):
        self.actor.draw()


class Room:
    def __init__(self, screen_width, screen_height, num_tiles_x, num_tiles_y, stage=1, tiles=0, tiles_z=0):
        if tiles == 0 or tiles_z == 0:
            tiles = ['tile1', 'tile2', 'tile3', 'tile4']
            tiles_z = ['tile5', *([-1] * 50)]
        self.stage = stage
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_tiles_x = num_tiles_x
        self.num_tiles_y = num_tiles_y
        self.tile_size = min((screen_width - 100) // num_tiles_x, (screen_height - 100) // num_tiles_y)
        self.width = num_tiles_x * self.tile_size
        self.height = num_tiles_y * self.tile_size
        self.x = 8 + (screen_width - self.width) // 2 + (screen_width - self.width) % 2
        self.y = 8 + (screen_height - self.height) // 2 + (screen_height - self.height) % 2

        self.contents = self.generate_contents(tiles)
        self.contents_z = self.generate_contents(tiles_z)
        self.doors = self.generate_doors()
        self.enemies = self.generate_enemies()
        self.coins = self.genetate_coins()

    def generate_contents(self, tile_image_names):
        contents = []
        for y in range(self.num_tiles_y):
            for x in range(self.num_tiles_x):
                tile_x = self.x + x * self.tile_size
                tile_y = self.y + y * self.tile_size
                image = random.choice(tile_image_names)
                if image != -1:
                    contents.append(Tile(tile_x, tile_y, self.tile_size, image))
        return contents

    def generate_doors(self):
        door_positions = [(self.x + self.width // 2, self.y),
                          (self.x, self.y + self.height // 2),
                          (self.x + self.width // 2, self.y + self.height - self.tile_size),
                          (self.x + self.width - self.tile_size, self.y + self.height // 2)]
        random.shuffle(door_positions)
        num_doors = random.randint(1, min(4, len(door_positions)))
        doors = []
        for i in range(num_doors):
            door_x, door_y = door_positions.pop()
            doors.append(Door(door_x, door_y, self.tile_size, 'door.png'))
        return doors

    def generate_enemies(self):
        enemy = Enemy('/slime/move/', '/slime/stand/', '/slime/attack/', (200, 200), (400, 400),
              (self.x, self.y, self.width, self.height), scale=5, move_speed=3)
        num_enemies = self.stage
        enemies = []
        for _ in range(num_enemies):
            enemy_x = random.randint(self.x, self.x + self.width - enemy.frame_width * enemy.scale)
            enemy_y = random.randint(self.y, self.y + self.height - enemy.frame_height * enemy.scale)
            while self.is_near_door(enemy_x, enemy_y):
                enemy_x = random.randint(self.x, self.x + self.width - enemy.frame_width * enemy.scale)
                enemy_y = random.randint(self.y, self.y + self.height - enemy.frame_height * enemy.scale)
            enemies.append(Enemy('/slime/move/', '/slime/stand/', '/slime/attack/', (enemy_x, enemy_y), (400, 400),
                                 (self.x, self.y, self.width, self.height), scale=random.randint(2, 3), move_speed=random.randint(1, 4)))
        return enemies

    def genetate_coins(self):
        coins = []
        for i in range(random.randint(1, 1000 // self.num_tiles_x // self.num_tiles_y)):
            coin_x = random.randint(self.x, self.x + self.width - self.tile_size * 2)
            coin_y = random.randint(self.y, self.y + self.height - self.tile_size * 2)
            while self.is_near_door(coin_x, coin_y):
                coin_x = random.randint(self.x, self.x + self.width - self.tile_size * 2)
                coin_y = random.randint(self.y, self.y + self.height - self.tile_size * 2)
            coin = Coin(coin_x, coin_y, self.tile_size * 2, 'coin.png')
            coins.append(coin)
        return coins

    def is_near_door(self, x, y):
        for door in self.doors:
            door_rect = Rect(door.x, door.y, door.size, door.size)
            if door_rect.collidepoint(x, y):
                return True
        return False

    def is_collided_with_enemy(self, actor):
        for enemy in self.enemies:
            enemy_rect = Rect(enemy.position[0], enemy.position[1], enemy.frame_width * enemy.scale,
                              enemy.frame_height * enemy.scale)
            if enemy_rect.colliderect(actor):
                return enemy
        return 0

    def is_collided_with_door(self, actor):
        for door in self.doors:
            door = Rect(door.x, door.y, door.size, door.size)
            if door.colliderect(actor):
                return True
        return False

    def is_collided_with_coin(self, actor):
        for coin in range(len(self.coins)):
            coin_ = Rect(self.coins[coin].x, self.coins[coin].y, self.coins[coin].size, self.coins[coin].size)
            if coin_.colliderect(actor):
                self.coins.pop(coin)
                return True
        return False

    def draw(self):
        for tile in self.contents:
            tile.draw()
        for tile in self.contents_z:
            tile.draw()
        for door in self.doors:
            door.draw()
        for coin in self.coins:
            coin.draw()
        for enemy in self.enemies:
            enemy.draw()
        return Rect((self.x - 8, self.y - 8), (self.width, self.height))

    def update(self, dt):
        for enemy in self.enemies:
            enemy.update(dt)


class Door:
    def __init__(self, x, y, size, image):
        self.x = x
        self.y = y
        self.size = size
        self.image = image
        self.actor = Actor(image, pos=(x, y))
        self.actor._surf = pygame.transform.scale(self.actor._surf, (size, size))

    def draw(self):
        self.actor.draw()


class Coin:
    def __init__(self, x, y, size, image):
        self.x = x
        self.y = y
        self.size = size
        self.image = image
        self.actor = Actor(image, pos=(x, y))
        self.actor._surf = pygame.transform.scale(self.actor._surf, (size, size))

    def draw(self):
        self.actor.draw()