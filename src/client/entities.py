import random
import pygame

import constants as c
from animator import Animation

class Entity(pygame.sprite.Sprite):
    """
    Base class for all entities in the game
    """

    def __init__(self, animation, pos=(c.WINDOW[0] // 2, c.WINDOW[1] // 2), gravity=True, collisions=False):
        """
        Initialize the entity
        :param animation: animation object
        :param pos: initial position (x,y)
        :param gravity: should gravity be applied to the entity
        :param collisions: should collisions be checked for the entity
        """
        super().__init__()
        self.gravity = gravity
        self.velocity_x = 0
        self.velocity_y = 0
        self.animation = animation

        self.image = self.animation.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.collisions = collisions

    def scroll(self, dx):
        """
        Scroll the entity across the screen
        :param dx: offset
        """
        self.rect.x -= dx

    def apply_movement(self):
        """
        Apply movement to the entity, based on its velocity and position
        """
        if self.gravity:
            self.velocity_y += c.GRAVITY  # Adjust gravity effect
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        if self.rect.bottom > c.WINDOW[1]:
            self.rect.bottom = c.WINDOW[1]
            self.velocity_y = 0  # Reset velocity when on the ground

    def update(self, move=True):
        """
        Update the entity - apply movement and update animation
        :param move: should the entity be moved
        """
        if move:
            self.apply_movement()

        self.animation.update()
        self.image = self.animation.get_image()


class Star(Entity):
    """
    Star entity
    It moves left and right, pausing for a while at each end,
    causing damage to the player when touched
    """
    WAIT_TIME = 30

    def __init__(self, pos, bound_start, bound_end):
        """
        Initialize the star entity
        :param pos: initial position
        :param bound_start: left bound of the movement
        :param bound_end: right bound of the movement
        """
        animation = Animation({
            'attack': 'resources/star/07-Attack',
            'idle': 'resources/star/01-Idle',
        })
        super().__init__(animation, pos)

        self.bound_start = bound_start
        self.bound_end = bound_end

        self.velocity_x = c.MOVE_STEP
        self.wait_counter = 0
        self.paused = False

    def update(self, move=True):
        """
        Update the star entity
        """
        super().update(move=(not self.paused))

        if self.paused:
            self.wait_counter += 1
            if self.wait_counter >= self.WAIT_TIME:
                self.unpause()
            return

        if self.rect.right >= self.bound_end:
            self.velocity_x = -c.STAR_MOVE_STEP
            self.animation.change_direction(False)
            self.pause()
        elif self.rect.left <= self.bound_start:
            self.velocity_x = c.STAR_MOVE_STEP
            self.animation.change_direction(True)
            self.pause()

    def pause(self):
        """
        Stop the star from moving
        """
        self.animation.change_state('idle')
        self.paused = True

    def unpause(self):
        """
        Resume the star movement
        """
        self.animation.change_state('attack')
        self.paused = False
        self.wait_counter = 0

    def scroll(self, dx):
        """
        Scroll the star entity
        :param dx: scroll offset
        """
        super().scroll(dx)
        self.bound_start -= dx
        self.bound_end -= dx


class Bullet(Entity):
    """
    Bullet entity, fired by the seashell entity
    """

    def __init__(self, pos):
        """
        Initialize the bullet entity
        :param pos: initial position
        """
        animation = Animation({
            'idle': 'resources/seashell/bullet',
        })
        super().__init__(animation, pos, False)

        self.velocity_x = -c.MOVE_STEP

    def update(self, move=True):
        """
        Update the bullet entity
        """
        super().update(move)

        if self.rect.left < 0 or self.velocity_x == 0:
            self.kill()


class Shell(Entity):
    """
    Seashell entity
    Fires bullets and bites the player interchangeably
    """

    WAITING_TIME = 20

    def __init__(self, pos):
        """
        Initialize the seashell entity
        :param pos: initial position
        """
        animation = Animation({
            'idle': 'resources/seashell/idle',
            'bite': 'resources/seashell/bite',
            'shoot': 'resources/seashell/shoot',
        })
        super().__init__(animation, pos, collisions=True)

        self.state = 'idle'

        self.timer = 0
        self.curr_state_timer = self.WAITING_TIME

    def update(self, move=True):
        """
        Update the seashell entity
        """
        super().update()

        if self.timer >= self.curr_state_timer:
            self.timer = 0
            self.next_state()
        self.timer += 1

    def next_state(self):
        """
        Switch the state of the seashell entity
        """
        if self.state == 'bite' or self.state == 'shoot':
            self.state = 'idle'
            self.animation.change_state(self.state)
            self.curr_state_timer = self.WAITING_TIME
            self.collisions = True
        else:
            self.state = random.choice(['bite', 'shoot'])
            self.animation.change_state(self.state)
            self.curr_state_timer = self.animation.get_full_time()

            if self.state == 'shoot':
                bullet = Bullet(self.rect.midleft)
                self.groups()[0].add(bullet)

            if self.state == 'bite':
                self.collisions = False


class Ship(Entity):
    """
    Ship entity
    It moves back and forth, making it possible to travel on it
    """

    def __init__(self, pos, bound_start, bound_end):
        """
        Initialize the ship entity
        :param pos: initial position
        :param bound_start: left bound of the movement
        :param bound_end: right bound of the movement
        """
        animation = Animation({'ship': 'resources/ship/base'})
        super().__init__(animation, pos, gravity=False, collisions=True)

        self.bound_start = bound_start
        self.bound_end = bound_end

    def update(self, move=True):
        """
        Update the ship entity
        """
        super().update()

        if self.rect.right >= self.bound_end:
            self.velocity_x = -c.SHIP_MOVE_STEP
            self.animation.change_direction(True)
        elif self.rect.left <= self.bound_start:
            self.velocity_x = c.SHIP_MOVE_STEP
            self.animation.change_direction(False)

    def scroll(self, dx):
        """
        Scroll the ship entity
        :param dx: scroll offset
        """
        super().scroll(dx)
        self.bound_start -= dx
        self.bound_end -= dx


class Player(Entity):
    """
    Player entity
    """

    def __init__(self):
        animation = Animation({
            'idle': 'resources/player/01-Idle',
            'run': 'resources/player/02-Run',
            'jump': 'resources/player/03-Jump',
            'fall': 'resources/player/04-Fall',
        })
        super().__init__(animation)

        self.health = 100
        self.jumped = False

    def update(self, move=True):
        """
        Update the player entity
        """

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.velocity_x = -c.MOVE_STEP
            self.animation.change_state('run')
            self.animation.change_direction(True)
        elif keys[pygame.K_d] and self.rect.right < c.WINDOW[0]:
            self.velocity_x = c.MOVE_STEP
            self.animation.change_state('run')
            self.animation.change_direction(False)
        else:
            self.animation.change_state('idle')
            self.velocity_x = 0

        if keys[pygame.K_SPACE] and self.velocity_y == 0 and not self.jumped:
            self.jumped = True
            self.velocity_y = -c.JUMP_HEIGHT

        super().update()
