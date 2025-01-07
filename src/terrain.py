import pygame

import constants as c

STONE_IMG_PATH = 'resources/terrain/bottom.png'
GRASS_IMG_PATH = 'resources/terrain/top.png'


class Terrain(pygame.sprite.Sprite):
    """
    Class representing a visual terrain block
    """

    def __init__(self, image_path, position):
        """
        Initialize the terrain block
        :param image_path: path to the texture
        :param position: position of the block
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = position


def generate_terrain(grid):
    """
    Generate terrain sprites from a grid
    :param grid: 2-dimensional array representing the terrain
    :return: a pygame group of terrain sprites
    """
    terrain_sprites = pygame.sprite.Group()
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == 0:
                continue

            position = (col_index * c.BLOCK_SIZE, row_index * c.BLOCK_SIZE)
            if cell == 1:  # Assuming 1 represents a terrain block
                terrain_block = Terrain(STONE_IMG_PATH, position)
                terrain_sprites.add(terrain_block)
            if cell == 2:  # Assuming 1 represents a terrain block
                terrain_block = Terrain(GRASS_IMG_PATH, position)
                terrain_sprites.add(terrain_block)
    return terrain_sprites


class Chunk:
    """
    Class representing a chunk of terrain
    """

    def __init__(self, grid, position):
        """
        Initialize the chunk
        :param grid: 2-dimensional array representing the terrain
        :param position: chunk position
        """
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.position = position
        self.terrain_sprites = generate_terrain(grid)
        self.entities = pygame.sprite.Group()
        self.update_positions()

    def update_positions(self):
        """
        Update the positions of the terrain sprites to match the chunk position
        :return:
        """
        for sprite in self.terrain_sprites:
            sprite.rect.x += self.position[0]
            sprite.rect.y += self.position[1]

    def get_end_position(self):
        """
        :return: the x-coordinate of the end of the chunk
        """
        return self.position[0] + self.width * 64

    def draw(self, screen):
        """
        Draws all the terrain sprites in the chunk
        :param screen: screen instance
        """
        self.terrain_sprites.draw(screen)

    def update(self):
        """
        Updates chunk terrain sprites
        """
        self.terrain_sprites.update()

    def scroll(self, dx):
        """
        Scroll the chunk
        :param dx: scroll offset
        """

        self.position[0] -= dx
        for sprite in self.terrain_sprites:
            sprite.rect.x -= dx
        for entity in self.entities:
            entity.scroll(dx)
