# Тут будут классы
import pygame
from pgzero import game


class AnimatedActor:
    def __init__(self, imagepath, position,
                 frame_width=24, frame_height=16,
                 move_images_row=2, move_images_count=5,
                 stand_images_row=1, stand_images_count=14,
                 move_speed=5, frames_count=14):
        self.position = position
        self.imagepath = imagepath

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

        self.time_since_last_frame = 0
        self.animation_speed = 0.1

    def load_move_images(self):
        full_image = pygame.image.load(self.imagepath)
        for x in range(0,
                       full_image.get_width() - self.frame_width * (self.frames_count - self.move_images_count),
                       self.frame_width):
            move_frame_surface = full_image.subsurface(
                pygame.Rect((x, self.frame_height * self.move_images_row), (self.frame_width, self.frame_height)))
            self.move_images.append(move_frame_surface)

    def load_stand_images(self):
        full_image = pygame.image.load(self.imagepath)
        for x in range(0,
                       full_image.get_width() - self.frame_width * (self.frames_count - self.stand_images_count),
                       self.frame_width):
            stand_frame_surface = full_image.subsurface(
                pygame.Rect((x, self.frame_height * self.stand_images_row), (self.frame_width, self.frame_height)))
            self.stand_images.append(stand_frame_surface)

    def on_move(self):
        pass

    def on_stand(self):
        pass

    def on_jump(self):
        pass

    def update(self, dt):
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.animation_speed:
            self.frame = (self.frame + 1) % len(self.move_images)
            self.time_since_last_frame -= self.animation_speed

    def draw(self):
        image = self.stand_images[self.frame % len(self.stand_images)]
        game.screen.blit(image, self.position)

