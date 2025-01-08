import random

import constants as c
import entities
from terrain import Chunk


def generate_tower_grid(start_height=2, end_height=6):
    num_towers = random.randint(3, 6)  # Random number of towers
    tower_width = 1  # Width of each tower
    tower_spacing = random.randint(3, 5)

    chunk_width = num_towers * tower_width + (num_towers - 1) * (tower_spacing - 1) + 2
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]

    prev_height = start_height
    for i in range(num_towers):
        min_height = 3 if prev_height <= 3 else prev_height - 2
        max_height = 6 if prev_height >= 6 else prev_height + 2
        tower_height = random.randint(min_height, max_height)  # Random height for each tower
        prev_height = tower_height

        tower_start_col = i * tower_spacing + 1
        gen_platform_grid(new_chunk_grid, tower_height, tower_start_col, tower_start_col + tower_width)

    return new_chunk_grid


def gen_star_grid(platform_height=3):
    chunk_width = random.randint(8, 12)
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]

    gen_platform_grid(new_chunk_grid, platform_height, 0, chunk_width)

    return new_chunk_grid


def gen_shell_grid(start_height=2):
    chunk_width = random.randint(7, 13)
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]
    ratio = 1.5
    height = 2
    part_size = int(chunk_width / ratio)

    gen_platform_grid(new_chunk_grid, start_height, 0, part_size)
    gen_platform_grid(new_chunk_grid, start_height + height, part_size, chunk_width)

    return new_chunk_grid


def gen_crab_grid(start_height=1):
    chunk_width = random.randint(15, 20)
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]
    platform_width = chunk_width // 5
    height = 2

    gen_platform_grid(new_chunk_grid, start_height, 0, platform_width)
    gen_platform_grid(new_chunk_grid, start_height + height, platform_width, platform_width * 2)
    gen_platform_grid(new_chunk_grid, start_height, platform_width * 2, platform_width * 3)
    gen_platform_grid(new_chunk_grid, start_height + height, platform_width * 3, platform_width * 4)
    gen_platform_grid(new_chunk_grid, start_height, platform_width * 4, chunk_width)

    return new_chunk_grid


def gen_platform_grid(grid, height, start, end):
    for row in range(c.CHUNK_HEIGHT - height, c.CHUNK_HEIGHT):
        for col in range(start, end):
            if row == c.CHUNK_HEIGHT - height:
                grid[row][col] = 2
            else:
                grid[row][col] = 1


def gen_gap_grid(min_width=2, max_width=5):
    chunk_width = random.randint(min_width, max_width)
    new_chunk_grid = [[0 for _ in range(chunk_width)] for _ in range(c.CHUNK_HEIGHT)]
    return new_chunk_grid


def gen_tower_chunk(pos):
    """
    Generates a chunk with towers
    :param pos: chunk position
    :return: generated chunk
    """
    return Chunk(generate_tower_grid(), pos)


def gen_star_chunk(pos):
    """
    Generates a chunk with star entity
    :param pos: chunk position
    :return: generated chunk
    """
    platform_height = random.randint(2, 3)
    chunk = Chunk(gen_star_grid(platform_height), pos)
    star = entities.Star((pos[0] + 128, c.WINDOW[1] - platform_height * 64), pos[0], chunk.get_end_position())
    chunk.entities.add(star)
    return chunk


def gen_shell_chunk(pos):
    """
    Generates a chunk with shell entity
    :param pos: chunk position
    :return: generated chunk
    """
    platform_height = random.randint(2, 3)
    chunk = Chunk(gen_shell_grid(platform_height), pos)
    shell = entities.Shell((int(chunk.width / 1.5) * 64 + pos[0] - 64, c.WINDOW[1] - platform_height * 64))
    chunk.entities.add(shell)
    return chunk


def gen_crab_chunk(pos):
    platform_height = random.randint(2, 3)
    chunk = Chunk(gen_crab_grid(platform_height), pos)
    return chunk


def gen_gap_chunk(pos):
    """
    Create an empty chunk
    :param pos: chunk position
    :return: generated chunk
    """
    return Chunk(gen_gap_grid(), pos)


def gen_ship_chunk(pos):
    """
    Create a chunk with a ship entity
    :param pos: chunk position
    :return: generated chunk
    """
    chunk = Chunk(gen_gap_grid(10, 20), pos)
    ship = entities.Ship((pos[0] + 100, c.WINDOW[1] - 32), pos[0], chunk.get_end_position())
    chunk.entities.add(ship)
    return chunk


# chunk_types = [gen_gap_chunk, gen_shell_chunk]
chunk_types = [gen_shell_chunk, gen_star_chunk, gen_tower_chunk, gen_gap_chunk, gen_ship_chunk]
prev_chunk = gen_gap_chunk


def gen_chunk(pos):
    """
    Generate a random chunk, different from the previous one
    :param pos: chunk position
    :return: generated chunk
    """
    global prev_chunk

    chunk_types.remove(prev_chunk)
    choice = random.choice(chunk_types)
    chunk_types.append(prev_chunk)
    prev_chunk = choice
    return choice(pos)
