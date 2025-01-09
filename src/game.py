import random
import sys

import pygame

import constants as c
import generator
from background import ScrollingBackground
from entities import Player
from src.animator import DamageOverlay
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

        return True
    return False


def handle_events():
    """
    Handle pygame events
    """
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
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

    for entity in chunk.entities:
        if entity.collisions and player.rect.bottom == entity.rect.top:
            player.inertia_x = entity.velocity_x


class Game:
    def __init__(self):
        self.damage_sound = pygame.mixer.Sound('resources/sounds/damage.mp3')
        self.loose_sound = pygame.mixer.Sound('resources/sounds/loose.mp3')
        pygame.mixer.music.load('resources/sounds/music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=1000)

        self.screen = pygame.display.set_mode(c.WINDOW)
        self.window = self.screen.get_size()
        pygame.display.set_caption("The pirate game")

        self.all_sprites = pygame.sprite.Group()
        middle = [self.window[0] // 2, self.window[1] // 2]
        self.player = Player(middle)
        self.all_sprites.add(self.player)

        self.background = ScrollingBackground(self.window)
        self.chunks = [Chunk(c.INITIAL_CHUNK_GRID, [0, 0])]
        self.chunk_generator = generator.ChunkGenerator(self.window)
        self.red_overlay = DamageOverlay(self.window)
        self.lost_ui = LostUI(self.window)

        self.lost = False
        self.damaged = False

    def handle_lost(self):
        self.lost_ui.draw(self.screen)
        if self.lost_ui.on_click():
            self.__init__()

    def damage_player(self):
        self.player.health -= 2
        self.red_overlay.draw(self.screen)
        screen_shake(self.screen)
        if not self.damaged:
            pygame.mixer.Sound.play(self.damage_sound)

        if self.player.health <= 0:
            self.loose()

    def loose(self):
        self.lost = True
        self.player.health = 0
        self.background.draw_health_bar(self.screen, self.player.health)
        self.red_overlay.draw(self.screen)
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(self.loose_sound)

    def scroll_map(self, player, chunks):
        """
        Scroll the map if the player is on the right side of the window
        :param player: player sprite
        :param chunks: all chunks
        """
        if player.rect.right > self.window[0] / 2 and player.velocity_x > 0:
            player.scroll(player.velocity_x)
            for chunk in chunks:
                chunk.scroll(player.velocity_x)

    def generate_chunks(self, chunks):
        """
        Generate new chunks if needed and remove old chunks
        :param chunks: current chunks array
        """

        # Generate new chunks if needed
        if self.window[0] > chunks[-1].get_end_position():
            new_chunk_position = [chunks[-1].get_end_position(), 0]
            new_chunk = self.chunk_generator.gen_chunk(new_chunk_position)
            chunks.append(new_chunk)

        # Remove old chunks if needed
        if chunks[0].get_end_position() < 0:
            chunk = chunks.pop(0)
            chunk.entities.remove()

    def handle_loop(self):
        if self.lost:
            self.handle_lost()
            return

        self.all_sprites.update()
        self.background.update()

        self.scroll_map(self.player, self.chunks)
        self.generate_chunks(self.chunks)
        check_chunk_collisions(self.player, self.chunks)

        self.background.draw(self.screen, self.player.health)

        collision = False
        for chunk in self.chunks:
            update_chunk(self.screen, chunk, self.player)

            if pygame.sprite.spritecollide(self.player, chunk.entities, False):
                collision = True

            if c.DEBUG:
                pygame.draw.line(self.screen,
                                 (255, 0, 0),
                                 (chunk.get_end_position(), 0), (chunk.get_end_position(), self.window), 2)

        self.all_sprites.draw(self.screen)

        if collision:
            self.damage_player()
            self.damaged = True
        else:
            self.damaged = False

        if self.player.rect.bottom >= self.window[1]:
            self.loose()


def main():
    pygame.display.init()
    pygame.font.init()
    pygame.mixer.init()

    game = Game()

    clock = pygame.time.Clock()
    while True:
        handle_events()
        game.handle_loop()

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
