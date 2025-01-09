import random

import constants as c
import entities
from terrain import Chunk


def generate_tower_grid():
    """
    Generate a grid with towers
    :return:
    """
    num_towers = random.randint(4, 9)
    tower_width = random.randint(1, 2)
    tower_spacing = random.randint(2, 4)

    chunk_width = num_towers * tower_width + num_towers * tower_spacing
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]

    prev_height = random.randint(1, 3)
    for i in range(num_towers):
        min_height = 3 if prev_height <= 3 else prev_height - 2
        max_height = 6 if prev_height >= 6 else prev_height + 2
        tower_height = random.randint(min_height, max_height)  # Random height for each tower
        prev_height = tower_height

        tower_start_col = i * (tower_spacing + tower_width)
        gen_platform_grid(new_chunk_grid, tower_height, tower_start_col, tower_start_col + tower_width)

    return new_chunk_grid


def gen_star_grid(platform_height=3):
    """
    Generates a flat grid
    :param platform_height: height of the platform
    :return:
    """
    chunk_width = random.randint(8, 16)
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]

    gen_platform_grid(new_chunk_grid, platform_height, 0, chunk_width)

    return new_chunk_grid


def gen_shell_grid(start_height=2):
    """
    Generates a grid at two levels, with a step on the right
    :param start_height: height of the first level
    :return:
    """

    chunk_width = random.randint(10, 14)
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]
    ratio = 1.5
    height = random.randint(1, 2)
    part_size = int(chunk_width / ratio)

    gen_platform_grid(new_chunk_grid, start_height, 0, part_size)
    gen_platform_grid(new_chunk_grid, start_height + height, part_size, chunk_width)

    return new_chunk_grid


def gen_crab_grid(start_height=1):
    """
    Generates a grid with 2 levels, with a step in the middle
    :param start_height: height of the base level
    :return:
    """
    chunk_width = random.randint(15, 20)
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]
    platform_width = chunk_width // 5
    height = random.randint(1, 2)

    gen_platform_grid(new_chunk_grid, start_height, 0, platform_width * 2)
    gen_platform_grid(new_chunk_grid, start_height + height, platform_width * 2, platform_width * 3)
    gen_platform_grid(new_chunk_grid, start_height, platform_width * 3, chunk_width)

    return new_chunk_grid


def gen_platform_grid(grid, height, start, end):
    """
    Generates a platform in the grid, of the given height, from start to end
    :param grid: a grid to modify
    :param height: platform height
    :param start: platform start column
    :param end: platform end column
    """

    for row in range(c.CHUNK_HEIGHT - height, c.CHUNK_HEIGHT):
        for col in range(start, end):
            if row == c.CHUNK_HEIGHT - height:
                grid[row][col] = 2
            else:
                grid[row][col] = 1


def gen_gap_grid(min_width=2, max_width=5):
    """
    Generates an empty grid
    :param min_width: minimum width
    :param max_width: maximum width
    :return:
    """
    chunk_width = random.randint(min_width, max_width)
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]
    return new_chunk_grid


def gen_tower_chunk(pos, window):
    """
    Generates a chunk with towers
    :param pos: chunk position
    :param window: window dimensions
    :return: generated chunk
    """
    return Chunk(generate_tower_grid(), pos)


def gen_star_chunk(pos, window):
    """
    Generates a chunk with star entity
    :param pos: chunk position
    :param window: window dimensions
    :return: generated chunk
    """
    platform_height = random.randint(2, 3)
    chunk = Chunk(gen_star_grid(platform_height), pos)
    star_pos = (pos[0] + 128, window[1] - platform_height * c.BLOCK_SIZE)
    star = entities.Star(star_pos, pos[0], chunk.get_end_position())
    chunk.entities.add(star)
    return chunk


def gen_shell_chunk(pos, window):
    """
    Generates a chunk with shell entity
    :param pos: chunk position
    :param window: window dimensions
    :return: generated chunk
    """
    platform_height = random.randint(2, 3)
    chunk = Chunk(gen_shell_grid(platform_height), pos)
    shell_pos = int(chunk.width / 1.5) * c.BLOCK_SIZE + pos[0] - c.BLOCK_SIZE, window[1] - platform_height * c.BLOCK_SIZE
    shell = entities.Shell(shell_pos)
    chunk.entities.add(shell)
    return chunk


def gen_crab_chunk(pos, window):
    """
    Generate a chunk with a crab entity
    :param pos: chunk position
    :param window: window dimensions
    :return: generated chunk
    """
    platform_height = random.randint(2, 3)
    chunk = Chunk(gen_crab_grid(platform_height), pos)
    crab_pos = int(chunk.width / 1.5) * c.BLOCK_SIZE + pos[0] - c.BLOCK_SIZE, window[1] - platform_height * c.BLOCK_SIZE
    crab = entities.Crab(crab_pos)
    chunk.entities.add(crab)
    return chunk


def gen_gap_chunk(pos, window):
    """
    Create an empty chunk
    :param pos: chunk position
    :param window: window dimensions
    :return: generated chunk
    """
    return Chunk(gen_gap_grid(), pos)


def gen_ship_chunk(pos, window):
    """
    Create a chunk with a ship entity
    :param pos: chunk position
    :param window: window dimensions
    :return: generated chunk
    """
    chunk = Chunk(gen_gap_grid(10, 20), pos)
    ship = entities.Ship((pos[0] + 100, window[1] - 32), pos[0], chunk.get_end_position())
    chunk.entities.add(ship)
    return chunk


CHUNK_TYPES = [
    gen_shell_chunk,
    gen_star_chunk,
    gen_gap_chunk,
    gen_ship_chunk,
    gen_crab_chunk,
    gen_tower_chunk,
    gen_tower_chunk
]


class ChunkGenerator:
    """
    Class used for randomly generating new chunks
    """

    def __init__(self, dims):
        self.available_chunk_types = list(CHUNK_TYPES)
        self.prev_chunk = gen_gap_chunk
        self.window = dims

    def gen_chunk(self, pos):
        """
        Generate a random chunk, different from the previous one
        :param pos: chunk position
        :return: generated chunk
        """

        self.available_chunk_types.remove(self.prev_chunk)
        if self.prev_chunk == gen_gap_chunk:
            self.available_chunk_types.remove(gen_ship_chunk)
            self.available_chunk_types.remove(gen_tower_chunk)
        elif self.prev_chunk == gen_ship_chunk or self.prev_chunk == gen_tower_chunk:
            self.available_chunk_types.remove(gen_gap_chunk)

        choice = random.choice(self.available_chunk_types)

        self.available_chunk_types = list(CHUNK_TYPES)
        self.prev_chunk = choice

        return choice(pos, self.window)
