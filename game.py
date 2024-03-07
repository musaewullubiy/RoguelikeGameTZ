# Тут будут классы
import pygame
from pgzero import game
from pgzero.actor import Actor
from pgzero.rect import Rect
import random


class AnimatedActor:
    def __init__(self, imagepath, position,
                 frame_width=24, frame_height=16,
                 move_images_row=2, move_images_count=5,
                 stand_images_row=1, stand_images_count=14,
                 move_speed=5, frames_count=14, scale=1.0):
        self.position = position
        self.imagepath = imagepath
        self.scale = scale

        self.frame = 0
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames_count = frames_count

        self.move_images = []
        self.move_images_row = move_images_row
        self.move_images_count = move_images_count
        self.load_move_images()

        self.stand_images = []
        self.stand_images_row = stand_images_row
        self.stand_images_count = stand_images_count
        self.load_stand_images()

        self.is_moving_x = False
        self.is_moving_y = False
        self.move_speed = move_speed
        self.x_move_direction = 0
        self.y_move_direction = 0
        self.time_since_last_frame = 0
        self.animation_speed = 0.6

    def load_move_images(self):
        full_image = Actor(self.imagepath)
        for x in range(0,
                       full_image.width - self.frame_width * (self.frames_count - self.move_images_count),
                       self.frame_width):
            move_frame_surface = full_image._surf.subsurface(
                pygame.Rect((x, self.frame_height * self.move_images_row), (self.frame_width, self.frame_height)))
            move_frame_surface = pygame.transform.scale(move_frame_surface,
                                                         (int(self.frame_width * self.scale),
                                                          int(self.frame_height * self.scale)))
            self.move_images.append(move_frame_surface)

    def load_stand_images(self):
        full_image = Actor(self.imagepath)
        for x in range(0,
                       full_image.width - self.frame_width * (self.frames_count - self.stand_images_count),
                       self.frame_width):
            stand_frame_surface = full_image._surf.subsurface(
                pygame.Rect((x, self.frame_height * self.stand_images_row), (self.frame_width, self.frame_height)))
            stand_frame_surface = pygame.transform.scale(stand_frame_surface,
                                                         (int(self.frame_width * self.scale),
                                                          int(self.frame_height * self.scale)))
            self.stand_images.append(stand_frame_surface)

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
            image = pygame.transform.flip(image, True, False)
        game.screen.blit(image, self.position)


class Tile:
    def __init__(self, x, y, size, image):
        self.x = x
        self.y = y
        self.size = size
        self.image = image
        self.actor = Actor(image, pos=(x, y))
        self.actor._surf = pygame.transform.scale(self.actor._surf, (size, size))

    def draw(self, surface):
        self.actor.draw()


class Room:
    def __init__(self, screen_width, screen_height, num_tiles_x, num_tiles_y, tiles=0, tiles_z=0):
        if tiles == 0 or tiles_z == 0:
            tiles = ['tile1', 'tile2', 'tile3', 'tile4']
            tiles_z = ['tile5', *([-1] * 50)]
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_tiles_x = num_tiles_x
        self.num_tiles_y = num_tiles_y
        self.tile_size = min((screen_width - 100) // num_tiles_x, (screen_height - 100) // num_tiles_y)
        self.width = num_tiles_x * self.tile_size
        self.height = num_tiles_y * self.tile_size
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        self.contents = self.generate_contents(tiles)
        self.contents_z = self.generate_contents(tiles_z)

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

    def draw(self, surface):
        for tile in self.contents:
            tile.draw(surface)
        for tile in self.contents_z:
            tile.draw(surface)
        return Rect((self.x - 8, self.y - 8), (self.width, self.height))
