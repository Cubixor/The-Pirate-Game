import os
from glob import glob

import pygame

import constants as c


class Animation:
    """
    Class for animating objects
    """
    def __init__(self, image_paths, scale=3):
        """
        Initialize the object with the images
        :param image_paths: map with paths to images for each state
        :param scale: scale of the images
        """
        self.images = {}
        for k, v in image_paths.items():
            image_path = glob(os.path.join(v, '*.png'))
            self.images[k] = []
            for path in image_path:
                img = pygame.image.load(path)
                scaled = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                self.images[k].append(scaled)

        self.curr_state = next(iter(image_paths))
        self.flipped = False
        self.frame_counter = 0
        self.image_index = 0
        self.image = self.images[self.curr_state][self.image_index]

    def update(self):
        """
        Update the animation, change frame if needed
        """

        self.frame_counter += 1
        if self.frame_counter >= c.ANIMATION_SPEED:
            images = self.images[self.curr_state]

            self.image_index = (self.image_index + 1) % len(images)
            self.image = images[self.image_index]
            self.frame_counter = 0

    def change_state(self, state):
        """
        Change the current animation state (switch to another animation)
        :param state: state to switch to
        """

        if self.curr_state == state:
            return

        self.image_index = 0
        self.curr_state = state
        self.image = self.images[state][self.image_index]

    def change_direction(self, flipped):
        """
        Change the direction of the images
        :param flipped: should images be flipped
        """

        if self.flipped == flipped:
            return

        self.flipped = flipped
        for k, v in self.images.items():
            for i in range(len(v)):
                self.images[k][i] = pygame.transform.flip(v[i], True, False)

    def get_image(self):
        """
        :return: current animation image
        """
        return self.image

    def get_full_time(self):
        """
        :return: how long a full animation cycle takes
        """
        return c.ANIMATION_SPEED * (len(self.images[self.curr_state]) - 1)
