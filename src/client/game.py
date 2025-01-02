import random
import sys

import pygame

import constants as c
import generator
from background import ScrollingBackground
from entities import Player
from terrain import Chunk
from ui import LostUI


def check_chunk_collisions(player, chunks):
    """
    Check for collisions between the player and the terrain sprites in the chunks
    :param player: player sprite
    :param chunks: chunk objects
    """
    for chunk in chunks:
        check_group_collisions(player, chunk.terrain_sprites)


def check_group_collisions(player, sprites):
    """
    Check for collisions between the player and the sprites in the group
    :param player: player sprite
    :param sprites: sprite group
    """
    collisions = pygame.sprite.spritecollide(player, sprites, False)
    if not collisions:
        return

    for block in collisions:
        check_single_collision(player, block)


def check_single_collision(player, block):
    """
    Check for collisions between the player and a single block (sprite)
    :param player: player sprite
    :param block: block sprite
    """

    if player.rect.colliderect(block.rect):
        # Calculate the overlap on each side
        overlap_left = player.rect.right - block.rect.left
        overlap_right = block.rect.right - player.rect.left
        overlap_top = player.rect.bottom - block.rect.top
        overlap_bottom = block.rect.bottom - player.rect.top

        # Find the smallest overlap
        smallest_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        # Resolve the collision based on the smallest overlap
        if smallest_overlap == overlap_left:
            player.rect.right = block.rect.left
            player.velocity_x = 0
        elif smallest_overlap == overlap_right:
            player.rect.left = block.rect.right
            player.velocity_x = 0
        elif smallest_overlap == overlap_top:
            player.rect.bottom = block.rect.top
            player.velocity_y = 0
            player.jumped = False
        elif smallest_overlap == overlap_bottom:
            player.rect.top = block.rect.bottom
            player.velocity_y = 0
            player.jumped = False


def scroll_map(player, chunks):
    """
    Scroll the map if the player is on the right side of the window
    :param player: player sprite
    :param chunks: all chunks
    """
    if player.rect.right > c.WINDOW[0] / 2:
        player.scroll(c.MOVE_STEP)
        for chunk in chunks:
            chunk.scroll(c.MOVE_STEP)


def generate_chunks(chunks):
    """
    Generate new chunks if needed and remove old chunks
    :param chunks: current chunks array
    """

    # Generate new chunks if needed
    if c.WINDOW[0] > chunks[-1].get_end_position():
        new_chunk_position = [chunks[-1].get_end_position(), 0]
        new_chunk = generator.gen_chunk(new_chunk_position)
        chunks.append(new_chunk)

    # Remove old chunks if needed
    if chunks[0].get_end_position() < 0:
        chunk = chunks.pop(0)
        chunk.entities.remove()


def handle_events():
    """
    Handle pygame events
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def screen_shake(screen, intensity=5):
    """
    Shake the screen
    :param screen: screen instance
    :param intensity: shake intensity
    """
    shake_x = random.randint(-intensity, intensity)
    shake_y = random.randint(-intensity, intensity)
    screen.blit(screen, (shake_x, shake_y))


def update_chunk(screen, chunk, player):
    """
    Draw, update and check collisions for a chunk
    :param screen: screen instance
    :param chunk: chunk object
    :param player: player sprite object
    :return:
    """

    chunk.draw(screen)
    chunk.entities.update()
    chunk.entities.draw(screen)
    for e in chunk.entities:
        check_group_collisions(e, chunk.terrain_sprites)
        if e.collisions:
            check_single_collision(player, e)


def main():
    pygame.init()
    screen = pygame.display.set_mode(c.WINDOW)
    pygame.display.set_caption("The pirate game")

    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    background = ScrollingBackground(2)
    chunks = [Chunk(c.INITIAL_CHUNK_GRID, [0, 0])]

    red_overlay = pygame.Surface(c.WINDOW)
    red_overlay.set_alpha(64)
    red_overlay.fill((255, 0, 0))

    lost_ui = LostUI()

    clock = pygame.time.Clock()
    while True:
        handle_events()

        if player.health < 0:
            lost_ui.draw(screen)
            pygame.display.flip()
            clock.tick(60)
            continue

        all_sprites.update()
        background.update()

        scroll_map(player, chunks)
        generate_chunks(chunks)
        check_chunk_collisions(player, chunks)

        background.draw(screen, player.health)

        for chunk in chunks:
            update_chunk(screen, chunk, player)

            collide_player = pygame.sprite.spritecollide(player, chunk.entities, False)
            if collide_player:
                player.health -= 2
                screen.blit(red_overlay, (0, 0))
                screen_shake(screen)

            # DEBUG
            # pygame.draw.line(screen, (255, 0, 0), (chunk.get_end_position(), 0), (chunk.get_end_position(), c.WINDOW[1]), 2)

        if player.rect.bottom == c.WINDOW[1]:
            player.health -= 10
            screen.blit(red_overlay, (0, 0))
            screen_shake(screen)

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
